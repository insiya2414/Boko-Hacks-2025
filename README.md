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



