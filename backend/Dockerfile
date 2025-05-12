# ===============================
# Ultima Bot — Backend Dockerfile
# ===============================

# --- Base Python Slim Image ---
FROM python:3.11-slim

# --- Environment Configuration ---
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# --- Working Directory ---
WORKDIR /app

# --- System Dependencies ---
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev \
    curl \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# --- Install Python Dependencies ---
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# --- Copy Backend App Source ---
COPY app ./app

# --- Optional: Copy Entrypoint Script (if used) ---
# COPY launch-ultima.sh ./launch-ultima.sh
# RUN chmod +x launch-ultima.sh

# --- Set Logging Level (optional override) ---
ENV LOG_LEVEL=info

# --- Expose Uvicorn Port ---
EXPOSE 8080

# --- Run FastAPI App via Uvicorn ---
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
