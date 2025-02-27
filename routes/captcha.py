from flask import Blueprint, send_file, session, request
from io import BytesIO
import random
import string
from utils.captcha import generate_captcha, generate_TTT_board, draw_TTT_captcha

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
    board, answer, winning_symbol = generate_TTT_board()
    
    # Store the answer in the session
    if answer:
        session["captcha_answer"] = answer
        session["winning_symbol"] = winning_symbol
        # Add instructions to the session
        session["captcha_instructions"] = f"Click on the cell where placing '{winning_symbol}' would win the game"
    else:
        # Handle the case where there are no empty cells left
        session["captcha_answer"] = None
        session["captcha_instructions"] = "CAPTCHA error. Please refresh."
    
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
    
    # Get the correct answer from the session
    correct_answer = session.get("captcha_answer")
    
    if correct_answer is None:
        return False
    
    correct_row, correct_col = correct_answer
    
    # Check if the submitted coordinates match the correct answer
    return row == correct_row and col == correct_col




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