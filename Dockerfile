# Use official Python 3.10 slim image as base
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy dependency list first (for better Docker layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Cloud Run injects the PORT environment variable at runtime.
# Gunicorn will bind to it using the shell form of CMD below.
ENV PORT=8080

# Run the app with gunicorn (production WSGI server)
# --bind 0.0.0.0:$PORT makes it accessible from outside the container
CMD gunicorn --bind 0.0.0.0:$PORT app:app
