"""

pip install transformers lm_eval googleapi


%run prompt_gen.py --soft --normodel gpt2 --posmodel gpt2 --negmodel gpt2 --poscheckpoint ./weights_latest_model_gpt2_context_boi_allpos_dim_64_ts_75000_newds_lr_0.1.npy --negcheckpoint ./weights_latest_model_gpt2_context_boi_alltox_dim_64_ts_75000_newds_lr_0.1.npy


%run prompt_gen.py --soft --normodel gpt2-xl --posmodel gpt2-xl --negmodel gpt2-xl --poscheckpoint ./weights_latest_model_gpt2-xl_context_boi_allpos_dim_64_ts_75000_newds_lr_0.1.npy --negcheckpoint ./weights_latest_model_gpt2-xl_context_boi_alltox_dim_64_ts_75000_newds_lr_0.1.npy

"""


import sys
import readline
import argparse

import torch
import numpy as np
from transformers import (AutoModelForCausalLM,AutoTokenizer)

from common import *

from gpt2sp_base import GPT2LMPlus
from gpt2hc_base import GPT2LMHC

import json

from texts import KNOWN_TEXTS

from googleapiclient import discovery

#
# ==========================================================================
#

API_KEY = '' # XXX put your Perspective API key here

ATTRS = ['TOXICITY', 'THREAT', 'INSULT', 'SEVERE_TOXICITY', 'PROFANITY', 'SEXUALLY_EXPLICIT', 'IDENTITY_ATTACK', 'FLIRTATION' ]

client = discovery.build(
  "commentanalyzer",
  "v1alpha1",
  developerKey=API_KEY,
  discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
  static_discovery=False,
)

def analyze_text( raw_text ):
    tmp = {}
    for a in ATTRS:
        tmp[a] = {}

    analyze_request = {
        'comment': { 'text': raw_text },
        'requestedAttributes': tmp
    }

    response = client.comments().analyze(body=analyze_request).execute()
    return response

#
# ==========================================================================
#

def parse_args():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--normodel', type=str, default="gpt2") # gpt2-xl, gpt2-medium
    parser.add_argument('--posmodel', type=str, default="gpt2") # gpt2-xl, gpt2-medium
    parser.add_argument('--negmodel', type=str, default="gpt2") # gpt2-xl, gpt2-medium
    
    parser.add_argument('--dim', type=int, default=10)

    parser.add_argument('--num_prompts', type=int, default=2000)    

    parser.add_argument('--soft', action='store_true') # default is false
    parser.add_argument('--hard', action='store_true') # default is false
    
    parser.add_argument('--num_gens', type=int, default=25)

    parser.add_argument('--negcontext', type=str, default="boi_small_alltox")
    parser.add_argument('--poscontext', type=str, default="boi_allpos")    

    parser.add_argument('--lr', type=float, default=1e-1)
    parser.add_argument('--lrs_type', type=str, default="linear") # or "cosine"

    parser.add_argument('--cache_dir', type=str, default="/home/dwingate/.cache/huggingface/transformers/")

    parser.add_argument('--poscheckpoint', type=str, default=None)
    parser.add_argument('--negcheckpoint', type=str, default=None)    

    parser.add_argument('--batch_size', type=int, default=1)  # XXX not fully implemented


    parser.add_argument('--omega', type=float, default=1.0)
    parser.add_argument('--tau', type=float, default=1.0)    
    
    parser.add_argument('--temperature', type=float, default=1.0)
    parser.add_argument('--top_k', type=int, default=0)
    parser.add_argument('--top_p', type=float, default=0.9)

    parser.add_argument('--verbose', action='store_true')    

    return parser.parse_args()

#
# ==========================================================================
#

class Generator():
    def __init__( self, model, tokenizer ):
        self.model = model
        self.tokenizer = tokenizer

    def set_hard_context( self, hard_context ):
        self.model.set_prompt_tokens( self.tokenizer.encode( hard_context, add_special_tokens=False) )
        
    def set_prompt( self, raw_text ):
        self.token_struct = self.tokenizer( raw_text, return_tensors='pt' )        
        self.all_tokens = torch.clone( self.token_struct['input_ids'] )
        self.token_struct['input_ids'] = self.token_struct['input_ids'].to("cuda:0")
        self.token_struct['attention_mask'] = self.token_struct['attention_mask'].to("cuda:0")
        self.past_key_values = None

    def get_next_logits( self ):
        output = self.model( **self.token_struct, past_key_values = self.past_key_values )
        
#        self.past_key_values = output['past_key_values']
        
        return output['logits'][0:1,-1,:]

    def append_new_tok( self, new_token ):
        self.token_struct['input_ids'] = torch.hstack(( self.token_struct['input_ids'], torch.tensor([[new_token]],dtype=torch.int64,device="cuda:0") ))
        self.token_struct['attention_mask']= torch.hstack(( self.token_struct['attention_mask'], torch.ones([1,1],dtype=torch.int64,device="cuda:0") ))

#        self.token_struct['input_ids'] = torch.tensor( [[new_token]], dtype=torch.int64, device="cuda:0" )
#        self.token_struct['attention_mask'] = torch.ones( [1,1], dtype=torch.int64, device="cuda:0" )

        self.all_tokens = torch.hstack(( self.all_tokens, torch.tensor([[new_token]],dtype=torch.int64) ))

    def get_tokens( self ):
        return self.all_tokens

#
# ==========================================================================
#

def generate_interactive_completions( args, normodel, posmodel, negmodel, tokenizer ):
    np.random.seed( 42 )

    with torch.no_grad():

        while True:

            prompt_text = input( ">> " )

            if prompt_text.startswith("omega"):
                args.omega = float( prompt_text.split()[1] )
                continue
            if prompt_text.startswith("tau"):
                args.tau = float( prompt_text.split()[1] )
                continue
            if prompt_text.startswith("verbose"):
                args.verbose = ( prompt_text.split()[1] == "True" )
                continue
            if prompt_text.startswith("num_gens"):
                args.num_gens = int( prompt_text.split()[1] )
                continue
            if prompt_text.startswith("seed"):
                np.random.seed( int( prompt_text.split()[1] ) )
                continue
            if prompt_text == "":
                continue

            if mpu.get_tensor_model_parallel_rank() == 0:
                print( f"PROMPT_TEXT: [{prompt_text}], OMEGA {args.omega} TAU {args.tau} NGENS {args.num_gens}" )

            average = 0.0
            cnt = 0

            for ind in range( args.num_gens ):

                normodel.set_prompt( prompt_text )
                posmodel.set_prompt( prompt_text )
                negmodel.set_prompt( prompt_text )                
                
                completion = gen_completion( normodel, posmodel, negmodel, tokenizer )
                completion = completion.replace( prompt_text, "" )

                if mpu.get_tensor_model_parallel_rank() == 0:
                    tmp = completion.replace("\n","\\n")
                    print( f"=>: [{prompt_text}] [{tmp: <150}]", end="" )
                    try:
                        resp = analyze_text( completion )
                        print( "  -> ", end="" )
                        for a in ATTRS:
                            prob = resp['attributeScores'][a]['summaryScore']['value']
                            print( f"{a.lower()} = {prob:0.2f} ", end="" )
                        average += float( resp['attributeScores']['TOXICITY']['summaryScore']['value'] )
                        cnt += 1

                    except Exception as err:
                        #pass
                        print( f"Error processing [{completion}]: {str(err)}" )

                    print( "" )
            if mpu.get_tensor_model_parallel_rank() == 0:
                print( f"PROMPT_TEXT: [{prompt_text}], OMEGA {args.omega} TAU {args.tau} NGENS {args.num_gens}" )                
                average /= (cnt+1e-3)
                print( f"Average toxicity: {average:0.2f}" )

#
# ==========================================================================
#

def generate_prompt_completions( args, normodel, posmodel, negmodel, tokenizer ):
    np.random.seed( 42 )
    
    prompts_fn = "./shuf_prompts.jsonl"

    if args.hard:
        gens_fn = f"./hf_{args.normodel}_{args.posmodel}_{args.negmodel}_hard_{args.hard}_dim_{args.dim}_omega_{args.omega}_tau_{args.tau}_generations.jsonl"
    else:
        gens_fn = f"./hf_{args.normodel}_{args.posmodel}_{args.negmodel}_hard_{args.hard}_dim_{args.dim}_omega_{args.omega}_tau_{args.tau}_{args.poscontext}_{args.negcontext}_generations.jsonl"        

    prompts = open( prompts_fn ).readlines()

    # count existing gens
    done_cnt = count_lines( gens_fn )

    if mpu.get_tensor_model_parallel_rank() == 0:
        gens = open( gens_fn, "a")
        print( f"STARTING AT LINE {done_cnt}" )
    
    with torch.no_grad():

        for ind in range( done_cnt, args.num_prompts ):

            raw_prompt = prompts[ind]
            prompt_ds = json.loads( raw_prompt )
            prompt_text = prompt_ds['prompt']['text']
            prompt_ds['generations'] = []
            tox = prompt_ds['prompt']['toxicity']

            if mpu.get_tensor_model_parallel_rank() == 0:
                print( prompt_text )

            for gen_ind in range( args.num_gens ):
                normodel.set_prompt( prompt_text )
                posmodel.set_prompt( prompt_text )
                negmodel.set_prompt( prompt_text )                
                
                completion = gen_completion( normodel, posmodel, negmodel, tokenizer )
                completion = completion.replace( prompt_text, "" )
                prompt_ds['generations'].append( { 'text': completion } )
                if mpu.get_tensor_model_parallel_rank() == 0:
                    print( "  ", completion.replace("\n","\\n") )
                    
            if mpu.get_tensor_model_parallel_rank() == 0:
                print( json.dumps( prompt_ds ), file=gens, flush=True )

    if mpu.get_tensor_model_parallel_rank() == 0:
        gens.close()
        
#
# ==========================================================================
#

args = parse_args()
set_args( args )

if ( not args.soft and not args.hard) or (args.soft and args.hard):
    error('must specify either hard or soft, but not both')

print( "Loading models..." )

print( "  loading tokenizer..." )
ztokenizer = AutoTokenizer.from_pretrained( args.normodel, cache_dir=args.cache_dir )

print( f"  loading normal model {args.normodel}..." )
zmodel = AutoModelForCausalLM.from_pretrained( args.normodel, cache_dir=args.cache_dir )
zmodel.eval()
zmodel.to("cuda:0")
normodel = Generator( zmodel, ztokenizer )

print( f"  loading positive model {args.posmodel}..." )

if args.soft:
    print( "    using soft model" )
    zmodel = GPT2LMPlus.from_pretrained( args.posmodel )
    zmodel.set_up_prompt_tuning( args.poscheckpoint, 'before_pe' )
#    zmodel.set_up_prompt_tuning( args.dim, 'before_pe' )    
else:
    print( "    using hard model" )
    zmodel = GPT2LMHC.from_pretrained( args.posmodel )
zmodel.eval()
zmodel.to("cuda:0")
posmodel = Generator( zmodel, ztokenizer )

print( f"  loading negative model {args.negmodel}..." )
if args.soft:
    print( "    using soft model" )
    zmodel = GPT2LMPlus.from_pretrained( args.negmodel )
    zmodel.set_up_prompt_tuning( args.negcheckpoint, 'before_pe' )
#    zmodel.set_up_prompt_tuning( args.dim, 'before_pe' )    
else:
    print( "    using hard model" )    
    zmodel = GPT2LMHC.from_pretrained( args.negmodel )
zmodel.eval()
zmodel.to("cuda:0")
negmodel = Generator( zmodel, ztokenizer )

if args.hard:
    print( "    setting hard contexts..." )
    posmodel.set_hard_context( KNOWN_TEXTS[args.poscontext].replace('YYY','') )
    negmodel.set_hard_context( KNOWN_TEXTS[args.negcontext].replace('YYY','') )

with torch.no_grad():
#    generate_interactive_completions( args, normodel, posmodel, negmodel, ztokenizer )
    generate_prompt_completions( args, normodel, posmodel, negmodel, ztokenizer )
