# Build stage
FROM python:3.9-slim as builder

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --user --no-cache-dir -r requirements.txt

# Copy all application code
COPY . .

# Production stage using distroless
FROM gcr.io/distroless/python3-debian11

# Copy Python packages from builder stage
COPY --from=builder /root/.local/lib/python3.9/site-packages /usr/lib/python3.9/site-packages

# Copy application code
COPY --from=builder /app /app

# Set working directory
WORKDIR /app

# Create necessary directories and copy config
COPY --from=builder /app/.streamlit /app/.streamlit

# Expose ports for both services
EXPOSE 8000 8501

# Start both services using Python modules
ENTRYPOINT ["python", "-m"]
CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]