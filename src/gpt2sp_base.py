import numpy as np
import torch
import torch.nn as nn
import transformers
import random

from transformers.models.gpt2.modeling_gpt2 import (
    logger,
    GPT2LMHeadModel,
    GPT2Model
)
from transformers.modeling_outputs import (
    BaseModelOutputWithPastAndCrossAttentions
)

class GPT2ModelPlus(GPT2Model):

    def __init__(self, config):
        super().__init__(config)
        self.do_prompt_tune = False
        self.vocab_len = config.vocab_size

    def set_up_prompt_tuning(self, k, entry_point):
        self.do_prompt_tune = True
        self.prompt_tuning_entry_point = entry_point

        if type(k) == int:
            self.prompt_tuning_k = k        
            # Initialize with random embeddings (not that this
            # does not include position encodings)
            k_idxs = random.sample(list(range(self.vocab_len)), k)
            self.pt_prefix = nn.Parameter(
                self.wte.weight[k_idxs].clone().detach().unsqueeze(0)
            )
        elif type(k) == str:
            print( f"    loading checkpoint {k}" )
            self.pt_prefix = nn.Parameter( torch.Tensor( np.load( k ) ) )
            self.prompt_tuning_k = self.pt_prefix.shape[1]
            

    def forward(
        self,
        input_ids=None,
        past_key_values=None,
        attention_mask=None,
        token_type_ids=None,
        position_ids=None,
        head_mask=None,
        inputs_embeds=None,
        encoder_hidden_states=None,
        encoder_attention_mask=None,
        use_cache=None,
        output_attentions=None,
        output_hidden_states=None,
        return_dict=None
    ):

        if output_attentions is None:
            output_attentions = self.config.output_attentions

        if output_hidden_states is None:
            output_hidden_states = self.config.output_hidden_states

        if use_cache is None:
            use_cache = self.config.use_cache

        if return_dict is None:
            return_dict = self.config.use_return_dict

        if input_ids is not None and inputs_embeds is not None:
            msg = ("You cannot specify both input_ids and "
                   "inputs_embeds at the same time")
            raise ValueError(msg)
        elif input_ids is not None:

            if input_ids.shape[1] + self.prompt_tuning_k > 1024:
                print( "WARNING: prompt too long, skipping adding soft prefix" )
                DO_SP = False
            else:
                DO_SP = True

            input_shape = input_ids.size()
            input_ids = input_ids.view(-1, input_shape[-1])
            batch_size = input_ids.shape[0]
        elif inputs_embeds is not None:
            input_shape = inputs_embeds.size()[:-1]
            batch_size = inputs_embeds.shape[0]
        else:
            msg = "You have to specify either input_ids or inputs_embeds"
            raise ValueError(msg)

        if input_ids is not None:
            device = input_ids.device
        else:
            device = inputs_embeds.device

        if token_type_ids is not None:
            token_type_ids = token_type_ids.view(-1, input_shape[-1])
        if position_ids is not None:
            position_ids = position_ids.view(-1, input_shape[-1])

        if past_key_values is None:
            past_length = 0
            past_key_values = tuple([None] * len(self.h))
        else:
            past_length = past_key_values[0][0].size(-2)
        if position_ids is None:
            position_ids = torch.arange(
                past_length,
                input_shape[-1]+past_length,
                dtype=torch.long,
                device=device
            )
            position_ids = position_ids.unsqueeze(0).view(-1, input_shape[-1])

        if attention_mask is None:
            if batch_size != 1:
                error("I don't know how to handle this")
            attention_mask = torch.ones( (batch_size, input_ids.shape[1]),
                                         dtype=torch.int64,
                                         device=device )

        #######################################################################
        if DO_SP and self.do_prompt_tune:
            # Make it so we attend to the prompt tuning prefix
            attention_mask = torch.cat((
                torch.ones(
                    (batch_size, self.prompt_tuning_k),
                    dtype=torch.int64,
                    device=device
                ),
                attention_mask
            ), dim=1)
        ##############################################################

        # GPT2Attention mask.
        if attention_mask is not None:
            if batch_size <= 0:
                raise ValueError("batch_size has to be defined and > 0")
            attention_mask = attention_mask.view(batch_size, -1)
            # We create a 3D attention mask from a 2D tensor mask.
            # Sizes are [batch_size, 1, 1, to_seq_length]
            # So we can broadcast to
            # [batch_size, num_heads, from_seq_length, to_seq_length]
            # this attention mask is more simple than the triangular
            # masking of causal attention used in OpenAI GPT, we
            # just need to prepare the broadcast dimension here.
            attention_mask = attention_mask[:, None, None, :]

            # Since attention_mask is 1.0 for positions we want
            # to attend and 0.0 for masked positions, this operation
            # will create a tensor which is 0.0 for positions we want
            # to attend and -10000.0 for masked positions.
            # Since we are adding it to the raw scores before the
            # softmax, this is effectively the same as removing these entirely.
            attention_mask = attention_mask.to(dtype=self.dtype)  # for fp16
            attention_mask = (1.0 - attention_mask) * -10000.0

        # If a 2D or 3D attention mask is provided for the cross-attention
        # we need to make broadcastable to
        # [batch_size, num_heads, seq_length, seq_length]
        if self.config.add_cross_attention and \
           encoder_hidden_states is not None:
            encoder_batch_size, \
                encoder_sequence_length, _ = encoder_hidden_states.size()
            encoder_hidden_shape = (
                encoder_batch_size, encoder_sequence_length
            )
            if encoder_attention_mask is None:
                encoder_attention_mask = torch.ones(
                    encoder_hidden_shape, device=device
                )
            encoder_attention_mask = self.invert_attention_mask(
                encoder_attention_mask
            )
        else:
            encoder_attention_mask = None

        # Prepare head mask if needed
        # 1.0 in head_mask indicate we keep the head
        # attention_probs has shape bsz x n_heads x N x N
        # head_mask has shape n_layer x batch x n_heads x N x N
        head_mask = self.get_head_mask(head_mask, self.config.n_layer)
        # print("New head_mask", head_mask)

        if inputs_embeds is None:
            inputs_embeds = self.wte(input_ids)

        ##############################################################
        if DO_SP and self.do_prompt_tune:

            if self.prompt_tuning_entry_point == "before_pe":
                # Add prompt tuning prefix on
                inputs_embeds = torch.cat((
                    self.pt_prefix.expand(batch_size, -1, -1),
                    inputs_embeds
                ), dim=1)

                # Change input shape to account for prefix
                input_shape = inputs_embeds.size()[:-1]
                # Update position_ids
                position_ids = torch.arange(
                    past_length,
                    input_shape[-1]+past_length,
                    dtype=torch.long,
                    device=device
                )
                position_ids = position_ids.unsqueeze(0).view(
                    -1, input_shape[-1]
                )
        ##############################################################

        position_embeds = self.wpe(position_ids)
        hidden_states = inputs_embeds + position_embeds

        ##############################################################
        if DO_SP and self.do_prompt_tune and \
           self.prompt_tuning_entry_point == "after_pe":
            # Add prompt tuning prefix on
            hidden_states = torch.cat((
                self.pt_prefix.expand(batch_size, -1, -1),
                hidden_states
            ), dim=1)
            # Change input shape to account for prefix
            input_shape = hidden_states.size()[:-1]
        ##############################################################

        # None by default
        if token_type_ids is not None:
            token_type_embeds = self.wte(token_type_ids)
            hidden_states = hidden_states + token_type_embeds

        hidden_states = self.drop(hidden_states)

        output_shape = input_shape + (hidden_states.size(-1),)

        presents = () if use_cache else None
        all_self_attentions = () if output_attentions else None

        if output_attentions and self.config.add_cross_attention:
            all_cross_attentions = ()
        else:
            all_cross_attentions = None

        all_hidden_states = () if output_hidden_states else None
        for i, (block, layer_past) in enumerate(zip(self.h, past_key_values)):

            # Model parallel
            if self.model_parallel:
                torch.cuda.set_device(hidden_states.device)
                # Ensure layer_past is on same device as
                # hidden_states (might not be correct)
                if layer_past is not None:
                    layer_past = tuple(
                        past_state.to(hidden_states.device)
                        for past_state in layer_past
                    )
                # Ensure that attention_mask is always on the same
                # device as hidden_states
                if attention_mask is not None:
                    attention_mask = attention_mask.to(hidden_states.device)
                if isinstance(head_mask, torch.Tensor):
                    head_mask = head_mask.to(hidden_states.device)
            if output_hidden_states:
                all_hidden_states = all_hidden_states + (hidden_states,)

            if self.gradient_checkpointing and self.training:

                if use_cache:
                    logger.warning(
                        ("`use_cache=True` is incompatible with "
                         "gradient checkpointing. Setting "
                         "`use_cache=False`...")
                    )
                    use_cache = False

                def create_custom_forward(module):
                    def custom_forward(*inputs):
                        # None for past_key_value
                        return module(*inputs, use_cache, output_attentions)

                    return custom_forward

                outputs = torch.utils.checkpoint.checkpoint(
                    create_custom_forward(block),
                    hidden_states,
                    None,
                    attention_mask,
                    head_mask[i],
                    encoder_hidden_states,
                    encoder_attention_mask,
                )
            else:
                outputs = block(
                    hidden_states,
                    layer_past=layer_past,
                    attention_mask=attention_mask,
                    head_mask=head_mask[i],
                    encoder_hidden_states=encoder_hidden_states,
                    encoder_attention_mask=encoder_attention_mask,
                    use_cache=use_cache,
                    output_attentions=output_attentions,
                )

            hidden_states = outputs[0]
            if use_cache is True:
                presents = presents + (outputs[1],)

            if output_attentions:
                all_self_attentions = all_self_attentions + \
                                      (outputs[2 if use_cache else 1],)
                if self.config.add_cross_attention:
                    all_cross_attentions = all_cross_attentions + \
                                           (outputs[3 if use_cache else 2],)

            # Model Parallel: If it's the last layer for that device,
            # put things on the next device
            if self.model_parallel:
                for k, v in self.device_map.items():
                    if i == v[-1] and "cuda:" + str(k) != self.last_device:
                        hidden_states = hidden_states.to("cuda:" + str(k + 1))

        hidden_states = self.ln_f(hidden_states)

        hidden_states = hidden_states.view(output_shape)
        # Add last hidden state
        if output_hidden_states:
            all_hidden_states = all_hidden_states + (hidden_states,)

        if not return_dict:
            return tuple(
                v
                for v in [hidden_states,
                          presents,
                          all_hidden_states,
                          all_self_attentions,
                          all_cross_attentions]
                if v is not None
            )

        ##############################################################
        if DO_SP and self.do_prompt_tune:
            # Remove the prefix from outputs
            hidden_states = hidden_states[:, self.prompt_tuning_k:, :]

        return BaseModelOutputWithPastAndCrossAttentions(
            last_hidden_state=hidden_states,
            past_key_values=presents,
            hidden_states=all_hidden_states,
            attentions=all_self_attentions,
            cross_attentions=all_cross_attentions,
        )


class GPT2LMPlus(GPT2LMHeadModel):

    def __init__(self, config):
        super().__init__(config)
        self.transformer = GPT2ModelPlus(config)
#        self.lm_head = nn.Linear(config.n_embd, config.vocab_size, bias=False)

        # Model parallel
        self.model_parallel = False
        self.device_map = None

        # Initialize weights and apply final processing
        self.post_init()

    def freeze_weights(self):
        for param in self.transformer.parameters():
            param.requires_grad = False

    def set_up_prompt_tuning(self, k, entry_point):
        self.freeze_weights()
        self.transformer.set_up_prompt_tuning(k, entry_point)

    def save_prompt_checkpoint( self, fn ):
        np.save( fn, self.transformer.pt_prefix.clone().detach().cpu().numpy() )

    def load_prompt_checkpoint( self, fn ):
        error('deprecated')
        foo = torch.Tensor( np.load( fn ) )
        if not foo.shape == self.transformer.pt_prefix.shape:
            error('shape mismatch!')
        device = self.transformer.pt_prefix.device
        self.transformer.pt_prefix.data = foo.to( device )
