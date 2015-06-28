"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided
import time
# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    move_results = []
    board_clone = board.clone()
    empty_squares = board_clone.get_empty_squares()
    for move_ in empty_squares: 
        board_clone1 = board_clone.clone()
        board_clone1.move(move_[0],move_[1],player)
        if board_clone1.check_win()!= None:
            # if find the maximum score(1), directly return position
            if SCORES[board_clone1.check_win()] * SCORES[player] ==1:
                return SCORES[board_clone1.check_win()],move_
            # else save the result for further comparaision
            else:
                if move_results == [] or SCORES[board_clone1.check_win()]* SCORES[player] > move_results[0]*SCORES[player]: 
                    move_results = SCORES[board_clone1.check_win()], move_
                continue;
        else:
            moves = mm_move(board_clone1, provided.switch_player(player))
            # if find the maximum score(1), directly return position
            if moves[0] * SCORES[player] ==1:
                return moves[0], move_
            # else save the result for further comparaision
            else:
                if move_results == [] or moves[0]* SCORES[player] > move_results[0]*SCORES[player]: 
                    move_results = moves[0], move_
                continue
    # compare all the result, return the one with the maximun score
    return move_results[0],move_results[1]

def convert_board(board,player,board_dim):
    board_string = ""
    empty_num = 0
    for row in range(board_dim):
        for col in range(board_dim):
            if board.square(row, col) == provided.EMPTY:
                empty_num += 1
                board_string += "0"
            elif board.square(row, col) == provided.PLAYERX: 
                board_string += "1"
            elif board.square(row, col) == provided.PLAYERO:
                board_string += "2"
    if player == provided.PLAYERX:
        board_string += "2"
    elif player == provided.PLAYERO: 
        board_string += "3"
    return board_string, empty_num

def memory_mm_move(board, player, mem_dict):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    move_results = []
    board_dim = board.get_dim()
    board_str, empty_num = convert_board(board,player, board_dim)
    if empty_num >= board_dim:
        if board_str in mem_dict.keys():
            return mem_dict[board_str]
    board_clone = board.clone()
    empty_squares = board_clone.get_empty_squares()
    for move_ in empty_squares: 
        board_clone1 = board_clone.clone()
        board_clone1.move(move_[0],move_[1],player)
        if board_clone1.check_win()!= None:
            # if find the maximum score(1), directly return position
            if SCORES[board_clone1.check_win()] * SCORES[player] ==1:
                if empty_num >= board_dim:
                    mem_dict[board_str] = SCORES[board_clone1.check_win()],move_
                return SCORES[board_clone1.check_win()],move_
            # else save the result for further comparaision
            else:
                if move_results == [] or SCORES[board_clone1.check_win()]* SCORES[player] > move_results[0]*SCORES[player]: 
                    move_results = SCORES[board_clone1.check_win()], move_
                continue;
        else:
            moves = memory_mm_move(board_clone1, provided.switch_player(player), mem_dict)
            # if find the maximum score(1), directly return position
            if moves[0] * SCORES[player] ==1:
                if empty_num >= board_dim:
                    mem_dict[board_str] = moves[0], move_
                return moves[0], move_
            # else save the result for further comparaision
            else:
                if move_results == [] or moves[0]* SCORES[player] > move_results[0]*SCORES[player]: 
                    move_results = moves[0], move_
                continue
    if empty_num >= board_dim:
        mem_dict[board_str] = move_results
    # compare all the result, return the one with the maximun score
    return move_results[0],move_results[1]

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    #move = mm_move(board, player)
    move = memory_mm_move(board, player,{})
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

#board = provided.TTTBoard(3, False, [[provided.PLAYERO, provided.PLAYERX,provided.EMPTY], [provided.PLAYERO, provided.PLAYERX,provided.EMPTY],[provided.PLAYERX, provided.PLAYERO, provided.PLAYERX]])
#print str(board)
# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.
#
time1 = time.time()
provided.play_game(move_wrapper, 1, False)
time2 = time.time()
print time2-time1
#poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)


