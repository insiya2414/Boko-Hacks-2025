# BokoHacks 2025
Our Group's Application Security Challenge Platform for Texas State University's 2025 BokoHacks


## Table of Contents  
- [Team Members](#team-members)  
- [Overview](#overview)  
- [Requirements](#requirements)  
- [Setup Instructions](#setup-instructions)  


## Team Members
- Alyana Imperial
- Insiya Raja
- Vaidic Soni


## Overview 
This project was a deliberately vulnerable web application created by Texas State University's BokoHacks committee, designed to help students learn about common web security vulnerabilities through hands-on practice. Our redesigned version remedies several challenges focusing on SQL injection, XSS (Cross-Site Scripting), access control flaws, and authentication bypass techniques. Our focus was to make sure the website was secure for regular users to traverse, adding both industry-standard and unique ways to strengthen authentication and accesses.

## Security Issues Resolved
- Randomized tic-tac-toe CAPTCHA is presented before registering an account, allowing a more unique and engaging way to prevent bots and recognize human interaction.
- Removed backend vulnerabilities in the Notes Application that would garner an attack (SQLInjection/XSS Attack) and improving access control, ensuring that users can only view their own notes. 
- Requires passwords to have at least 8 characters, including uppercase, lowercase, special characters, and digits
- Secure Password Storage: Hashes passwords before storing them using secure algorithms like bcrypt or Argon2. This ensures that even if the database is compromised, passwords remain unreadable.
- Protection Against SQL Injection: Uses SQLAlchemy ORM, which parameterizes queries and prevents direct execution of user input. This eliminates risks of malicious SQL code being injected to manipulate the database
- Environment Variable for API Key: Loads API keys securely from .env files instead of hardcoding them in the codebase. This prevents accidental exposure in version control systems like Git
- URL Prefix for Blueprint: Groups API routes under /apps/news, keeping endpoint organization structured and secure.
- API Key Existence Check: Ensures an API key is present before making external API requests.
- Timeout for API Requests: Sets a 10-second timeout on external API requests to prevent indefinite waiting, mitigate Denial of Service (DoS) attacks and unresponsive API endpoints.
- Safe Data Extraction – Uses .get() instead of direct dictionary access to avoid KeyError crashes
- Login Attempts Restricted: Does not allow brute force logins to avoid a non-authorized user to login
- Prevents Arbitrary Account Resets: Ensures that only the logged-in user can reset their own account. This prevents attackers from resetting other users’ accounts maliciously. 
- Rate Limiting: Uses Flask-Limiter to restrict repeated API calls, such as login attempts or balance checks. This helps prevent abuse, brute-force attacks, and API overuse.



## Requirements
- Python 3.8 or higher → [Download Python](https://www.python.org/downloads/)
- Pip (Python package installer)
- SQLite → [Download SQLite](https://www.sqlite.org/download.html) (Optional if you want binaries otherwise; dependencies should install automatically)
- Modern web browser (Chrome/Firefox recommended)
- Text editor or IDE VS Code recommended → [VS Code Setup](https://code.visualstudio.com/docs/python/environments)

### How To Run ###

## Setup Instructions
1. Clone the repository:
```bash
git clone https://github.com/insiya2414/Boko-Hacks-2025.git
cd boko-hacks-2025
```
2. Git Setup (For Beginners)

1) Install Git
- Download and install Git from [git-scm.com](https://git-scm.com/downloads)
- After installation, verify Git is installed by running command prompt:
```
git --version
```
2) Configure Git (Required for First-Time Users)
Run the following commands to set your username and email (needed for commits):
```
git config --global user.name "Your Name"
git config --global user.email "youremail@example.com"
```
To check your Git settings:
```
git config --list
```
3) Using Git with HTTPS (Easiest for Beginners)
- Clone repositories using HTTPS (no extra setup required):
```
git clone https://github.com/Nick4453/Boko-Hacks-2025.git
```
- If prompted for credentials frequently, enable credential manager:
```
git config --global credential.helper cache
```
4) Setting Up Git in VS Code
- Open VS Code and install the Git Extension (built-in for most versions).
- Open terminal in VS Code and check Git is recognized:
```
git --version
```
- Set VS Code as your default Git editor:
```
git config --global core.editor "code --wait"
```

5) Create and activate a virtual environment (recommended): (You can also do this through VS Code)
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Mac/Linux
python3 -m venv .venv
source .venv/bin/activate
```
VS Code Setup ---> https://code.visualstudio.com/docs/python/environments

4. Install dependencies:
```bash
pip install -r requirements.txt
```
5. Install dependencies
```bash
pip install flask-wtf
pip install flask-limiter
pip install python-dotenv
```
6. Initialize the database: (You may not need to do this step; if it doesn't work, check that your env path is correct)
```bash
python -c "from app import app, setup_database; app.app_context().push(); setup_database()"
```

8. Start the application: 
```bash
python app.py
```

9. Open http://localhost:5000 in your browser and access the given URL (To stop runnning: ^C)



