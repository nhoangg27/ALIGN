CUDA_VISIBLE_DEVICES=0 fairseq-train \
    --user-dir /workspaces/align/graphormer \
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
    --lr 1e-4 \
    --fp16 \
    --encoder-layers 8 \
    --wandb-project 'CCS_preds' \
    --encoder-embed-dim 512 \
    --encoder-ffn-embed-dim 512 \
    --encoder-attention-heads 128 \
    --mlp-layers 5 \
    --max-epoch 100 \
    --no-epoch-checkpoints \
    --freeze-level -4  \
    --save-dir '/workspaces/align/checkpoints' \
    --pretrained-model-name /workspaces/align/model_weights/129/best_model_last_129.pt \
	  --finetune-from-model /workspaces/align/model_weights/129/best_model_last_129.pt \



