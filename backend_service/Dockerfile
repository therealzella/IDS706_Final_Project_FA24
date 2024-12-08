# Build stage
FROM python:3.9-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir uvicorn

# Copy source code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser

# Final stage using distroless
FROM gcr.io/distroless/python3-debian11

# Copy Python installation and libraries
COPY --from=builder /usr/local/lib /usr/local/lib
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /app /app
COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /lib /lib

# Set working directory
WORKDIR /app

# Use non-root user
USER appuser

# Create volume for logs
VOLUME /app/logs

# Expose FastAPI port
EXPOSE 8000

# Run the application
ENTRYPOINT ["/usr/local/bin/uvicorn"]
CMD ["app:app", "--host", "0.0.0.0", "--port", "8000"]