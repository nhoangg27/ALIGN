#!/bin/bash

# Dynamically find the project root (2 levels up)
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
PROJECT_ROOT=$(realpath "$SCRIPT_DIR/../../")

python evaluate_CCS.py \
    --user-dir "$PROJECT_ROOT/graphormer" \
    --num-workers 32 \
    --ddp-backend=legacy_ddp \
	--user-data-dir CCS_loader \
	--dataset-name CCS_test \
    --task graph_prediction \
	--criterion rmse \
	--arch graphormer_base \
    --encoder-layers 8 \
    --encoder-embed-dim  512 \
    --encoder-ffn-embed-dim 512 \
    --encoder-attention-heads 128 \
    --mlp-layers 5 \
    --batch-size 64 \
    --num-classes 1 \
    --save-dir "$PROJECT_ROOT/CCS_checkpoints/checkpoint_last.pt" \
    --split train \
    # --save-path "$PROJECT_ROOT/results/CCS_sample.csv" \
