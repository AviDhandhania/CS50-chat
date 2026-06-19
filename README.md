# CS50 Chat

A real-time chat application built with Flask, SQLite, and Socket.IO. Users
register, log in, create chat rooms, and (once Socket.IO is wired up) message
each other live without reloading the page.

#### Video Demo: <TO BE ADDED>

## Features

- User registration and login (passwords hashed with Werkzeug)
- Session-based authentication with access control
- Create and browse chat rooms
- Per-room message history
- Real-time messaging via Socket.IO *(in progress)*

## Tech Stack

- **Backend:** Flask, Flask-SocketIO, Flask-Session
- **Database:** SQLite (via the CS50 SQL library)
- **Frontend:** Jinja templates, Bootstrap 5, vanilla JavaScript

## Setup

1. Install dependencies:

pip install -r requirements.txt



2. Create a `.env` file in the project root with a secret key:

SECRET_KEY=your_random_secret_here



Generate one with: `python -c "import secrets; print(secrets.token_hex(32))"`

3. Create the database:

python setup.py



4. Run the app:

python app.py



Then open http://127.0.0.1:5000 in your browser.

## Project Structure

- `app.py` — routes and (soon) Socket.IO event handlers
- `helpers.py` — `login_required` decorator and `apology` helper
- `schema.sql` — database schema (users, rooms, messages)
- `setup.py` — creates the database from the schema
- `templates/` — Jinja HTML templates
- `static/` — CSS and JavaScript
Notes:

I marked real-time messaging as (in progress) — accurate right now. Drop that tag once step 3 works.
CS50 requires a video demo URL in the README — I added a placeholder line. Don't forget it; it's a submission requirement.
Left the install commands as plain code blocks (not bash-highlighted) to keep it simple.