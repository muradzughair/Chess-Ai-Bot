import pygame

pygame.init()

# the borad:

# the screen size
WIDTH, HEIGHT = 800, 800
# each square size
SQUARE_SIZE = WIDTH // 8
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Board")

# the chess colors
WHITE = (238, 238, 210)
BLACK = (118, 150, 86)

# function to draw the borad
def draw_board():
    for row in range(8):
        for col in range(8):
            # white if even and balck id odd
            color = WHITE if (row + col) % 2 == 0 else BLACK
            # put the square in the right place with the right color
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            # first parameter for screen, second parameter for the color, third one (x postion, y postion, width, height)


# chess peices pictures (download the pictures from the repo and puth their path here):
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

# Resize the chess pieces to fit the squares
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
    """Draw the chess pieces on the board."""
    for row in range(8):
        for col in range(8):
            piece = chess_board[row][col]
            if piece != "":
                screen.blit(pieces[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))


def is_valid_move(piece, start, end):
    """
    Checks if the move is valid based on the piece type.
    - piece: a string like "wp" (white pawn), "bk" (black king)
    - start: (row, col) starting position
    - end: (row, col) target position
    """
    start_row, start_col = start
    end_row, end_col = end

    if piece == "wp":  # White Pawn
        if start_col == end_col:  # Moving straight
            if end_row == start_row - 1:  # Normal move
                return True
            elif start_row == 6 and end_row == 4:  # First move, double step
                return True
        # Capturing diagonally
        elif abs(start_col - end_col) == 1 and end_row == start_row - 1:
            return True

    elif piece == "bp":  # Black Pawn
        if start_col == end_col:
            if end_row == start_row + 1:
                return True
            elif start_row == 1 and end_row == 3:
                return True
        elif abs(start_col - end_col) == 1 and end_row == start_row + 1:
            return True

    elif piece in ["wr", "br"]:  # Rook (White or Black)
        return start_row == end_row or start_col == end_col  # Move in straight lines

    elif piece in ["wb", "bb"]:  # Bishop (White or Black)
        return abs(start_row - end_row) == abs(start_col - end_col)  # Move diagonally

    elif piece in ["wq", "bq"]:  # Queen (White or Black)
        return (start_row == end_row or start_col == end_col) or \
               (abs(start_row - end_row) == abs(start_col - end_col))  # Like Rook & Bishop

    elif piece in ["wk", "bk"]:  # King (White or Black)
        return max(abs(start_row - end_row), abs(start_col - end_col)) == 1  # One step any direction

    elif piece in ["wn", "bn"]:  # Knight (White or Black)
        return (abs(start_row - end_row), abs(start_col - end_col)) in [(2, 1), (1, 2)]  # L-shape move

    return False  # If move does not match any rule


def is_king_in_check(board, king_color):
    """
    Checks if the king is under attack.
    - board: current chess board
    - king_color: "w" for white, "b" for black
    """
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

    # Check if any enemy piece can attack the king
    for piece, pos in enemy_pieces:
        if is_valid_move(piece, pos, king_pos):
            return True

    return False


def has_legal_moves(board, turn):
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece and piece[0] == turn:  # Check only current player's pieces
                for nr in range(8):
                    for nc in range(8):
                        if is_valid_move(piece, (r, c), (nr, nc)):
                            return True
    return False



selected_piece = None
selected_pos = None
turn = "w"  # White moves first
running=True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            row, col = y // SQUARE_SIZE, x // SQUARE_SIZE

            if selected_piece is None:  # Selecting a piece
                if chess_board[row][col] and chess_board[row][col][0] == turn:
                    selected_piece = chess_board[row][col]
                    selected_pos = (row, col)
            else:  # Moving a piece
                
                if is_valid_move(selected_piece, selected_pos, (row, col)):  # Check valid move
                    chess_board[row][col] = selected_piece
                    chess_board[selected_pos[0]][selected_pos[1]] = ""
                    turn = "b" if turn == "w" else "w"  # Switch turns
                    # **Check for Checkmate or Stalemate**
                    if not has_legal_moves(chess_board, turn):
                        if is_king_in_check(chess_board, turn):
                            print(f"Checkmate! {turn} loses.")
                        else:
                            print("Stalemate! It's a draw.")
                        running = False  # End game loop
                selected_piece = None
                selected_pos = None

    draw_board()
    draw_pieces()
    pygame.display.flip()

pygame.quit()
