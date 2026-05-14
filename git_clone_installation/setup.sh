#!/bin/bash
set -e
echo "Verifying environment..."

WORKSPACE_DIR="/workspace/align"

# Handle Model Weights Symlink (if needed by your code logic)
if [ -d "$WORKSPACE_DIR/model_weights" ]; then
  echo "Setting up model weights directory..."
  mkdir -p /opt/align
  ln -sf "$WORKSPACE_DIR/model_weights" /opt/align/model_weights
fi

echo "Ready!"
