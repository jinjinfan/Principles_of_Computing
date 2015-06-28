"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 5         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
    
# Add your functions here.
def mc_trial(board, player):
    """
    This function plays a game starting with the given player by making 
    random moves, alternating between players until the game is over
    """
    player_tmp = player
    winner = None
    # game is in progress
    while winner == None:
        empty = board.get_empty_squares()
        row, col = random.choice(empty)
        board.move(row, col, player_tmp)
        winner = board.check_win()
        player_tmp = provided.switch_player(player_tmp)

def mc_update_scores(scores, board, player):
    """
    This function scores the completed board and updates the scores grid
    """
    # get the winner player
    winner = board.check_win()
    # get board dim 
    dim = board.get_dim()
    # when DRAW, no need to calculate score
    if winner == provided.DRAW:
        return
    else:
        player_loss = winner
        player_loss = provided.switch_player(player_loss)
        for row in range(dim):
            for col in range(dim):
                if board.square(row, col) == winner:
                    scores[row][col] += 1
                if board.square(row, col) == player_loss:
                    scores[row][col] -= 1

def get_best_move(board, scores):
    """
    This function finds all of the empty squares with the maximum score and 
    randomly return one of them.
    """
    # get the mininum score from scores
    dim = board.get_dim()
    min_score = 0
    for row in range(dim):
        for col in range(dim):
            if scores[row][col] < min_score:
                min_score = scores[row][col]
    # get all possible empty board
    empty_squares = board.get_empty_squares()
    # find the maximun score
    max_score = min_score
    best_moves = []
    for (row, col) in empty_squares:
        if scores[row][col] > max_score:
            max_score = scores[row][col]
    # get the best move lists
    for (row, col) in empty_squares:
        if scores[row][col] == max_score:
            best_moves.append((row, col))
    return random.choice(best_moves)
               
def mc_move(board, player, trials):
    """
    This function uses the Monte Carlo simulation to return a move for 
    the machine player.
    """
    # set the score
    score_dim = board.get_dim()
    board_for_trial = board.clone()
    scores = [[0 for dummycol in range(score_dim)] 
                 for dummyrow in range(score_dim)]
    for dummy in range(trials):
        board_for_trial = board.clone()
        # play an entire game on this board by just randomly 
        # choosing a move for each player
        mc_trial(board_for_trial, player)
        # score the resulting board
        mc_update_scores(scores, board_for_trial, player)
 
    # when an empty square existes in the current board
    if len(board.get_empty_squares()) != 0:
        return get_best_move(board, scores)
        
# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

#provided.play_game(mc_move, NTRIALS, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)

