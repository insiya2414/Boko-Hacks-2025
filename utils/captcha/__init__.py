from flask import Blueprint, session, send_file, request
from PIL import Image, ImageDraw, ImageFont
import random
import io

captcha_bp = Blueprint("captcha", __name__)

#creating a tic tac toe board
GRID_SIZE = 3
CELL_SIZE = 60
BOARD_SIZE = GRID_SIZE * CELL_SIZE

def generate_TTT_board():

    board = [[ "" for _ in range(GRID_SIZE) for _ in range(GRID_SIZE)]]
    moves = [[ (r,c) for r in range(GRID_SIZE) for c in range(GRID_SIZE)]]

    for _ in range(random.randint(3,5)):
        r, c = random.choice(moves)
        moves.random((r, c))
        board[r][c] = random.choice(["X", "O"])
    
    winning_symbol = "X" if random.choice([True, False]) else "O"

    if moves:  # Check if there are still empty cells
        row, col = random.choice(moves)
        board[row][col] = winning_symbol
        
        # Store the answer in the session
        session["captcha_answer"] = (row, col)
        session["winning_symbol"] = winning_symbol
    else:
        # Handle the case where there are no empty cells left
        session["captcha_answer"] = None
        session["winning_symbol"] = winning_symbol
    

    return board

#drawing the tictactoe captcha board
def draw_TTT_captcha(board):
    image = Image.new("RGB", (BOARD_SIZE, BOARD_SIZE), "white")
    draw = ImageDraw.Draw(image)

    for i in range(1, GRID_SIZE):
        draw.line([(i * CELL_SIZE, 0), (i * CELL_SIZE, BOARD_SIZE)], fill="black", width=3)
        draw.line([(0, i * CELL_SIZE), (BOARD_SIZE, i * CELL_SIZE)], fill="black", width=3)

    # Draw Xs and Os
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if board[r][c]:
                x = c * CELL_SIZE + CELL_SIZE // 4
                y = r * CELL_SIZE + CELL_SIZE // 4
                draw.text((x, y), board[r][c], fill="black")

    return image

@captcha_bp.route("/captcha")

def get_captcha():

    board = generate_TTT_board

    image = draw_TTT_captcha

    img_io = io.BytesIO()
    image.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')

@captcha_bp.route("/verify-captcha", methods=["POST"])

def verify_captcha():

    row = request.form.get("captcha_row", type=int)
    col = request.form.get("captcha_col", type=int)

    #this should get the correct answer
    correct_answer = session.get("captcha_answer")

    if correct_answer is None:
        return False
    
    correct_row, correct_col = correct_answer

    return row == correct_row and col == correct_col






# def generate_captcha(text: str = None, width: int = 200, height: int = 80) -> Image:

#     image = Image.new('RGB', (width, height), (255, 255, 255))
#     draw = ImageDraw.Draw(image)
    
#     draw.rectangle([0, 0, width-1, height-1], outline=(200, 200, 200))
    
#     font = ImageFont.load_default()
    
#     text_bbox = draw.textbbox((0, 0), text, font=font)
#     text_width = text_bbox[2] - text_bbox[0]
#     text_height = text_bbox[3] - text_bbox[1]
    
#     x = (width - text_width) // 2 - text_bbox[0]  
#     y = (height - text_height) // 2 - text_bbox[1]  
    
#     draw.text((x, y), text, font=font, fill=(0, 0, 0))
    
#     return image