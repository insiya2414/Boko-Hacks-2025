import re
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from models.user import User
from extensions import db

register_bp = Blueprint("register", __name__)

def is_valid_password(password):
    """Checks if the password meets all security criteria."""
    
    # At least 8 characters long
    if len(password) < 8:
        return "Password must be at least 8 characters long."

    # At least one uppercase letter
    if not any(char.isupper() for char in password):
        return "Password must contain at least one uppercase letter."

    # At least one lowercase letter
    if not any(char.islower() for char in password):
        return "Password must contain at least one lowercase letter."

    # At least one digit
    if not any(char.isdigit() for char in password):
        return "Password must contain at least one digit."

    return None

@register_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        captcha_response = request.form.get("captcha")
        stored_captcha = session.get("captcha_text")

        if not stored_captcha or captcha_response.upper() != stored_captcha:
            flash("Invalid CAPTCHA. Please try again.", "error")
            return redirect(url_for("register.register"))

        session.pop("captcha_text", None)

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists. Please choose a different one.", "error")
            return redirect(url_for("register.register"))

        password_error = is_valid_password(password)
        if password_error:
            flash(password_error, "error")
            return redirect(url_for("register.register"))
        
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for("login.login"))

    return render_template("register.html")

