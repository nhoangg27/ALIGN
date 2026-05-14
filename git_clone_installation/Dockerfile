# Use NVIDIA CUDA 12.4 image to match the host system
FROM nvidia/cuda:12.4.0-runtime-ubuntu22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC
ENV CUDA=cu121

# Explicitly set NVIDIA environment variables
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    git \
    curl \
    build-essential \
    ca-certificates \
    nvidia-cuda-toolkit \
    && rm -rf /var/lib/apt/lists/*

# Install Miniconda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-py310_24.1.2-0-Linux-x86_64.sh -O miniconda.sh && \
    bash miniconda.sh -b -p /opt/conda && \
    rm miniconda.sh

# Setup Conda in PATH
ENV PATH="/opt/conda/bin:$PATH"

# Create and activate environment (renamed to align)
RUN conda create -n align python=3.9.18 -y
ENV CONDA_DEFAULT_ENV=align
ENV PATH="/opt/conda/envs/align/bin:$PATH"

# Downgrade pip to avoid incompatibilities
RUN pip install --upgrade "pip<24.1"

# Install heavy dependencies
RUN pip install dgl==1.1.3+${CUDA} -f https://data.dgl.ai/wheels/${CUDA}/repo.html
RUN pip install torch-geometric==2.4.0
RUN pip install torch-scatter torch-sparse -f https://data.pyg.org/whl/torch-2.1.0+${CUDA}.html
RUN pip install torch==2.1.0+${CUDA} torchvision==0.16.0+${CUDA} --index-url https://download.pytorch.org/whl/${CUDA}

RUN pip install \
    ogb==1.3.2 \
    matplotlib \
    numpy==1.23 \
    dgllife==0.3.2 \
    mordred==1.2.0 \
    torchaudio==2.1.0 \
    rdkit==2023.9.1 \
    Cython==3.0.4

# Set workspace
WORKDIR /workspaces/align

# Cache-busting ARG: Change this value to force a fresh clone
ARG CACHEBUST=1

# Remove existing folder if it exists and clone the ALIGN repo
RUN rm -rf /workspaces/align && \
    git clone https://github.com/nhoangg27/ALIGN.git .

# Install the internal fairseq subdirectory
WORKDIR /workspaces/align/fairseq
RUN pip install --editable . && \
    python setup.py build_ext --inplace

# Return to main workspace
WORKDIR /workspaces/align

# Environment variable for model weights
ENV MODEL_WEIGHTS_PATH=/workspaces/align/model_weights

# Verify GPU access
RUN nvidia-smi || echo "Note: nvidia-smi may fail during build"
RUN python3 -c "import torch; print('CUDA Config Check: PyTorch version', torch.__version__); print('CUDA Available:', torch.cuda.is_available())" || echo "Check failed"

# Add message to bash startup
RUN echo 'echo "Run setup.sh to initialize the ALIGN development environment"' >> /root/.bashrc

CMD ["/bin/bash"]
