#!/bin/bash

# Python Sandbox Installation Script
# This script installs and configures the Python Sandbox on Ubuntu/Debian systems

set -e

echo "🐍 Python Sandbox Installation Script"
echo "======================================"

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo "❌ This script should not be run as root for security reasons."
   echo "Please run as a regular user with sudo privileges."
   exit 1
fi

# Check for sudo privileges
if ! sudo -n true 2>/dev/null; then
    echo "❌ This script requires sudo privileges."
    echo "Please ensure your user can run sudo commands."
    exit 1
fi

# Detect OS
if [[ -f /etc/debian_version ]]; then
    OS="debian"
elif [[ -f /etc/redhat-release ]]; then
    OS="redhat"
else
    echo "❌ Unsupported operating system. This script supports Debian/Ubuntu and RHEL/CentOS."
    exit 1
fi

echo "📋 Detected OS: $OS"

# Update package manager
echo "📦 Updating package manager..."
if [[ $OS == "debian" ]]; then
    sudo apt-get update
elif [[ $OS == "redhat" ]]; then
    sudo yum update -y
fi

# Install dependencies
echo "📦 Installing dependencies..."
if [[ $OS == "debian" ]]; then
    sudo apt-get install -y python3 python3-pip nginx curl
elif [[ $OS == "redhat" ]]; then
    sudo yum install -y python3 python3-pip nginx curl
fi

# Install Python packages
echo "🐍 Installing Python packages..."
pip3 install --user flask

# Create application directory
APP_DIR="/opt/python-sandbox"
echo "📁 Creating application directory: $APP_DIR"
sudo mkdir -p $APP_DIR
sudo chown $USER:$USER $APP_DIR

# Copy application files
echo "📄 Copying application files..."
cp codesandbox_backend.py $APP_DIR/
cp codesandbox.html $APP_DIR/
cp login.html $APP_DIR/
cp README.md $APP_DIR/

# Create systemd service
echo "⚙️ Creating systemd service..."
sudo tee /etc/systemd/system/python-sandbox.service > /dev/null <<EOF
[Unit]
Description=Python Sandbox Web Application
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$APP_DIR
Environment=PATH=/home/$USER/.local/bin:/usr/local/bin:/usr/bin:/bin
ExecStart=/usr/bin/python3 codesandbox_backend.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Configure nginx
echo "🌐 Configuring nginx..."
sudo cp nginx.conf /etc/nginx/nginx.conf

# Test nginx configuration
if ! sudo nginx -t; then
    echo "❌ Nginx configuration test failed. Please check the configuration."
    exit 1
fi

# Create log directory
sudo mkdir -p /var/log/python-sandbox
sudo chown $USER:$USER /var/log/python-sandbox

# Enable and start services
echo "🚀 Starting services..."
sudo systemctl daemon-reload
sudo systemctl enable python-sandbox
sudo systemctl start python-sandbox
sudo systemctl enable nginx
sudo systemctl restart nginx

# Check service status
echo "🔍 Checking service status..."
if systemctl is-active --quiet python-sandbox; then
    echo "✅ Python Sandbox service is running"
else
    echo "❌ Python Sandbox service failed to start"
    echo "Check logs with: sudo journalctl -u python-sandbox"
    exit 1
fi

if systemctl is-active --quiet nginx; then
    echo "✅ Nginx service is running"
else
    echo "❌ Nginx service failed to start"
    echo "Check logs with: sudo journalctl -u nginx"
    exit 1
fi

# Test the application
echo "🧪 Testing application..."
sleep 5
if curl -s -o /dev/null -w "%{http_code}" http://localhost:7111 | grep -q "200"; then
    echo "✅ Application is responding correctly"
else
    echo "⚠️ Application might not be responding. Check the logs."
fi

# Display success message
echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "📝 Next steps:"
echo "1. Open your web browser and navigate to: http://localhost:7111"
echo "2. Use one of these demo accounts to login:"
echo "   - Username: admin, Password: admin"
echo "   - Username: user1, Password: password"
echo "   - Username: demo, Password: demo123"
echo ""
echo "🔧 Management commands:"
echo "   Start:   sudo systemctl start python-sandbox"
echo "   Stop:    sudo systemctl stop python-sandbox"
echo "   Restart: sudo systemctl restart python-sandbox"
echo "   Status:  sudo systemctl status python-sandbox"
echo "   Logs:    sudo journalctl -u python-sandbox -f"
echo ""
echo "⚠️ Security Note:"
echo "Remember to change the default passwords in production!"
echo "Edit $APP_DIR/codesandbox_backend.py to modify user accounts."
echo ""
echo "📚 For more information, see the README.md file."
