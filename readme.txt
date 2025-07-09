===========================================================
MIMICKING HUMAN INTUITION IN A CONNECT-4 AI
===========================================================

This project explores the gap between the "optimizing" paradigm of modern superhuman AI and the efficient, heuristic-based problem-solving of humans. It presents two Connect-4 AI agents developed to computationally model distinct human cognitive strategies, grounded in the theoretical frameworks of bounded rationality, problem space theory, and dual-process theory. The agents achieve high performance with exceptional computational efficiency, demonstrating that decision-making patterns similar to human cognition can be powerful and transparent.


--- CORE CONCEPTS ---

This project departs from traditional brute-force AI to explore the efficiency of human cognitive shortcuts. Instead of finding the mathematically *optimal* move, these agents are designed to find a *"good enough"* move quickly, a strategy known as *satisficing*. The entire system is designed as a computational experiment in cognitive science.


--- THE COGNITIVE AGENTS ---

Two distinct agents were designed to model different aspects of human thought.

1. The Rule-Based Agent (`Rule.py`)
------------------------------------
This agent computationally models the explicit, conscious strategies a human player might use. It doesn't perform a deep search; instead, it scores each possible move based on a set of codified heuristics.

Key Modeled Heuristics:

Rule Implemented         Score      Cognitive Interpretation
------------------------   --------   ------------------------------------------------------------
Immediate Win              +10000     Seeking victory, the primary goal.
Block Opponent's Win       +10001     *Loss Aversion*; the fear of losing is slightly stronger
                                    than the desire to win.
Create Open Three          +5000      Recognizing and creating powerful, game-deciding threats.
Block Open Three           +5001      Defensive pattern recognition.
Avoid Traps                -10000     *Negative Insight*; intuitively avoiding fatal mistakes.
Default Move               Centered   The common beginner's heuristic that center control is
                                    advantageous.


2. The Heuristic-Enhanced Search Agent
---------------------------------------
This agent is a hybrid model designed as a computational implementation of *Dual-Process Theory*, which posits that human thought arises from the interplay of two systems.

  System 1: Fast, Intuitive Judgment (`heuristic.py`)
  This is the agent's intuition. It uses fast, pattern-matching functions to immediately spot critical situations without needing a deep search.
    - `attack_critical_choice()`: Finds a move that results in an immediate win (a positive "Aha!" insight).
    - `protect_critical_choice()`: Finds a move that is essential to block an opponent's win (a negative "Uh-oh!" insight).
  If this system finds a decisive move, it *overrides* the analytical engine and executes the move immediately, mirroring how human intuition can override deliberation.

  System 2: Slow, Analytical Search (`minmax_d6_agent.py`)
  This is the agent's deep, analytical thought process. It is only activated when the intuitive System 1 finds no immediate critical moves. It exhibits all the characteristics of analytical thought:
    - *Slow and Expensive:* It uses a Minimax search with Alpha-Beta Pruning to explore the game tree.
    - *Hypothetical Thinking:* It simulates future move sequences to find the best outcome.
    - *High Working Memory Load:* It requires storing the search path and node scores, analogous to human concentration.


--- PROJECT ARCHITECTURE ---

File                  Description
--------------------  --------------------------------------------------------------------
`Run_Agent.py`          >> Main entry point. Run this file to start the game.

`minmax_d6_agent.py`    >> The Analytical Engine (System 2). Contains the Minimax
                         search, alpha-beta pruning, and the evaluation function.

`heuristic.py`          >> The Intuitive Module (System 1). Contains `attack_critical_choice`
                         and `protect_critical_choice` for detecting immediate
                         win/loss states.

`Rule.py`               >> The complete Rule-Based Agent. A self-contained AI that
                         operates on explicit, conscious rules.

`connect4_utils.py`     >> Game Utilities. Provides helper functions for displaying
                         the board, checking for a winner, and processing user input.

`eval/`                 >> Evaluation Knowledge Base. Contains text files with
                         pre-calculated scores for thousands of line patterns.

`convert_score.py`      >> Score File Utility. A script used to enhance the evaluation
                         tables by adding threat-potential scores.

`mean_eval.py`          >> Score File Utility. A script to average two different
                         score files, useful for blending evaluation models.


--- GETTING STARTED ---

Prerequisites
- Python 3.x

Installation
Clone the repository to your local machine:
  git clone https://github.com/glofiniteJun/Connect4-Cognitive-Agent.git
  cd Connect4

Running the Game
Execute the main agent file from your terminal:
  python3 Run_Agent.py

You will be prompted to play first or second. On the AI's turn, you will be asked to select which cognitive model (`Heuristic Search` or `Rule-Based`) you want it to use for its move.


--- A NOTE ON EXPLAINABLE AI (XAI) ---

A significant advantage of this cognitive modeling approach is its contribution to *Explainable AI (XAI)*. Unlike "black box" models, this agent's decisions are transparent and interpretable because they are analogous to human thought processes.

- The *Rule-Based Agent* can explain its move by pointing to a specific rule (e.g., "I chose column 6 because it scored 10001 points for blocking your threat").
- The *Heuristic-Enhanced Agent* can state whether its decision was an "intuitive" one or an "analytical" one (e.g., "I made this move instantly because I detected a winning pattern" or "I found no immediate threats, so I performed a deep search").
