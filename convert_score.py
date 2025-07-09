def load_score_data(filepath):
    """Loads the initial score data from a given file path."""
    print(f"-> Loading base scores from '{filepath}'...")
    score_map = {}
    with open(filepath, 'r') as f:
        for line in f:
            state, key = line.split()
            score_map[state] = int(key)
    print(f"-> Loaded {len(score_map)} score entries.")
    return score_map


def save_processed_scores(filepath, scores):
    """Saves the fully processed scores to the output file."""
    print(f"-> Saving {len(scores)} processed scores to '{filepath}'...")
    with open(filepath, 'w') as f:
        for state, score in scores.items():
            f.write(f"{state} {score}\n")
    print("-> Save complete.")


def apply_scoring_rules(initial_scores):
    """
    Applies a series of pattern-based rules to refine board state scores.
    It returns a new dictionary with the updated scores.
    """
    processed_scores = initial_scores.copy()

    # --- Define patterns for players ---
    # Player '1' is the AI (our agent). Player '2' is the opponent.
    # Patterns represent sequences of pieces on the board.
    # '0' is an empty space, '3' will represent a potential winning move.
    
    # Opponent's patterns (defensive scoring)
    opponent_wins = ['2222']
    opponent_threats_3 = ['02220', '0222', '2220', '2202', '2022']
    opponent_threats_2 = ['02020', '00220', '02200']

    # AI's patterns (offensive scoring)
    ai_wins = ['1111']
    ai_opportunities_3 = ['01110', '0111', '1110', '1101', '1011']
    ai_opportunities_2 = ['01010', '00110', '01100']
    
    # This dictionary defines how to create new, high-value states by replacing
    # a pattern with one including a potential move ('3').
    # Format: 'original_pattern': [('new_pattern_string', score), ...]
    opponent_critical_upgrades = {
        '02220': [('32220', -10000), ('02223', -10000), ('32223', -10000)],
        '0222': [('3222', -10000)], '2220': [('2223', -10000)],
        '2202': [('2232', -10000)], '2022': [('2322', -10000)],
        '02020': [('02320', -10000), ('32320', -10000), ('32323', -10000)],
        '02200': [('32233', -10000)], '00220': [('33223', -10000)]
    }

    ai_critical_upgrades = {
        '01110': [('31110', 50), ('01113', 50), ('31113', 10000)],
        '0111': [('3111', 20)], '1110': [('1113', 40)],
        '1101': [('1131', 30)], '1011': [('1311', 30)],
        '01010': [('01310', 30), ('31310', 40), ('31313', 40)],
        '01100': [('31133', 50)], '00110': [('33113', 50)]
    }

    print("-> Applying scoring enhancement rules...")
    # Iterate over a copy of the keys, as the dictionary size will change.
    for state in list(initial_scores.keys()):
        
        # --- Apply rules for Opponent's patterns (Defensive values) ---
        all_opponent_patterns = opponent_threats_2 + opponent_threats_3 + opponent_wins
        for pattern in all_opponent_patterns:
            if pattern in state:
                # Assign a base score for containing the pattern
                if pattern in opponent_wins:
                    processed_scores[state] = -10000
                else: # threats
                    processed_scores[state] = -200
                
                # Check if this pattern has special "critical move" variations
                if pattern in opponent_critical_upgrades:
                    for new_pattern_str, score in opponent_critical_upgrades[pattern]:
                        new_state = state.replace(pattern, new_pattern_str)
                        processed_scores[new_state] = score

        # --- Apply rules for AI's patterns (Offensive values) ---
        all_ai_patterns = ai_opportunities_2 + ai_opportunities_3 + ai_wins
        for pattern in all_ai_patterns:
            if pattern in state:
                # Assign a base score
                if pattern in ai_wins:
                    processed_scores[state] = 10000
                else: # opportunities
                    processed_scores[state] = 200
                
                # Check for critical move variations
                if pattern in ai_critical_upgrades:
                    for new_pattern_str, score in ai_critical_upgrades[pattern]:
                        new_state = state.replace(pattern, new_pattern_str)
                        processed_scores[new_state] = score

    return processed_scores


def main():
    """
    Main execution function to run the score conversion process.
    """
    # Configure which files to process. Change these paths as needed.
    # The original code was set up for 5, 6, and 7-length patterns.
    # This example is configured for the 7-length pattern file.
    input_filepath = "./eval/old_7ki.txt"
    output_filepath = "./eval/7ki.txt"
    
    # Run the process
    initial_data = load_score_data(input_filepath)
    final_scores = apply_scoring_rules(initial_data)
    save_processed_scores(output_filepath, final_scores)
    
    print("\n[+] Score conversion process finished successfully!")


if __name__ == "__main__":
    main()