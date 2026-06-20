# CS50 Chat

A real-time chat application built with Flask, SQLite, and Socket.IO. Users
register, log in, create chat rooms, and message each other live without
reloading the page.

#### Video Demo: <YOUR VIDEO URL HERE>

## Features

- User registration and login (passwords hashed with Werkzeug)
- Session-based authentication with access control
- Create and browse chat rooms
- Per-room message history
- Real-time messaging via Socket.IO

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

- `app.py` — routes and Socket.IO event handlers
- `helpers.py` — `login_required` decorator and `apology` helper
- `schema.sql` — database schema (users, rooms, messages)
- `setup.py` — creates the database from the schema
- `templates/` — Jinja HTML templates
- `static/` — CSS and JavaScript