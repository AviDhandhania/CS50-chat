from flask import Flask, redirect, render_template, request, session
from cs50 import SQL
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required
import os
from dotenv import load_dotenv
from flask_socketio import SocketIO, join_room, emit
from datetime import datetime

load_dotenv()

# configure application
app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)
socketio = SocketIO(app)
db = SQL("sqlite:///chat.db")


@app.route("/")
@login_required
def index():
    rooms = db.execute("SELECT * FROM rooms ORDER BY created_at DESC")
    return render_template("index.html", rooms=rooms)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("must provide username", 403)
        if not password:
            return apology("must provide password", 403)
        if not confirmation:
            return apology("must provide confirmation", 403)

        if password != confirmation:
            return apology("passwords must match", 403)

        if db.execute("SELECT * FROM users WHERE username=?", username):
            return apology("username already exists", 400)

        user_id = db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)",
            username,
            generate_password_hash(password),
        )

        session["user_id"] = user_id
        session["username"] = username
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return apology("must provide username")

        if not password:
            return apology("must provide password")

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("username and/or password incorrect")

        session["user_id"] = rows[0]["id"]
        session["username"] = username

        return redirect("/")

    else:
        session.clear()
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/rooms", methods=["POST"])
@login_required
def create_room():
    name = request.form.get("name", "").strip()

    if not name:
        return apology("must provide room name", 400)

    rooms = db.execute("SELECT * FROM rooms WHERE name = ?", name)
    if len(rooms) != 0:
        return apology("room already exists", 400)

    db.execute(
        "INSERT INTO rooms (name, created_by) VALUES (?,?)", name, session["user_id"]
    )
    return redirect("/")


@app.route("/room/<int:room_id>")
@login_required
def room(room_id):
    rooms = db.execute("SELECT * FROM rooms WHERE id = ?", room_id)

    if len(rooms) != 1:
        return apology("room not found", 400)

    messages = db.execute(
        """SELECT messages.content, messages.timestamp, users.username FROM messages JOIN users ON messages.user_id = users.id WHERE messages.room_id = ? ORDER BY messages.timestamp""",
        room_id,
    )

    return render_template("room.html", room=rooms[0], messages=messages)


@socketio.on("join")
def on_join(data):
    join_room(data["room_id"])


@socketio.on("send_message")
def on_send_message(data):
    room_id = data["room_id"]
    content = data["content"].strip()
    if not content:
        return

    db.execute(
        "INSERT INTO messages (room_id, user_id, content) VALUES (?, ?, ?)",
        room_id,
        session["user_id"],
        content,
    )

    emit(
        "new_message",
        {
            "username": session["username"],
            "content": content,
            "timestamp": datetime.utcnow().strftime("%H:%M"),
        },
        room=room_id,
    )


if __name__ == "__main__":
    socketio.run(app, debug=True)
