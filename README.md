# BruteForce Flask Panel

A web-based brute force control panel built with Flask, including login protection, live updates, iframe previews, and result display.

## Features
- Admin login (username: `admin`, password: `kader11000`)
- Start/Stop/Resume brute force attack
- Display terminal-style output
- View successful login guesses in a table
- Live iframe view of the target site
- Editable request panel

## Installation

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
pip install -r requirements.txt
python app.py
Then open http://127.0.0.1:5000
in your browser 
