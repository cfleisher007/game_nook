from flask import Flask, flask, redirect, render_template, request, session
from flask_session import Session

#configure application
app = Flask(__name__)

#configure sessions to use filesystems
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

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




