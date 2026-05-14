#!/bin/bash
set -e
echo "Setting up environment after container creation..."

WORKSPACE_DIR="/workspace/align"
FAIRSEQ_DIR="$WORKSPACE_DIR/fairseq"

# 1. Verify workspace exists
if [ ! -d "$WORKSPACE_DIR" ]; then
  echo "ERROR: Workspace directory not found at $WORKSPACE_DIR"
  exit 1
fi

# 2. Clean up and Install Fairseq
if [ -d "$FAIRSEQ_DIR" ]; then
  echo "Found fairseq source at: $FAIRSEQ_DIR"
  cd "$FAIRSEQ_DIR"
  
  # Remove any previous broken editable links or build artifacts
  pip uninstall fairseq -y || echo "No existing fairseq to uninstall"
  rm -rf *.egg-info build/ dist/

  echo "Installing fairseq into Conda environment (Standard Install)..."
  # Standard install copies the files to site-packages, preventing shadowing
  pip install .
else
  echo "ERROR: fairseq directory not found at $FAIRSEQ_DIR"
  exit 1
fi

# 3. Handle Model Weights Symlink
if [ -d "$WORKSPACE_DIR/model_weights" ]; then
  echo "Setting up model weights directory..."
  mkdir -p /opt/graphormer
  # Use -sf to force/overwrite the symlink if it already exists
  ln -sf "$WORKSPACE_DIR/model_weights" /opt/graphormer/model_weights
fi

echo "Environment setup complete!"
