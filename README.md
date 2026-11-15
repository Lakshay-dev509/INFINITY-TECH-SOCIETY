# INFINITY – AI-Powered Interactive Web Platform

Python + NiceGUI starter project.

## Project status
This is a runnable project scaffold. The home page is a basic working shell;
About, Features, Dashboard, Contact, authentication, and database integration
are placeholders. Official project-specific claims and functionality must be
based on the verified hackathon brief and official references.

## Setup

### Windows PowerShell
```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py
```

Open http://localhost:8080 in your browser.

## Structure
- `app/`: configuration and application setup
- `pages/`: page-level UI
- `components/`: reusable UI elements
- `services/`: backend services
- `models/`: data models
- `data/`: sample data and future database location
- `assets/`: images, CSS, and media
- `tests/`: automated tests

## Configuration
Copy `.env.example` to `.env` and adjust values if needed.

## Deployment
Deploy on a Python-compatible host that supports persistent processes and
exposes the configured port. Set `APP_PORT` from the host's environment
when required. Do not commit secrets or the local `.env` file.
