# Define the 8 directions for checking neighboring pieces, starting from top-left.
# (row_delta, col_delta)
EIGHT_DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),  # Top-left, Top, Top-right
    (0, -1),           (0, 1),   # Left, Right
    (1, -1),  (1, 0),  (1, 1)    # Bottom-left, Bottom, Bottom-right
]

# --- Core Helper Functions ---

def _get_playable_slots(board):
    """Finds the next available [row, col] for each of the 7 columns."""
    slots = []
    for c in range(7):
        slot_found = False
        for r in range(6):
            if board[r][c] == 0:
                slots.append([r, c])
                slot_found = True
                break
        if not slot_found:
            slots.append(None) # Use None for full columns
    return slots

def _get_piece_in_direction(board, start_row, start_col, direction, steps):
    """
    Gets the piece ID located a number of steps away in a given direction.
    Returns -1 if the position is off the board.
    """
    dr, dc = direction
    target_row = start_row + dr * steps
    target_col = start_col + dc * steps

    if 0 <= target_row < 6 and 0 <= target_col < 7:
        return board[target_row][target_col]
    else:
        return -1 # Represents an off-board position

def _calculate_line_threat(board, base_r, base_c, player_id):
    """
    Calculates the threat score for a given player around a potential move.
    It checks all 8 directions for lines of 2 or 3 pieces.
    """
    total_score = 0
    
    # Check all 4 axes (horizontal, vertical, 2 diagonals)
    for i in range(4):
        direction = EIGHT_DIRECTIONS[i]
        opposite_direction = EIGHT_DIRECTIONS[7-i]
        
        line_length = 1
        
        # Count consecutive pieces in the primary direction
        front_blocked = False
        for step in range(1, 4):
            piece = _get_piece_in_direction(board, base_r, base_c, direction, step)
            if piece == player_id:
                line_length += 1
            else:
                if piece != 0: front_blocked = True
                break
        
        # Count consecutive pieces in the opposite direction
        back_blocked = False
        for step in range(1, 4):
            piece = _get_piece_in_direction(board, base_r, base_c, opposite_direction, step)
            if piece == player_id:
                line_length += 1
            else:
                if piece != 0: back_blocked = True
                break
        
        # --- Assign score based on the detected line ---
        score = 0
        if line_length >= 4:
            score = 10000 # A winning line
        elif line_length == 3:
            if not front_blocked and not back_blocked:
                score = 5000 # An open-ended three-in-a-row is a huge threat
            elif not front_blocked or not back_blocked:
                score = 1000 # A semi-open three-in-a-row
        
        if score > total_score:
            total_score = score
            
    return total_score

def _check_setup_risk(board, column_no):
    """
    Calculates the risk of placing a piece that gives the opponent
    a winning spot on the row directly above.
    """
    playable_slots = _get_playable_slots(board)
    move_pos = playable_slots[column_no]

    if move_pos is None or move_pos[0] >= 5:
        return 0 # No risk if column is full or move is on the top row

    # Calculate the threat for the opponent on the spot ABOVE our potential move
    above_row, above_col = move_pos[0] + 1, move_pos[1]
    
    # Temporarily place our piece to accurately check the situation above
    r, c = move_pos
    board[r][c] = 1 # Assume we place our piece
    
    opponent_threat_score = _calculate_line_threat(board, above_row, above_col, 2)
    
    board[r][c] = 0 # Backtrack
    
    # If their threat score is a winning one, return a huge penalty
    return -opponent_threat_score if opponent_threat_score >= 10000 else 0


def rule_eval(board):
    """
    Evaluates the board using a rule-based system and returns the best column to play.

    This function analyzes each valid move and assigns it a score based on:
    - Offensive potential (creating threats for our AI)
    - Defensive urgency (blocking opponent's threats)
    - Suicide move prevention (avoiding setting up the opponent for a win)

    Args:
        board (list): The current 6x7 game board.

    Returns:
        int: The index of the column (0-6) with the highest score.
    """
    column_scores = [0] * 7
    playable_slots = _get_playable_slots(board)

    for i in range(7):
        move_pos = playable_slots[i]
        
        # If a column is full, it's an invalid move. Give it the lowest possible score.
        if move_pos is None:
            column_scores[i] = -99999
            continue
        
        r, c = move_pos
        
        # 1. Calculate our offensive score for this move
        ai_score = _calculate_line_threat(board, r, c, 1)

        # 2. Calculate the defensive score (blocking opponent's threats)
        # We give a slight bonus to defensive moves by multiplying the score.
        opponent_score = _calculate_line_threat(board, r, c, 2) * 1.1

        # 3. Calculate the risk of setting up the opponent for a win above this move
        setup_penalty = _check_setup_risk(board, i)

        # The final score for the column is the greater of offense or defense,
        # plus any penalty for setting up the opponent.
        column_scores[i] = max(ai_score, opponent_score) + setup_penalty

    # If all moves have a score of 0 (e.g., at the start of the game),
    # use a default strategy to prioritize center columns.
    if all(score == 0 for score in column_scores):
        initial_values = {3: 10, 2: 5, 4: 5, 1: 2, 5: 2, 0: 1, 6: 1}
        for i in range(7):
            if playable_slots[i] is not None: # Only apply to non-full columns
                column_scores[i] = initial_values.get(i, 0)
    
    # Find the column index with the highest score
    best_score = -float('inf')
    best_column = -1
    # Iterate in a standard order to break ties consistently
    for i in range(7):
        if column_scores[i] > best_score:
            best_score = column_scores[i]
            best_column = i
            
    return best_column if best_column != -1 else 3 # Default to center if all else fails