from flask import Blueprint, render_template, jsonify, request, session, redirect, url_for
from extensions import db
from models.user import User
from flask_wtf.csrf import CSRFProtect
from werkzeug.exceptions import BadRequest
import time
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import re

# Blueprint setup
retirement_bp = Blueprint("retirement", __name__, url_prefix="/apps/401k")
csrf = CSRFProtect()

# Rate limiter (prevents abuse)
limiter = Limiter(key_func=get_remote_address)

# Simulated user data storage (should use a database in production)
user_accounts = {
    "alice": {"funds": 10000, "401k_balance": 5000},
    "bob": {"funds": 12000, "401k_balance": 7500},
    "charlie": {"funds": 15000, "401k_balance": 8084},
    "admin": {"funds": 20000, "401k_balance": 12000}
}

# Input validation function
def validate_amount(amount):
    """ Validates amount to prevent injection and abuse """
    if not isinstance(amount, (int, float)):
        return False
    if amount <= 0 or amount > 50000:  # Avoid extremely large transactions
        return False
    return True

@retirement_bp.route("/")
def retirement_dashboard():
    if "user" not in session:
        return redirect(url_for("auth.login"))  # Redirect if not logged in
    session.modified = True  # Prevents session hijacking
    return render_template("401k.html", username=session["user"])

@retirement_bp.route("/balance")
@limiter.limit("10 per minute")  # Limits balance checks to 10 requests per minute
def get_balance():
    if "user" not in session:
        return jsonify({"error": "Not logged in"}), 401

    username = session["user"]
    session.modified = True  # Prevents session hijacking

    if username not in user_accounts:
        user_accounts[username] = {"funds": 10000, "401k_balance": 0}

    return jsonify(user_accounts[username])

@retirement_bp.route("/contribute", methods=["POST"])
@csrf.exempt  # Remove this if CSRF protection is enabled globally
@limiter.limit("5 per minute")  # Prevents spamming contributions
def contribute():
    if "user" not in session:
        return jsonify({"error": "Not logged in"}), 401

    try:
        data = request.get_json()
        if not data or "amount" not in data:
            raise BadRequest("Missing amount in request")
        
        amount = data.get("amount", 0)
        if not validate_amount(amount):
            return jsonify({"message": "Invalid contribution amount!"}), 400

        username = session["user"]
        session.modified = True

        if username not in user_accounts:
            user_accounts[username] = {"funds": 10000, "401k_balance": 0}

        user_data = user_accounts[username]

        if amount > user_data["funds"]:
            return jsonify({"message": "Insufficient personal funds!"}), 400

        # Contribution process
        company_match = amount * 0.5  # Employer matches 50%
        total_contribution = amount + company_match

        user_data["funds"] -= amount
        user_data["401k_balance"] += total_contribution

        return jsonify({
            "message": f"Contributed ${amount}. Employer matched ${company_match}!",
            "funds": user_data["funds"],
            "401k_balance": user_data["401k_balance"]
        })
    
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception:
        return jsonify({"error": "An unexpected error occurred"}), 500

@retirement_bp.route("/reset", methods=["POST"])
@csrf.exempt  # Remove if CSRF protection is enabled globally
@limiter.limit("3 per minute")  # Prevents abuse of resetting accounts
def reset_account():
    if "user" not in session:
        return jsonify({"error": "Not logged in"}), 401

    username = session["user"]
    session.modified = True

    if username not in user_accounts:
        return jsonify({"message": "Account not found!"}), 404

    # Reset funds and balance
    user_accounts[username] = {"funds": 10000, "401k_balance": 0}

    return jsonify({
        "message": "Account reset successfully!",
        "funds": user_accounts[username]["funds"],
        "401k_balance": user_accounts[username]["401k_balance"]
    })
