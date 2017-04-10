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

#%% Letters
# all possible letters
LETTERS = frozenset('abcdefghijklmnopqrstuvwxyz?')
# all vowels
VOWELS  = frozenset('aeiou')
# all consonants
CONSONANTS = frozenset(LETTERS - VOWELS - {'?'})

#%% Letter values
WWF_SCORES = {'a': 1, 'b': 4, 'c': 4, 'd': 2, 'e': 1, 'f': 4, 'g': 3, 'h': 3, 'i': 1, 'j': 10, \
          'k': 5, 'l': 2, 'm': 4, 'n': 2, 'o': 1, 'p': 4, 'q': 10, 'r': 1, 's': 1, 't': 1, \
          'u': 2, 'v': 5, 'w': 4, 'x': 8, 'y': 3, 'z': 10, '?': 0}
SCRAB_SCORES = {}

#%% Tile counts
WWF_COUNTS = {'a': 9, 'b': 2, 'c': 2, 'd': 5, 'e': 13, 'f': 2, 'g': 3, 'h': 4, 'i': 8, 'j': 1, \
          'k': 1, 'l': 4, 'm': 2, 'n': 5, 'o': 8, 'p': 2, 'q': 1, 'r': 6, 's': 5, 't': 7, \
          'u': 4, 'v': 2, 'w': 2, 'x': 1, 'y': 2, 'z': 1, '?': 2}
# TODO: update these smaller counts
WWF_SMALL_COUNTS = {'a': 9, 'b': 2, 'c': 2, 'd': 5, 'e': 13, 'f': 2, 'g': 3, 'h': 4, 'i': 8, 'j': 1, \
          'k': 1, 'l': 4, 'm': 2, 'n': 5, 'o': 8, 'p': 2, 'q': 1, 'r': 6, 's': 5, 't': 7, \
          'u': 4, 'v': 2, 'w': 2, 'x': 1, 'y': 2, 'z': 1, '?': 2}
SCRAB_COUNTS = {}

#%% color definitions
COLOR          = {}
COLOR['board'] = (0.5, 0.5, 1.0)
COLOR['edge']  = (0.0, 0.0, 0.0)
COLOR['tile']  = ()
COLOR['.']     = ()
COLOR['d']     = ()
COLOR['s']     = ()
COLOR['t']     = ()
COLOR['D']     = ()
COLOR['T']     = ()

#%% Board layouts
MAX_LEN = 15
BOARD_SYMBOLS = frozenset('.dstDT\n')

# Board Layout
WWF_BOARD = r"""
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

# Smaller board layout
WWF_SMALL_BOARD = r"""
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

SCRAB_BOARD = r"""
""".strip()

#%% Defaults
BOARD  = WWF_BOARD
SCORES = WWF_SCORES
COUNTS = WWF_COUNTS
DICT   = 'wwf_v4.0_master.txt'

#%% Unit Test
if __name__ == '__main__':
    unittest.main(module='dstauffman2.games.scrabble.tests.test_constants', exit=False)
    doctest.testmod(verbose=False)
