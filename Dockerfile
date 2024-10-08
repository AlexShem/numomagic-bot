# Stage 1: Build Stage
FROM python:3.11-slim as builder

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install Rust
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Устанавливаем рабочую директорию в контейнере
WORKDIR /bot

# Копируем файлы проекта в контейнер
COPY . /bot

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Stage 2: Final Image
FROM python:3.11-slim

# Copy installed packages and application code from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /bot /app

WORKDIR /app

CMD ["python3", "./main.py"]