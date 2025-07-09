import re

def display_board(board=None):
    """
    Prints a human-readable representation of the game board to the console.
    
    Args:
        board (list): The 6x7 list representing the game board.
    """
    if board is None:
        board = [[]]

    def _get_piece_char(piece_id):
        """Converts a player ID (0, 1, 2) to its character representation."""
        if piece_id == 1: return "X"  # AI Player
        if piece_id == 2: return "Y"  # Human Player
        return " "      # Empty slot

    # --- Print Board Header ---
    print("\n\n                       --------------------------- ")
    
    # --- Print Board Rows ---
    # We iterate through the board in reverse to display row 0 at the bottom.
    for row_index in range(5, -1, -1):
        # Format and print each cell in the current row
        row_str = "                      [%s] [%s] [%s] [%s] [%s] [%s] [%s] " % tuple(
            _get_piece_char(p) for p in board[row_index]
        )
        print(row_str)

    # --- Print Board Footer ---
    print("                       --------------------------- ")
    print("                       1   2   3   4   5   6   7   \n")


def check_for_winner(board=None):
    """
    Checks the board for a winning condition (four pieces in a row).

    Args:
        board (list): The 6x7 game board.

    Returns:
        int: The winner's ID (1 for AI, 2 for Human) if a winner is found.
        None: If there is no winner yet.
    """
    if board is None:
        board = [[]]
    
    WIN_P1 = [1, 1, 1, 1]
    WIN_P2 = [2, 2, 2, 2]

    # --- Check all 4 directions for a win ---

    # 1. Horizontal check
    for r in range(6):
        for c in range(4):
            line = board[r][c:c+4]
            if line == WIN_P1: return 1
            if line == WIN_P2: return 2

    # 2. Vertical check
    for c in range(7):
        for r in range(3):
            line = [board[r+i][c] for i in range(4)]
            if line == WIN_P1: return 1
            if line == WIN_P2: return 2

    # 3. Positive diagonal check (/)
    for r in range(3):
        for c in range(4):
            line = [board[r+i][c+i] for i in range(4)]
            if line == WIN_P1: return 1
            if line == WIN_P2: return 2
            
    # 4. Negative diagonal check (\)
    for r in range(3):
        for c in range(3, 7):
            line = [board[r+i][c-i] for i in range(4)]
            if line == WIN_P1: return 1
            if line == WIN_P2: return 2

    # No winner found
    return None

def _get_playable_slots(board):
    """
    Finds the next available row for each column.

    Returns:
        dict: A dictionary mapping a column index to its available row index.
              e.g., {0: 0, 1: 0, 2: 1} means col 0 and 1 are empty, 
              col 2 has one piece.
    """
    slots = {}
    for col_idx in range(7):
        for row_idx in range(6):
            if board[row_idx][col_idx] == 0:
                slots[col_idx] = row_idx
                break
    return slots


def process_human_move(board, col_input):
    """
    Validates a human player's input and updates the board.

    Args:
        board (list): The game board to modify.
        col_input (str): The column number string entered by the user (e.g., "4").
    """
    
    # Pre-compile regex for performance, though minor in this case.
    is_numeric = re.compile("^[1-7]$")
    
    playable_slots = _get_playable_slots(board)
    
    is_valid_move = False
    while not is_valid_move:
        # Check if input is a valid, playable column number
        if is_numeric.match(col_input):
            col_index = int(col_input) - 1
            if col_index in playable_slots:
                # Find the correct row and place the piece
                row_index = playable_slots[col_index]
                board[row_index][col_index] = 2 # Player 2 is the human
                is_valid_move = True
        
        # If the move was not valid, prompt for a new one
        if not is_valid_move:
            print("INVALID MOVE! Please enter a number from 1 to 7 for a non-full column.")
            col_input = input("Your move (column 1-7): ")


def generate_board_hash(board):
    """
    Generates a unique string representation of the current board state.
    Useful for transposition tables or memoization.
    """
    hash_str = ""
    for c in range(7):
        for r in range(6):
            piece = board[r][c]
            if piece == 0:
                break
            hash_str += str(piece)
        hash_str += "|"
    return hash_str