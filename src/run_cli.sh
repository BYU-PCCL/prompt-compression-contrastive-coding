#!/bin/bash

docker run -it \
  --rm \
  --gpus \"device=$1\" \
  -v /home/wingated:/home/wingated \
  -w `pwd` \
  --net host \
  -e NVIDIA_DRIVER_CAPABILITIES=all \
  pytorch/pytorch:1.8.1-cuda11.1-cudnn8-devel /bin/bash

#  softprompt:0.1 /bin/bash
# pip install transformers lm_eval


