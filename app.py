import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, apology

app = Flask(__name__)
# session expire on user exit / storing to server side
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
# connect to database
db = sqlite3.connect('data.db', check_same_thread=False)

# homepage displays calender
@app.route("/")
@login_required
def index():
    return render_template("calendar.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST) "user just submitted form
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username, username being the value from /login file
        rows = db.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))

        # Ensure username exists and password is correct
        user = rows.fetchone()

        if user is None or not check_password_hash(user[2], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = user[0]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    session.clear()

    if request.method == "POST":

        if not request.form.get("username"):
            return apology("provide a username", 403)

        elif not request.form.get("password"):
            return apology("provide a password", 403)

        elif request.form.get("vpassword") != request.form.get("password"):
            return apology("Password does not match!", 403)

        rows = db.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))

        # Ensure username does not exist
        user = rows.fetchone()

        if user is None:
            result = db.execute("INSERT INTO users (username, password) VALUES(?, ?)", (request.form.get("username") ,generate_password_hash(request.form.get("password"))))

            # Get the ID of the newly inserted user
            user_id = result.lastrowid

            db.commit()

            # Remember which user has logged in
            session["user_id"] = user_id

            # Redirect user to home page
            return redirect("/")

        else:
            return apology("Username already exists", 403)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route('/history')
def history():

        # Use a parameterized query to avoid SQL injection
        workouts = db.execute("SELECT * FROM workouts ORDER BY strftime('%Y-%m-%dT%H:%M:%S', start_date) DESC")

        return render_template("history.html", workouts=workouts)


@app.route('/calendar')
def calendar():

    return render_template("calendar.html")


