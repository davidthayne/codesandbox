# Advanced Python Sandbox Web Application

A feature-rich, secure, web-based Python sandbox with advanced functionality including built-in apps, user management, and modern UI features. Runs completely locally without any external dependencies.

## ✨ Key Features

### 🔒 Advanced Security & Authentication
- **Sandboxed Execution**: Python code runs in isolated environments with restricted access
- **Resource Limits**: Memory, CPU time, and file size restrictions prevent system abuse
- **Password Management**: Change passwords, admin controls, and user configuration
- **Session-based Authentication**: Secure login system with timeout protection
- **Session Isolation**: Each user gets their own isolated Python environment
- **Admin Panel**: Administrative controls for user management and system settings

### 🖥️ Modern Web Interface
- **Responsive Design**: Clean, modern UI that works on all screen sizes
- **Advanced Code Editor**: Syntax highlighting, line numbers, and auto-completion
- **Terminal Theme Toggle**: Switch between light and dark themes for the code editor
- **Fullscreen Support**: Full-screen mode for code editor and output areas with keyboard shortcuts
- **Real-time Output**: Instant display of code execution results and errors
- **Split Layout**: Resizable panels for optimal workspace organization

### 📱 Built-in Applications
- **Advanced Notepad**: Multi-tab text editor with file management, themes, and localStorage persistence
- **Memory Game**: Interactive memory card game with multiple difficulty levels and responsive design
- **Persistent Storage**: User apps and data survive container restarts
- **App Management**: Save, load, and organize your custom applications

### 🎮 Interactive Features
- **Code Examples**: Comprehensive library of Python examples and tutorials
- **Keyboard Shortcuts**: 
  - `Ctrl+Enter`: Run code
  - `F11`: Toggle fullscreen for code editor
  - `Shift+F11`: Toggle fullscreen for output area
  - `Escape`: Exit fullscreen mode
- **Session Management**: Automatic cleanup and environment isolation

### 🐳 Production-Ready Deployment
- **Docker Container**: Single command deployment with Docker Compose support
- **Nginx Integration**: Production-ready reverse proxy configuration
- **No External Dependencies**: Fully self-contained with no CDN requirements
- **Easy Installation**: Automated setup scripts included

## Quick Start

### Option 1: Docker Deployment (Recommended)

1. **Build the Docker image:**
   ```bash
   docker build -t python-sandbox .
   ```

2. **Run the container:**
   ```bash
   docker run -d -p 7111:7111 --name python-sandbox python-sandbox
   ```

3. **Access the application:**
   Open your web browser and navigate to: `http://localhost:7111`

### Option 2: Manual Installation

1. **Install dependencies:**
   ```bash
   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install python3 python3-pip nginx
   
   # Install Python packages
   pip3 install flask
   ```

2. **Configure nginx:**
   ```bash
   sudo cp nginx.conf /etc/nginx/nginx.conf
   sudo systemctl restart nginx
   ```

3. **Run the application:**
   ```bash
   python3 codesandbox_backend.py
   ```

4. **Access the application:**
   Open your web browser and navigate to: `http://localhost:7111`

## Default User Accounts

The system comes with three pre-configured demo accounts:

| Username | Password | Description |
|----------|----------|-------------|
| `admin`  | `admin`  | Administrator account |
| `user1`  | `password` | Regular user account |
| `demo`   | `demo123` | Demo account |

**⚠️ Important**: Change these default passwords in production by modifying the `USERS` dictionary in `codesandbox_backend.py`.

## Usage

### Logging In
1. Navigate to the application URL
2. Use one of the default accounts or configure your own
3. Click "Sign In" to access the sandbox

### Password Management
- **Change Password**: Use the settings panel to update your password
- **Admin Controls**: Admins can manage user accounts and system settings
- **Configuration Panel**: Access advanced settings through the gear icon

### Code Editor Features
1. **Writing Code**: Use the advanced code editor with syntax highlighting
2. **Running Code**: Click "Run Code" or press `Ctrl+Enter` to execute
3. **Theme Toggle**: Switch between light and terminal (dark) themes
4. **Fullscreen Mode**: 
   - Press `F11` or click the fullscreen button for code editor
   - Press `Shift+F11` for output area fullscreen
   - Press `Escape` to exit fullscreen mode
5. **View Output**: Results appear in the right panel with error highlighting

### Built-in Applications
1. **Notepad App**: 
   - Multi-tab text editor with file management
   - Multiple themes (light, dark, blue, purple)
   - File explorer with create, rename, delete operations
   - Auto-save with localStorage persistence
   
2. **Memory Game**: 
   - Interactive card matching game
   - Multiple difficulty levels (Easy: 4x4, Medium: 6x6, Hard: 8x8)
   - Responsive design that works on all devices
   - Track your moves and completion time

3. **Custom Apps**: Save and organize your own Python applications with persistent storage

### Code Examples
- Click the "Examples" button to access a comprehensive library
- Examples include Python basics, advanced concepts, and practical applications
- One-click loading into the editor for immediate testing

### Keyboard Shortcuts
- `Ctrl+Enter`: Execute code
- `F11`: Toggle code editor fullscreen
- `Shift+F11`: Toggle output area fullscreen  
- `Escape`: Exit fullscreen mode
- Standard editor shortcuts (Ctrl+C, Ctrl+V, Ctrl+Z, etc.)

### Session Management
- Sessions automatically expire after 30 minutes of inactivity
- Use "Logout" to manually end your session
- Each user gets an isolated Python environment
- App data persists between sessions

## Security Features

### Code Execution Restrictions
- **No System Access**: Code cannot access system files or directories
- **No Network Access**: No internet or network connectivity from code
- **Memory Limits**: Maximum 50MB RAM per execution
- **Time Limits**: Maximum 10 seconds execution time
- **Safe Modules Only**: Restricted to safe Python built-in functions

### Prevented Actions
- File system access outside sandbox
- Network requests
- System command execution
- Import of dangerous modules (os, subprocess, sys, etc.)
- Long-running or infinite loops
- Memory exhaustion attacks

### Session Security
- Secure session cookies
- Password hashing with SHA-256
- Session timeout protection
- Cross-site scripting (XSS) protection
- Cross-site request forgery (CSRF) protection

## Configuration

### Modifying Security Settings

Edit `codesandbox_backend.py` to adjust security parameters:

```python
# Timeout for code execution (seconds)
TIMEOUT_SECONDS = 10

# Maximum memory usage (MB)
MAX_MEMORY_MB = 50

# Maximum output size (characters)
MAX_OUTPUT_SIZE = 10000

# Session timeout (minutes)
SESSION_TIMEOUT_MINUTES = 30
```

### Adding/Modifying Users

Edit the `USERS` dictionary in `codesandbox_backend.py`:

```python
USERS = {
    'username': 'sha256_hashed_password',
    # Add more users here
}
```

To generate a password hash:
```python
import hashlib
password = "your_password"
hash_value = hashlib.sha256(password.encode()).hexdigest()
print(hash_value)
```

### Port Configuration

To change the port, modify:
- `nginx.conf`: Change the `listen` directive
- `Dockerfile`: Change the `EXPOSE` directive
- Docker run command: Change the port mapping

## Maintenance

### Viewing Logs
```bash
# Docker logs
docker logs python-sandbox

# Nginx logs (if running manually)
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Updating the Application
```bash
# Stop and remove old container
docker stop python-sandbox
docker rm python-sandbox

# Rebuild and restart
docker build -t python-sandbox .
docker run -d -p 7111:7111 --name python-sandbox python-sandbox
```

### Backup User Data
User sessions are stored in memory and will be lost when the container restarts. If you need persistent user management, consider implementing a database backend.

## Troubleshooting

### Common Issues

1. **Port already in use:**
   ```bash
   # Find and kill process using port 7111
   sudo lsof -i :7111
   sudo kill -9 <PID>
   ```

2. **Docker build fails:**
   ```bash
   # Clean up Docker cache
   docker system prune -f
   docker build --no-cache -t python-sandbox .
   ```

3. **Login not working:**
   - Check that you're using the correct username/password
   - Verify that the Flask secret key is properly set
   - Check browser console for JavaScript errors

4. **Code execution timeout:**
   - Increase `TIMEOUT_SECONDS` in the backend configuration
   - Check for infinite loops in your code
   - Verify system resources are available

### Performance Tuning

For better performance with multiple users:
- Increase Docker container memory limits
- Adjust nginx worker processes
- Monitor system resource usage

## Development

### File Structure
```
.
├── codesandbox_backend.py     # Flask backend with authentication & app management
├── codesandbox.html          # Main UI with advanced features
├── login.html               # Login page
├── nginx.conf              # Nginx configuration
├── Dockerfile              # Docker build instructions
├── docker-compose.yml      # Docker Compose configuration
├── start.sh               # Container startup script
├── install.sh             # Installation script
├── test_apps_workflow.py   # Backend API tests
├── test_html.py           # Frontend tests
├── DEPLOYMENT_GUIDE.md     # Detailed deployment instructions
├── README.md              # This file
└── .gitignore            # Git ignore rules
```

### Key Components

#### Backend (`codesandbox_backend.py`)
- Flask application with session management
- Secure code execution with sandboxing
- User authentication and password management
- Persistent app storage using JSON files
- Admin controls and configuration API

#### Frontend (`codesandbox.html`)
- Modern responsive UI with advanced features
- Built-in applications (Notepad, Memory Game)
- Fullscreen support with keyboard shortcuts
- Terminal theme toggle for code editor
- Real-time code execution and output display

#### Security Features
- Sandboxed Python execution environment
- Resource limits (memory, time, output size)
- Session-based authentication with timeouts
- Input validation and XSS protection
- Restricted module imports and system access

### Adding New Features

The modular design makes it easy to extend functionality:

1. **New Applications**: Add entries to the `apps` array in the frontend
2. **API Endpoints**: Extend `codesandbox_backend.py` with new routes
3. **UI Components**: Add new sections to `codesandbox.html`
4. **Themes**: Extend the CSS theme system
5. **Authentication**: Modify the user management system

### Testing

Run the included test suites:
```bash
# Test backend API
python3 test_apps_workflow.py

# Test frontend functionality  
python3 test_html.py
```

## License

This project is provided as-is for educational and development purposes. Use responsibly and ensure proper security measures are in place for production deployments.

## Support

This is a self-contained local application with no external dependencies or support services. All code execution and data storage happens locally on your machine or server.
