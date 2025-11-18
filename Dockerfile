# Multi-stage build for optimized image
FROM python:3.10-slim as builder

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg libsm6 libxext6 libxrender-dev libgomp1 git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Download Whisper model
RUN python -c "from faster_whisper import WhisperModel; WhisperModel('base')"

# Final stage
FROM python:3.10-slim

RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

WORKDIR /app
COPY . .

RUN mkdir -p data/models data/input data/output data/temp

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
