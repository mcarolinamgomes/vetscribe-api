FROM python:3.10-slim

# System dependencies: ffmpeg is required by whisper, gcc/g++/libffi for building wheels
RUN apt-get update && apt-get install -y \
    ffmpeg \
    gcc \
    g++ \
    libffi-dev \
    libsndfile1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy only requirements first for layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source code
COPY . .

# Run FastAPI with Hypercorn
CMD ["hypercorn", "main:app", "--bind", "0.0.0.0:8000"]
