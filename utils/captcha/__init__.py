from PIL import Image, ImageDraw, ImageFont
import random
import string
import io

# Keep the old text-based captcha function
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

def check_win(board, row, col, symbol):
    """Check if placing symbol at (row, col) would create a win"""
    # Make a copy of the board with the symbol placed
    test_board = [row[:] for row in board]
    test_board[row][col] = symbol
    
    # Check row
    if all(test_board[row][c] == symbol for c in range(GRID_SIZE)):
        return True
        
    # Check column
    if all(test_board[r][col] == symbol for r in range(GRID_SIZE)):
        return True
        
    # Check diagonals if applicable
    if row == col:  # Main diagonal
        if all(test_board[i][i] == symbol for i in range(GRID_SIZE)):
            return True
            
    if row + col == GRID_SIZE - 1:  # Anti-diagonal
        if all(test_board[i][GRID_SIZE-1-i] == symbol for i in range(GRID_SIZE)):
            return True
            
    return False

def generate_TTT_board():
    """Generate a TicTacToe board with a potential winning move"""
    # Initialize empty board - FIXED: Proper 2D list initialization
    board = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    
    # Choose a winning symbol
    winning_symbol = "X" if random.choice([True, False]) else "O"
    
    # CHANGED: Now intentionally creates a position with a potential winning move
    win_type = random.choice(["row", "column", "diagonal"])
    
    if win_type == "row":
        # Pick a random row
        row = random.randint(0, GRID_SIZE - 1)
        # Place the winning symbol in 2 random positions in that row
        cols = random.sample(range(GRID_SIZE), 2)
        for col in cols:
            board[row][col] = winning_symbol
        # Save the empty position as the winning move
        empty_col = [c for c in range(GRID_SIZE) if c not in cols][0]
        winning_cell = (row, empty_col)
        
    elif win_type == "column":
        # Pick a random column
        col = random.randint(0, GRID_SIZE - 1)
        # Place the winning symbol in 2 random positions in that column
        rows = random.sample(range(GRID_SIZE), 2)
        for row in rows:
            board[row][col] = winning_symbol
        # Save the empty position as the winning move
        empty_row = [r for r in range(GRID_SIZE) if r not in rows][0]
        winning_cell = (empty_row, col)
        
    else:  # diagonal
        if random.choice([True, False]):
            # Main diagonal
            positions = random.sample(range(GRID_SIZE), 2)
            for pos in positions:
                board[pos][pos] = winning_symbol
            # Save the empty position as the winning move
            empty_pos = [p for p in range(GRID_SIZE) if p not in positions][0]
            winning_cell = (empty_pos, empty_pos)
        else:
            # Anti-diagonal
            positions = random.sample(range(GRID_SIZE), 2)
            for pos in positions:
                board[pos][GRID_SIZE - 1 - pos] = winning_symbol
            # Save the empty position as the winning move
            empty_pos = [p for p in range(GRID_SIZE) if p not in positions][0]
            winning_cell = (empty_pos, GRID_SIZE - 1 - empty_pos)
    
    # Add some random X's and O's in other positions
    other_symbol = "O" if winning_symbol == "X" else "X"
    empty_cells = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) 
                  if board[r][c] == '' and (r, c) != winning_cell]
    
    # Place 2-4 of the other symbol
    for _ in range(min(random.randint(2, 4), len(empty_cells))):
        if not empty_cells:
            break
        r, c = random.choice(empty_cells)
        empty_cells.remove((r, c))
        board[r][c] = other_symbol
    
    # Verify the winning cell actually creates a win
    win_row, win_col = winning_cell
    if not check_win(board, win_row, win_col, winning_symbol):
        # If somehow our logic failed, regenerate the board
        return generate_TTT_board()
        
    return board, winning_cell, winning_symbol

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