# -*- coding: utf-8 -*-
r"""
Classes module file for the "scrabble" game.  It defines the classes used by the rest of the game.

Notes
-----
#.  Written by David C. Stauffer in March 2017.
"""

#%% Imports
import doctest
import unittest
from dstauffman import Frozen
from dstauffman2.games.scrabble.constants import BOARD
from dstauffman2.games.scrabble.utils     import validate_board

#%% Options
class Options(Frozen):
    pass

#%% Board
class Board(Frozen):
    r"""
    Class that holds the board.
    """
    def __init__(self, board=BOARD, played=None):
        (num_rows, num_cols) = validate_board(board)
        self.board    = board
        self.num_rows = num_rows
        self.num_cols = num_cols
        if played is None:
            self.played =  (' ' * num_cols + '\n') * num_rows
        else:
            self.played = played

#%% Move
class Move(Frozen):
    r"""
    Class that contains an individual move.
    """
    def __init__(self, word='', row=0, col=0, dir_=0, score=0):
        self.word  = word
        self.row   = row
        self.col   = col
        self.dir   = dir_
        self.score = score

#%% Unit Test
if __name__ == '__main__':
    unittest.main(module='dstauffman2.games.scrabble.tests.test_classes', exit=False)
    doctest.testmod(verbose=False)
