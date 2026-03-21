# Base image: Python 3.9-slim as per best practices
FROM python:3.9-slim

# Set working directory to /app as per requirements
WORKDIR /app

# Install system dependencies needed for GCC and ML libraries
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files into the container
COPY . .

# Expose port 8501 for Streamlit (Phase 8)
EXPOSE 8501

# Default command (overridden by docker-compose for services)
CMD ["python", "--version"]