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
from dstauffman2.games.scrabble.utils import validate_board, validate_move

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

    def make_move(self, move):
        # check if the move is not null
        if not move.word:
            return
        # check if move is valid
        validate_move(self.board, self.played, move)
        # make the move
        word_len = len(move.word)
        if move.dir == 0:
            ix = move.row * (self.num_cols+1) + move.col
            self.played = self.played[:ix] + move.word + self.played[ix+word_len:]
        elif move.dir == 1:
            rows = self.played.split('\n')
            for i in range(word_len):
                r = move.row + i
                rows[r] = rows[r][:move.col] + move.word[i] + rows[r][move.col+1:]
            self.played = '\n'.join(rows)
        else:
            raise ValueError(f'Bad Move direction: {move.dir_}.')

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

    board = Board()
    move = Move('sword', 7, 7, 0, 10)
    board.make_move(move)

    print(board.board)
    print(board.played)
