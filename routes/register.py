from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from models.user import User
from extensions import db

register_bp = Blueprint("register", __name__)

@register_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Check which type of CAPTCHA is being used
        if "captcha" in request.form:
            # Text-based CAPTCHA (legacy)
            captcha_response = request.form.get("captcha")
            stored_captcha = session.get("captcha_text")
            
            if not stored_captcha or captcha_response.upper() != stored_captcha:
                flash("Invalid CAPTCHA. Please try again.", "error")
                return redirect(url_for("register.register"))
                
            session.pop("captcha_text", None)
            
        elif "captcha_row" in request.form and "captcha_col" in request.form:
            # TicTacToe CAPTCHA
            captcha_row = request.form.get("captcha_row", type=int)
            captcha_col = request.form.get("captcha_col", type=int)
            
            # Check if captcha row/col were provided
            if captcha_row is None or captcha_col is None:
                flash("Please complete the CAPTCHA challenge by clicking on a cell.", "error")
                return redirect(url_for("register.register"))
            
            # Get correct answer from session
            correct_answer = session.get("captcha_answer")
            if correct_answer is None:
                flash("CAPTCHA session expired. Please try again.", "error")
                return redirect(url_for("register.register"))
            
            correct_row, correct_col = correct_answer
            
            # Verify CAPTCHA
            if captcha_row != correct_row or captcha_col != correct_col:
                flash("Incorrect CAPTCHA. Please try again.", "error")
                return redirect(url_for("register.register"))
            
            # Clear CAPTCHA from session
            session.pop("captcha_answer", None)
            session.pop("winning_symbol", None)
            session.pop("captcha_instructions", None)
        
        else:
            # No CAPTCHA response found
            flash("Please complete the CAPTCHA challenge.", "error")
            return redirect(url_for("register.register"))

        # Process user registration
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists. Please choose a different one.", "error")
            return redirect(url_for("register.register"))

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for("login.login"))

    return render_template("register.html")





#old code IN CASE:
# register_bp = Blueprint("register", __name__)

# @register_bp.route("/register", methods=["GET", "POST"])
# def register():
#     if request.method == "POST":
#         username = request.form.get("username")
#         password = request.form.get("password")
#         captcha_response = request.form.get("captcha")
#         stored_captcha = session.get("captcha_text")

#         if not stored_captcha or captcha_response.upper() != stored_captcha:
#             flash("Invalid CAPTCHA. Please try again.", "error")
#             return redirect(url_for("register.register"))

#         session.pop("captcha_text", None)

#         existing_user = User.query.filter_by(username=username).first()
#         if existing_user:
#             flash("Username already exists. Please choose a different one.", "error")
#             return redirect(url_for("register.register"))

#         new_user = User(username=username)
#         new_user.set_password(password)
#         db.session.add(new_user)
#         db.session.commit()

#         flash("Registration successful! You can now log in.", "success")
#         return redirect(url_for("login.login"))

#     return render_template("register.html")

