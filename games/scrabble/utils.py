# -*- coding: utf-8 -*-
r"""
Utils module file for the "scrabble" game.  It defines the generic utility functions.

Notes
-----
#.  Written by David C. Stauffer in March 2017.
"""

#%% Imports
from collections import defaultdict
import doctest
import itertools
import os
import re
import unittest
from dstauffman2 import get_root_dir as dcs_root_dir
from dstauffman2 import get_data_dir as dcs_data_dir
from dstauffman2.games.scrabble.classes   import Options
from dstauffman2.games.scrabble.constants import LETTERS

#%% Option instance
OPTS = Options()

#%% get_root_dir
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
    folder = os.path.join(dcs_root_dir(), 'games', 'scrabble')
    return folder

#%% get_enable_path
def get_enable_path():
    r"""
    Gets the full path to the ENABLE2K text dictionary.
    """
    path = os.path.join(dcs_data_dir(), 'enable2k.txt')
    return path

#%% get_raw_dictionary
def get_raw_dictionary(filename=None):
    if filename is None:
        filename = get_enable_path()
    words = set()
    with open(filename, 'rt') as file:
        for line in file.readlines():
            word = line.rstrip('\n')
            if word:
                words.add(word)
    return words

#%% create_dictionary_from_text
def create_dict(filename, min_len=2, max_len=20):
    r"""
    Reads in the ENABLE2K or similar data file and creates a Python words dictionary.

    Notes
    -----
    #.  The input data file has one word per line with no defaults and all lowercase letters.
    #.  The output is a dict with keys being the sorted list of characters, and the values a list
        of all possible words based on those characters.

    Examples
    --------

    >>> from dstauffman2 import get_data_dir
    >>> from dstauffman2.games.scrabble import create_dict, get_enable_path
    >>> filename = get_enable_path()
    >>> words = create_dict(filename)

    """
    raw_words = get_raw_dictionary(filename)
    words = defaultdict(list)
    for word in raw_words:
        if len(set(word) - LETTERS) == 0 and len(word) >= min_len and len(word) <= max_len:
            key = ''.join(sorted(word))
            words[key].append(word)
    return dict(words)

#%% count_num_words
def count_num_words(words):
    num_keys = 0
    num_words = 0
    for (key, value) in words.items():
        num_keys += 1
        num_words += len(value)
    return (num_keys, num_words)

#%% find_all_words
def find_all_words(tiles, words, pattern=''):
    r"""
    Finds all the anagrams of the given tiles.

    Examples
    --------

    >>> from dstauffman2.games.scrabble import create_dict, find_all_words, get_enable_path
    >>> from dstauffman2 import get_data_dir
    >>> tiles    = ['w', 'o', 'r', 'd', 's']
    >>> filename = get_enable_path()
    >>> words    = create_dict(filename)
    >>> out = find_all_words(tiles, words)

    """
    def wrapped(tiles, words):
        r"""Wrapped solver function."""
        # find all the possible keys
        keys = []
        for r in range(2, len(tiles)+1):
            for subset in itertools.combinations(tiles, r):
                this_key = ''.join(subset)
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
    full_tiles = [x for x in tiles if x != '?'] + extra_letters

    # ensure that tiles are sorted
    full_tiles = sorted(full_tiles)

    # convert the blanks to possible letters
    num_blanks = tiles.count('?')
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

#%% Unit test
if __name__ == '__main__':
    unittest.main(module='dstauffman2.games.scrabble.tests.test_utils', exit=False)
    doctest.testmod(verbose=False)

    #filename = get_enable_path()
    #words = create_dict(filename)
    #(num_keys, num_words) = count_num_words(words)

    #tiles = ['w', 'o', 'r', 'd', 's']
    #out = find_all_words(tiles, words)

    #out2 = find_all_words(tiles, words, pattern='a..$')
