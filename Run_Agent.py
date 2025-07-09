# Import necessary libraries and modules from the project
import time
from copy import deepcopy
from heuristic import attack_critical_choice, protect_critical_choice
# Use the new, refactored function names from Con4Utils.py
from Connect4Utils import display_board, check_for_winner, process_human_move
from Rule import rule_eval

# --- Global Configurations & Game State ---

# The game board state. 0: empty, 1: AI, 2: Human
GAME_BOARD = [[0] * 7 for _ in range(6)]

# Strategic column evaluation order, starting from the center.
COLUMN_PRIORITY = [3, 2, 4, 1, 5, 0, 6]

# Dictionaries to hold scores for board patterns, loaded from files.
SCORE_TABLES = {4: {}, 5: {}, 6: {}, 7: {}}


# --- AI Core Logic: Evaluation and Search ---

def _convert_line_to_key(line_pattern):
    """
    Converts a list representing a line on the board into a single integer key.
    This key is used to look up the line's score in the score tables.
    """
    key = 0
    for i, piece in enumerate(reversed(line_pattern)):
        key += (10 ** i) * piece
    return key

def _get_line_score(line, score_table):
    """
    Looks up the score for a line pattern. If the exact pattern
    (with potential moves marked as '3') isn't found, it checks for a
    fallback pattern where '3's are treated as empty '0's.
    """
    primary_key = _convert_line_to_key(line)
    if primary_key in score_table:
        return score_table[primary_key]

    fallback_line = [p if p != 3 else 0 for p in line]
    fallback_key = _convert_line_to_key(fallback_line)
    return score_table.get(fallback_key, 0)

def evaluate_board_state(board):
    """
    Calculates a heuristic score for the entire board state.
    A higher score favors the AI (player 1).
    """
    evaluation = 0
    valid_moves = get_prioritized_moves(board)
    for r, c in valid_moves:
        board[r][c] = 3

    # Score Horizontal, Vertical, and Diagonal Lines
    for r in range(6):
        evaluation += _get_line_score(board[r][:], SCORE_TABLES[7])
    for c in range(7):
        evaluation += _get_line_score([board[r][c] for r in range(6)], SCORE_TABLES[6])
    
    diag_lines = [
        ([board[i][i] for i in range(6)], 6), ([board[i][i+1] for i in range(6)], 6),
        ([board[5-i][i] for i in range(6)], 6), ([board[5-i][i+1] for i in range(6)], 6),
        ([board[i+1][i] for i in range(5)], 5), ([board[i][i+2] for i in range(5)], 5),
        ([board[4-i][i] for i in range(5)], 5), ([board[5-i][i+2] for i in range(5)], 5),
        ([board[i+2][i] for i in range(4)], 4), ([board[i][i+3] for i in range(4)], 4),
        ([board[3-i][i] for i in range(4)], 4), ([board[5-i][i+3] for i in range(4)], 4)
    ]
    for line, length in diag_lines:
        evaluation += _get_line_score(line, SCORE_TABLES[length])

    for r, c in valid_moves:
        board[r][c] = 0
    return evaluation


def find_best_move_alpha_beta(board, depth, start_time, time_limit_sec):
    """Top-level function to start the alpha-beta search."""
    alpha = -float('inf')
    beta = float('inf')
    
    def _max_value(current_board, d, a, b):
        moves = get_prioritized_moves(current_board)
        if d == 0 or not moves:
            return evaluate_board_state(current_board)
        
        v = -float('inf')
        for r, c in moves:
            current_board[r][c] = 1
            v = max(v, _min_value(current_board, d - 1, a, b))
            current_board[r][c] = 0
            if v >= b: return v
            a = max(a, v)
        return v

    def _min_value(current_board, d, a, b):
        moves = get_prioritized_moves(current_board)
        if d == 0 or not moves:
            return evaluate_board_state(current_board)

        v = float('inf')
        for r, c in moves:
            current_board[r][c] = 2
            v = min(v, _max_value(current_board, d - 1, a, b))
            current_board[r][c] = 0
            if v <= a: return v
            b = min(b, v)
        return v

    best_score = -float('inf')
    best_move_index = 0
    possible_moves = get_prioritized_moves(board)

    for i, (r, c) in enumerate(possible_moves):
        if time.time() - start_time >= time_limit_sec:
            return "TIMEOUT", None

        board[r][c] = 1
        score = _min_value(board, depth - 1, alpha, beta)
        board[r][c] = 0

        if score > best_score:
            best_score = score
            best_move_index = i
        alpha = max(alpha, best_score)

    return best_move_index, best_score


def find_move_with_iterative_deepening(board, time_limit_sec=8):
    """Performs an iterative deepening search to find the best move."""
    start_time = time.time()
    best_move_so_far = 0 
    
    for depth in range(1, 10):
        if time.time() - start_time >= time_limit_sec:
            print(f"Time limit reached. Using best move from depth {depth - 1}.")
            break

        print(f"Searching at depth {depth}...")
        
        board_copy = deepcopy(board)
        move_index, score = find_best_move_alpha_beta(board_copy, depth, start_time, time_limit_sec)

        if move_index == "TIMEOUT":
            print(f"Search timed out at depth {depth}. Using best move from depth {depth - 1}.")
            break
        
        best_move_so_far = move_index
        elapsed = time.time() - start_time
        print(f"Depth {depth} complete in {elapsed:.2f}s. Best move index: {best_move_so_far} (Score: {score})")

        if elapsed > time_limit_sec / 2:
             print("Stopping early to avoid timeout on next depth.")
             break

    return best_move_so_far

# --- Game Utilities & Move Execution ---

def get_prioritized_moves(board):
    """Returns a list of valid moves in a strategically prioritized order."""
    moves = []
    for col in COLUMN_PRIORITY:
        for row in range(6):
            if board[row][col] == 0:
                moves.append([row, col])
                break
    return moves

def get_standard_moves(board):
    """Returns a list of valid moves for each column (0-6) for the Rule.py module."""
    moves = []
    for col in range(7):
        is_full = True
        for row in range(6):
            if board[row][col] == 0:
                moves.append([row, col])
                is_full = False
                break
        if is_full:
            moves.append([1000, 1000])
    return moves

def make_ai_move(board, move_index, player_id):
    """Makes a move for the AI based on the move's index in the prioritized list."""
    valid_moves = get_prioritized_moves(board)
    if move_index < len(valid_moves):
        r, c = valid_moves[move_index]
        board[r][c] = player_id

def make_rule_based_move(board, column_index, player_id):
    """Makes a move based on the column index provided by the rule-based engine."""
    moves_by_column = get_standard_moves(board)
    if column_index < len(moves_by_column):
        r, c = moves_by_column[column_index]
        if r < 1000:
            board[r][c] = player_id

def load_evaluation_tables():
    """Loads all score tables from their respective files."""
    print("Loading AI evaluation tables...")
    for i in range(4, 8):
        try:
            with open(f"eval/{i}ki.txt") as f:
                for line in f:
                    tok = line.split()
                    SCORE_TABLES[i][int(tok[0])] = int(tok[1])
        except FileNotFoundError:
            print(f"Error: Could not find eval/{i}ki.txt. AI will not function correctly.")
            exit()
    print("...Loading complete.")


def prompt_ai_mode():
    """Prompts the user to select the AI's strategy for the turn."""
    while True:
        print("\nSelect AI Mode for this turn:")
        print(" [1] Hybrid Heuristic Search (slower, stronger)")
        print(" [2] Rule-Based (faster, simpler)")
        choice = input(">> Select: ")
        if choice == '1': return "Heuristic"
        if choice == '2': return "Rule"
        print("Invalid input. Please enter 1 or 2.")


# --- Main Game Execution ---

if __name__ == "__main__":
    
    load_evaluation_tables()
    GAME_BOARD.reverse() # Maintained for compatibility with Con4Utils.py

    turn_counter = 0

    first = input("Do you want to play first? (y/n) >> ").lower()
    is_human_turn = (first == 'y')

    while True:
        display_board(GAME_BOARD)
        
        winner = check_for_winner(GAME_BOARD)
        if winner == 1:
            print("\n*** AI WINS! ***")
            break
        elif winner == 2:
            print("\n*** YOU WIN! ***")
            break
            
        if not get_prioritized_moves(GAME_BOARD):
            print("\n--- IT'S A DRAW ---")
            break

        if is_human_turn:
            move_input = input("Your move (column 1-7): ")
            process_human_move(GAME_BOARD, move_input)
        else: # AI's Turn
            turn_counter += 1
            print("\nAI is thinking...")
            start_c = time.time()
            
            if turn_counter == 1 and not (first == 'y'):
                print("AI makes its opening move.")
                make_ai_move(GAME_BOARD, 1, 1)
            else:
                ai_mode = prompt_ai_mode()
                
                if ai_mode == "Rule":
                    best_col = rule_eval(GAME_BOARD)
                    make_rule_based_move(GAME_BOARD, best_col, 1)
                else: # Heuristic mode
                    moves = get_prioritized_moves(GAME_BOARD)
                    
                    attack_move = attack_critical_choice(GAME_BOARD, moves)
                    if attack_move != "not critical":
                        print("Critical Attack! AI sees a win.")
                        make_ai_move(GAME_BOARD, attack_move, 1)
                    else:
                        defend_move = protect_critical_choice(GAME_BOARD, moves)
                        if defend_move != "not critical":
                            print("Critical Defense! AI is blocking a threat.")
                            make_ai_move(GAME_BOARD, defend_move, 1)
                        else:
                            best_move = find_move_with_iterative_deepening(GAME_BOARD)
                            make_ai_move(GAME_BOARD, best_move, 1)

            print(f"AI took {time.time() - start_c:.2f} seconds to move.")
        
        is_human_turn = not is_human_turn
        
    display_board(GAME_BOARD)
    print("Game Over.")