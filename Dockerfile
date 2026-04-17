# Use lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Prevent Python buffering issues
ENV PYTHONUNBUFFERED=1

# Install system dependencies (important for numpy, sklearn)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy full project
COPY . .

# Expose port (Render uses 10000 internally)
EXPOSE 10000

# Start FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]