FROM nvidia/cuda:13.0.0-devel-ubuntu22.04

# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

# ---------------------------------------------------------------------------
# Create non-root user
# ---------------------------------------------------------------------------
RUN groupadd -g 61000 app \
    && useradd -g 61000 -u 61000 -ms /bin/bash app

# ---------------------------------------------------------------------------
# Application code
# ---------------------------------------------------------------------------
WORKDIR /app

# 1. Installa git (serve come root per scaricare da GitHub)
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN uv pip sync requirements.txt --system

# 2. Fix bitsandbytes per CUDA 13
COPY requirements.txt ./
RUN uv pip sync requirements.txt --system

# Compila bitsandbytes from source per CUDA 13
RUN apt-get update && apt-get install -y cmake && rm -rf /var/lib/apt/lists/* && \
    pip uninstall bitsandbytes -y && \
    git clone https://github.com/bitsandbytes-foundation/bitsandbytes.git /tmp/bnb && \
    cd /tmp/bnb && \
    cmake -DCOMPUTE_BACKEND=cuda -S . && \
    make && \
    pip install -e . --no-build-isolation
COPY --chown=app:app . .

# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------
RUN chmod +x /app/scripts/entrypoint.sh

USER app

EXPOSE 8000

ENTRYPOINT ["/app/scripts/entrypoint.sh"]
CMD ["chill"]

# ---------------------------------------------------------------------------
# Bitsandbytes Fix for CUDA 13
# ---------------------------------------------------------------------------

FROM nvidia/cuda:12.4.1-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    CUDA_HOME=/usr/local/cuda \
    PATH=/usr/local/cuda/bin:$PATH \
    LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip python3-dev git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip

RUN pip install --no-cache-dir torch==2.5.1 torchvision torchaudio \
    --index-url https://download.pytorch.org/whl/cu124

# Lascia che unsloth-zoo scelga le sue versioni di transformers/trl/accelerate
RUN pip install --no-cache-dir \
    "git+https://github.com/unslothai/unsloth-zoo.git" \
    "unsloth @ git+https://github.com/unslothai/unsloth.git"

# Fix torchao dopo unsloth (unsloth-zoo lo forza a 0.17.0)
RUN pip install --no-cache-dir --force-reinstall torchao==0.6.1

# bitsandbytes >= 0.46.1 richiesto da transformers 5.5.0
RUN pip install --no-cache-dir "bitsandbytes>=0.46.1"

# agno per la simulazione
RUN pip install --no-cache-dir agno datasets

COPY . /app

CMD ["python3", "agents/3_barista_digital_twin_simulation/fine_tuning_barista.py"]

RUN pip uninstall -y hf_transfer hf-xet