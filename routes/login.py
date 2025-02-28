from flask import Blueprint, render_template, request, flash, redirect, session, url_for
from models.user import User
from extensions import db
import time

login_bp = Blueprint("login", __name__)

# Set maximum login attempts and lockout duration (in seconds)
MAX_ATTEMPTS = 5
LOCKOUT_TIME = 180  # 2 minutes

@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if "failed_attempts" not in session:
        session["failed_attempts"] = 0
    if "lockout_time" in session:
        remaining_time = session["lockout_time"] - time.time()
        if remaining_time > 0:
            flash(f"Too many failed attempts. Try again in {int(remaining_time)} seconds.", "error")
            return render_template("login.html")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session["user"] = user.username
            session.pop("failed_attempts", None)  # Reset failed attempts on success
            session.pop("lockout_time", None)  # Clear lockout if it existed
            flash("Login successful!", "success")
            return redirect(url_for("hub.hub"))
        else:
            session["failed_attempts"] += 1
            if session["failed_attempts"] >= MAX_ATTEMPTS:
                session["lockout_time"] = time.time() + LOCKOUT_TIME
                flash(f"Too many failed attempts. Please try again later.", "error")
            else:
                flash(f"Invalid username or password. Attempts left: {MAX_ATTEMPTS - session['failed_attempts']}", "error")

    return render_template("login.html")

@login_bp.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("failed_attempts", None)  # Reset on logout
    session.pop("lockout_time", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("login.login"))

