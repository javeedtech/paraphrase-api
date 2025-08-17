FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy application code first
COPY . .

# Install dependencies directly with pip
RUN pip install --no-cache-dir \
    flask>=3.1.1 \
    flask-cors>=6.0.1 \
    flask-sqlalchemy>=3.1.1 \
    gunicorn>=23.0.0 \
    psycopg2-binary>=2.9.10 \
    requests>=2.32.4 \
    email-validator>=2.2.0 \
    torch>=2.0.0 \
    transformers>=4.30.0

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "main:app"]