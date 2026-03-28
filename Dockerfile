# Base image: Python 3.9-slim as per best practices
FROM python:3.9-slim

# Set working directory to /app
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose ports for both API and UI Layers
EXPOSE 8000
EXPOSE 8501

# Run FastAPI using uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]