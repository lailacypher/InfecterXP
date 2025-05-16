import os
import platform
import socket
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import hashlib
import threading
import json
import base64
from datetime import datetime, timedelta
import time
import webbrowser
import sys
import getpass
import requests
from cryptography.fernet import Fernet

# Configuration
PORT = 8080
ADMIN_PASSWORD = "A9!Z6%ZXCv"  # Web panel password
SESSION_TIMEOUT = 30  # minutes
ENCRYPTION_KEY = Fernet.generate_key()  # Communication encryption key

# Tunneling settings (optional)
USE_NGROK = True  # Set to False to disable Ngrok
NGROK_AUTH_TOKEN = ""  # Your Ngrok auth token (optional)

# Session storage
active_sessions = {}
fernet = Fernet(ENCRYPTION_KEY)

def setup_tunneling():
    """Configure Ngrok tunneling for external access"""
    if not USE_NGROK:
        return None
    
    try:
        from pyngrok import ngrok
        import pyngrok.conf
        
        # Configure Ngrok
        config = pyngrok.conf.PyngrokConfig(auth_token=NGROK_AUTH_TOKEN) if NGROK_AUTH_TOKEN else None
        public_url = ngrok.connect(PORT, "http", config=config)
        print(f"\nNgrok tunnel created: {public_url}")
        return public_url
    except Exception as e:
        print(f"\nError configuring Ngrok: {e}")
        return None

def get_public_ip():
    """Get server's public IP"""
    try:
        return requests.get('https://api.ipify.org').text
    except:
        return "Not available"

def get_system_info():
    """Get cross-platform system information"""
    system_info = {
        "system": platform.system(),
        "node": platform.node(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "current_user": getpass.getuser(),
        "local_ip": socket.gethostbyname(socket.gethostname()),
        "public_ip": get_public_ip()
    }
    
    # Add Windows-specific info
    if platform.system() == "Windows":
        try:
            import win32api
            system_info["domain"] = win32api.GetDomainName()
        except:
            system_info["domain"] = "Not available"
    
    return system_info

def execute_command_safely(command):
    """Safely execute commands on any system"""
    try:
        if platform.system() == "Windows":
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                text=True,
                encoding='cp850'  # Windows common encoding
            )
        else:
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                text=True,
                executable='/bin/bash' if platform.system() == "Linux" else '/bin/zsh'
            )
        
        stdout, stderr = process.communicate(timeout=60)
        return {
            "success": True,
            "output": stdout,
            "error": stderr,
            "return_code": process.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Command timed out (60s timeout)",
            "return_code": -1
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "return_code": -1
        }

class AdminServer(BaseHTTPRequestHandler):
    def _authenticate(self):
        """Verify token authentication"""
        auth_header = self.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return False
        
        token = auth_header[7:]
        if token in active_sessions:
            if datetime.now() < active_sessions[token]["expires"]:
                active_sessions[token]["expires"] = datetime.now() + timedelta(minutes=SESSION_TIMEOUT)
                return True
            else:
                del active_sessions[token]
        return False
    
    def _send_response(self, data, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        # Encrypt sensitive responses
        if status_code == 200 and 'token' not in data:
            encrypted_data = fernet.encrypt(json.dumps(data).encode())
            self.wfile.write(encrypted_data)
        else:
            self.wfile.write(json.dumps(data, indent=2).encode())
    
    def _decrypt_request(self, post_data):
        """Decrypt received data"""
        try:
            return json.loads(fernet.decrypt(post_data).decode())
        except:
            try:
                return json.loads(post_data.decode())
            except:
                return {}

    def do_GET(self):
        """Handle GET requests for web panel"""
        if self.path == '/':
            # Login page
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Remote Administration Panel</title>
                <style>
                    body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
                    .container {{ background: #f5f5f5; padding: 20px; border-radius: 5px; }}
                    input[type="password"] {{ padding: 8px; width: 200px; }}
                    button {{ padding: 8px 15px; background: #4CAF50; color: white; border: none; cursor: pointer; }}
                    #commandOutput {{ background: #333; color: #0f0; padding: 10px; font-family: monospace; white-space: pre; }}
                    .connection-info {{ background: #e9f7ef; padding: 10px; border-radius: 5px; margin-bottom: 20px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Remote Administration Panel</h1>
                    <div class="connection-info">
                        <h3>Connection Information</h3>
                        <p id="connectionDetails">Loading...</p>
                    </div>
                    
                    <div id="loginSection">
                        <h2>Authentication</h2>
                        <input type="password" id="password" placeholder="Enter password">
                        <button onclick="login()">Login</button>
                        <p id="loginError" style="color:red;"></p>
                    </div>
                    <div id="adminPanel" style="display:none;">
                        <h2>System Information</h2>
                        <pre id="systemInfo"></pre>
                        
                        <h2>Execute Command</h2>
                        <input type="text" id="command" placeholder="Enter command" style="width: 400px;">
                        <button onclick="executeCommand()">Execute</button>
                        <div id="commandOutput"></div>
                    </div>
                </div>
                
                <script>
                    let token = '';
                    
                    // Load connection info
                    fetch('/connection_info')
                        .then(response => response.json())
                        .then(data => {{
                            document.getElementById('connectionDetails').innerHTML = `
                                <strong>Server:</strong> ${data.hostname}<br>
                                <strong>Local IP:</strong> ${data.local_ip}<br>
                                <strong>Public IP:</strong> ${data.public_ip}<br>
                                <strong>External URL:</strong> ${data.public_url || 'Not configured'}
                            `;
                        }});
                    
                    function login() {{
                        const password = document.getElementById('password').value;
                        fetch('/login', {{
                            method: 'POST',
                            headers: {{ 'Content-Type': 'application/json' }},
                            body: JSON.stringify({{ password: password }})
                        }})
                        .then(response => response.json())
                        .then(data => {{
                            if (data.token) {{
                                token = data.token;
                                document.getElementById('loginSection').style.display = 'none';
                                document.getElementById('adminPanel').style.display = 'block';
                                loadSystemInfo();
                            }} else {{
                                document.getElementById('loginError').textContent = 'Incorrect password';
                            }}
                        }});
                    }}
                    
                    function loadSystemInfo() {{
                        fetch('/system_info', {{
                            headers: {{ 'Authorization': 'Bearer ' + token }}
                        }})
                        .then(response => response.json())
                        .then(data => {{
                            document.getElementById('systemInfo').textContent = JSON.stringify(data, null, 2);
                        }});
                    }}
                    
                    function executeCommand() {{
                        const command = document.getElementById('command').value;
                        const outputDiv = document.getElementById('commandOutput');
                        outputDiv.textContent = 'Executing...';
                        
                        fetch('/execute', {{
                            method: 'POST',
                            headers: {{
                                'Content-Type': 'application/json',
                                'Authorization': 'Bearer ' + token
                            }},
                            body: JSON.stringify({{ command: command }})
                        }})
                        .then(response => response.json())
                        .then(data => {{
                            if (data.success) {{
                                outputDiv.textContent = data.output || '(No output)';
                                if (data.error) {{
                                    outputDiv.textContent += '\\n\\nErrors:\\n' + data.error;
                                }}
                            }} else {{
                                outputDiv.textContent = 'Error: ' + data.error;
                            }}
                        }});
                    }}
                </script>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
            return
        
        if self.path == '/system_info':
            if not self._authenticate():
                self._send_response({"error": "Unauthorized"}, 401)
                return
            
            self._send_response(get_system_info())
            return
        
        if self.path == '/connection_info':
            self._send_response({
                "hostname": socket.gethostname(),
                "local_ip": socket.gethostbyname(socket.gethostname()),
                "public_ip": get_public_ip(),
                "public_url": public_url if 'public_url' in globals() else None
            })
            return
        
        self._send_response({"error": "Endpoint not found"}, 404)
    
    def do_POST(self):
        if self.path == '/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = self._decrypt_request(post_data)
                if data.get('password') == ADMIN_PASSWORD:
                    token = base64.b64encode(os.urandom(32)).decode('utf-8')
                    active_sessions[token] = {
                        "expires": datetime.now() + timedelta(minutes=SESSION_TIMEOUT),
                        "ip": self.client_address[0]
                    }
                    self._send_response({"token": token})
                else:
                    self._send_response({"error": "Invalid password"}, 401)
            except:
                self._send_response({"error": "Invalid request"}, 400)
            return
        
        if not self._authenticate():
            self._send_response({"error": "Unauthorized"}, 401)
            return
        
        if self.path == '/execute':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = self._decrypt_request(post_data)
                command = data.get('command')
                
                if not command:
                    self._send_response({"error": "No command specified"}, 400)
                    return
                
                result = execute_command_safely(command)
                self._send_response(result)
            except Exception as e:
                self._send_response({"error": str(e)}, 500)
            return
        
        self._send_response({"error": "Endpoint not found"}, 404)

def cleanup_sessions():
    """Clean up expired sessions periodically"""
    while True:
        now = datetime.now()
        expired = [token for token, sess in active_sessions.items() if now > sess["expires"]]
        for token in expired:
            del active_sessions[token]
        time.sleep(60)

def get_local_ip():
    """Reliably get local IP"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return socket.gethostbyname(socket.gethostname())

if __name__ == '__main__':
    # Configure tunneling (Ngrok)
    public_url = setup_tunneling() if USE_NGROK else None
    
    # Start session cleanup
    threading.Thread(target=cleanup_sessions, daemon=True).start()
    
    # Get local IP address
    local_ip = get_local_ip()
    
    # Start server
    server = HTTPServer(('0.0.0.0', PORT), AdminServer)
    
    print(f"\nRemote administration server started:")
    print(f"Local URL: http://{local_ip}:{PORT}")
    print(f"Public URL: {public_url or 'Not configured'}")
    print(f"Access password: {ADMIN_PASSWORD}")
    print("\nAccess from any network using the public URL above")
    
    # Try to open browser automatically
    try:
        webbrowser.open(f"http://{local_ip}:{PORT}")
    except:
        pass
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        print("\nServer stopped")
