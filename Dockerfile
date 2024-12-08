# Build stage
FROM python:3.9-slim as builder

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application code
COPY . .

# Production stage using distroless
FROM gcr.io/distroless/python3-debian11

# Copy Python environment from builder
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /app /app

# Set working directory
WORKDIR /app

# Expose ports for both services
EXPOSE 8000 8501

# Using Python module to start both services
ENTRYPOINT ["python", "-m"]
CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]