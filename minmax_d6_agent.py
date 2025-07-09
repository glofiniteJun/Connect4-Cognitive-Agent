import time
from copy import deepcopy

class ConnectFourGame:
    """
    Encapsulates all the logic for a self-contained Connect Four game instance.
    """
    def __init__(self, ai_depth=5):
        self.AI_PLAYER = 'X'
        self.HUMAN_PLAYER = 'O'
        self.EMPTY_SLOT = '-'
        
        self.BOARD_ROWS = 6
        self.BOARD_COLS = 7
        
        self.ai_search_depth = ai_depth
        self.board = [[self.EMPTY_SLOT for _ in range(self.BOARD_COLS)] for _ in range(self.BOARD_ROWS)]

    def _display_board(self):
        """Prints the current state of the board to the console."""
        print("\n  " + " ".join(map(str, range(self.BOARD_COLS))))
        print("  " + "-" * (self.BOARD_COLS * 2 - 1))
        for row in self.board:
            print("| " + " ".join(row) + " |")
        print("  " + "-" * (self.BOARD_COLS * 2 - 1))

    def _is_valid_column(self, col):
        """Checks if a column is within bounds and not full."""
        return 0 <= col < self.BOARD_COLS and self.board[0][col] == self.EMPTY_SLOT

    def _get_next_open_row(self, col):
        """Finds the next available row in a given column."""
        for r in range(self.BOARD_ROWS - 1, -1, -1):
            if self.board[r][col] == self.EMPTY_SLOT:
                return r
        return -1 # Should not happen if _is_valid_column is checked first

    def _is_winning_move(self, board_state, row, col, player):
        """Checks if placing a piece at [row, col] results in a win for the player."""
        # Define the four axes to check (horizontal, vertical, two diagonals)
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for dr, dc in directions:
            line_count = 1
            # Count in the positive direction
            for i in range(1, 4):
                r, c = row + dr * i, col + dc * i
                if 0 <= r < self.BOARD_ROWS and 0 <= c < self.BOARD_COLS and board_state[r][c] == player:
                    line_count += 1
                else:
                    break
            # Count in the negative direction
            for i in range(1, 4):
                r, c = row - dr * i, col - dc * i
                if 0 <= r < self.BOARD_ROWS and 0 <= c < self.BOARD_COLS and board_state[r][c] == player:
                    line_count += 1
                else:
                    break
            
            if line_count >= 4:
                return True
        return False

    def _evaluate_board_heuristic(self, board_state):
        """
        Calculates a heuristic score for a given board state.
        The score is based on the number of potential winning lines,
        with a heavy weight given to blocking the opponent.
        """
        ai_score = 0
        human_score = 0

        # Iterate through every potential spot on the board
        for r in range(self.BOARD_ROWS):
            for c in range(self.BOARD_COLS):
                if board_state[r][c] == self.EMPTY_SLOT:
                    
                    # Calculate value for the AI
                    if self._is_winning_move(board_state, r, c, self.AI_PLAYER):
                        # The heuristic values were fine-tuned based on human play.
                        # The 0.8 weighting prioritizes moves lower on the board.
                        ai_score += (0.8 ** (self.BOARD_ROWS - 1 - r))
                        
                    # Calculate value for the Human (opponent)
                    if self._is_winning_move(board_state, r, c, self.HUMAN_PLAYER):
                        # Defensive moves are weighted 4x more heavily than offensive ones.
                        human_score += 4 * (0.8 ** (self.BOARD_ROWS - 1 - r))
        
        return ai_score - human_score
        
    def _search_best_play_recursive(self, board_state, depth, is_ai_turn):
        """
        Recursively explores the game tree to find the average heuristic value
        of possible future states.
        """
        if depth == 0:
            return self._evaluate_board_heuristic(board_state)

        next_player = self.HUMAN_PLAYER if is_ai_turn else self.AI_PLAYER
        total_heuristic_value = 0
        playable_moves = 0

        for col in range(self.BOARD_COLS):
            if self.board[0][col] == self.EMPTY_SLOT:
                row = self._get_next_open_row(col)
                
                # Check for immediate terminal states
                if self._is_winning_move(board_state, row, col, next_player):
                    if next_player == self.AI_PLAYER: return 1000 # A guaranteed win is highly valuable
                    if next_player == self.HUMAN_PLAYER: return -4000 # A guaranteed loss is highly negative
                
                board_copy = deepcopy(board_state)
                board_copy[row][col] = next_player
                
                total_heuristic_value += self._search_best_play_recursive(board_copy, depth - 1, not is_ai_turn)
                playable_moves += 1
        
        return total_heuristic_value / playable_moves if playable_moves > 0 else 0


    def find_ai_move(self):
        """
        Determines the AI's best move by checking for immediate wins/blocks,
        then falling back to the recursive search.
        """
        # 1. Check for any move that results in an immediate win
        for col in range(self.BOARD_COLS):
            if self._is_valid_column(col):
                row = self._get_next_open_row(col)
                if self._is_winning_move(self.board, row, col, self.AI_PLAYER):
                    return col

        # 2. Check for any move that blocks an opponent's immediate win
        for col in range(self.BOARD_COLS):
            if self._is_valid_column(col):
                row = self._get_next_open_row(col)
                if self._is_winning_move(self.board, row, col, self.HUMAN_PLAYER):
                    return col

        # 3. If no critical moves, perform a deeper search for the best column
        best_col = -1
        best_score = -float('inf')

        for col in range(self.BOARD_COLS):
            if self._is_valid_column(col):
                board_copy = deepcopy(self.board)
                row = self._get_next_open_row(col)
                board_copy[row][col] = self.AI_PLAYER
                
                # Avoid moves that let the opponent win on the next turn
                if row > 0 and self._is_winning_move(board_copy, row - 1, col, self.HUMAN_PLAYER):
                    score = -5000
                else:
                    score = self._search_best_play_recursive(board_copy, self.ai_search_depth, False)

                if score > best_score:
                    best_score = score
                    best_col = col
        
        return best_col if best_col != -1 else 3 # Default to center column if all else fails

    def play_game(self):
        """Main game loop to run the program."""
        winner = None
        while not winner:
            self._display_board()
            
            # --- Human's Turn ---
            human_col = -1
            while not self._is_valid_column(human_col):
                try:
                    move_input = input(f"Your move (Player {self.HUMAN_PLAYER}), enter column [0-6]: ")
                    human_col = int(move_input)
                    if not self._is_valid_column(human_col):
                        print("Invalid move. Column is full or out of range.")
                except (ValueError, IndexError):
                    print("Invalid input. Please enter a number between 0 and 6.")

            human_row = self._get_next_open_row(human_col)
            self.board[human_row][human_col] = self.HUMAN_PLAYER
            if self._is_winning_move(self.board, human_row, human_col, self.HUMAN_PLAYER):
                winner = self.HUMAN_PLAYER
                break

            # Check for a draw
            if all(self.board[0][c] != self.EMPTY_SLOT for c in range(self.BOARD_COLS)):
                winner = "Draw"
                break

            # --- AI's Turn ---
            print("\nAI is thinking...")
            ai_col = self.find_ai_move()
            
            if ai_col is None or not self._is_valid_column(ai_col):
                # Fallback if AI fails to find a valid move
                for c in range(self.BOARD_COLS):
                    if self._is_valid_column(c):
                        ai_col = c
                        break
            
            print(f"AI chooses column {ai_col}.")
            ai_row = self._get_next_open_row(ai_col)
            self.board[ai_row][ai_col] = self.AI_PLAYER
            if self._is_winning_move(self.board, ai_row, ai_col, self.AI_PLAYER):
                winner = self.AI_PLAYER
        
        # --- Game Over ---
        print("\n----- GAME OVER -----")
        self._display_board()
        if winner == "Draw":
            print("It's a draw!")
        else:
            print(f"Winner is Player {winner}!")

if __name__ == '__main__':
    game = ConnectFourGame(ai_depth=5)
    game.play_game()