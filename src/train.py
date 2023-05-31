"""

pip install transformers lm_eval

python ./main.py --dim=4

"""


import argparse
import numpy as np
import random
import json
from tqdm import tqdm

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset
from torch.optim import ( Adam, AdamW, SGD )

from transformers import get_scheduler
from transformers import (AutoModelForCausalLM,AutoTokenizer)

from texts import get_modified_text, KNOWN_TEXTS

from gpt2sp import *

#
# ==========================================================================
#

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, default="gpt2") # gpt2-xl, gpt2-medium
    parser.add_argument('--dim', type=int, default=10)

    parser.add_argument('--num_epochs', type=int, default=1)
    parser.add_argument('--num_training_steps', type=int, default=20000)
    parser.add_argument('--num_warmup_steps', type=int, default=0)

    parser.add_argument('--context', type=str, default="boi_small_alltox")

    parser.add_argument('--lr', type=float, default=1e-1)
    parser.add_argument('--lrs_type', type=str, default="linear") # or "cosine"

    parser.add_argument('--cache_dir', type=str, default="/home/wingated/.cache/huggingface/transformers/")

    parser.add_argument('--train_datafile', type=str, default="./small_training_data.jsonl")

    parser.add_argument('--batch_size', type=int, default=1)  # XXX not fully implemented

    return parser.parse_args()

#
# ==========================================================================
#

def trim_ship_and_run( token_struct, model, dim ):
    MAXLEN = 1024 - dim - 5

    if token_struct['input_ids'].shape[1] > MAXLEN:
        # XXX this probably shouldn't be silent
        error('nope')
        token_struct['input_ids'] = token_struct['input_ids'][:,-MAXLEN:]
        token_struct['attention_mask'] = token_struct['attention_mask'][:,-MAXLEN:]

    token_struct['input_ids'] = token_struct['input_ids'].to( device )
    token_struct['attention_mask'] = token_struct['attention_mask'].to( device )
    output = model( **token_struct )
    return output

def normalize_full_logits( logits ):
    # expects as input a tensor of shape [batch,sequence,vocab]
    if len( logits.shape ) != 3:
        error('wrong logits shape!')
    (maxvals,maxinds) = torch.max( logits, dim=2, keepdims=True )

    logits = logits - maxvals
    logits = logits - torch.log( torch.sum( torch.exp( logits ), dim=2, keepdims=True ) )
    return logits

def make_lc_text( CONTEXT, text ):
    if type(text) == str:
        return CONTEXT.replace("YYY",text)
    elif type(text) == list:
        return [ CONTEXT.replace("YYY",x) for x in text ]
    error('unknown type')

#
# ==========================================================================
#

class TextDataset(Dataset):
    def __init__(self, fn):
        self.lines = open( fn ).readlines()
        print( f"Loaded {len(self.lines)} lines" )

    def __len__(self):
        return len(self.lines)

    def __getitem__(self, idx):
        return json.loads( self.lines[idx] )['text'].strip()

#
# ==========================================================================
#

args = parse_args()

print( "Loading model..." )

device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

tokenizer = AutoTokenizer.from_pretrained( args.model, cache_dir=args.cache_dir )#, local_files_only=True )
tokenizer.pad_token = tokenizer.eos_token
#tokenizer.add_special_tokens({'pad_token': '[PAD]'})  # XXX this seems to cause problems???

# long context model
model_lc = AutoModelForCausalLM.from_pretrained( args.model, cache_dir=args.cache_dir )#, local_files_only=True )
model_lc.eval()
model_lc.to( device )

# distilled prompt model
model_dp = GPT2LMPlus.from_pretrained( args.model, cache_dir=args.cache_dir )
model_dp.set_up_prompt_tuning( args.dim, 'before_pe' )
#model_dp.load_prompt_checkpoint( './weights_latest.npy' )
model_dp.to( device )

#
# ==========================================================================
#

print( "Loading dataset" )

train_dataset = TextDataset( args.train_datafile )
train_dataloader = DataLoader( train_dataset, shuffle=False, batch_size=args.batch_size ) # XXX if you change batch_size, go think about the attention_mask and the loss!

optimizer = Adam( model_dp.parameters(), lr=args.lr )

lr_scheduler = get_scheduler( name=args.lrs_type, optimizer=optimizer, num_warmup_steps=args.num_warmup_steps, num_training_steps=args.num_training_steps )

CONTEXT = KNOWN_TEXTS[ args.context ]

#
# ==========================================================================
#

prompt_token_struct = tokenizer( CONTEXT.replace('YYY',''), return_tensors='pt', padding=True, return_token_type_ids=False )
prompt_tokens = prompt_token_struct['input_ids']
num_prompt_toks = prompt_tokens.shape[1]

step_ind = 0
losses = []
for epoch in range(args.num_epochs):
    print( "EPOCH:", epoch )

    for (batch_ind, batch) in enumerate( train_dataloader ):

        if step_ind % 1000 == 0:
            print( "CHECKPOINTING..." )
            #np.save( f"./losses_b_{batch_ind}_e_{epoch}.npy", losses )
            model_dp.save_prompt_checkpoint( f"./weights_cp_model_{args.model}_context_{args.context}_dim_{args.dim}_e_{epoch}_si_{step_ind}_ts_{args.num_training_steps}_newds_lr_{args.lr}.npy" )

        if step_ind > args.num_training_steps:
            break

        step_ind += 1

        orig_text = batch[0]  # batch is a list of strings
        token_struct = tokenizer( orig_text, return_tensors='pt', padding=True, return_token_type_ids=False )

        maxlen = 1024 - num_prompt_toks - args.dim - 5
        token_struct['input_ids'] = token_struct['input_ids'][:,-maxlen:]
        token_struct['attention_mask'] = token_struct['attention_mask'][:,-maxlen:]
        num_toks = token_struct['input_ids'].shape[1]

        new_token_struct = {}
        new_token_struct['input_ids'] = torch.cat( (prompt_tokens,token_struct['input_ids']), dim=1 )
        new_token_struct['attention_mask'] = torch.ones( (1,new_token_struct['input_ids'].shape[1] ) )

        try:

            outputs_dp = trim_ship_and_run( token_struct, model_dp, args.dim )
            with torch.no_grad():
                outputs_lc = trim_ship_and_run( new_token_struct, model_lc, args.dim )
            model_logits = normalize_full_logits( outputs_dp[0] )
            target_logits = normalize_full_logits( outputs_lc[0][:,-num_toks:,:] )

            # train just the nucleus
            # union of the nuclei
            # kl divergence
            # XXX what about the attention mask?
            loss = torch.mean( torch.sum( torch.exp( model_logits )*(model_logits-target_logits), dim=2 ) )

            loss.backward()
            optimizer.step()
            lr_scheduler.step()
            optimizer.zero_grad()

            li = loss.item()

            if step_ind > 500:
                tmp = np.mean(np.array(losses)[-500:])
                print( f"{epoch}\t{batch_ind}\t{tmp:0.5f}\t{li:0.5f}" )
            else:
                print( f"{epoch}/{batch_ind}\t{li:0.5f}" )

            losses.append( li )

        except Exception as e:
            print( "-------------------------> ERROR: ", len(orig_text), str(e) )

tmp = np.mean( np.array(losses)[-500:] )
print( f"MEAN OF LAST 500 LOSSES: {tmp:0.5f}"  )

model_dp.save_prompt_checkpoint( f"./weights_latest_model_{args.model}_context_{args.context}_dim_{args.dim}_ts_{args.num_training_steps}_newds_lr_{args.lr}.npy" )
