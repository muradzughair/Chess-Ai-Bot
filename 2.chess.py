import pygame

pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 800
SQUARE_SIZE = WIDTH // 8
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Board")

# Colors
WHITE = (238, 238, 210)
BLACK = (118, 150, 86)
HIGHLIGHT = (247, 247, 105, 150)  # Yellow for selected piece
GREEN = (0, 255, 0, 150)         # Green for empty squares
RED = (255, 0, 0, 150)           # Red for captures

# Load piece images
pieces = {
    "wp": pygame.image.load("C:/Users/user/Desktop/projects/2.chess/images/w_pawn.png"),
    "wr": pygame.image.load("C:/Users/user/Desktop/projects/2.chess/images/w_rook.png"),
    "wn": pygame.image.load("C:/Users/user/Desktop/projects/2.chess/images/w_horse.png"),
    "wb": pygame.image.load("C:/Users/user/Desktop/projects/2.chess/images/w_bishop.png"),
    "wq": pygame.image.load("C:/Users/user/Desktop/projects/2.chess/images/w_queen.png"),
    "wk": pygame.image.load("C:/Users/user/Desktop/projects/2.chess/images/w_king.png"),
    "bp": pygame.image.load("C:/Users/user/Desktop/projects/2.chess/images/b_pawn.png"),
    "br": pygame.image.load("C:/Users/user/Desktop/projects/2.chess/images/b_rook.png"),
    "bn": pygame.image.load("C:/Users/user/Desktop/projects/2.chess/images/b_horse.png"),
    "bb": pygame.image.load("C:/Users/user/Desktop/projects/2.chess/images/b_bishop.png"),
    "bq": pygame.image.load("C:/Users/user/Desktop/projects/2.chess/images/b_queen.png"),
    "bk": pygame.image.load("C:/Users/user/Desktop/projects/2.chess/images/b_king.png"),
}

# Resize pieces
for key in pieces:
    pieces[key] = pygame.transform.scale(pieces[key], (SQUARE_SIZE, SQUARE_SIZE))

# Initial board setup
chess_board = [
    ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
    ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
    ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"],
]

def draw_board():
    """Draw the chess board"""
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces():
    """Draw chess pieces on the board"""
    for row in range(8):
        for col in range(8):
            piece = chess_board[row][col]
            if piece != "":
                screen.blit(pieces[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))

def draw_highlights(selected_pos):
    """Draw highlights for selected piece and valid moves"""
    if selected_pos:
        row, col = selected_pos
        piece = chess_board[row][col]
        
        # Highlight selected piece
        s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        s.fill(HIGHLIGHT)
        screen.blit(s, (col * SQUARE_SIZE, row * SQUARE_SIZE))
        
        # Highlight valid moves
        for r in range(8):
            for c in range(8):
                if is_valid_move(piece, (row, col), (r, c)):
                    s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                    # Use red for captures, green for empty squares
                    if chess_board[r][c] != "":
                        s.fill(RED)
                    else:
                        s.fill(GREEN)
                    screen.blit(s, (c * SQUARE_SIZE, r * SQUARE_SIZE))

def is_valid_move(piece, start, end):
    """Check if a move is valid for a given piece"""
    start_row, start_col = start
    end_row, end_col = end

    # Check if move is within bounds
    if not (0 <= end_row < 8 and 0 <= end_col < 8):
        return False

    # Get piece color and type
    color = piece[0]
    piece_type = piece[1]
    target = chess_board[end_row][end_col]

    # Check if target is own piece
    if target and target[0] == color:
        return False

    # Pawn movement
    if piece_type == 'p':
        direction = -1 if color == 'w' else 1
        start_rank = 6 if color == 'w' else 1

        # Forward move
        if start_col == end_col:
            if target == "":
                # Single step
                if end_row == start_row + direction:
                    return True
                # Double step from starting position
                if (start_row == start_rank and 
                    end_row == start_row + 2 * direction and 
                    chess_board[start_row + direction][start_col] == ""):
                    return True
            return False
        
        # Capture
        elif abs(start_col - end_col) == 1 and end_row == start_row + direction:
            return target != ""  # Must capture opponent's piece

    # Knight movement (L-shape)
    elif piece_type == 'n':
        return (abs(start_row - end_row), abs(start_col - end_col)) in [(2, 1), (1, 2)]

    # Bishop movement (diagonal)
    elif piece_type == 'b':
        if abs(start_row - end_row) != abs(start_col - end_col):
            return False
        
        row_step = 1 if end_row > start_row else -1
        col_step = 1 if end_col > start_col else -1
        row, col = start_row + row_step, start_col + col_step
        
        while row != end_row and col != end_col:
            if chess_board[row][col] != "":
                return False
            row += row_step
            col += col_step
        return True

    # Rook movement (straight)
    elif piece_type == 'r':
        if start_row == end_row:  # Horizontal
            step = 1 if end_col > start_col else -1
            for col in range(start_col + step, end_col, step):
                if chess_board[start_row][col] != "":
                    return False
        elif start_col == end_col:  # Vertical
            step = 1 if end_row > start_row else -1
            for row in range(start_row + step, end_row, step):
                if chess_board[row][start_col] != "":
                    return False
        else:
            return False
        return True

    # Queen movement (rook + bishop)
    elif piece_type == 'q':
        if start_row == end_row or start_col == end_col:  # Rook-like
            if start_row == end_row:
                step = 1 if end_col > start_col else -1
                for col in range(start_col + step, end_col, step):
                    if chess_board[start_row][col] != "":
                        return False
            else:
                step = 1 if end_row > start_row else -1
                for row in range(start_row + step, end_row, step):
                    if chess_board[row][start_col] != "":
                        return False
        elif abs(start_row - end_row) == abs(start_col - end_col):  # Bishop-like
            row_step = 1 if end_row > start_row else -1
            col_step = 1 if end_col > start_col else -1
            row, col = start_row + row_step, start_col + col_step
            while row != end_row and col != end_col:
                if chess_board[row][col] != "":
                    return False
                row += row_step
                col += col_step
        else:
            return False
        return True

    # King movement (one square any direction)
    elif piece_type == 'k':
        return max(abs(start_row - end_row), abs(start_col - end_col)) == 1

    return False

def is_king_in_check(board, color):
    """Check if the king of the given color is in check"""
    king_pos = None
    enemy_pieces = []

    # Find king and enemy pieces
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece == color + "k":
                king_pos = (r, c)
            elif piece and piece[0] != color:
                enemy_pieces.append((piece, (r, c)))

    if king_pos is None:
        return False  # Shouldn't happen in a valid game

    # Check if any enemy piece can attack the king
    for piece, pos in enemy_pieces:
        if is_valid_move(piece, pos, king_pos):
            return True

    return False

def has_legal_moves(board, turn):
    """Check if the player has any legal moves"""
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece and piece[0] == turn:
                for nr in range(8):
                    for nc in range(8):
                        if is_valid_move(piece, (r, c), (nr, nc)):
                            # Make temporary move
                            temp_board = [row[:] for row in board]
                            temp_board[nr][nc] = piece
                            temp_board[r][c] = ""
                            if not is_king_in_check(temp_board, turn):
                                return True
    return False

# Game state
selected_piece = None
selected_pos = None
turn = "w"  # White moves first
running = True
game_over = False

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            x, y = pygame.mouse.get_pos()
            row, col = y // SQUARE_SIZE, x // SQUARE_SIZE

            if selected_piece is None:  # Selecting a piece
                if chess_board[row][col] and chess_board[row][col][0] == turn:
                    selected_piece = chess_board[row][col]
                    selected_pos = (row, col)
            else:  # Moving a piece
                if is_valid_move(selected_piece, selected_pos, (row, col)):
                    # Make the move
                    chess_board[row][col] = selected_piece
                    chess_board[selected_pos[0]][selected_pos[1]] = ""
                    
                    # Switch turns
                    turn = "b" if turn == "w" else "w"
                    
                    # Check for game over
                    if not has_legal_moves(chess_board, turn):
                        if is_king_in_check(chess_board, turn):
                            print(f"Checkmate! {'Black' if turn == 'w' else 'White'} wins!")
                        else:
                            print("Stalemate! It's a draw.")
                        game_over = True
                
                selected_piece = None
                selected_pos = None

    # Draw everything
    draw_board()
    draw_highlights(selected_pos)  # Draw highlights before pieces
    draw_pieces()
    
    pygame.display.flip()

pygame.quit()