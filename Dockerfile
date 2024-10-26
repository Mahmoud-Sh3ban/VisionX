# Stage 1: Builder
FROM python:3.9-slim-buster AS builder

# Set up the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Final image
FROM python:3.9-slim-buster

# Install NGINX
RUN apt-get update && \
    apt-get install -y nginx && \
    rm -rf /var/lib/apt/lists/*

# Set up the working directory
WORKDIR /app

# Copy installed Python packages from builder stage
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

# Copy application code
COPY . .

# Copy the NGINX configuration
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

# Expose ports and set environment variables
ENV PYTHONUNBUFFERED=1
EXPOSE 80 5000

# Start both the Flask app and NGINX
CMD ["sh", "-c", "python3 /app/app.py & nginx -g 'daemon off;'"]

