r"""
Scrabble or Words With Friends Solver with graphics support.

Notes
-----
#.  Written by David C. Stauffer in March 2017.
"""

# %% Logging
import logging

logger = logging.getLogger()
logger.setLevel(logging.WARNING)
# logger.setLevel(logging.DEBUG)

# %% Imports
# fmt: off
from .classes   import Board, Move
from .constants import LETTERS, VOWELS, CONSONANTS, WWF_SCORES, SCRAB_SCORES, WWF_COUNTS, \
                           WWF_SMALL_COUNTS, SCRAB_COUNTS, COLOR, MAX_LEN, BOARD_SYMBOLS, \
                           WWF_BOARD, WWF_SMALL_BOARD, SCRAB_BOARD, BOARD, SCORES, COUNTS, DICT
from .gui       import GuiSettings, ScrabbleGui
from .plotting  import plot_board, plot_tile, plot_letter, plot_draw_stats, plot_move_strength, \
                           display_tile_bag
from .special   import find_all, find_all_two_letter_words, find_all_three_letter_words, \
                           find_all_four_letter_words, find_all_consonant_words, \
                           find_all_one_vowel_words, find_all_one_consonant_words, \
                           find_all_vowel_words, find_all_q_without_u_words, \
                           find_starting_with_de, find_starting_with_re, find_starting_with_un, \
                           find_starting_with_x, find_ending_with_est, find_ending_with_iest, \
                           find_ending_with_ing, find_ending_with_j, find_ending_with_ness, \
                           find_ending_with_q, find_ending_with_ted, find_ending_with_u, \
                           find_ending_with_v, find_ending_with_x, find_ending_with_z
from .utils     import get_root_dir, get_dict_path, get_raw_dictionary, create_dict, \
                           count_num_words, find_all_words, validate_board, validate_move, \
                           score_move, get_board_played, get_board_open, get_board_must_play
# fmt: on

# %% Unit Test
if __name__ == "__main__":
    pass
