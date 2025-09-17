# Alumni Platform (HTML5UP Saṅgam)

This project includes the original HTML5UP Saṅgam template plus new pages and a Python Flask backend for a government-verified alumni platform prototype.

## Contents
- Student Signup: `student-signup.html`
- Alumni Signup: `alumni-signup.html`
- Login: `login.html`
- Frontend JS: `assets/js/auth.js`
- Backend: `app.py` (Flask), `requirements.txt`
- Data stores: MongoDB (pymongo) and SQLite (`alumni_platform.db`)

---

## Prerequisites
- Python 3.7+ installed
- MongoDB running locally (or a cloud URI)
- Windows PowerShell/Command Prompt for the commands below

## Setup

1) Open the folder in a terminal
```powershell
cd "C:\Users\nikhi\Desktop\Hackathon Projects\html5up-landed"
```

2) Optional: Create `.env`
```ini
PORT=3000
MONGO_URI=mongodb://127.0.0.1:27017/alumni_platform
```

3) Create virtual environment (recommended)
```powershell
python -m venv venv
venv\Scripts\activate
```

4) Install Python dependencies
```powershell
pip install -r requirements.txt
```

5) Start the server (choose one option):

**Option A: Simple Python Server (No dependencies required)**
```powershell
python app_simple.py
```

**Option B: Flask Server (Requires pip packages)**
```powershell
python app.py
```

The site will be available at `http://localhost:3000/`.

## Pages
- Homepage: `http://localhost:3000/`
- Student signup: `http://localhost:3000/student-signup.html`
- Alumni signup: `http://localhost:3000/alumni-signup.html`
- Login: `http://localhost:3000/login.html`

## API Endpoints (used by `assets/js/auth.js`)
- POST `/api/signup/student`
  - Body JSON: `{ fullName, rollNo, collegeName, department, address, emailOrMobile, password }`
- POST `/api/signup/alumni`
  - Body JSON: `{ fullName, rollNo, collegeName, currentlyWorkingAs, address, emailOrMobile, password }`
- POST `/api/login`
  - Body JSON: `{ emailOrMobile, password }`
- GET `/api/health`
  - Returns server health status

Note: Login succeeds if credentials match a user in either students or alumni table.

## Data Storage
- MongoDB: main user collections (`students` and `alumni` in `alumni_platform` database)
- SQLite: `alumni_platform.db` file with separate `students` and `alumni` tables

## Troubleshooting
- Python not found: ensure Python 3.7+ is installed and in PATH
- MongoDB not running: install/start MongoDB or set `MONGO_URI` to a remote cluster
- Port in use: change `PORT` in `.env` and restart
- Virtual environment issues: recreate with `python -m venv venv --clear`

## Clean Up
- Stop the server (Ctrl+C)
- Deactivate virtual environment: `deactivate`
- Delete `alumni_platform.db` to clear local SQL data (optional)

---

### Credits (HTML5UP Saṅgam)
- Design: HTML5 UP — `https://html5up.net/`
- Icons: Font Awesome
- Scripts: jQuery, Scrollex, Responsive Tools
