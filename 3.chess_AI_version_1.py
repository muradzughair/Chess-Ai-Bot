import pygame
import copy
import math
import random

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
CHECK = (255, 100, 100, 200)     # Red tint for king in check

# Piece values for evaluation
PIECE_VALUES = {
    'p': 10, 'n': 30, 'b': 30, 'r': 50, 'q': 90, 'k': 900
}

def draw_board():
    """Draw the chess board"""
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# chess pieces pictures:
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

# Resize the chess pieces
for i in pieces:
    pieces[i] = pygame.transform.scale(pieces[i], (SQUARE_SIZE, SQUARE_SIZE))

# Initial chess board setup
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
                    # Check if move would leave king in check
                    temp_board = copy.deepcopy(chess_board)
                    temp_board[r][c] = piece
                    temp_board[row][col] = ""
                    if not is_king_in_check(temp_board, piece[0]):
                        s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                        # Use red for captures, green for empty squares
                        if chess_board[r][c] != "":
                            s.fill(RED)
                        else:
                            s.fill(GREEN)
                        screen.blit(s, (c * SQUARE_SIZE, r * SQUARE_SIZE))

def highlight_check():
    """Highlight the king if it's in check"""
    for color in ['w', 'b']:
        king_pos = find_king(chess_board, color)
        if king_pos and is_king_in_check(chess_board, color):
            row, col = king_pos
            s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            s.fill(CHECK)
            screen.blit(s, (col * SQUARE_SIZE, row * SQUARE_SIZE))

def find_king(board, color):
    """Find the position of the king of the given color"""
    for row in range(8):
        for col in range(8):
            if board[row][col] == f"{color}k":
                return (row, col)
    return None

def is_valid_move(piece, start, end):
    if not end:  # Check if end position is valid
        return False
        
    start_row, start_col = start
    end_row, end_col = end

    # Check if move is within board bounds
    if not (0 <= end_row < 8 and 0 <= end_col < 8):
        return False

    if piece == "wp":  # White Pawn
        if start_col == end_col:  # Moving straight
            if chess_board[end_row][end_col] != "":  # Can't capture straight
                return False
            if end_row == start_row - 1:  # Normal move
                return True
            elif start_row == 6 and end_row == 4 and chess_board[5][end_col] == "":  # First move, double step
                return True
        elif abs(start_col - end_col) == 1 and end_row == start_row - 1:  # Capturing diagonally
            return chess_board[end_row][end_col].startswith("b")  # Must capture black piece

    elif piece == "bp":  # Black Pawn
        if start_col == end_col:  # Moving straight
            if chess_board[end_row][end_col] != "":  # Can't capture straight
                return False
            if end_row == start_row + 1:  # Normal move
                return True
            elif start_row == 1 and end_row == 3 and chess_board[2][end_col] == "":  # First move, double step
                return True
        elif abs(start_col - end_col) == 1 and end_row == start_row + 1:  # Capturing diagonally
            return chess_board[end_row][end_col].startswith("w")  # Must capture white piece

    elif piece in ["wr", "br"]:  # Rook
        if start_row == end_row:  # Horizontal move
            step = 1 if end_col > start_col else -1
            for col in range(start_col + step, end_col, step):
                if chess_board[start_row][col] != "":
                    return False
        elif start_col == end_col:  # Vertical move
            step = 1 if end_row > start_row else -1
            for row in range(start_row + step, end_row, step):
                if chess_board[row][start_col] != "":
                    return False
        else:
            return False
        # Check if target square is empty or has opponent's piece
        target = chess_board[end_row][end_col]
        return target == "" or target[0] != piece[0]

    elif piece in ["wb", "bb"]:  # Bishop
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
        # Check if target square is empty or has opponent's piece
        target = chess_board[end_row][end_col]
        return target == "" or target[0] != piece[0]

    elif piece in ["wq", "bq"]:  # Queen
        # Rook-like move
        if start_row == end_row or start_col == end_col:
            if start_row == end_row:  # Horizontal move
                step = 1 if end_col > start_col else -1
                for col in range(start_col + step, end_col, step):
                    if chess_board[start_row][col] != "":
                        return False
            else:  # Vertical move
                step = 1 if end_row > start_row else -1
                for row in range(start_row + step, end_row, step):
                    if chess_board[row][start_col] != "":
                        return False
        # Bishop-like move
        elif abs(start_row - end_row) == abs(start_col - end_col):
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
        # Check if target square is empty or has opponent's piece
        target = chess_board[end_row][end_col]
        return target == "" or target[0] != piece[0]

    elif piece in ["wk", "bk"]:  # King
        # Check if target square is adjacent
        if max(abs(start_row - end_row), abs(start_col - end_col)) == 1:
            target = chess_board[end_row][end_col]
            return target == "" or target[0] != piece[0]
        return False

    elif piece in ["wn", "bn"]:  # Knight
        if (abs(start_row - end_row), abs(start_col - end_col)) in [(2, 1), (1, 2)]:
            target = chess_board[end_row][end_col]
            return target == "" or target[0] != piece[0]
        return False

    return False

def is_king_in_check(board, king_color):
    king_pos = None
    enemy_pieces = []

    # Find King position and enemy pieces
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece == king_color + "k":
                king_pos = (r, c)
            elif piece and piece[0] != king_color:
                enemy_pieces.append((piece, (r, c)))

    # If king not found (shouldn't happen in normal game)
    if king_pos is None:
        return False

    # Check if any enemy piece can attack the king
    for piece, pos in enemy_pieces:
        if is_valid_move(piece, pos, king_pos):
            return True

    return False

def has_legal_moves(board, turn):
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece and piece[0] == turn:
                for nr in range(8):
                    for nc in range(8):
                        if is_valid_move(piece, (r, c), (nr, nc)):
                            # Make a temporary move
                            temp_board = copy.deepcopy(board)
                            temp_piece = temp_board[r][c]
                            temp_board[nr][nc] = temp_piece
                            temp_board[r][c] = ""
                            # Check if king would be in check after this move
                            if not is_king_in_check(temp_board, turn):
                                return True
    return False

def evaluate_board(board):
    score = 0
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece:
                # Add piece value
                value = PIECE_VALUES[piece[1]]
                if piece[0] == 'w':
                    score += value
                else:
                    score -= value
                
                # Add positional bonuses
                if piece[1] == 'p':  # Pawns
                    if piece[0] == 'w':
                        score += (7 - row) * 0.5  # Encourage advancing
                    else:
                        score -= row * 0.5
                elif piece[1] == 'k':  # Kings
                    # Encourage king safety in endgame
                    pawn_count = sum(1 for r in range(8) for c in range(8) if board[r][c] and board[r][c][1] == 'p')
                    if pawn_count < 8:  # Endgame
                        if piece[0] == 'w':
                            score += (row - 4) ** 2 * -0.2  # Center is better
                        else:
                            score -= (row - 4) ** 2 * -0.2
    return score

def get_all_valid_moves(board, color):
    moves = []
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece and piece[0] == color:
                for nr in range(8):
                    for nc in range(8):
                        if is_valid_move(piece, (r, c), (nr, nc)):
                            # Make a copy of the board to test the move
                            new_board = copy.deepcopy(board)
                            new_board[nr][nc] = piece
                            new_board[r][c] = ""
                            
                            # Check if this move leaves our king in check
                            if not is_king_in_check(new_board, color):
                                moves.append(((r, c), (nr, nc)))
    return moves

def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0:
        return evaluate_board(board), None
    
    if maximizing_player:
        max_eval = -math.inf
        best_move = None
        for move in get_all_valid_moves(board, 'b'):
            new_board = copy.deepcopy(board)
            start, end = move
            piece = new_board[start[0]][start[1]]
            new_board[end[0]][end[1]] = piece
            new_board[start[0]][start[1]] = ""
            
            evaluation, _ = minimax(new_board, depth-1, alpha, beta, False)
            if evaluation > max_eval:
                max_eval = evaluation
                best_move = move
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = math.inf
        best_move = None
        for move in get_all_valid_moves(board, 'w'):
            new_board = copy.deepcopy(board)
            start, end = move
            piece = new_board[start[0]][start[1]]
            new_board[end[0]][end[1]] = piece
            new_board[start[0]][start[1]] = ""
            
            evaluation, _ = minimax(new_board, depth-1, alpha, beta, True)
            if evaluation < min_eval:
                min_eval = evaluation
                best_move = move
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        return min_eval, best_move

def ai_move():
    _, best_move = minimax(chess_board, 2, -math.inf, math.inf, True)  
    if best_move:
        start, end = best_move
        piece = chess_board[start[0]][start[1]]
        chess_board[end[0]][end[1]] = piece
        chess_board[start[0]][start[1]] = ""
        return True
    return False

selected_piece = None
selected_pos = None
turn = "w"  # White moves first
running = True
game_over = False
checkmate = False
stalemate = False

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            if turn == "w":  # Only allow human to move when it's their turn
                x, y = pygame.mouse.get_pos()
                row, col = y // SQUARE_SIZE, x // SQUARE_SIZE

                if selected_piece is None:  # Selecting a piece
                    if chess_board[row][col] and chess_board[row][col][0] == turn:
                        selected_piece = chess_board[row][col]
                        selected_pos = (row, col)
                else:  # Moving a piece
                    if is_valid_move(selected_piece, selected_pos, (row, col)):
                        # Make temporary move to check if it leaves king in check
                        temp_board = copy.deepcopy(chess_board)
                        temp_board[row][col] = selected_piece
                        temp_board[selected_pos[0]][selected_pos[1]] = ""
                        
                        if not is_king_in_check(temp_board, turn):
                            # Make the actual move
                            chess_board[row][col] = selected_piece
                            chess_board[selected_pos[0]][selected_pos[1]] = ""
                            turn = "b"  # Switch to AI's turn
                            
                            # Check for game end conditions
                            if not has_legal_moves(chess_board, turn):
                                if is_king_in_check(chess_board, turn):
                                    print(f"Checkmate! {'Black' if turn == 'w' else 'White'} wins!")
                                    game_over = True
                                    checkmate = True
                                else:
                                    print("Stalemate! It's a draw.")
                                    game_over = True
                                    stalemate = True
                    
                    selected_piece = None
                    selected_pos = None
    
    # AI's turn (Black)
    if turn == "b" and not game_over:
        pygame.time.delay(500)  # Add small delay so AI doesn't move instantly
        if ai_move():
            turn = "w"  # Switch back to human's turn
            
            # Check for game end conditions
            if not has_legal_moves(chess_board, turn):
                if is_king_in_check(chess_board, turn):
                    print(f"Checkmate! {'Black' if turn == 'w' else 'White'} wins!")
                    game_over = True
                    checkmate = True
                else:
                    print("Stalemate! It's a draw.")
                    game_over = True
                    stalemate = True

    # Draw everything
    draw_board()
    highlight_check()  # Highlight king if in check
    draw_highlights(selected_pos)  # Draw highlights before pieces
    draw_pieces()
    
    # Display game over message
    if game_over:
        font = pygame.font.SysFont("Arial", 48)
        if checkmate:
            text = font.render(f"Checkmate! {'Black' if turn == 'w' else 'White'} wins!", True, (255, 0, 0))
        else:
            text = font.render("Stalemate! It's a draw.", True, (255, 0, 0))
        text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(text, text_rect)
    
    pygame.display.flip()

pygame.quit()