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
            if captcha_row is None or captcha_col is None or captcha_row == "" or captcha_col == "":
                flash("Please complete the CAPTCHA challenge by clicking on a cell.", "error")
                return redirect(url_for("register.register"))
            
            # Get the stored data from session
            stored_board = session.get("captcha_board")
            winning_symbol = session.get("winning_symbol")
            
            if not stored_board or not winning_symbol:
                flash("CAPTCHA session expired. Please try again.", "error")
                return redirect(url_for("register.register"))
                
            # Check if this is a valid selection (empty cell)
            if captcha_row < 0 or captcha_row >= 3 or captcha_col < 0 or captcha_col >= 3:
                flash("Invalid CAPTCHA selection. Please try again.", "error")
                return redirect(url_for("register.register"))
                
            if stored_board[captcha_row][captcha_col] != '':
                flash("Selected cell is already occupied. Please try again.", "error")
                return redirect(url_for("register.register"))
            
            # Now check if this is a winning move
            from utils.captcha import check_win
            is_winning_move = check_win(stored_board, captcha_row, captcha_col, winning_symbol)
            
            # Also check against the expected answer
            correct_answer = session.get("captcha_answer")
            direct_match = False
            if correct_answer:
                correct_row, correct_col = correct_answer
                direct_match = (captcha_row == correct_row and captcha_col == correct_col)
            
            if not (is_winning_move or direct_match):
                flash("Incorrect CAPTCHA solution. Please select a cell that would create a winning line.", "error")
                return redirect(url_for("register.register"))
            
            # Clear CAPTCHA from session
            session.pop("captcha_answer", None)
            session.pop("captcha_board", None)
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

