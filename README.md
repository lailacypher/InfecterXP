# InfectXP - Remote Administration & Security Audit Tool

By: Laila19

## This Python-based Remote Administration & Security Audit Tool allows authorized users to securely manage and audit systems over a network. It provides:

### Web-based access (local or remote via Ngrok tunneling)

Command execution on the host machine

System information gathering (OS, users, network details)

Encrypted authentication with token-based sessions

### Key Features

✔ Cross-Platform – Works on Windows, Linux, and macOS
✔ Remote Access – Supports Ngrok tunneling for external connections
✔ Secure Authentication – Password-protected (A9!Z6%ZXCv by default) with encrypted sessions
✔ Command Execution – Run any CMD/Bash/Zsh commands and view output
✔ System Audit – Retrieve hostname, IP, users, OS details, and more
✔ Responsive Web UI – Easy-to-use browser-based interface

### Use Cases

IT Administrators – Remotely troubleshoot systems

Security Auditors – Check system vulnerabilities

Network Managers – Execute commands across devices

### Security Considerations

🔒 Always change the default password

🔐 Use in trusted networks only

⚠ Disable Ngrok tunneling (USE_NGROK = False) if not needed

### How It Works

Starts a local HTTP server (0.0.0.0:8080)

Optionally creates an Ngrok tunnel for external access

Authenticates users via password (SHA-256 hashed)

Allows command execution with real-time output

Auto-cleans expired sessions

### Setup & Usage
```bash
pip install pyngrok requests cryptography
```

### Dependecies
Dependencies List:
```
- cryptography
- pyngrok (optional, for tunneling)
- requests
- flask (for web interface)
- pywin32 (Windows only)
- colorama (for colored menu)
```
Installation Commands:
Base dependencies (required for all platforms):

```bash
pip install cryptography requests flask colorama
```
Optional dependencies (for tunneling):

```bash
pip install pyngrok
```
Windows-specific dependencies:

```bash
pip install pywin32
```
Complete Installation Command (all-in-one):
For most users, this command will install everything needed:

```bash
pip install cryptography requests flask colorama pyngrok pywin32
```
Notes:
The pywin32 package is only needed if running on Windows

The pyngrok package is optional and only required if you want to use the tunneling feature

If you encounter any permission issues, try adding --user to the pip command:

````bash
pip install --user cryptography requests flask colorama pyngrok pywin32
The tool will work without the optional dependencies, but some features like Ngrok tunneling won't be available unless you install pyngrok.
```

### Run the server
```
python remote_admin.py
````
Access Methods
Local Network: http://[local-ip]:8080
External (Ngrok): https://[random-subdomain].ngrok.io

Notes
🔧 Customizable – Modify ADMIN_PASSWORD, PORT, and ALLOWED_COMMANDS as needed.
