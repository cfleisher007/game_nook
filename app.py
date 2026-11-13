from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
import json
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

@app.route("/save-game-state", methods=["POST"])
#in js, make sure user is logged in
def save_game_state():
    user_id = session.get("user_id")
    data = request.get_json()
    game_name = data.get("game_name")
    game_data = json.dumps(data.get("game_data"))

    db.execute("INSERT OR REPLACE INTO game_saves (user_id, game_name, game_data) VALUES (?, ?, ?)", user_id, game_name, game_data)

    return ("", 204)


@app.route("/2048")
def game_2048():
    user_id = session.get("user_id")

    if user_id:
        game_data = db.execute("SELECT game_data FROM game_saves WHERE user_id = ? AND game_name = '2048'", user_id)
        data = json.loads(game_data[0]["game_data"]) if game_data else None
        return render_template("game-2048.html", game_data=data)

    else:
        return render_template("game-2048.html", game_data=None)


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        new_nickname = request.form.get("nickname")
        user_id = session.get("user_id")
        if not new_nickname:
            flash("Nickname cannot be blank")
            return render_template("profile.html", nickname=session.get("nickname"))
        
        if session.get("nickname") and session.get("nickname") == new_nickname:
            flash("Nickname cannot be the same!")
            return render_template("profile.html")

        db.execute("UPDATE users SET nickname = ? WHERE id = ?", new_nickname, user_id)
        session["nickname"] = new_nickname
        flash("Nickname changed!")
        return render_template("profile.html", nickname=new_nickname)

    else:
        return render_template("profile.html", nickname=session.get("nickname"))


@app.route("/delete-account", methods=["GET", "POST"])
@login_required
def delete_account():
    if request.method == "POST":
        user_id = session.get("user_id")
        password = request.form.get("password")

        rows = db.execute("SELECT hash FROM users WHERE id = ?", user_id)
        if password != check_password_hash(rows[0]["password"]):
            flash("Incorrect password!")
            return render_template("delete-account.html")

        db.execute("DELETE FROM scores WHERE user_id = ?", user_id)
        db.execute("DELETE FROM users WHERE id = ?", user_id)

        session.clear()
        return redirect("/")

    else:
        return render_template("delete-account.html")

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
        nickname = request.form.get("nickname")
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

        if nickname:
            nickname_rows = db.execute("UPDATE users SET nickname = ? WHERE username = ?", nickname, username)
            session["nickname"] = nickname

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
        rows = db.execute("SELECT nickname FROM users WHERE username = ?", username)
        name = ""
        if rows[0]["nickname"]:
            name = rows[0]["nickname"]
        else:
            name = username
        flash(f"Welcome back, {name}!")
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

