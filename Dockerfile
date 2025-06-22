# Use the Python 3 Alpine official image
FROM python:3.10-alpine

# Set working directory
WORKDIR /app

# Install ffmpeg and other build dependencies
RUN apk add --no-cache ffmpeg gcc musl-dev libffi-dev

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the web service on container startup
CMD ["hypercorn", "main:app", "--bind", "::"]
