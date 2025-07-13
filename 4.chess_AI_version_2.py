import pygame
import copy
import math
import random
import time
from collections import defaultdict


pygame.init()


WIDTH, HEIGHT = 800, 800
SQUARE_SIZE = WIDTH // 8
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess AI")


WHITE = (238, 238, 210)
BLACK = (118, 150, 86)
HIGHLIGHT = (247, 247, 105, 150)
RED = (255, 0, 0, 150)
GREEN = (0, 255, 0, 150)

# Piece values 
PIECE_VALUES = {
    'p': 100, 'n': 320, 'b': 330, 'r': 500, 'q': 900, 'k': 20000
}

# Piece-square tables (positional bonuses)
PIECE_SQUARE_TABLES = {
    'p': [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [5, 5, 10, 25, 25, 10, 5, 5],
        [0, 0, 0, 20, 20, 0, 0, 0],
        [5, -5, -10, 0, 0, -10, -5, 5],
        [5, 10, 10, -20, -20, 10, 10, 5],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ],
    'n': [
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20, 0, 0, 0, 0, -20, -40],
        [-30, 0, 10, 15, 15, 10, 0, -30],
        [-30, 5, 15, 20, 20, 15, 5, -30],
        [-30, 0, 15, 20, 20, 15, 0, -30],
        [-30, 5, 10, 15, 15, 10, 5, -30],
        [-40, -20, 0, 5, 5, 0, -20, -40],
        [-50, -40, -30, -30, -30, -30, -40, -50]
    ],
    'b': [
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-10, 0, 5, 10, 10, 5, 0, -10],
        [-10, 5, 5, 10, 10, 5, 5, -10],
        [-10, 0, 10, 10, 10, 10, 0, -10],
        [-10, 10, 10, 10, 10, 10, 10, -10],
        [-10, 5, 0, 0, 0, 0, 5, -10],
        [-20, -10, -10, -10, -10, -10, -10, -20]
    ],
    'r': [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [5, 10, 10, 10, 10, 10, 10, 5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [-5, 0, 0, 0, 0, 0, 0, -5],
        [0, 0, 0, 5, 5, 0, 0, 0]
    ],
    'q': [
        [-20, -10, -10, -5, -5, -10, -10, -20],
        [-10, 0, 0, 0, 0, 0, 0, -10],
        [-10, 0, 5, 5, 5, 5, 0, -10],
        [-5, 0, 5, 5, 5, 5, 0, -5],
        [0, 0, 5, 5, 5, 5, 0, -5],
        [-10, 5, 5, 5, 5, 5, 0, -10],
        [-10, 0, 5, 0, 0, 0, 0, -10],
        [-20, -10, -10, -5, -5, -10, -10, -20]
    ],
    'k': [
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-30, -40, -40, -50, -50, -40, -40, -30],
        [-20, -30, -30, -40, -40, -30, -30, -20],
        [-10, -20, -20, -20, -20, -20, -20, -10],
        [20, 20, 0, 0, 0, 0, 20, 20],
        [20, 30, 10, 0, 0, 10, 30, 20]
    ],
    'k_endgame': [
        [-50, -40, -30, -20, -20, -30, -40, -50],
        [-30, -20, -10, 0, 0, -10, -20, -30],
        [-30, -10, 20, 30, 30, 20, -10, -30],
        [-30, -10, 30, 40, 40, 30, -10, -30],
        [-30, -10, 30, 40, 40, 30, -10, -30],
        [-30, -10, 20, 30, 30, 20, -10, -30],
        [-30, -30, 0, 0, 0, 0, -30, -30],
        [-50, -30, -30, -30, -30, -30, -30, -50]
    ]
}

# Load chess piece images (replace with your own paths)
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

#peices positions
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

def is_valid_move(piece, start, end):
    """Check if a move is valid for a given piece"""
    if not end:
        return False
        
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

def has_legal_moves(board, color):
    """Check if the player has any legal moves"""
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece and piece[0] == color:
                for nr in range(8):
                    for nc in range(8):
                        if is_valid_move(piece, (r, c), (nr, nc)):
                            # Make temporary move
                            temp_board = copy.deepcopy(board)
                            temp_board[nr][nc] = piece
                            temp_board[r][c] = ""
                            if not is_king_in_check(temp_board, color):
                                return True
    return False

def is_checkmate(board, color):
    """Check if the current player is in checkmate"""
    return is_king_in_check(board, color) and not has_legal_moves(board, color)

def is_stalemate(board, color):
    """Check if the current player is in stalemate"""
    return not is_king_in_check(board, color) and not has_legal_moves(board, color)

def get_game_state(board, turn):
    """Determine the current game state"""
    if is_checkmate(board, turn):
        return "checkmate", "black" if turn == "w" else "white"
    elif is_stalemate(board, turn):
        return "stalemate", None
    return "ongoing", None

class AIPlayer:
    def __init__(self):
        self.transposition_table = {}
        self.killer_moves = defaultdict(list)
        self.history_table = defaultdict(int)
        self.nodes_searched = 0
        self.search_depth = 3  # Default depth
    
    def evaluate_board(self, board):
        """Evaluate the board position"""
        score = 0
        material = 0
        pawn_count = 0
        
        # Count material and pawns for game phase
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece:
                    if piece[1] == 'p':
                        pawn_count += 1
                    material += PIECE_VALUES[piece[1]]
        
        # Determine game phase (0 = opening/midgame, 1 = endgame)
        game_phase = 0 if pawn_count > 8 else 1
        
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece:
                    value = PIECE_VALUES[piece[1]]
                    color = 1 if piece[0] == 'w' else -1
                    
                    # Material score
                    score += value * color
                    
                    # Positional score
                    if piece[1] == 'k' and game_phase == 1:
                        table = PIECE_SQUARE_TABLES['k_endgame']
                    else:
                        table = PIECE_SQUARE_TABLES.get(piece[1], [[0]*8 for _ in range(8)])
                    
                    # Flip table for black pieces
                    actual_row = row if piece[0] == 'w' else 7 - row
                    score += table[actual_row][col] * color * 0.1
        
        return score
    
    def order_moves(self, board, moves, color):
        """Order moves to improve alpha-beta pruning"""
        scored_moves = []
        for move in moves:
            start, end = move
            piece = board[start[0]][start[1]]
            capture = board[end[0]][end[1]]
            
            score = 0
            # Prioritize captures
            if capture:
                score = 10 * PIECE_VALUES[capture[1]] - PIECE_VALUES[piece[1]]
            # Prioritize checks
            temp_board = copy.deepcopy(board)
            temp_board[end[0]][end[1]] = piece
            temp_board[start[0]][start[1]] = ""
            if is_king_in_check(temp_board, 'b' if color == 'w' else 'w'):
                score += 50
            # Killer moves
            if move in self.killer_moves.get((start[0], start[1]), []):
                score += 20
            # History heuristic
            score += self.history_table.get((start, end), 0) // 32
            
            scored_moves.append((score, move))
        
        # Sort moves by score (highest first)
        scored_moves.sort(reverse=True, key=lambda x: x[0])
        return [move for (score, move) in scored_moves]
    
    def quiescence_search(self, board, alpha, beta, color):
        """Search until position is quiet (no captures available)"""
        stand_pat = self.evaluate_board(board)
        
        if stand_pat >= beta:
            return beta
        if alpha < stand_pat:
            alpha = stand_pat
        
        # Get all capture moves
        capture_moves = []
        for r in range(8):
            for c in range(8):
                piece = board[r][c]
                if piece and piece[0] == color:
                    for nr in range(8):
                        for nc in range(8):
                            target = board[nr][nc]
                            if target and target[0] != color:  # Capture move
                                if is_valid_move(piece, (r, c), (nr, nc)):
                                    capture_moves.append(((r, c), (nr, nc)))
        
        # Order capture moves
        capture_moves = self.order_moves(board, capture_moves, color)
        
        for move in capture_moves:
            start, end = move
            piece = board[start[0]][start[1]]
            captured = board[end[0]][end[1]]
            
            # Make the move
            new_board = copy.deepcopy(board)
            new_board[end[0]][end[1]] = piece
            new_board[start[0]][start[1]] = ""
            
            # Recursive call
            score = -self.quiescence_search(new_board, -beta, -alpha, 'b' if color == 'w' else 'w')
            
            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
        
        return alpha
    
    def minimax(self, board, depth, alpha, beta, color, is_root=False):
        """Minimax with alpha-beta pruning"""
        self.nodes_searched += 1
        
        # Check for draw by insufficient material
        if self.is_insufficient_material(board):
            return 0, None
        
        # Check transposition table
        board_key = self.get_board_key(board, color)
        if board_key in self.transposition_table:
            entry = self.transposition_table[board_key]
            if entry['depth'] >= depth:
                return entry['score'], entry['best_move']
        
        # Leaf node - evaluate or quiescence search
        if depth == 0:
            score = self.quiescence_search(board, alpha, beta, color)
            return score, None
        
        moves = self.get_all_valid_moves(board, color)
        if not moves:
            if is_king_in_check(board, color):
                return -math.inf if color == 'w' else math.inf, None  # Checkmate
            else:
                return 0, None  # Stalemate
        
        # Order moves
        ordered_moves = self.order_moves(board, moves, color)
        
        best_move = None
        best_score = -math.inf if color == 'w' else math.inf
        
        for move in ordered_moves:
            start, end = move
            piece = board[start[0]][start[1]]
            
            # Make the move
            new_board = copy.deepcopy(board)
            new_board[end[0]][end[1]] = piece
            new_board[start[0]][start[1]] = ""
            
            # Recursive minimax call
            if color == 'w':
                score, _ = self.minimax(new_board, depth-1, alpha, beta, 'b')
                if score > best_score:
                    best_score = score
                    best_move = move
                    alpha = max(alpha, best_score)
            else:
                score, _ = self.minimax(new_board, depth-1, alpha, beta, 'w')
                if score < best_score:
                    best_score = score
                    best_move = move
                    beta = min(beta, best_score)
            
            # Alpha-beta pruning
            if beta <= alpha:
                # Store killer move
                if len(self.killer_moves[(start[0], start[1])]) < 2:
                    self.killer_moves[(start[0], start[1])].append(move)
                # Update history heuristic
                self.history_table[(start, end)] += depth * depth
                break
        
        # Store in transposition table
        self.transposition_table[board_key] = {
            'score': best_score,
            'depth': depth,
            'best_move': best_move
        }
        
        return best_score, best_move
    
    def get_all_valid_moves(self, board, color):
        """Get all legal moves for the given color"""
        moves = []
        for r in range(8):
            for c in range(8):
                piece = board[r][c]
                if piece and piece[0] == color:
                    for nr in range(8):
                        for nc in range(8):
                            if is_valid_move(piece, (r, c), (nr, nc)):
                                # Make temporary move
                                temp_board = copy.deepcopy(board)
                                temp_board[nr][nc] = piece
                                temp_board[r][c] = ""
                                if not is_king_in_check(temp_board, color):
                                    moves.append(((r, c), (nr, nc)))
        return moves
    
    def get_board_key(self, board, color):
        """Create a hash key for the board position"""
        key = []
        for row in board:
            for piece in row:
                key.append(piece if piece else '-')
        return ''.join(key) + color
    
    def is_insufficient_material(self, board):
        """Check for draw by insufficient material"""
        pieces = defaultdict(int)
        for row in board:
            for piece in row:
                if piece:
                    pieces[piece[1]] += 1
        
        # King vs king
        if len(pieces) == 2 and 'k' in pieces:
            return True
        
        # King + bishop/knight vs king
        if len(pieces) == 3 and 'k' in pieces:
            if ('b' in pieces and pieces['b'] == 1) or ('n' in pieces and pieces['n'] == 1):
                return True
        
        return False
    
    def make_move(self, board):
        """Make the best move found by minimax"""
        start_time = time.time()
        self.nodes_searched = 0
        
        # Increase depth in endgame
        pawn_count = sum(1 for row in board for piece in row if piece and piece[1] == 'p')
        depth = self.search_depth + (1 if pawn_count < 8 else 0)
        
        score, best_move = self.minimax(board, depth, -math.inf, math.inf, 'b', True)
        
        if best_move:
            start, end = best_move
            piece = board[start[0]][start[1]]
            board[end[0]][end[1]] = piece
            board[start[0]][start[1]] = ""
            
            # Print stats
            elapsed = time.time() - start_time
            print(f"AI moved {piece} from {start} to {end}")
            print(f"Evaluation: {score:.1f}")
            print(f"Nodes searched: {self.nodes_searched}")
            print(f"Time: {elapsed:.2f}s")
            print(f"Depth: {depth}")
            print("------")
            
            return True
        return False

# Initialize AI
ai_player = AIPlayer()

# Game state
selected_piece = None
selected_pos = None
turn = "w"  # White moves first
running = True
game_over = False
winner = None
result = None

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            if turn == "w":  # Human's turn
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
                        
                        # Check game state
                        result, winner = get_game_state(chess_board, "b")
                        if result != "ongoing":
                            game_over = True
                        else:
                            turn = "b"  # Switch to AI's turn
                    selected_piece = None
                    selected_pos = None
    
    # AI's turn
    if turn == "b" and not game_over:
        pygame.time.delay(500)  # Small delay for AI move
        if ai_player.make_move(chess_board):
            # Check game state
            result, winner = get_game_state(chess_board, "w")
            if result != "ongoing":
                game_over = True
            else:
                turn = "w"  # Switch to human's turn

    # Draw everything
    draw_board()
    draw_pieces()
    
    # Highlight selected piece
    if selected_piece:
        row, col = selected_pos
        s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        s.fill(HIGHLIGHT)
        screen.blit(s, (col * SQUARE_SIZE, row * SQUARE_SIZE))
    
    # Highlight legal moves
    if selected_piece:
        row, col = selected_pos
        for r in range(8):
            for c in range(8):
                if is_valid_move(selected_piece, (row, col), (r, c)):
                    s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                    s.fill(GREEN if chess_board[r][c] == "" else RED)
                    screen.blit(s, (c * SQUARE_SIZE, r * SQUARE_SIZE))
    
    # Display game over message
    if game_over:
        font = pygame.font.SysFont("Arial", 48)
        if result == "checkmate":
            text = font.render(f"Checkmate! {winner.capitalize()} wins!", True, (255, 0, 0))
        else:
            text = font.render("Stalemate! Draw!", True, (255, 0, 0))
        text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(text, text_rect)
    
    pygame.display.flip()

pygame.quit()