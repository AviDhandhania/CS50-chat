from flask import Flask, redirect, render_template, request, session
from cs50 import SQL
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required
import os
from dotenv import load_dotenv

load_dotenv()

# configure application
app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)
db = SQL("sqlite:///chat.db")


@app.route("/")
@login_required
def index():
    rooms = db.execute("SELECT * FROM rooms ORDER BY created_at DESC")
    return render_template("index.html", rooms=rooms, username=session["username"])


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
            return apology("username already exists", 402)

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
    session.clear()

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
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
