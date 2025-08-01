r"""
Utils module file for the "scrabble" game.  It defines the generic utility functions.

Notes
-----
#.  Written by David C. Stauffer in March 2017.

"""

# %% Imports
from collections import defaultdict
import doctest
import itertools
import os
import re
import unittest

from dstauffman2 import get_data_dir as dcs_data_dir, get_root_dir as dcs_root_dir
from dstauffman2.games.scrabble.constants import BOARD_SYMBOLS, DICT, LETTERS


# %% get_root_dir
def get_root_dir():
    r"""
    Gets the full path to the root directory of the scrabble game.

    Returns
    -------
    folder : str
        Path to the scrabble root folder

    Examples
    --------
    >>> from dstauffman2.games.scrabble import get_root_dir
    >>> folder = get_root_dir()

    """
    folder = os.path.join(dcs_root_dir(), "games", "scrabble")
    return folder


# %% get_data_dir
get_data_dir = dcs_data_dir  # TODO: override docstring?


# %% get_dict_path
def get_dict_path(name=DICT):
    r"""
    Gets the full path to the specified or default dictionary.

    Parameters
    ----------
    name : str, optional
        Name of the dictionary to load from the data folder

    Returns
    -------
    path : str
        Full path to the word list

    Examples
    --------
    >>> from dstauffman2.games.scrabble import get_dict_path
    >>> path = get_dict_path()
    >>> print(path) # doctest: +SKIP

    >>> path2 = get_dict_path('sowpods.txt')
    >>> print(path2) # doctest: +SKIP

    """
    path = os.path.join(get_data_dir(), name)
    return path


# %% get_raw_dictionary
def get_raw_dictionary(filename=None, min_len=2, max_len=20):
    r"""
    Loads the entire dictionary into a Python set.

    Parameters
    ----------
    filename : str, optional
        Full path to the desired word list
    min_len : int, optional
        Minimum length of word to include
    max_len : int, optional
        Maximum length of word to include

    Returns
    -------
    words : set
        List of all valid words as a Python set

    Notes
    -----
    #.  This function returns the list of words as a set, which can sometimes be convenient,
        although the anagram solver instead uses the form where each key is a sorted version of the
        letters that form those words.

    Examples
    --------
    >>> from dstauffman2.games.scrabble import get_raw_dictionary
    >>> words = get_raw_dictionary()
    >>> assert isinstance(words, set)
    >>> print(len(words))
    173003

    >>> words2 = get_raw_dictionary(min_len=0, max_len=10000)
    >>> print(len(words2))
    173122

    >>> min_len_word = min(len(x) for x in words2)
    >>> print(min_len_word)
    2

    >>> max_len_word = max(len(x) for x in words2)
    >>> print(max_len_word)
    28

    """
    if filename is None:
        filename = get_dict_path()
    words = set()
    with open(filename, "rt") as file:
        for line in file:
            word = line.rstrip("\n")
            if min_len <= len(word) <= max_len:
                words.add(word)
    return words


# %% create_dictionary_from_text
def create_dict(filename, min_len=2, max_len=20):
    r"""
    Reads in the word list and creates a Python words dictionary by anagrammed keys.

    Parameters
    ----------
    filename : str, optional
        Full path to the desired word list
    min_len : int, optional
        Minimum length of word to include
    max_len : int, optional
        Maximum length of word to include

    Returns
    -------
    words : dict
        Dictionary of words by sorted, anagrammed keys

    Notes
    -----
    #.  The input data file has one word per line with no defaults and all lowercase letters.
    #.  The output is a dict with keys being the sorted list of characters, and the values a list
        of all possible words based on those characters.

    Examples
    --------
    >>> from dstauffman2 import get_data_dir
    >>> from dstauffman2.games.scrabble import create_dict, get_dict_path
    >>> filename = get_dict_path()
    >>> words = create_dict(filename)
    >>> print(len(words))
    156532

    """
    raw_words = get_raw_dictionary(filename)
    words = defaultdict(list)
    for word in raw_words:
        if len(set(word) - LETTERS) == 0 and len(word) >= min_len and len(word) <= max_len:
            key = "".join(sorted(word))
            words[key].append(word)
    return dict(words)


# %% count_num_words
def count_num_words(words):
    r"""
    Counts the number of keys, words, and words by length in the dictionary.

    Parameters
    ----------
    words : dict
        Dictionary of words by sorted, anagrammed keys

    Returns
    -------
    num_keys : int
        Number of keys in the dictionary
    num_words : int
        Number of words in the dictionary, since keys can have more than one word
    len_count : dict
        Dictionary of number of words by word length, which are the keys

    Examples
    --------
    >>> from dstauffman2 import get_data_dir
    >>> from dstauffman2.games.scrabble import create_dict, get_dict_path, count_num_words
    >>> filename = get_dict_path()
    >>> words = create_dict(filename)
    >>> (num_keys, num_words, len_count) = count_num_words(words)
    >>> print(num_keys)
    156532

    >>> print(num_words)
    173003

    >>> print(sorted(len_count.keys()))
    [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

    >>> assert sum(len_count[key] for key in len_count) == num_words

    """
    num_keys   = 0
    num_words  = 0
    temp_count = defaultdict(int)
    for key, value in words.items():
        new_words = len(value)
        num_keys += 1
        num_words += new_words
        len_key = len(key)
        temp_count[len_key] += new_words
    # reorganize dictionary
    len_count = {key: temp_count[key] for key in sorted(temp_count.keys())}
    return (num_keys, num_words, len_count)


# %% find_all_words
def find_all_words(tiles, words, pattern=""):
    r"""
    Finds all the anagrams of the given tiles.

    Parameters
    ----------
    tiles : str or list of chars
        Letters to anagram
    words : dict
        Dictionary of words by sorted, anagrammed keys
    pattern : str, optional
        Regular expression pattern to apply to matching

    Returns
    -------
    out : list of str
        List of valid words based on the given tiles, words, and pattern

    Examples
    --------
    >>> from dstauffman2.games.scrabble import create_dict, find_all_words, get_dict_path
    >>> from dstauffman2 import get_data_dir
    >>> tiles    = ['w', 'o', 'r', 'd', 's']
    >>> filename = get_dict_path()
    >>> words    = create_dict(filename)
    >>> out = find_all_words(tiles, words)
    >>> print(out[:11])
    ['sword', 'words', 'dors', 'dows', 'rods', 'rows', 'sord', 'word', 'dor', 'dos', 'dow']

    >>> print(out[11:])
    ['ods', 'ors', 'rod', 'row', 'sod', 'sow', 'wos', 'do', 'od', 'or', 'os', 'ow', 'so', 'wo']

    >>> out2 = find_all_words(tiles='words', words=words, pattern='a..$')
    >>> print(out2[:10])
    ['draws', 'roads', 'sward', 'woads', 'daws', 'oars', 'rads', 'raws', 'sard', 'wads']

    >>> print(out2[10:])
    ['ward', 'wars', 'ado', 'ads', 'ars']

    """

    def wrapped(tiles, words):
        r"""Wrapped solver function."""
        # find all the possible keys
        keys = []
        for r in range(2, len(tiles) + 1):
            for subset in itertools.combinations(tiles, r):
                this_key = "".join(subset)
                keys.append(this_key)

        # find all the possible words based on the found keys
        soln = set()
        for this_key in keys:
            if this_key in words:
                soln |= set(words[this_key])
        return soln

    # check for any extra letters in the pattern
    extra_letters = [letter for letter in pattern if letter in LETTERS]

    # create a working list of all the tiles
    full_tiles = [x for x in tiles if x != "?"] + extra_letters

    # ensure that tiles are sorted
    full_tiles = sorted(full_tiles)

    # convert the blanks to possible letters
    num_blanks = tiles.count("?")
    if num_blanks == 0:
        soln = wrapped(full_tiles, words)
    else:
        extra_combs = [list(x) for x in itertools.product(LETTERS, repeat=num_blanks)]
        soln = set()
        for this_comb in extra_combs:
            this_tiles = sorted(full_tiles + this_comb)
            soln |= wrapped(this_tiles, words)

    # limit based on the given pattern
    if pattern:
        r1 = re.compile(pattern)
        out = [word for word in soln if r1.search(word)]
    else:
        out = list(soln)

    # sort the output words
    out.sort(key=lambda item: (-len(item), item))
    return out


# %% Functions - validate_board
def validate_board(board):
    r"""Validates a given board."""
    num_squares = len(board)
    rows = board.split("\n")
    num_rows = len(rows)
    temp_cols = set(len(x) for x in rows)
    # board assertions
    if len(temp_cols) != 1:
        raise ValueError("Board does not have an equal number of columns in each row.")
    num_cols = temp_cols.pop()
    if num_squares != num_rows * (num_cols + 1) - 1:
        raise ValueError("Board is not sized properly, check for extra newline characters.")
    if not all(x in BOARD_SYMBOLS for x in board):
        raise ValueError("Invalid board characters")
    return (num_rows, num_cols)


# %% Functions - validate_move
def validate_move(board, played, move):
    r"""Validates whether the desired move is legal."""
    return True  # TODO: write this


# %% Functions - score_move
def score_move(board, played, move):
    r"""Scores a given move based on a board layout and played tiles."""
    # initialize output
    score = 0
    # TODO: write this
    return score


# %% Functions - get_board_played
def get_board_played(played):
    r"""
    Finds the indices to positions that have been played.

    Examples
    --------
    >>> from dstauffman2.games.scrabble import get_board_played
    >>> played = '     \n     \n cat \n     \n     '
    >>> out = get_board_played(played)
    >>> print(sorted(list(out)))
    [13, 14, 15]

    """
    out = {ix for (ix, char) in enumerate(played) if (char != " " and char != "\n")}
    return out


# %% Functions - get_board_open
def get_board_open(played):
    r"""
    Finds the indices to positions that are open to play.

    Examples
    --------
    >>> from dstauffman2.games.scrabble import get_board_open
    >>> played = '     \n     \n cat \n     \n     '
    >>> out = get_board_open(played)
    >>> print(sorted(list(out)))
    [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 12, 16, 18, 19, 20, 21, 22, 24, 25, 26, 27, 28]

    """
    out = {ix for (ix, char) in enumerate(played) if char == " "}
    return out


# %% Functions - get_board_must_play
def get_board_must_play(board, num_rows, num_cols, played):
    r"""
    Finds the indices to positions that are open to play.

    Examples
    --------
    >>> from dstauffman2.games.scrabble import get_board_must_play
    >>> board    = '.....\n.....\n..s..\n.....\n.....'
    >>> played   = '     \n     \n cat \n     \n     '
    >>> num_rows = 5
    >>> num_cols = 5
    >>> out      = get_board_must_play(board, num_rows, num_cols, played)
    >>> print(sorted(list(out)))
    [7, 8, 9, 12, 16, 19, 20, 21]

    """
    # check for special case of an empty board
    if all(char in {" ", "\n"} for char in played):
        out = {ix for (ix, char) in enumerate(board) if char == "s"}
        return out
    # find the currently occupied places
    occupied = get_board_played(played)
    # alias the stride for each row
    stride = num_cols + 1
    # initialize the output
    out = set()
    # loop through the board
    for row in range(num_rows):
        for col in range(num_cols):
            # alias this index
            ix = col * stride + row
            # check if it's already occupied
            if ix in occupied:
                continue
            # check to the left, right, above, and below for occupied squares
            if (row > 0) and (col * stride + row - 1 in occupied):
                out.add(ix)
            elif (row < num_rows - 1) and (col * stride + row + 1 in occupied):
                out.add(ix)
            elif (col > 0) and ((col - 1) * stride + row in occupied):
                out.add(ix)
            elif (col < num_cols - 1) and ((col + 1) * stride + row in occupied):
                out.add(ix)
    return out


# %% Unit test
if __name__ == "__main__":
    unittest.main(module="dstauffman2.games.scrabble.tests.test_utils", exit=False)
    doctest.testmod(verbose=False)
