import pygame
import copy
import math
import time
from collections import defaultdict

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
SQUARE_SIZE = WIDTH // 8
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess AI")

# Colors
WHITE = (238, 238, 210)
BLACK = (118, 150, 86)
HIGHLIGHT = (247, 247, 105, 150)
RED = (255, 0, 0, 150)
GREEN = (0, 255, 0, 150)

# Simplified Piece values
PIECE_VALUES = {
    'p': 100, 'n': 300, 'b': 300, 'r': 500, 'q': 900, 'k': 20000
}

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

class AIPlayer:
    def __init__(self):
        self.max_depth = 3  # Reduced from 4
        self.nodes_searched = 0
        self.max_nodes = 5000  # Limit nodes searched per move
    
    def evaluate_board(self, board):
        """Simplified evaluation function"""
        score = 0
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece:
                    value = PIECE_VALUES[piece[1]]
                    score += value if piece[0] == 'w' else -value
        return score
    
    def get_all_valid_moves(self, board, color):
        """Get all legal moves for the given color"""
        moves = []
        for r in range(8):
            for c in range(8):
                piece = board[r][c]
                if piece and piece[0] == color:
                    for nr in range(8):
                        for nc in range(8):
                            if self.is_valid_move(piece, (r, c), (nr, nc)):
                                # Make temporary move
                                temp_board = copy.deepcopy(board)
                                temp_board[nr][nc] = piece
                                temp_board[r][c] = ""
                                if not self.is_king_in_check(temp_board, color):
                                    moves.append(((r, c), (nr, nc)))
        return moves
    
    def is_valid_move(self, piece, start, end):
        """Check if a move is valid for a given piece"""
        start_row, start_col = start
        end_row, end_col = end

        if not (0 <= end_row < 8 and 0 <= end_col < 8):
            return False

        color = piece[0]
        piece_type = piece[1]
        target = chess_board[end_row][end_col]

        if target and target[0] == color:
            return False

        # Pawn movement
        if piece_type == 'p':
            direction = -1 if color == 'w' else 1
            start_rank = 6 if color == 'w' else 1

            if start_col == end_col:  # Forward
                if target == "":
                    if end_row == start_row + direction:
                        return True
                    if (start_row == start_rank and 
                        end_row == start_row + 2 * direction and 
                        chess_board[start_row + direction][start_col] == ""):
                        return True
                return False
            elif abs(start_col - end_col) == 1 and end_row == start_row + direction:
                return target != ""

        # Knight movement
        elif piece_type == 'n':
            return (abs(start_row - end_row), abs(start_col - end_col)) in [(2, 1), (1, 2)]

        # Bishop movement
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

        # Rook movement
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

        # Queen movement
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

        # King movement
        elif piece_type == 'k':
            return max(abs(start_row - end_row), abs(start_col - end_col)) == 1

        return False

    def is_king_in_check(self, board, color):
        """Check if the king of the given color is in check"""
        king_pos = None
        enemy_pieces = []

        for r in range(8):
            for c in range(8):
                piece = board[r][c]
                if piece == color + "k":
                    king_pos = (r, c)
                elif piece and piece[0] != color:
                    enemy_pieces.append((piece, (r, c)))

        if king_pos is None:
            return False

        for piece, pos in enemy_pieces:
            if self.is_valid_move(piece, pos, king_pos):
                return True

        return False

    def minimax(self, board, depth, alpha, beta, color):
        """Simplified minimax with alpha-beta pruning"""
        self.nodes_searched += 1
        if self.nodes_searched > self.max_nodes:
            return self.evaluate_board(board), None

        if depth == 0:
            return self.evaluate_board(board), None

        moves = self.get_all_valid_moves(board, color)
        if not moves:
            if self.is_king_in_check(board, color):
                return -math.inf if color == 'w' else math.inf, None
            else:
                return 0, None

        best_move = None
        best_score = -math.inf if color == 'w' else math.inf

        for move in moves:
            start, end = move
            piece = board[start[0]][start[1]]
            
            new_board = copy.deepcopy(board)
            new_board[end[0]][end[1]] = piece
            new_board[start[0]][start[1]] = ""
            
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
            
            if beta <= alpha:
                break

        return best_score, best_move

    def make_move(self, board):
        """Make the best move found by minimax"""
        self.nodes_searched = 0
        start_time = time.time()
        
        score, best_move = self.minimax(board, self.max_depth, -math.inf, math.inf, 'b')
        
        if best_move:
            start, end = best_move
            piece = board[start[0]][start[1]]
            board[end[0]][end[1]] = piece
            board[start[0]][start[1]] = ""
            
            print(f"AI moved {piece} from {start} to {end}")
            print(f"Evaluation: {score:.1f}")
            print(f"Nodes searched: {self.nodes_searched}")
            print(f"Time: {time.time()-start_time:.2f}s")
            return True
        return False

# Initialize AI
ai_player = AIPlayer()

# Game state
selected_piece = None
selected_pos = None
turn = "w"
running = True
game_over = False

def draw_board():
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces():
    for row in range(8):
        for col in range(8):
            piece = chess_board[row][col]
            if piece:
                # Draw colored circles as pieces (replace with your images)
                if piece[0] == 'w':
                    pygame.draw.circle(screen, (255, 255, 255), 
                                     (col*SQUARE_SIZE + SQUARE_SIZE//2, row*SQUARE_SIZE + SQUARE_SIZE//2), 
                                     SQUARE_SIZE//2 - 5)
                else:
                    pygame.draw.circle(screen, (50, 50, 50), 
                                     (col*SQUARE_SIZE + SQUARE_SIZE//2, row*SQUARE_SIZE + SQUARE_SIZE//2), 
                                     SQUARE_SIZE//2 - 5)
                
                # Draw piece letter
                font = pygame.font.SysFont(None, 36)
                text = font.render(piece[1].upper(), True, (0, 0, 0) if piece[0] == 'w' else (255, 255, 255))
                text_rect = text.get_rect(center=(col*SQUARE_SIZE + SQUARE_SIZE//2, row*SQUARE_SIZE + SQUARE_SIZE//2))
                screen.blit(text, text_rect)

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            if turn == "w":  # Human's turn
                x, y = pygame.mouse.get_pos()
                row, col = y // SQUARE_SIZE, x // SQUARE_SIZE

                if selected_piece is None:
                    if chess_board[row][col] and chess_board[row][col][0] == turn:
                        selected_piece = chess_board[row][col]
                        selected_pos = (row, col)
                else:
                    if ai_player.is_valid_move(selected_piece, selected_pos, (row, col)):
                        chess_board[row][col] = selected_piece
                        chess_board[selected_pos[0]][selected_pos[1]] = ""
                        turn = "b"
                    selected_piece = None
                    selected_pos = None
    
    # AI's turn
    if turn == "b" and not game_over:
        pygame.time.delay(300)  # Small delay so moves don't happen too fast
        if ai_player.make_move(chess_board):
            turn = "w"

    # Draw everything
    draw_board()
    
    # Highlight selected piece and moves
    if selected_piece:
        row, col = selected_pos
        s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        s.fill(HIGHLIGHT)
        screen.blit(s, (col * SQUARE_SIZE, row * SQUARE_SIZE))
        
        for r in range(8):
            for c in range(8):
                if ai_player.is_valid_move(selected_piece, (row, col), (r, c)):
                    s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                    s.fill(GREEN if chess_board[r][c] == "" else RED)
                    screen.blit(s, (c * SQUARE_SIZE, r * SQUARE_SIZE))
    
    draw_pieces()
    pygame.display.flip()

pygame.quit()