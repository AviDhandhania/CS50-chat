from flask import Flask, redirect, render_template, request, session
from cs50 import SQL
from flask_session import Session

#configure application
app = Flask(__name__)

app.config["SECRET_KEY"] = "your_secret_key_here"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

db = SQL("sqlite:///chat.db")


@app.route('/')
def index():
    if not session.get("user_id"):
        return redirect("/login")
    
    rooms = db.execute("SELECT * FROM rooms ORDER BY name ASC")
    return render_template("index.html", rooms = rooms)


@app.route("/login", methods = ["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return apology
    return "<h1>Login<h1>"

@app.route("/register", methods = ["GET", "POST"])
def register():
    return "<h1>register<h1>"

if __name__ == '__main__':
    app.run(debug=True)
