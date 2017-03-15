# -*- coding: utf-8 -*-
r"""
Scrabble or Words With Friends Solver with graphics support.

Notes
-----
#.  Written by David C. Stauffer in March 2017.
"""

#%% Logging
import logging
logger = logging.getLogger()
logger.setLevel(logging.WARNING)
#logger.setLevel(logging.DEBUG)

#%% Imports
from .classes   import Options
from .constants import MAX_LEN, COLOR, LETTERS, VOWELS, CONSONANTS, BOARD, SCORES, COUNTS, \
                           SMALL_BOARD, SMALL_COUNTS
from .gui       import ScrabbleGui
from .plotting  import plot_board, plot_tile, plot_letter
from .utils     import get_root_dir, get_enable_path, create_dict, count_num_words, find_all_words

#%% Unit Test
if __name__ == '__main__':
    pass
