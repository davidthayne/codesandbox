FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    nginx \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip install --no-cache-dir flask

# Set working directory
WORKDIR /root

# Copy application files
COPY codesandbox_backend.py /root/codesandbox_backend.py
COPY codesandbox.html /root/codesandbox.html
COPY login.html /root/login.html
COPY nginx.conf /etc/nginx/nginx.conf
COPY start.sh /root/start.sh

# Make start script executable
RUN chmod +x /root/start.sh

# Create directory for sandboxes
RUN mkdir -p /tmp/sandboxes

# Expose port
EXPOSE 7111

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:7111/ || exit 1

# Start the application
CMD ["/root/start.sh"]
