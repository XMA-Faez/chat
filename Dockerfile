FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV REDIS_HOST=localhost

# Set work directory
WORKDIR /app

# Install system dependencies including Redis
RUN apt-get update && apt-get install -y \
    gcc \
    netcat-traditional \
    redis-server \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . /app/

# Create directory for static files and logs
RUN mkdir -p /app/staticfiles /var/log/supervisor

# Setup Redis config for container
RUN echo "daemonize no" >> /etc/redis/redis.conf && \
    echo "bind 127.0.0.1" >> /etc/redis/redis.conf

# Copy supervisor config
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Copy and make entrypoint executable
COPY docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh

# Expose port
EXPOSE 8000

# Run supervisor to manage both Redis and Django
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]