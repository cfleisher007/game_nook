from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

#configure application
app = Flask(__name__)

#configure sessions to use filesystems
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#configure database
db = SQL("sqlite:///games.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    """Show game options"""
    return render_template("index.html")

@app.route("/leaderboard")
@login_required
def leaderboard():
    scores_2048 = db.execute(
        "SELECT username, score FROM scores JOIN users ON scores.user_id = users.id" \
        "WHERE game_name = '2048'ORDER by score DESC"
    )

    scores_mastermind = db.execute(
        "SELECT username, score FROM scores JOIN users ON scores.user_id = user.id" \
        "WHERE game_name = 'Mastermind' ORDER BY score ASC"
    )

    scores_minesweeper = db.execute(
        "SELECT username, score FROM scores JOIN users ON scores.user_id = user.id" \
        "WHERE game_name = 'Minesweeper' ORDER BY score ASC"
    )

    scores_by_game = {
        "2048": scores_2048,
        "Mastermind": scores_mastermind,
        "Minesweeper": scores_minesweeper
    }

    return render_template("leaderboard.html", scores_by_game=scores_by_game)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not password or not confirmation:
            flash("All fields are required!")
            return render_template("register.html")

        if password != confirmation:
            flash("Passwords do not match!")
            return render_template("register.html", username=username)

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) > 0:
            flash("Username already exists")
            return render_template("register.html", username=username)

        hash = generate_password_hash(password)
        db.execute("INSERT INTO users(username, hash) VALUES (?, ?)", username, hash)

        new_user = db.execute("SELECT id FROM users WHERE username = ?", username)
        session["user_id"] = new_user[0]["id"]

        flash("Registration successful!")
        return redirect("/")

    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        if not username:
            flash("Must provide username")
            return render_template("login.html")

        if not request.form.get("password"):
            flash("Must provide password")
            return render_template("login.html", username=username)

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) != 1:
            flash("Username doesn't exist")
            return render_template("login.html")

        if not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("Incorrect password!")
            return render_template("login.html", username=username)

        session["user_id"] = rows[0]["id"]
        flash(f"Welcome back, {username}!")
        return redirect("/")

    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()

    return redirect("/")

@app.route("/change-password", methods=["GET", "POST"])
def change_password():
    if request.method == "POST":
        user_id = session.get("user_id")
        old_password = request.form.get("old-password")
        new_password = request.form.get("new-password")
        confirm_new_password = request.form.get("confirm-new-password")

        if not (old_password and new_password and confirm_new_password):
            flash("All fields are required!")
            return render_template("change-password.html")
        if new_password != confirm_new_password:
            flash("New passwords do not match!")
            return render_template("change-password.html")

        rows = db.execute("SELECT hash FROM users WHERE id = ?", user_id)
        if not check_password_hash(rows[0]["hash"], old_password):
            flash("Please input correct password")
            return render_template("change-password")
        if old_password == new_password:
            flash("New password cannot match old password")
            return render_template("change-password.html")

        hash = generate_password_hash(new_password)
        db.execute("UPDATE users SET hash = ? WHERE id = ?", hash, user_id)

        flash("Password change successful!")
        return redirect("/")

    else:
        return render_template("change-password.html")

