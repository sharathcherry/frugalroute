# ============================================================
# FrugalRoute — Submission Dockerfile
# AMD Developer Hackathon ACT II · Track 1
#
# Build: docker build -t frugalroute .
#
# Run (submission contract):
#   docker run --rm \
#     --device=/dev/kfd --device=/dev/dri \
#     -e REMOTE_BASE_URL -e REMOTE_API_KEY -e REMOTE_MODEL \
#     -v /path/tasks.jsonl:/data/tasks.jsonl:ro \
#     -v /path/out:/data/out \
#     frugalroute
#
# The entrypoint:
#   1. Starts vLLM serving the baked-in local model (AMD ROCm).
#   2. Waits for the endpoint to become ready.
#   3. Runs the FrugalRoute pipeline over /data/tasks.jsonl.
#   4. Writes /data/out/results.jsonl  (id, answer, source, remote_tokens).
# ============================================================

# ---- Stage 1: model-download (separate cache layer) ----
# We use a plain Python image here so the Hugging Face download can be cached
# independently of the ROCm layer (which is large).  At build time we pull
# only the model weights into /model-cache; the ROCm stage copies them in.
FROM python:3.11-slim AS model-fetch

ARG HF_MODEL=Qwen/Qwen2.5-7B-Instruct
ENV HF_HOME=/model-cache \
    TRANSFORMERS_CACHE=/model-cache \
    HF_HUB_DISABLE_PROGRESS_BARS=1

RUN pip install --no-cache-dir huggingface_hub && \
    python -c "from huggingface_hub import snapshot_download; \
               snapshot_download('${HF_MODEL}', ignore_patterns=['*.msgpack','*.h5','flax_*'])"

# ---- Stage 2: ROCm runtime + FrugalRoute ----
FROM rocm/vllm:latest AS runtime
# rocm/vllm ships ROCm + vLLM pre-installed; swap tag for a pinned version if needed.

WORKDIR /app

# Python deps (router code only — vLLM already in base image)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application code
COPY . .

# Baked-in model weights from fetch stage
ARG HF_MODEL=Qwen/Qwen2.5-7B-Instruct
ENV HF_MODEL=${HF_MODEL} \
    HF_HOME=/model-cache \
    TRANSFORMERS_CACHE=/model-cache

COPY --from=model-fetch /model-cache /model-cache

# ---- Runtime environment defaults ----
ENV MOCK=0 \
    LOCAL_BASE_URL=http://127.0.0.1:8001/v1 \
    LOCAL_API_KEY=frugalroute-local \
    LOCAL_MODEL=${HF_MODEL} \
    JUDGE_MODE=selfrate \
    GATE_MODE=calibrated \
    CONFIDENCE_THRESHOLD=0.7 \
    CALIB_PATH=calib.json \
    COMPRESS=1 \
    COMPRESS_RATE=0.5 \
    CACHE_BACKEND=difflib \
    # Remote provider creds injected at runtime (not baked in)
    REMOTE_PROVIDER=fireworks

# ---- Entrypoint ----
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

# Default command reads from the submission-standard path; override at runtime.
CMD ["--input", "/data/tasks.jsonl", "--output", "/data/out/results.jsonl"]
