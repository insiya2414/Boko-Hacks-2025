from PIL import Image, ImageDraw, ImageFont
import random
import string
import io

def generate_captcha(text=None, width=200, height=80):
    """Generate a text-based CAPTCHA image"""
    if text is None:
        text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    
    image = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    
    draw.rectangle([0, 0, width-1, height-1], outline=(200, 200, 200))
    
    font = ImageFont.load_default()
    
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (width - text_width) // 2 - text_bbox[0]  
    y = (height - text_height) // 2 - text_bbox[1]  
    
    draw.text((x, y), text, font=font, fill=(0, 0, 0))
    
    return image

# TicTacToe CAPTCHA settings
GRID_SIZE = 3
CELL_SIZE = 60
BOARD_SIZE = GRID_SIZE * CELL_SIZE

def generate_TTT_board():
    """Generate a TicTacToe board with random X and O positions"""
    # Initialize empty board
    board = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    
    # Create a list of all possible moves
    moves = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE)]
    
    # Place 3-5 random X's and O's
    for _ in range(random.randint(3, 5)):
        if not moves:  # Check if moves list is empty
            break
        r, c = random.choice(moves)
        moves.remove((r, c))
        board[r][c] = random.choice(["X", "O"])
    
    # Choose a winning symbol
    winning_symbol = "X" if random.choice([True, False]) else "O"
    
    # Place the winning symbol in a random empty cell
    if moves:  # Check if there are still empty cells
        row, col = random.choice(moves)
        board[row][col] = winning_symbol
        return board, (row, col), winning_symbol
    else:
        # Handle the case where there are no empty cells left
        return board, None, winning_symbol

def draw_TTT_captcha(board):
    """Draw the TicTacToe board as an image"""
    # Create a new white image
    image = Image.new("RGB", (BOARD_SIZE, BOARD_SIZE), "white")
    draw = ImageDraw.Draw(image)
    
    # Draw the grid lines
    for i in range(1, GRID_SIZE):
        draw.line([(i * CELL_SIZE, 0), (i * CELL_SIZE, BOARD_SIZE)], fill="black", width=2)
        draw.line([(0, i * CELL_SIZE), (BOARD_SIZE, i * CELL_SIZE)], fill="black", width=2)
    
    # Use default font since custom fonts might not be available
    font = ImageFont.load_default()
    
    # Draw X's and O's
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if board[r][c]:
                x = c * CELL_SIZE + CELL_SIZE // 4
                y = r * CELL_SIZE + CELL_SIZE // 4
                draw.text((x, y), board[r][c], fill="black", font=font)
    
    return image
#old code for transparency:
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