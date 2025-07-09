def load_score_file(filepath):
    """
    Loads a score file into a dictionary.

    Args:
        filepath (str): The path to the score file.

    Returns:
        dict: A dictionary mapping board state strings to integer scores.
    """
    scores = {}
    print(f"-> Reading scores from '{filepath}'...")
    try:
        with open(filepath, 'r') as f:
            for line in f:
                state, score_str = line.split()
                scores[state] = int(score_str)
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")
        return None
        
    print(f"-> Found {len(scores)} entries.")
    return scores


def save_merged_scores(filepath, scores):
    """
    Saves the final, merged scores to a file.

    Args:
        filepath (str): The path for the output file.
        scores (dict): The dictionary of scores to save.
    """
    print(f"-> Saving {len(scores)} merged scores to '{filepath}'...")
    with open(filepath, 'w') as f:
        for state, score in scores.items():
            f.write(f"{state} {score}\n")
    print("-> Save complete.")


def merge_and_average_scores(base_scores, old_scores):
    """
    Merges two sets of scores by averaging values for common states.

    Args:
        base_scores (dict): The primary score dictionary. This one will be modified.
        old_scores (dict): The secondary score dictionary to average with.

    Returns:
        dict: The modified base_scores dictionary with averaged values.
    """
    if not base_scores or not old_scores:
        print("-> One or both score sets are empty. No merge possible.")
        return base_scores

    print("\n-> Averaging scores for common states...")
    
    # This is much more efficient than a nested loop.
    # We iterate through the base scores and directly check if the state
    # exists in the old scores dictionary.
    
    averaged_count = 0
    final_scores = base_scores.copy()
    
    for state, base_score in final_scores.items():
        if state in old_scores:
            old_score = old_scores[state]
            # Calculate the integer average of the two scores
            final_scores[state] = int((base_score + old_score) / 2)
            averaged_count += 1
            
    print(f"-> Averaged {averaged_count} common states.")
    return final_scores


def main():
    """
    Main function to orchestrate the file loading, averaging, and saving process.
    """
    # --- Configuration ---
    # Define the input and output files.
    # Change these to process different sets of evaluation files (e.g., 5ki, 6ki, 7ki).
    base_file = "./eval/4ki.txt"
    old_file = "./eval/old_4ki.txt"
    output_file = "./eval/new_4ki.txt"
    
    # --- Execution ---
    base_score_data = load_score_file(base_file)
    old_score_data = load_score_file(old_file)
    
    if base_score_data and old_score_data:
        merged_data = merge_and_average_scores(base_score_data, old_score_data)
        save_merged_scores(output_file, merged_data)
        print("\n[+] Score averaging process finished successfully!")
    else:
        print("\n[!] Process aborted due to file loading errors.")


if __name__ == "__main__":
    main()