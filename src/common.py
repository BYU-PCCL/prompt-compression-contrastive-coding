import torch
import torch.nn.functional as F
import numpy as np

#
# ==========================================================================
#

_args = None
def set_args( args ):
    global _args
    _args = args
    
def get_args():
    return _args

class MPU():
    def __init__( self ):
        pass
    def get_tensor_model_parallel_rank( self ):
        return 0
    def get_tensor_model_parallel_group( self ):
        return 0

mpu = MPU()

#
# ==========================================================================
#

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

def clean_detok( tokenizer, tokens ):
#    tokenizer = get_tokenizer()
    try:
        #clean_toks = list( filter( lambda x: x!=tokenizer.eod, tokens ) )
        #result = tokenizer.detokenize( clean_toks )
        result = tokenizer.decode( tokens )
    except Exception as err:
        print( str(err) )
        result = "<error decoding>"
    return result

def top_k_logits(logits, top_k=0, top_p=0.0, filter_value=-float('Inf')):
    """ This function has been mostly taken from huggingface conversational
     ai code at
         https://medium.com/huggingface/how-to-build-a-state-of-the-art-
              conversational-ai-with-transfer-learning-2d818ac26313 """

    if top_k > 0:
        # Remove all tokens with a probability less than the
        # last token of the top-k
        indices_to_remove = logits < torch.topk(logits, top_k)[0][..., -1, None]
        logits[indices_to_remove] = filter_value

    if top_p > 0.0:
        # Cconvert to 1D
        sorted_logits, sorted_indices = torch.sort(
            logits, descending=True, dim=-1)
        cumulative_probs = torch.cumsum(F.softmax(sorted_logits, dim=-1),
                                        dim=-1)

        # Remove tokens with cumulative probability above the threshold
        sorted_indices_to_remove = cumulative_probs > top_p
        # Shift the indices to the right to keep also the first token
        # above the threshold
        sorted_indices_to_remove[..., 1:] \
            = sorted_indices_to_remove[..., :-1].clone()
        sorted_indices_to_remove[..., 0] = 0
        for i in range(sorted_indices.size(0)):
            indices_to_remove = sorted_indices[i][sorted_indices_to_remove[i]]
            logits[i][indices_to_remove] = filter_value

    return logits, indices_to_remove

def sample_tok( logits ):
    args = get_args()

    logits /= args.temperature
    logits, itr = top_k_logits( logits, top_k=args.top_k, top_p=args.top_p )
    probs = F.softmax( logits, dim=-1 )

    new_tok = torch.multinomial(probs, num_samples=1).view(-1)
    new_tok = new_tok.item()

    return new_tok, itr, probs #logits

def normalize_logits( logits ):
    # expects as input a tensor of shape [1,V]
    if len( logits.shape ) != 2:
        error('wrong logits shape!')
    logits = logits - torch.max( logits )
    logits = logits - torch.log( torch.sum( torch.exp( logits ) ) )
    return logits


def create_bonus( nor_logits, pos_logits, neg_logits ):
    args = get_args()
    PTAU = args.tau

#    pos_logits = torch.clone( pos_logits )
#    neg_logits = torch.clone( neg_logits )
#    pos_logits = normalize_logits( pos_logits )
#    neg_logits = normalize_logits( neg_logits )
#    bonus_1 = -nor_logits + PTAU* torch.minimum( nor_logits, nor_logits + (pos_logits - neg_logits) )
#    return bonus_1, 0

#    bonus_1 = -nor_logits + PTAU* pos_logits
#    return bonus_1, 0

    c1_logits = torch.clone( pos_logits )
    c2_logits = torch.clone( neg_logits )
    c1_logits = normalize_logits( c1_logits )
    c2_logits = normalize_logits( c2_logits )
    tmp = torch.cat( [c1_logits, c2_logits], axis=0)
    bonus = F.log_softmax( PTAU*tmp, dim=0 )
    bonus_1 = bonus[0:1,:]
    bonus_2 = bonus[1:2,:]
    return bonus_1, bonus_2

def gen_completion( normodel, posmodel, negmodel, tokenizer, tok_cnt=20 ):
    args = get_args()

    for tok_ind in range( tok_cnt ):
        nor_logits = normodel.get_next_logits()
        pos_logits = posmodel.get_next_logits()
        neg_logits = negmodel.get_next_logits()

        bonus_1, bonus_2 = create_bonus( nor_logits, pos_logits, neg_logits )

        final_logits = nor_logits + args.omega*bonus_1
        final_logits = normalize_logits( final_logits )

        # if mpu.get_tensor_model_parallel_rank() == 0 and tok_ind == 0:
        #     dump_logits( "normal"+normal_text, normalize_logits( nor_logits ) )
        #     dump_logits( "pos"+normal_text, normalize_logits( pos_logits ) )
        #     dump_logits( "neg"+normal_text, normalize_logits( neg_logits ) )
        #     dump_logits( "final"+normal_text, normalize_logits( final_logits ) )
        #     dump_logits( "bonus"+normal_text, bonus_1 )

        # XXX note that this modifies final_logits
        new_tok, itr, topkprobs = sample_tok( final_logits )

        if mpu.get_tensor_model_parallel_rank() == 0 and args.verbose:
            print( f"  Tokens left: {topkprobs.shape[1] - len(itr)}\t", end="" )

            #tmp_normal_logits = normalize_logits( normal_logits )
            _, _, tmp_normal_probs = sample_tok( nor_logits )

            tmp = topkprobs.cpu().numpy().ravel()
            inds = np.flip( np.argsort( tmp ) )
            #print( "Inds: ", inds )
            result = ""
            for ind in range( 15 ):
                tok = inds[ind]
                try:
#                    tmp = tokenizer.detokenize( [tok] ).replace("\n","")
                    tmp = tokenizer.decode( [tok] ).replace("\n","")
                except:
                    tmp = "!"+str(tok)+"!"
                tmp = "[" + tmp + "] " + f"{topkprobs[0,tok]:0.3f} <- {tmp_normal_probs[0,tok]:0.3f}"
                result +=  f"{tmp: <30}"
            print( result )

        normodel.append_new_tok( new_tok )
        posmodel.append_new_tok( new_tok )
        negmodel.append_new_tok( new_tok )

    cpu_toks = normodel.get_tokens().cpu().numpy().ravel()
    rstr = clean_detok( tokenizer, cpu_toks )
    return rstr

def count_lines( fn ):
    try:
        f = open( fn, "r" )
        lines = f.readlines()
        f.close()
        return len(lines)
    except:
        return 0

