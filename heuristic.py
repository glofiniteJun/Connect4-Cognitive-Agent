############################################################################
#
# ConnectFour Critical Move Heuristics
# Author: My "Unique" Alias
# Date: July 2025
#
# Description:
# This module provides heuristic functions to detect immediate, critical
# game situations.
#   - attack_critical_choice: Finds a move for an instant win.
#   - protect_critical_choice: Finds a move to block an opponent's
#     imminent win.
# These functions are designed to be called before the main search algorithm
# to quickly handle obvious win/loss scenarios.
#
############################################################################

def attack_critical_choice(board, valid_moves_list):
    """
    Scans the board for any move that will result in an immediate win for the AI.
    A "critical attack" is a line of three AI pieces with one empty, playable spot.

    Args:
        board (list): The 6x7 game board state.
        valid_moves_list (list): A list of currently playable moves, e.g., [[r1, c1], [r2, c2]].

    Returns:
        int: The index of the winning move in `valid_moves_list`.
        str: "not critical" if no immediate winning move is found.
    """
    # Iterate through each cell to check for potential winning lines
    for row in range(6):
        for col in range(7):
            
            # --- 1. Check for Vertical Wins ---
            # Pattern: Three '1's stacked vertically below an empty spot.
            if row >= 3 and board[row][col] == 0:
                if board[row-1][col] == 1 and board[row-2][col] == 1 and board[row-3][col] == 1:
                    if [row, col] in valid_moves_list:
                        return valid_moves_list.index([row, col])

            # --- 2. Check for Horizontal Wins ---
            # Checks for patterns like 111_, 11_1, 1_11
            if col <= 3: # Boundary check to prevent IndexError
                # Pattern: 1 1 1 _
                if board[row][col] == 1 and board[row][col+1] == 1 and board[row][col+2] == 1:
                    if [row, col+3] in valid_moves_list:
                        return valid_moves_list.index([row, col+3])
                # Pattern: 1 1 _ 1
                if board[row][col] == 1 and board[row][col+1] == 1 and board[row][col+3] == 1:
                    if [row, col+2] in valid_moves_list:
                        return valid_moves_list.index([row, col+2])
                # Pattern: 1 _ 1 1
                if board[row][col] == 1 and board[row][col+2] == 1 and board[row][col+3] == 1:
                    if [row, col+1] in valid_moves_list:
                        return valid_moves_list.index([row, col+1])
            if col >= 3: # Check for _ 1 1 1
                if board[row][col] == 1 and board[row][col-1] == 1 and board[row][col-2] == 1:
                    if [row, col-3] in valid_moves_list:
                        return valid_moves_list.index([row, col-3])

            # --- 3. Check for Positive Diagonal Wins (/) ---
            if row <= 2 and col <= 3: # Boundary check
                # Pattern: 1 1 1 _
                if board[row][col] == 1 and board[row+1][col+1] == 1 and board[row+2][col+2] == 1:
                    if [row+3, col+3] in valid_moves_list:
                        return valid_moves_list.index([row+3, col+3])
                # Pattern: 1 1 _ 1
                if board[row][col] == 1 and board[row+1][col+1] == 1 and board[row+3][col+3] == 1:
                     if [row+2, col+2] in valid_moves_list:
                        return valid_moves_list.index([row+2, col+2])
                # Pattern: 1 _ 1 1
                if board[row][col] == 1 and board[row+2][col+2] == 1 and board[row+3][col+3] == 1:
                     if [row+1, col+1] in valid_moves_list:
                        return valid_moves_list.index([row+1, col+1])
            if row >= 3 and col >= 3: # Check for _ 1 1 1
                if board[row][col] == 1 and board[row-1][col-1] == 1 and board[row-2][col-2] == 1:
                    if [row-3, col-3] in valid_moves_list:
                        return valid_moves_list.index([row-3, col-3])

            # --- 4. Check for Negative Diagonal Wins (\) ---
            if row <= 2 and col >= 3: # Boundary check
                # Pattern: 1 1 1 _
                if board[row][col] == 1 and board[row+1][col-1] == 1 and board[row+2][col-2] == 1:
                    if [row+3, col-3] in valid_moves_list:
                        return valid_moves_list.index([row+3, col-3])
                # Pattern: 1 1 _ 1
                if board[row][col] == 1 and board[row+1][col-1] == 1 and board[row+3][col-3] == 1:
                    if [row+2, col-2] in valid_moves_list:
                        return valid_moves_list.index([row+2, col-2])
                # Pattern: 1 _ 1 1
                if board[row][col] == 1 and board[row+2][col-2] == 1 and board[row+3][col-3] == 1:
                    if [row+1, col-1] in valid_moves_list:
                        return valid_moves_list.index([row+1, col-1])
            if row >=3 and col <=3: # Check for _ 1 1 1
                if board[row][col] == 1 and board[row-1][col+1] == 1 and board[row-2][col+2] == 1:
                    if [row-3, col+3] in valid_moves_list:
                        return valid_moves_list.index([row-3, col+3])

    return "not critical"


def protect_critical_choice(board, valid_moves_list):
    """
    Scans the board to find if the opponent has a winning move on their next
    turn, and returns the move required to block it.
    A "critical defense" is blocking a line of three opponent pieces.

    Args:
        board (list): The 6x7 game board state.
        valid_moves_list (list): A list of currently playable moves.

    Returns:
        int: The index of the blocking move in `valid_moves_list`.
        str: "not critical" if no immediate threat is found.
    """
    
    # --- Helper functions nested inside for encapsulation ---
    def _is_opponent_triple(p1, p2, p3):
        """Checks if three pieces all belong to the opponent (player 2)."""
        return p1 == 2 and p2 == 2 and p3 == 2

    def _get_all_playable_slots(current_board):
        """Gets all available moves, including placeholders for full columns."""
        slots = []
        for c in range(7):
            slot_found = False
            for r in range(6):
                if current_board[r][c] == 0:
                    slots.append([r, c])
                    slot_found = True
                    break
            if not slot_found:
                slots.append([-1, c]) # Placeholder for full column
        return slots

    # --- Main Logic ---
    playable_slots = _get_all_playable_slots(board)

    # 1. Check Diagonal Threats
    # This logic iterates through board sections checking for 3-in-a-row for player 2.
    
    # Positive diagonals (/)
    for r in range(3):
        for c in range(4):
            # Check for gapped threats like 2_22 or 22_2
            if _is_opponent_triple(board[r][c], board[r+1][c+1], board[r+3][c+3]) and [r+2, c+2] in playable_slots:
                return valid_moves_list.index([r+2, c+2])
            if _is_opponent_triple(board[r][c], board[r+2][c+2], board[r+3][c+3]) and [r+1, c+1] in playable_slots:
                return valid_moves_list.index([r+1, c+1])
            
            # Check for a solid line of three (222)
            if _is_opponent_triple(board[r+1][c+1], board[r+2][c+2], board[r+3][c+3]) and [r, c] in playable_slots:
                return valid_moves_list.index([r, c])

    # Negative diagonals (\)
    for r in range(3):
        for c in range(3, 7):
             # Check for gapped threats
            if _is_opponent_triple(board[r][c], board[r+1][c-1], board[r+3][c-3]) and [r+2, c-2] in playable_slots:
                return valid_moves_list.index([r+2, c-2])
            if _is_opponent_triple(board[r][c], board[r+2][c-2], board[r+3][c-3]) and [r+1, c-1] in playable_slots:
                return valid_moves_list.index([r+1, c-1])
            
            # Check for a solid line of three
            if _is_opponent_triple(board[r+1][c-1], board[r+2][c-2], board[r+3][c-3]) and [r, c] in playable_slots:
                 return valid_moves_list.index([r, c])


    # 2. Check Horizontal and Vertical Threats
    # This iterates through the available moves and checks if placing a piece there
    # would be adjacent to an opponent's 3-in-a-row threat.
    for r, c in playable_slots:
        if r == -1: # Skip full columns
            continue

        # Check for a vertical threat directly below the playable slot
        if r >= 3 and _is_opponent_triple(board[r-1][c], board[r-2][c], board[r-3][c]):
            return valid_moves_list.index([r, c])

        # Check for horizontal threats around the playable slot
        # Pattern: 222_
        if c >= 3 and _is_opponent_triple(board[r][c-1], board[r][c-2], board[r][c-3]):
            return valid_moves_list.index([r, c])
        # Pattern: _222
        if c <= 3 and _is_opponent_triple(board[r][c+1], board[r][c+2], board[r][c+3]):
            return valid_moves_list.index([r, c])
        # Pattern: 2_22
        if c >= 1 and c <= 4 and _is_opponent_triple(board[r][c-1], board[r][c+1], board[r][c+2]):
            return valid_moves_list.index([r, c])
        # Pattern: 22_2
        if c >= 2 and c <= 5 and _is_opponent_triple(board[r][c-2], board[r][c-1], board[r][c+1]):
            return valid_moves_list.index([r, c])

    return "not critical"