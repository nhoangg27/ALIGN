#!/bin/bash

# Dynamically find the project root (2 levels up)
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
PROJECT_ROOT=$(realpath "$SCRIPT_DIR/../../")

CUDA_VISIBLE_DEVICES=0 fairseq-train \
    --user-dir "$PROJECT_ROOT/graphormer" \
    --batch-size 64 \
    --num-workers 20 \
    --ddp-backend=legacy_ddp \
    --seed 23 \
    --user-data-dir CCS_loader \
    --dataset-name CCS \
    --task graph_prediction_with_flag \
    --criterion rmse \
    --arch graphormer_base \
    --num-classes 1 \
    --attention-dropout 0.15 --act-dropout 0.10 --dropout 0.10 \
    --optimizer adam --adam-betas '(0.9, 0.999)' --adam-eps 1e-8 --clip-norm 5.0 --weight-decay 0.01 \
    --lr-scheduler polynomial_decay --power 1 --warmup-updates 95 --total-num-update 631 \
    --lr 3e-4 \
    --fp16 \
    --encoder-layers 8 \
    --encoder-embed-dim 512 \
    --encoder-ffn-embed-dim 512 \
    --encoder-attention-heads 128 \
    --mlp-layers 5 \
    --max-epoch 100 \
    --no-epoch-checkpoints \
    --freeze-level 0  \
    --save-dir "$PROJECT_ROOT/CCS_checkpoints" \
    --pretrained-model-name "$PROJECT_ROOT/model_weights/129/best_model_last_129.pt" \
	--finetune-from-model "$PROJECT_ROOT/model_weights/129/best_model_last_129.pt" \



