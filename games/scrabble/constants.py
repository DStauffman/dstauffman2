# -*- coding: utf-8 -*-
r"""
Constants module file for the "scrabble" game.  It defines constants.

Notes
-----
#.  Written by David C. Stauffer in March 2017.
"""

#%% Imports
import doctest
import unittest

#%% Constants
MAX_LEN = 15

# color definitions
COLOR             = {}
COLOR['board']    = (0.5, 0.5, 1.0)
COLOR['edge']     = (0.0, 0.0, 0.0)

# all possible letters
LETTERS = frozenset('abcdefghijklmnopqrstuvwxyz?')

VOWELS  = frozenset('aeiou')

CONSONANTS = frozenset(LETTERS - VOWELS - {'?'})

BOARD_SYMBOLS = frozenset('.dstDT\n')

# Board Layout
BOARD = r"""
...T..t.t..T...
..d..D...D..d..
.d..d.....d..d.
T..t...D...t..T
..d...d.d...d..
.D...d...d...D.
t...D.....D...t
...D...s...D...
t...D.....D...t
.D...d...d...D.
..d...d.d...d..
T..t...D...t..T
.d..d.....d..d.
..d..D...D..d..
...T..t.t..T...
""".strip()

# Letter values
SCORES = {'a': 1, 'b': 4, 'c': 4, 'd': 2, 'e': 1, 'f': 4, 'g': 3, 'h': 3, 'i': 1, 'j': 10, \
          'k': 5, 'l': 2, 'm': 4, 'n': 2, 'o': 1, 'p': 4, 'q': 10, 'r': 1, 's': 1, 't': 1, \
          'u': 2, 'v': 5, 'w': 4, 'x': 8, 'y': 3, 'z': 10, '?': 0}

# Tile counts
COUNTS = {'a': 9, 'b': 2, 'c': 2, 'd': 5, 'e': 13, 'f': 2, 'g': 3, 'h': 4, 'i': 8, 'j': 1, \
          'k': 1, 'l': 4, 'm': 2, 'n': 5, 'o': 8, 'p': 2, 'q': 1, 'r': 6, 's': 5, 't': 7, \
          'u': 4, 'v': 2, 'w': 2, 'x': 1, 'y': 2, 'z': 1, '?': 2}

# Smaller board layout
SMALL_BOARD = r"""
t.T.....T.t
.D...D...D.
T.d.d.d.d.T
...t...t...
..d.....d..
.D...s...D.
..d.....d..
...t...t...
T.d.d.d.d.T
.D...D...D.
t.T.....T.t
""".strip()

# TODO: update these smaller counts
SMALL_COUNTS = {'a': 9, 'b': 2, 'c': 2, 'd': 5, 'e': 13, 'f': 2, 'g': 3, 'h': 4, 'i': 8, 'j': 1, \
          'k': 1, 'l': 4, 'm': 2, 'n': 5, 'o': 8, 'p': 2, 'q': 1, 'r': 6, 's': 5, 't': 7, \
          'u': 4, 'v': 2, 'w': 2, 'x': 1, 'y': 2, 'z': 1, '?': 2}

#%% Unit Test
if __name__ == '__main__':
    unittest.main(module='dstauffman2.games.scrabble.tests.test_constants', exit=False)
    doctest.testmod(verbose=False)
