# CS50 Chat

#### Video Demo: <https://youtu.be/vlTkDaA4-Ww>

#### Description:

CS50 Chat is a multi-room real-time chat web application built with Python
(Flask), SQLite, and Socket.IO. Registered users can log in, create chat rooms,
join any room, and exchange messages with other users instantly — messages
appear on everyone's screen the moment they are sent, with no page reload. Every
message is also saved to a database, so when a user opens a room they can see
the full history of what was said before they arrived.

I built this project because a chat application touches every layer of web
development at once — authentication, a relational database, server-side routing,
templating, and, most interestingly, real-time bidirectional communication. The
last part is what makes it more than a standard CRUD app: ordinary web pages
follow a request-response model where the browser asks and the server answers,
but a chat needs the server to *push* new messages to users without being asked.
That is the problem Socket.IO solves, and learning it was the core of this project.

## AI Assistance

For this project, AI tools were used only to assist with CSS styling and visual design.

- layout.html: CSS styling assistance.
- static/css/styles.css: CSS styling assistance.
- README.md: wording and grammar formatting

All application logic, Flask routes, database design, authentication, Socket.IO
functionality, and JavaScript chat functionality were implemented by me.

## How It Works

When a user opens a room, the Flask route `/room/<id>` loads that room's past
messages from the database and renders them into the page. At the same time, the
JavaScript opens a Socket.IO connection back to the server and emits a `join`
event, which adds that user to a Socket.IO "room" — a named group of connections.
When the user types a message and submits the form, the browser does not reload;
instead it emits a `send_message` event over the open connection. The server
saves that message to the database and then broadcasts a `new_message` event to
every connection in that room, including the sender. Each browser receives the
event and appends the new message to the screen. Because the broadcast reaches
everyone at once, all users see the message appear simultaneously. This split —
the database for permanent history and Socket.IO for live delivery — is the
foundation of the whole application.

## Files

**app.py** is the heart of the application. It configures Flask, loads the secret
key, initializes Flask-Session and Flask-SocketIO, and connects to the SQLite
database. It defines the standard HTTP routes — `/register`, `/login`, `/logout`,
the index page listing all rooms, `/rooms` for creating a room, and `/room/<id>`
for viewing a room and its message history. It also defines two Socket.IO event
handlers: `join`, which places a user's connection into a Socket.IO room so
broadcasts only reach the right people, and `send_message`, which validates and
saves an incoming message to the database and then broadcasts it to everyone in
that room with the sender's username and a timestamp.

**helpers.py** contains two helper functions adapted from CS50 Finance: the
`login_required` decorator, which redirects logged-out users to the login page so
that protected routes cannot be reached without an account, and `apology`, which
renders a friendly error page with a message and HTTP status code.

**schema.sql** defines the database structure: a `users` table (username and
hashed password), a `rooms` table, and a `messages` table that links each message
to a room and a user through foreign keys. Using foreign keys keeps the data
consistent — every message is tied to a real user and a real room. **setup.py**
is a small script that reads schema.sql and creates the database file, so the
database can be rebuilt from scratch at any time.

**templates/** holds the Jinja HTML templates. `layout.html` is the base template
with the Bootstrap navbar and shared structure that every other page extends
through Jinja template inheritance, so I only had to write the navigation and
head section once. `index.html` shows the room list and a form to create rooms,
`room.html` displays a single room's messages and the message input box, and
`login.html`, `register.html`, and `apology.html` handle their respective pages.

**static/script/script.js** is the client-side JavaScript that makes the chat
live. It opens a Socket.IO connection, joins the current room, sends messages
when the form is submitted, and renders incoming messages into the page as they
arrive. **static/css/styles.css** adds styling so messages appear as chat bubbles.
A `.env` file (not committed to version control) holds the secret key, and
**requirements.txt** lists the Python dependencies.

## Design Choices

The most important decision was using **Socket.IO rather than polling**. I could
have had the browser repeatedly ask the server "any new messages?" every second,
but that is wasteful and laggy. Socket.IO keeps a single connection open so the
server can push messages instantly — true real-time behavior.

I chose to **save every message to the database before broadcasting it**. This
means messages persist as history and survive page refreshes, rather than only
existing live. The trade-off is a database write on every message, which is
acceptable at this scale.

For security, the `send_message` handler takes the sender's identity from the
**server-side session**, never from data the browser sends, so users cannot
impersonate one another. On the client, messages are inserted using `textContent`
instead of `innerHTML`, which prevents users from injecting HTML or scripts
through their messages (a cross-site scripting attack). Passwords are hashed with
Werkzeug and never stored in plain text, and the Flask secret key is loaded from
a `.env` file rather than hard-coded into the source.

Timestamps are stored and displayed in UTC for consistency, since all users share
one server clock; converting to each user's local timezone added complexity that
was not worth it for this project.

## Challenges and What I Learned

The hardest part was shifting my thinking from the request-response model to
event-driven, real-time code. With normal Flask routes there is a clear page
reload to inspect, but with Socket.IO the page never reloads, so debugging meant
watching the browser console and the server terminal at the same time. Getting
the client and server to agree on event names and data shapes took several
iterations. I also learned why separating the live layer (Socket.IO) from the
storage layer (the database) matters: each does one job well, and together they
give both instant delivery and permanent history.

## Future Improvements

If I continued this project, I would add typing indicators and an online-users
list to make the rooms feel more alive, the ability to delete or leave rooms, and
support for each user's local timezone. For larger scale, I would move from
SQLite to a database like PostgreSQL and add a message store such as Redis so the
app could run across multiple servers.

## How to Run

Install dependencies with `pip install -r requirements.txt`, create a `.env` file
containing a `SECRET_KEY`, run `python setup.py` to build the database, then start
the app with `python app.py` and visit http://127.0.0.1:5000.

