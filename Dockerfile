FROM python:3.9-slim

# Install system dependencies required for image processing (OpenCV)
# rembg depends on opencv-python-headless which might need these
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create a directory for u2net models to persist/cache if possible, 
# though on Railway standard ephemeral storage this resets on redeploy.
# We set the environment variable for rembg to store models in a known path
ENV U2NET_HOME=/app/.u2net

# Expose the port (Railway will override PORT env var)
EXPOSE 8000

# Command to run the application
# We use shell form to allow variable expansion if needed, but array form is safer.
# Railway sets $PORT variable. We must bind to 0.0.0.0.
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
