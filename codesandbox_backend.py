from flask import Flask, request, jsonify, session, render_template_string, send_from_directory
import subprocess
import tempfile
import os
import sys
import time
import hashlib
import secrets
import json
import shutil
import signal
import resource
import html
import uuid
import re
from functools import wraps
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Secure random secret key

# Configuration
TIMEOUT_SECONDS = 5
MAX_MEMORY_MB = 50
MAX_OUTPUT_SIZE = 10 * 1024  # 10KB
SESSION_TIMEOUT_MINUTES = 30
SANDBOX_BASE_DIR = '/tmp/sandbox'
HTML_OUTPUT_DIR = '/tmp/html_outputs'  # Directory for HTML outputs

# App configuration
DEMO_MODE = False  # Set to True to enable demo mode restrictions
ALLOW_PASSWORD_CHANGE = True  # Set to False to disable password changes
ALLOW_USER_REGISTRATION = False  # Set to True to allow new user registration

# Create HTML output directory
os.makedirs(HTML_OUTPUT_DIR, exist_ok=True)

# Store user sessions and sandboxes
user_sessions = {}
user_sandboxes = {}

# Apps storage for each user
user_apps = {}  # {user_id: {app_id: {name, code, created_at, is_html}}}
APPS_STORAGE_FILE = '/tmp/user_apps.json'

def load_user_apps():
    """Load user apps from file"""
    global user_apps
    try:
        if os.path.exists(APPS_STORAGE_FILE):
            with open(APPS_STORAGE_FILE, 'r') as f:
                user_apps = json.load(f)
    except Exception as e:
        print(f"Error loading user apps: {e}")
        user_apps = {}

def save_user_apps():
    """Save user apps to file"""
    try:
        with open(APPS_STORAGE_FILE, 'w') as f:
            json.dump(user_apps, f, indent=2)
    except Exception as e:
        print(f"Error saving user apps: {e}")

# Load existing apps on startup
load_user_apps()

# Simple user store (in production, use a proper database)
USERS = {
    'admin': '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918',  # 'admin'
    'user1': '0a041b9462caa4a31bac3567e0b6e6fd9100787db2ab433d96f6d178cabfce90',  # 'password'
    'demo': '2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b'   # 'demo123'
}

def require_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session['user_id'] not in user_sessions:
            return jsonify({'error': 'Authentication required'}), 401
        
        # Check session timeout
        user_session = user_sessions.get(session['user_id'])
        if user_session and datetime.now() > user_session['expires']:
            del user_sessions[session['user_id']]
            session.clear()
            return jsonify({'error': 'Session expired'}), 401
            
        # Refresh session
        user_sessions[session['user_id']]['expires'] = datetime.now() + timedelta(minutes=SESSION_TIMEOUT_MINUTES)
        
        return f(*args, **kwargs)
    return decorated_function

def create_user_sandbox(user_id):
    """Create an isolated sandbox directory for a user"""
    sandbox_dir = f"/tmp/sandbox_{user_id}_{int(time.time())}"
    os.makedirs(sandbox_dir, exist_ok=True)
    
    # Set restrictive permissions
    os.chmod(sandbox_dir, 0o700)
    
    user_sandboxes[user_id] = {
        'dir': sandbox_dir,
        'created': time.time()
    }
    
    return sandbox_dir

def cleanup_user_sandbox(user_id):
    """Clean up user's sandbox directory"""
    if user_id in user_sandboxes:
        sandbox_dir = user_sandboxes[user_id]['dir']
        if os.path.exists(sandbox_dir):
            shutil.rmtree(sandbox_dir, ignore_errors=True)
        del user_sandboxes[user_id]

def set_resource_limits():
    """Set resource limits for the subprocess"""
    # Limit memory usage
    resource.setrlimit(resource.RLIMIT_AS, (MAX_MEMORY_MB * 1024 * 1024, MAX_MEMORY_MB * 1024 * 1024))
    # Limit CPU time
    resource.setrlimit(resource.RLIMIT_CPU, (TIMEOUT_SECONDS, TIMEOUT_SECONDS))
    # Prevent file creation beyond temp directory
    resource.setrlimit(resource.RLIMIT_FSIZE, (1024 * 1024, 1024 * 1024))  # 1MB max file size

def secure_exec(code, sandbox_dir):
    """Execute code in a secure sandboxed environment"""
    # Properly indent user code for the try block
    indented_code = '\n'.join('    ' + line if line.strip() else line for line in code.split('\n'))
    
    # Create a restricted Python code template
    restricted_code = f"""
import sys
import signal
import math
import random
import json
import re
import datetime
import time

# Restrict builtins to safe functions only
safe_builtins = {{
    'print': print, 'len': len, 'str': str, 'int': int, 'float': float,
    'list': list, 'dict': dict, 'tuple': tuple, 'set': set,
    'range': range, 'enumerate': enumerate, 'zip': zip,
    'min': min, 'max': max, 'sum': sum, 'abs': abs,
    'round': round, 'sorted': sorted, 'reversed': reversed,
    'bool': bool, 'type': type, 'isinstance': isinstance,
    'hasattr': hasattr, 'getattr': getattr, 'setattr': setattr,
    'chr': chr, 'ord': ord, 'hex': hex, 'bin': bin,
    'Exception': Exception, 'ValueError': ValueError,
    'TypeError': TypeError, 'IndexError': IndexError,
    'KeyError': KeyError, 'AttributeError': AttributeError,
    'StopIteration': StopIteration, 'RuntimeError': RuntimeError,
    'NotImplementedError': NotImplementedError,
    # Safe modules
    'math': math, 'random': random, 'json': json, 're': re,
    'datetime': datetime, 'time': time
}}

# Restrict access to dangerous functions
__builtins__ = safe_builtins

# Remove dangerous modules from sys.modules
dangerous_modules = ['os', 'subprocess', 'importlib', '__builtin__', 'builtins', 'sys']
for module in list(sys.modules.keys()):
    if any(dangerous in module for dangerous in ['os', 'subprocess', 'socket', 'urllib', 'http']):
        if module in sys.modules:
            del sys.modules[module]

# Set alarm for timeout
signal.alarm({TIMEOUT_SECONDS})

try:
{indented_code}
except Exception as e:
    print(f"Error: {{type(e).__name__}}: {{e}}")
"""

    # Write code to temp file in sandbox
    temp_file = os.path.join(sandbox_dir, f"code_{int(time.time())}.py")
    
    try:
        with open(temp_file, 'w') as f:
            f.write(restricted_code)
        
        # Execute with restrictions
        result = subprocess.run(
            [sys.executable, temp_file],
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
            cwd=sandbox_dir,
            preexec_fn=set_resource_limits,
            env={'PATH': '/usr/bin:/bin', 'PYTHONPATH': ''}  # Minimal environment
        )
        
        output = result.stdout
        if result.stderr:
            output += "\nErrors:\n" + result.stderr
            
        # Limit output size
        if len(output) > MAX_OUTPUT_SIZE:
            output = output[:MAX_OUTPUT_SIZE] + f"\n... (output truncated, max {MAX_OUTPUT_SIZE} characters)"
            
        return output
        
    except subprocess.TimeoutExpired:
        return f"Error: Code execution timed out after {TIMEOUT_SECONDS} seconds"
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        # Clean up temp file
        if os.path.exists(temp_file):
            os.unlink(temp_file)

def detect_html_output(code, output):
    """Detect if the code is generating HTML/CSS content"""
    # Check if code contains HTML generation patterns
    html_patterns = [
        r'<html[^>]*>',
        r'<body[^>]*>',
        r'<div[^>]*>',
        r'<h[1-6][^>]*>',
        r'<p[^>]*>',
        r'<style[^>]*>',
        r'<!DOCTYPE',
        r'print\s*\(\s*["\']<.*?["\']',
        r'f["\']<.*?["\']',
        r'""".*?<.*?"""',
        r"'''.*?<.*?'''"
    ]
    
    code_lower = code.lower()
    for pattern in html_patterns:
        if re.search(pattern, code_lower, re.DOTALL):
            return True
    
    # Check if output contains HTML
    if re.search(r'<[^>]+>', output):
        return True
        
    return False

def extract_html_from_output(output):
    """Extract HTML content from Python output"""
    # Look for HTML content in the output
    html_match = re.search(r'(<!DOCTYPE.*|<html.*|<div.*|<style.*)', output, re.DOTALL | re.IGNORECASE)
    if html_match:
        # Try to extract complete HTML document
        html_content = output[html_match.start():]
        
        # Clean up any Python print artifacts
        html_content = re.sub(r'^[^<]*', '', html_content)
        html_content = html_content.strip()
        
        return html_content
    
    # If no HTML tags found but output exists, wrap in basic HTML
    if output.strip():
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Sandbox Output</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .output {{ background-color: #f5f5f5; padding: 15px; border-radius: 5px; }}
    </style>
</head>
<body>
    <div class="output">
        <pre>{html.escape(output)}</pre>
    </div>
</body>
</html>"""
    
    return None

def save_html_output(user_id, html_content):
    """Save HTML content and return URL"""
    # Generate unique filename
    file_id = str(uuid.uuid4())
    filename = f"{user_id}_{file_id}.html"
    filepath = os.path.join(HTML_OUTPUT_DIR, filename)
    
    # Write HTML content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return f"/view/{filename}"

@app.route('/')
def index():
    if 'user_id' in session and session['user_id'] in user_sessions:
        return render_template_string(open('/root/codesandbox.html').read())
    else:
        return render_template_string(open('/root/login.html').read())

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', '')
    password = request.json.get('password', '')
    
    # Hash the password
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    if username in USERS and USERS[username] == password_hash:
        session['user_id'] = username
        user_sessions[username] = {
            'login_time': datetime.now(),
            'expires': datetime.now() + timedelta(minutes=SESSION_TIMEOUT_MINUTES),
            'sandbox_created': False
        }
        return jsonify({'success': True, 'message': 'Login successful'})
    else:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

@app.route('/logout', methods=['POST'])
@require_login
def logout():
    user_id = session['user_id']
    cleanup_user_sandbox(user_id)
    if user_id in user_sessions:
        del user_sessions[user_id]
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully'})

@app.route('/run', methods=['POST'])
@require_login
def run_code():
    user_id = session['user_id']
    code = request.json.get('code', '')
    
    if not code.strip():
        return jsonify({'output': 'No code provided'})
    
    # Create sandbox if not exists
    if user_id not in user_sandboxes:
        create_user_sandbox(user_id)
        user_sessions[user_id]['sandbox_created'] = True
    
    sandbox_dir = user_sandboxes[user_id]['dir']
    
    try:
        output = secure_exec(code, sandbox_dir)
        
        # Detect and handle HTML output
        if detect_html_output(code, output):
            html_content = extract_html_from_output(output)
            if html_content:
                # Save HTML content and return URL
                html_url = save_html_output(user_id, html_content)
                return jsonify({'output': 'HTML content generated', 'html_url': html_url})
        
        return jsonify({'output': output})
    except Exception as e:
        return jsonify({'output': f'System error: {str(e)}'})

@app.route('/reset', methods=['POST'])
@require_login
def reset_environment():
    user_id = session['user_id']
    cleanup_user_sandbox(user_id)
    create_user_sandbox(user_id)
    return jsonify({'success': True, 'message': 'Environment reset successfully'})

@app.route('/status')
@require_login
def status():
    user_id = session['user_id']
    user_session = user_sessions.get(user_id, {})
    sandbox_info = user_sandboxes.get(user_id, {})
    
    return jsonify({
        'user': user_id,
        'session_expires': user_session.get('expires', '').isoformat() if user_session.get('expires') else '',
        'sandbox_created': bool(sandbox_info),
        'sandbox_age': int(time.time() - sandbox_info.get('created', 0)) if sandbox_info else 0
    })

@app.route('/view/<filename>')
@require_login
def view_html(filename):
    """Serve HTML output files"""
    # Security check: ensure filename belongs to current user
    user_id = session['user_id']
    if not filename.startswith(f"{user_id}_"):
        return "Access denied", 403
    
    try:
        return send_from_directory(HTML_OUTPUT_DIR, filename)
    except FileNotFoundError:
        return "File not found", 404

@app.route('/apps', methods=['GET'])
@require_login
def get_apps():
    """Get list of user's saved apps"""
    user_id = session['user_id']
    apps = user_apps.get(user_id, {})
    
    # Convert to list format for frontend
    apps_list = []
    for app_id, app_data in apps.items():
        apps_list.append({
            'id': app_id,
            'name': app_data['name'],
            'description': app_data.get('description', ''),
            'created_at': app_data['created_at'],
            'is_html': app_data.get('is_html', False)
        })
    
    # Sort by creation date (newest first)
    apps_list.sort(key=lambda x: x['created_at'], reverse=True)
    return jsonify({'apps': apps_list})

@app.route('/apps', methods=['POST'])
@require_login
def save_app():
    """Save a new app"""
    user_id = session['user_id']
    data = request.json
    
    name = data.get('name', '').strip()
    code = data.get('code', '').strip()
    description = data.get('description', '').strip()
    
    if not name or not code:
        return jsonify({'success': False, 'message': 'Name and code are required'}), 400
    
    # Generate unique app ID
    app_id = str(uuid.uuid4())
    
    # Detect if it's an HTML app
    is_html = detect_html_output(code, '')
    
    # Initialize user apps if not exists
    if user_id not in user_apps:
        user_apps[user_id] = {}
    
    # Save the app
    user_apps[user_id][app_id] = {
        'name': name,
        'code': code,
        'description': description,
        'created_at': datetime.now().isoformat(),
        'is_html': is_html
    }
    
    # Save user apps to file
    save_user_apps()
    
    return jsonify({'success': True, 'message': f'App "{name}" saved successfully', 'app_id': app_id})

@app.route('/apps/<app_id>', methods=['GET'])
@require_login
def get_app(app_id):
    """Get a specific app"""
    user_id = session['user_id']
    
    if user_id not in user_apps or app_id not in user_apps[user_id]:
        return jsonify({'success': False, 'message': 'App not found'}), 404
    
    app_data = user_apps[user_id][app_id]
    return jsonify({
        'success': True,
        'app': {
            'id': app_id,
            'name': app_data['name'],
            'code': app_data['code'],
            'description': app_data.get('description', ''),
            'created_at': app_data['created_at'],
            'is_html': app_data.get('is_html', False)
        }
    })

@app.route('/apps/<app_id>', methods=['DELETE'])
@require_login
def delete_app(app_id):
    """Delete an app"""
    user_id = session['user_id']
    
    if user_id not in user_apps or app_id not in user_apps[user_id]:
        return jsonify({'success': False, 'message': 'App not found'}), 404
    
    app_name = user_apps[user_id][app_id]['name']
    del user_apps[user_id][app_id]
    
    # Save user apps to file
    save_user_apps()
    
    return jsonify({'success': True, 'message': f'App "{app_name}" deleted successfully'})

@app.route('/apps/<app_id>', methods=['PUT'])
@require_login
def update_app(app_id):
    """Update an app"""
    user_id = session['user_id']
    
    if user_id not in user_apps or app_id not in user_apps[user_id]:
        return jsonify({'success': False, 'message': 'App not found'}), 404
    
    data = request.json
    name = data.get('name', '').strip()
    code = data.get('code', '').strip()
    
    if not name or not code:
        return jsonify({'success': False, 'message': 'Name and code are required'}), 400
    
    # Update the app
    user_apps[user_id][app_id]['name'] = name
    user_apps[user_id][app_id]['code'] = code
    user_apps[user_id][app_id]['is_html'] = detect_html_output(code, '')
    
    # Save user apps to file
    save_user_apps()
    
    return jsonify({'success': True, 'message': f'App "{name}" updated successfully'})

@app.route('/change-password', methods=['POST'])
@require_login
def change_password():
    """Change user password"""
    if not ALLOW_PASSWORD_CHANGE:
        return jsonify({'success': False, 'message': 'Password changes are disabled'}), 403
    
    user_id = session['user_id']
    data = request.json
    
    current_password = data.get('current_password', '')
    new_password = data.get('new_password', '')
    confirm_password = data.get('confirm_password', '')
    
    if not current_password or not new_password or not confirm_password:
        return jsonify({'success': False, 'message': 'All fields are required'}), 400
    
    if new_password != confirm_password:
        return jsonify({'success': False, 'message': 'New passwords do not match'}), 400
    
    if len(new_password) < 6:
        return jsonify({'success': False, 'message': 'Password must be at least 6 characters long'}), 400
    
    # Verify current password
    current_password_hash = hashlib.sha256(current_password.encode()).hexdigest()
    if user_id not in USERS or USERS[user_id] != current_password_hash:
        return jsonify({'success': False, 'message': 'Current password is incorrect'}), 401
    
    # Update password
    new_password_hash = hashlib.sha256(new_password.encode()).hexdigest()
    USERS[user_id] = new_password_hash
    
    return jsonify({'success': True, 'message': 'Password changed successfully'})

@app.route('/app-settings', methods=['GET'])
@require_login
def get_app_settings():
    """Get app configuration settings"""
    user_id = session['user_id']
    is_admin = user_id == 'admin'  # Only admin can see/change global settings
    
    settings = {
        'demo_mode': DEMO_MODE,
        'allow_password_change': ALLOW_PASSWORD_CHANGE,
        'allow_user_registration': ALLOW_USER_REGISTRATION,
        'is_admin': is_admin,
        'current_user': user_id
    }
    
    return jsonify({'success': True, 'settings': settings})

@app.route('/app-settings', methods=['POST'])
@require_login
def update_app_settings():
    """Update app configuration settings (admin only)"""
    user_id = session['user_id']
    
    if user_id != 'admin':
        return jsonify({'success': False, 'message': 'Admin access required'}), 403
    
    data = request.json
    global DEMO_MODE, ALLOW_PASSWORD_CHANGE, ALLOW_USER_REGISTRATION
    
    if 'demo_mode' in data:
        DEMO_MODE = bool(data['demo_mode'])
    
    if 'allow_password_change' in data:
        ALLOW_PASSWORD_CHANGE = bool(data['allow_password_change'])
    
    if 'allow_user_registration' in data:
        ALLOW_USER_REGISTRATION = bool(data['allow_user_registration'])
    
    return jsonify({'success': True, 'message': 'Settings updated successfully'})

# Cleanup on exit
import atexit

def cleanup_all_sandboxes():
    for user_id in list(user_sandboxes.keys()):
        cleanup_user_sandbox(user_id)

atexit.register(cleanup_all_sandboxes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
