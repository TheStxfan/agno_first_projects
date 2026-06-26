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