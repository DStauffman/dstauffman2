r"""
Utils module file for the "tictactoe" game.  It defines the generic utility functions.

Notes
-----
#.  Written by David C. Stauffer in January 2016.
"""

# %% Imports
import doctest
import logging
import os
import unittest

import numpy as np

from dstauffman2 import get_root_dir as dcs_root_dir
from dstauffman2.games.tictactoe.classes import Move, Options
from dstauffman2.games.tictactoe.constants import COLOR, PLAYER, SCORING, SIZES, WIN
from dstauffman2.games.tictactoe.plotting import plot_piece

# %% Option instance
OPTS = Options()


# %% get_root_dir
def get_root_dir():
    r"""
    Gets the full path to the root directory of the tictactoe game.

    Returns
    -------
    folder : str
        Path to the tictactoe root folder

    Examples
    --------
    >>> from dstauffman2.games.tictactoe import get_root_dir
    >>> folder = get_root_dir()

    """
    folder = os.path.join(dcs_root_dir(), "games", "tictactoe")
    return folder


# %% calc_cur_move
def calc_cur_move(cur_move, cur_game):
    r"""
    Calculates whose move it is based on the turn and game number.

    Parameters
    ----------
    cur_move : int
        Current move number
    cur_game : int
        Current game number

    Returns
    -------
    move : int
        Current move, from {1=o, -1=x}

    Examples
    --------
    >>> from dstauffman2.games.tictactoe import calc_cur_move
    >>> move = calc_cur_move(0, 0)
    >>> print(move)
    1

    """
    if np.mod(cur_move + cur_game, 2) == 0:
        move = PLAYER["o"]
    else:
        move = PLAYER["x"]
    return move


# %% check_for_win
def check_for_win(board):
    r"""
    Checks for a win.

    Parameters
    ----------
    board : 2D int ndarray
        Board position

    Examples
    --------
    >>> from dstauffman2.games.tictactoe import check_for_win, PLAYER
    >>> import numpy as np
    >>> board = np.full((3, 3), PLAYER['none'], dtype=int)
    >>> board[0:3, 0] = PLAYER['x']
    >>> board[1:3, 1] = PLAYER['o']
    >>> (winner, win_mask) = check_for_win(board)
    >>> print(winner)
    -1

    >>> print(win_mask)
    [[ True False False]
     [ True False False]
     [ True False False]]

    """
    # find wins
    o = np.flatnonzero(np.sum(np.expand_dims(board.ravel() == PLAYER["o"], axis=1) * WIN, axis=0) == 3)
    x = np.flatnonzero(np.sum(np.expand_dims(board.ravel() == PLAYER["x"], axis=1) * WIN, axis=0) == 3)

    # determine winner
    if len(o) == 0:
        if len(x) == 0:
            winner = PLAYER["none"]
        else:
            winner = PLAYER["x"]
    else:
        if len(x) == 0:
            winner = PLAYER["o"]
        else:
            winner = PLAYER["draw"]

    # check for a full game board after determining no other win was found
    if winner == PLAYER["none"] and not np.any(board == PLAYER["none"]):
        winner = PLAYER["draw"]

    # find winning pieces on the board
    if winner == PLAYER["none"]:
        win_mask = np.zeros((3, 3), dtype=bool)
    else:
        logging.debug('Win detected.  Winner is {}.'.format(list(PLAYER)[list(PLAYER.values()).index(winner)]))
        win_mask = np.reshape(np.sum(WIN[:, x], axis=1) + np.sum(WIN[:, o], axis=1), (SIZES['board'], SIZES['board'])) != 0

    return (winner, win_mask)


# %% find_moves
def find_moves(board):
    r"""
    Finds the best current move.

    Parameters
    ----------
    board : 2D int ndarray
        Board position

    Examples
    --------
    >>> from dstauffman2.games.tictactoe import find_moves, PLAYER, SIZES
    >>> import numpy as np
    >>> board = np.full((SIZES['board'], SIZES['board']), PLAYER['none'], dtype=int)
    >>> board[0, 0] = PLAYER['o']
    >>> board[0, 1] = PLAYER['o']
    >>> board[1, 1] = PLAYER['o']
    >>> (o_moves, x_moves) = find_moves(board)

    """

    def calculate_move_score(wins, block_wins, win_in_2, block_in_2, lines, block_lines):
        r"""Calculates the numeric value for the current move."""
        if this_move in wins:
            score = SCORING["win"]
        elif this_move in block_wins:
            score = SCORING["block_win"]
        elif this_move in win_in_2:
            score = SCORING["win_in_two"]
        elif this_move in block_in_2:
            score = SCORING["block_in_two"]
        else:
            score = SCORING["normal_line"] * lines + SCORING["block_line"] * block_lines
        return score

    # calculate the number of total squares
    num_pieces = SIZES["board"] * SIZES["board"]

    # find all the available moves
    open_moves = np.arange(num_pieces)[board.ravel() == PLAYER["none"]]

    # check that there are at least some available moves
    assert len(open_moves) > 0, "At least one move must be available."

    # expand the board to a linear 2D matrix
    big_board = np.expand_dims(board.ravel(), axis=1)

    # correlate the boards to the winning positions
    test = big_board * WIN

    # find the scores
    score = np.sum(test, axis=0)

    # test for already winning positions that shouldn't exist
    if np.any(np.abs(score) >= 3):
        raise ValueError("Board should not already be in a winning position.")

    # find the remaining possible wins
    rem_o_wins = WIN[:, np.sum((big_board == PLAYER["x"]) * WIN, axis=0) == 0]
    rem_x_wins = WIN[:, np.sum((big_board == PLAYER["o"]) * WIN, axis=0) == 0]

    # calculate a score for each possible move
    o_scores = np.sum(rem_o_wins, axis=1)
    x_scores = np.sum(rem_x_wins, axis=1)

    # find win in one moves
    o_win_in_one = rem_o_wins[:, np.sum(big_board * rem_o_wins, axis=0) == 2]
    x_win_in_one = rem_x_wins[:, np.sum(big_board * rem_x_wins, axis=0) == -2]
    o_pos = np.logical_and(np.logical_xor(np.abs(big_board), o_win_in_one), o_win_in_one)
    x_pos = np.logical_and(np.logical_xor(np.abs(big_board), x_win_in_one), x_win_in_one)
    o_win = np.flatnonzero(o_pos)
    x_win = np.flatnonzero(x_pos)

    # find win in two moves
    o_win_in_two = np.flatnonzero(np.sum(rem_o_wins[:, np.sum(big_board * rem_o_wins, axis=0) == 1], axis=1) > 1)
    x_win_in_two = np.flatnonzero(np.sum(rem_x_wins[:, np.sum(big_board * rem_x_wins, axis=0) == -1], axis=1) > 1)

    # create the list of moves and incorporate the score
    o_moves = []
    x_moves = []
    for this_move in open_moves:
        row     = this_move // SIZES['board']
        column  = np.mod(this_move, SIZES['board'])
        o_score = calculate_move_score(o_win, x_win, o_win_in_two, x_win_in_two, o_scores[this_move], x_scores[this_move])
        x_score = calculate_move_score(x_win, o_win, x_win_in_two, o_win_in_two, x_scores[this_move], o_scores[this_move])
        o_moves.append(Move(row, column, o_score))
        x_moves.append(Move(row, column, x_score))

    # sort by best moves
    o_moves.sort(reverse=True)
    x_moves.sort(reverse=True)
    return (o_moves, x_moves)


# %% make_move
def make_move(ax, board, x, y, cur_move, cur_game, game_hist):
    r"""
    Does the actual move.

    Parameters
    ----------
    ax : object
        Axis to plot on
    board : 2D int ndarray
        Board position
    x : float
        X-axis (board row)
    y : float
        Y-axis (board column)
    cur_move : int
        Current move number
    cur_game : int
        Current game number
    game_hist : list of class GameStats
        Game history of statistics for each game

    Notes
    -----
    #.  Modifies `board`, `cur_move` and `game_hist` in-place.

    Examples
    --------
    >>> from dstauffman2.games.tictactoe import make_move, PLAYER, GameStats
    >>> from dstauffman import Counter
    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> plt.ioff()
    >>> fig = plt.figure()
    >>> ax = fig.add_subplot(111)
    >>> _ = ax.set_xlim(-0.5, 2.5)
    >>> _ = ax.set_ylim(-0.5, 2.5)
    >>> ax.invert_yaxis()
    >>> board = np.full((3, 3), PLAYER['none'], dtype=int)
    >>> x = 1
    >>> y = 0
    >>> cur_move = Counter(0)
    >>> cur_game = Counter(0)
    >>> game_hist = [GameStats(1, PLAYER['o'])]
    >>> make_move(ax, board, x, y, cur_move, cur_game, game_hist)

    >>> print(board)
    [[0 0 0]
     [1 0 0]
     [0 0 0]]

    >>> print(cur_move)
    1

    >>> print(game_hist[0].move_list)
    [<row: 1, col: 0, pwr: None>]

    >>> plt.close(fig)

    """
    logging.debug("Placing current piece.")
    current_player = calc_cur_move(cur_move, cur_game)
    # update board position
    board[x, y] = current_player
    # plot the piece
    if current_player == PLAYER["o"]:
        piece = plot_piece(ax, x, y, SIZES["piece"], COLOR["o"], PLAYER["o"])
    elif current_player == PLAYER["x"]:
        piece = plot_piece(ax, x, y, SIZES["piece"], COLOR["x"], PLAYER["x"])
    else:
        raise ValueError("Unexpected player to move next.")  # pragma: no cover
    assert piece
    # increment move list
    assert game_hist[cur_game].num_moves >= cur_move, "Number of moves = {}, Current Move = {}".format(
        game_hist[cur_game].num_moves, cur_move
    )
    this_move = Move(x, y)
    if game_hist[cur_game].num_moves == cur_move:
        game_hist[cur_game].add_move(this_move)
    else:
        game_hist[cur_game].move_list[cur_move] = this_move
        game_hist[cur_game].remove_moves(cur_move + 1)
    # increment current move
    cur_move += 1


# %% play_ai_game
def play_ai_game(ax, board, cur_move, cur_game, game_hist):
    r"""
    Computer AI based play.

    Parameters
    ----------
    ax : object
        Axis to plot on
    board : 2D int ndarray
        Board position
    cur_move : int
        Current move number
    cur_game : int
        Current game number
    game_hist : list of class GameStats
        Game history of statistics for each game

    Notes
    -----
    #.  Modifies `board`, `cur_move` and `game_hist` in-place.

    Examples
    --------
    >>> from dstauffman2.games.tictactoe import play_ai_game, PLAYER, GameStats, Options
    >>> from dstauffman import Counter
    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> plt.ioff()
    >>> fig = plt.figure()
    >>> ax = fig.add_subplot(111)
    >>> _ = ax.set_xlim(-0.5, 2.5)
    >>> _ = ax.set_ylim(-0.5, 2.5)
    >>> ax.invert_yaxis()
    >>> board = np.full((3, 3), PLAYER['none'], dtype=int)
    >>> cur_move = Counter(0)
    >>> cur_game = Counter(0)
    >>> game_hist = [GameStats(1, PLAYER['o'])]
    >>> Options.o_is_computer = True
    >>> Options.x_is_computer = True
    >>> play_ai_game(ax, board, cur_move, cur_game, game_hist) # doesn't play move as it's not the computers turn

    >>> print(board)
    [[0 0 0]
     [0 1 0]
     [0 0 0]]

    >>> print(cur_move)
    1

    >>> print(game_hist[0].move_list)
    [<row: 1, col: 1, pwr: None>]

    >>> plt.close(fig)

    """
    current_player = calc_cur_move(cur_move, cur_game)
    if current_player == PLAYER["o"] and OPTS.o_is_computer:
        (moves, _) = find_moves(board)
    elif current_player == PLAYER["x"] and OPTS.x_is_computer:
        (_, moves) = find_moves(board)
    else:
        return
    this_move = moves[0]
    # potentially pick another equivalent move
    for next_move in moves[1:]:
        if next_move.power == this_move.power:
            if np.random.rand() < 0.5:
                this_move = next_move
    make_move(ax, board, this_move.row, this_move.column, cur_move, cur_game, game_hist)


# %% create_board_from_moves
def create_board_from_moves(moves, first_player):
    r"""
    Recreates a board from a move history.

    Parameters
    ----------
    moves : list of class Move
        Move list
    first_player : int
        First player to move

    Returns
    -------
    board : 2D int ndarray
        Board position

    Examples
    --------
    >>> from dstauffman2.games.tictactoe import create_board_from_moves, Move, PLAYER
    >>> moves = [Move(0, 0), Move(1, 1), Move(2, 2)]
    >>> first_player = PLAYER['x']
    >>> board = create_board_from_moves(moves, first_player)
    >>> print(board)
    [[-1  0  0]
     [ 0  1  0]
     [ 0  0 -1]]

    """
    # make sure the first player is valid
    assert first_player == PLAYER["x"] or first_player == PLAYER["o"]
    # create the initial board
    board = np.full((SIZES["board"], SIZES["board"]), PLAYER["none"], dtype=int)
    # alias this player
    this_player = first_player
    # loop through the move history
    for this_move in moves:
        # check that square is empty
        assert board[this_move.row, this_move.column] == PLAYER["none"], "Invalid move encountered."
        # place the piece
        board[this_move.row, this_move.column] = this_player
        # update the next player to move
        this_player = PLAYER["x"] if this_player == PLAYER["o"] else PLAYER["o"]
    return board


# %% Unit test
if __name__ == "__main__":
    unittest.main(module="dstauffman2.games.tictactoe.tests.test_utils", exit=False)
    doctest.testmod(verbose=False)
