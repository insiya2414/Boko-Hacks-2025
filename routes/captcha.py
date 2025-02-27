from flask import Blueprint, send_file, session, request, jsonify
from io import BytesIO
import random
import string
from utils.captcha import generate_captcha, generate_TTT_board, draw_TTT_captcha, check_win

captcha_bp = Blueprint("captcha", __name__)

@captcha_bp.route("/captcha/generate", methods=["GET"])
def get_text_captcha():
    """Generate a text-based CAPTCHA image (legacy route)"""
    
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    
    session['captcha_text'] = captcha_text
    
    image = generate_captcha(captcha_text)
    img_io = BytesIO()
    image.save(img_io, 'PNG')
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/png')

@captcha_bp.route("/captcha", methods=["GET"])
def get_captcha():
    """Generate a TicTacToe CAPTCHA image"""
    
    # Generate a new TicTacToe board
    board, winning_cell, winning_symbol = generate_TTT_board()
    
    # Store the solution in the session
    session["captcha_answer"] = winning_cell
    session["captcha_board"] = [row[:] for row in board]  # Store a copy of the board
    session["winning_symbol"] = winning_symbol
    
    # Add instructions to the session
    session["captcha_instructions"] = f"Click on the cell where placing '{winning_symbol}' would create a winning line"
    
    # Draw the board as an image
    image = draw_TTT_captcha(board)
    
    # Save the image to a bytes buffer
    img_io = BytesIO()
    image.save(img_io, 'PNG')
    img_io.seek(0)
    
    # Return the image as a response
    return send_file(img_io, mimetype='image/png')

@captcha_bp.route("/verify-captcha", methods=["POST"])
def verify_captcha():
    """Verify the CAPTCHA response"""
    
    # Get the submitted coordinates
    row = request.form.get("captcha_row", type=int)
    col = request.form.get("captcha_col", type=int)
    
    # Get the correct answer and board from the session
    correct_answer = session.get("captcha_answer")
    stored_board = session.get("captcha_board")
    winning_symbol = session.get("winning_symbol")
    
    if not correct_answer or not stored_board or not winning_symbol:
        return jsonify({"success": False, "message": "CAPTCHA session expired"})
    
    # Check if the selected cell is empty
    if row < 0 or row >= 3 or col < 0 or col >= 3:
        return jsonify({"success": False, "message": "Invalid cell selection"})
        
    if stored_board[row][col] != '':
        return jsonify({"success": False, "message": "Cell already occupied"})
    
    # Check if this move creates a win
    is_winning_move = check_win(stored_board, row, col, winning_symbol)
    
    # Direct match with the expected winning cell
    correct_row, correct_col = correct_answer
    direct_match = (row == correct_row and col == correct_col)
    
    if is_winning_move or direct_match:
        return jsonify({"success": True, "message": "Correct!"})
    else:
        return jsonify({"success": False, "message": "Incorrect move"})

# Add an API endpoint to check if a move is valid without submitting the whole form
@captcha_bp.route("/check-move", methods=["POST"])
def check_move():
    """Check if a move is valid for the CAPTCHA"""
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No data provided"})
        
    row = data.get("row")
    col = data.get("col")
    
    if row is None or col is None:
        return jsonify({"success": False, "message": "Invalid coordinates"})
    
    # Get the stored board and winning symbol
    stored_board = session.get("captcha_board")
    winning_symbol = session.get("winning_symbol")
    
    if not stored_board or not winning_symbol:
        return jsonify({"success": False, "message": "CAPTCHA session expired"})
    
    # Check if the cell is already occupied
    if row < 0 or row >= 3 or col < 0 or col >= 3:
        return jsonify({"success": False, "message": "Invalid cell selection"})
        
    if stored_board[row][col] != '':
        return jsonify({"success": False, "message": "Cell already occupied"})
    
    # Check if this is a winning move
    is_winning_move = check_win(stored_board, row, col, winning_symbol)
    
    if is_winning_move:
        correct_answer = session.get("captcha_answer")
        if correct_answer:
            correct_row, correct_col = correct_answer
            if row == correct_row and col == correct_col:
                # Exact match with our expected solution
                message = "Perfect! That's the winning move."
            else:
                # Found another winning move (edge case but possible)
                message = "Nice! That's a winning move."
        else:
            message = "That's a winning move!"
            
        # Save the user's selection
        session["user_captcha_selection"] = (row, col)
        return jsonify({"success": True, "message": message})
    else:
        return jsonify({"success": False, "message": "That's not a winning move. Try again!"})

#old code:
# from flask import Blueprint, send_file, session
# from io import BytesIO
# import random
# import string
# from utils.captcha import generate_captcha

# captcha_bp = Blueprint("captcha", __name__)

# @captcha_bp.route("/captcha/generate", methods=["GET"])
# def get_captcha():
#     """Generate a new CAPTCHA image - intentionally simplified"""
    
#     captcha_text = "12345"
    
#     session['captcha_text'] = captcha_text
    
#     image = generate_captcha(captcha_text)
#     img_io = BytesIO()
#     image.save(img_io, 'PNG')
#     img_io.seek(0)
    
#     return send_file(img_io, mimetype='image/png')