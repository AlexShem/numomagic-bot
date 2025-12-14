# Stage 1: Build Stage
FROM python:3.13-slim as builder

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Copy uv binary from official uv container image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set working directory in container
WORKDIR /bot

# Copy project metadata files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv (system-wide installation)
RUN uv pip install --system .

# Copy remaining application code
COPY . /bot

# Stage 2: Final Image
FROM python:3.13-slim

# Copy uv binary from official uv container image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy installed packages and application code from the builder stage
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /bot /app

WORKDIR /app

# Expose port for webhook mode (Railway uses PORT env var)
EXPOSE 8000

CMD ["uv", "run", "python", "main.py"]