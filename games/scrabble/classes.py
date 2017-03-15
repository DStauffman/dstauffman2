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

#%% Options
class Options(Frozen):
    pass

#%% Unit Test
if __name__ == '__main__':
    unittest.main(module='dstauffman2.games.scrabble.tests.test_classes', exit=False)
    doctest.testmod(verbose=False)
