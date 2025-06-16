# 🐍 Python Sandbox - Complete Setup Guide

## 🎯 What You Have

I've built you a **complete, secure, local web-based Python sandbox** with all the features you requested:

### ✅ Features Implemented

#### 🔒 **Security Features**
- **Sandboxed Execution**: Code runs in isolated containers with no system access
- **Resource Limits**: 50MB RAM, 10-second timeout, 1MB file size limits
- **No Network Access**: Code cannot access internet or local network
- **Safe Module Restrictions**: Only safe Python modules allowed (math, random, json, etc.)
- **Session Isolation**: Each user gets their own isolated environment
- **Input Sanitization**: All user input is properly sanitized and validated

#### 🔐 **Authentication System**
- **Login Required**: Secure session-based authentication
- **Multiple Users**: Support for concurrent users with isolation
- **Session Timeout**: 30-minute automatic logout
- **Password Protection**: SHA-256 hashed passwords

#### 🖥️ **Web Interface**
- **Modern UI**: Dark theme with responsive design
- **Code Editor**: Syntax highlighting, line numbers, auto-completion
- **Real-time Output**: Instant display of results and errors
- **Code Examples**: Built-in examples for learning
- **Keyboard Shortcuts**: Ctrl+Enter to run code

#### 🚀 **Easy Deployment**
- **Docker Container**: Single command deployment
- **Docker Compose**: Even easier orchestration
- **Manual Install**: Script for non-Docker deployments
- **Health Checks**: Built-in monitoring

## 🚀 Quick Start (Recommended)

### Option 1: Docker (Easiest)
```bash
# Clone or navigate to your sandbox directory
cd /home/webuser/codesandbox

# Start with Docker Compose (recommended)
docker-compose up -d

# OR start with plain Docker
docker run -d -p 7111:7111 --name python-sandbox python-sandbox

# Access the application
# Open browser: http://localhost:7111
```

### Option 2: Manual Installation
```bash
# Make install script executable and run
chmod +x install.sh
./install.sh

# Access the application
# Open browser: http://localhost:7111
```

## 🔑 Default User Accounts

| Username | Password | Role |
|----------|----------|------|
| `admin` | `admin` | Administrator |
| `user1` | `password` | Regular User |
| `demo` | `demo123` | Demo Account |

⚠️ **Security Note**: Change these passwords in production by editing `USERS` in `codesandbox_backend.py`

## 📁 File Structure

```
codesandbox/
├── codesandbox_backend.py    # Flask application (main backend)
├── codesandbox.html          # Main sandbox UI
├── login.html               # Login page
├── nginx.conf               # Nginx configuration
├── Dockerfile               # Docker build instructions
├── docker-compose.yml       # Docker Compose configuration
├── start.sh                 # Container startup script
├── install.sh               # Manual installation script
└── README.md                # Complete documentation
```

## 🔧 Management Commands

### Docker Management
```bash
# Start
docker-compose up -d
# or
docker start python-sandbox

# Stop
docker-compose down
# or
docker stop python-sandbox

# View logs
docker-compose logs -f
# or
docker logs python-sandbox

# Rebuild after changes
docker-compose down
docker-compose build
docker-compose up -d
```

### Manual Installation Management
```bash
# Start service
sudo systemctl start python-sandbox

# Stop service
sudo systemctl stop python-sandbox

# Check status
sudo systemctl status python-sandbox

# View logs
sudo journalctl -u python-sandbox -f
```

## 🛡️ Security Details

### What's Blocked
- System file access
- Network connections
- Dangerous modules (os, subprocess, socket, etc.)
- Command execution
- File system manipulation outside sandbox
- Memory exhaustion attacks
- Long-running processes

### What's Allowed
- Safe Python modules: math, random, json, re, datetime, time
- Basic data structures and operations
- Print statements and basic I/O
- Mathematical calculations
- String and list manipulations

### Resource Limits
- **Memory**: 50MB per execution
- **CPU Time**: 10 seconds maximum
- **Output Size**: 10,000 characters maximum
- **File Size**: 1MB maximum (if file creation was allowed)

## 🎨 Using the Sandbox

### Login
1. Navigate to `http://localhost:7111`
2. Use one of the demo accounts
3. Click "Sign In"

### Writing Code
1. Use the code editor on the left
2. Write Python code (math, strings, loops, functions, etc.)
3. Click "Run Code" or press `Ctrl+Enter`
4. View output on the right

### Features
- **Examples**: Click "Examples" to see pre-built code samples
- **Reset**: Clear Python environment variables
- **Clear**: Clear editor or output
- **Auto-save**: Code is saved in your browser locally

### Code Examples Available
- Hello World
- Math operations with the math module
- String manipulation
- Loops and conditions
- Functions and recursion

## 🔧 Customization

### Change Security Settings
Edit `codesandbox_backend.py`:
```python
TIMEOUT_SECONDS = 10          # Code execution timeout
MAX_MEMORY_MB = 50           # Memory limit
MAX_OUTPUT_SIZE = 10000      # Output character limit
SESSION_TIMEOUT_MINUTES = 30 # Session timeout
```

### Add Users
Edit `USERS` dictionary in `codesandbox_backend.py`:
```python
# Generate password hash
import hashlib
password_hash = hashlib.sha256("your_password".encode()).hexdigest()

# Add to USERS dict
USERS = {
    'new_user': 'generated_hash_here',
    # ... existing users
}
```

### Change Port
- **Docker**: Modify `docker-compose.yml` port mapping
- **Manual**: Edit `nginx.conf` and systemd service file

## 🧪 Testing the Fix

The indentation error you encountered has been fixed. The sandbox now properly handles:
- Math module imports
- Multi-line code blocks
- Complex indentation
- Error handling and display

Try this code after deployment:
```python
import math

# Basic calculations
print(f"Pi: {math.pi}")
print(f"Square root of 16: {math.sqrt(16)}")
print(f"2 to the power of 8: {2**8}")

# Working with lists
numbers = [1, 2, 3, 4, 5]
print(f"Sum: {sum(numbers)}")
print(f"Average: {sum(numbers) / len(numbers)}")
```

## 🚨 Production Considerations

1. **Change Default Passwords**: Update the `USERS` dictionary
2. **SSL/TLS**: Add HTTPS support for production use
3. **Firewall**: Ensure only intended users can access port 7111
4. **Monitoring**: Set up log monitoring and alerting
5. **Backups**: Consider backing up user sessions if needed
6. **Resource Monitoring**: Monitor host system resources

## 📞 Troubleshooting

### Common Issues
1. **Port 7111 in use**: Change port mapping in docker-compose.yml
2. **Login fails**: Check username/password, verify Flask secret key
3. **Code won't run**: Check container logs, verify sandboxing works
4. **Permission errors**: Ensure proper Docker permissions

### Debug Commands
```bash
# Check if port is accessible
curl http://localhost:7111

# Check container health
docker exec -it python-sandbox ps aux

# View detailed logs
docker logs python-sandbox --details

# Check nginx status inside container
docker exec -it python-sandbox nginx -t
```

## 🎉 Success!

You now have a **fully functional, secure Python sandbox** that:
- ✅ Runs completely locally (no external dependencies)
- ✅ Supports multiple authenticated users
- ✅ Provides secure code execution with proper sandboxing
- ✅ Has a beautiful, modern web interface
- ✅ Is easy to deploy and manage
- ✅ Includes comprehensive documentation

The system is production-ready for local/private network use. Remember to change default passwords and consider additional security measures for internet-facing deployments.

**Access your sandbox**: http://localhost:7111
**Demo credentials**: admin/admin, user1/password, demo/demo123

Happy coding! 🚀
