# -*- coding: utf-8 -*-
r"""
Special module file for the "scrabble" game.  It defines the functions that find special words.

Notes
-----
#.  Written by David C. Stauffer in March 2017.
"""

#%% Imports
import doctest
import unittest

from dstauffman2.games.scrabble.constants import CONSONANTS, MAX_LEN, VOWELS
from dstauffman2.games.scrabble.utils import get_raw_dictionary

#%% Support function
def find_all(words=None, func=None):
    r"""
    Finds all the valid words using the provided function, `func`

    Paramters
    ---------
    words : set, optional
        List of all valid words as a Python set
    func : function
        Function to use as criterion for valid words

    Returns
    -------
    out : list
        List of valid words

    Examples
    --------

    >>> from dstauffman2.games.scrabble import find_all, get_raw_dictionary
    >>> words = get_raw_dictionary()
    >>> out = find_all(words, func=lambda x: len(x) == 20)
    >>> print(out[:3])
    ['acetylcholinesterase', 'adrenocorticosteroid', 'adrenocorticotrophic']

    >>> print(len(out))
    160

    """
    # if not given, load the default word list
    if words is None:
        words = get_raw_dictionary()
    # apply the given function as a filter to the word list
    out = list(filter(func, words))
    # sort the output based on the length of the words, longest first, then alphabetically
    out.sort(key=lambda item: (-len(item), item))
    return out

#%% find_all_two_letter_words
def find_all_two_letter_words(words=None):
    r"""
    Finds all the two letter valid words

    Paramters
    ---------
    words : set, optional
        List of all valid words as a Python set

    Returns
    -------
    out : list
        List of valid two letter words

    Examples
    --------

    >>> from dstauffman2.games.scrabble import find_all_two_letter_words
    >>> out = find_all_two_letter_words()
    >>> print(out[:10])
    ['aa', 'ab', 'ad', 'ae', 'ag', 'ah', 'ai', 'al', 'am', 'an']

    """
    return find_all(words, func=lambda x: len(x) == 2)

#%% find_all_three_letter_words
def find_all_three_letter_words(words=None):
    return find_all(words, func=lambda x: len(x) == 3)

#%% find_all_four_letter_words
def find_all_four_letter_words(words=None):
    return find_all(words, func=lambda x: len(x) == 4)

#%% find_all_consonant_words
def find_all_consonant_words(words=None):
    return find_all(words, func=lambda x: all(i in CONSONANTS for i in x))

#%% find_all_one_vowel_words
def find_all_one_vowel_words(words=None):
    return find_all(words, func=lambda x: sum(i in VOWELS for i in x) == 1)

#%% find_all_one_consonant_words
def find_all_one_consonant_words(words=None):
    return find_all(words, func=lambda x: sum(i in CONSONANTS for i in x) == 1)

#%% find_all_vowel_words
def find_all_vowel_words(words=None):
    return find_all(words, func=lambda x: all(i in VOWELS for i in x))

#%% find_all_q_without_u_words
def find_all_q_without_u_words(words=None):
    return find_all(words, func=lambda x: 'q' in x and not 'u' in x)

#%% find_starting_with_de
def find_starting_with_de(words=None, max_len=MAX_LEN):
    return find_all(words, func=lambda x: x.startswith('de') and len(x)<=max_len)

#%% find_starting_with_re
def find_starting_with_re(words=None, max_len=MAX_LEN):
    return find_all(words, func=lambda x: x.startswith('re') and len(x)<=max_len)

#%% find_starting_with_un
def find_starting_with_un(words=None, max_len=MAX_LEN):
    return find_all(words, func=lambda x: x.startswith('un') and len(x)<=max_len)

#%% find_starting_with_x
def find_starting_with_x(words=None, max_len=MAX_LEN):
    return find_all(words, func=lambda x: x.startswith('x') and len(x)<=max_len)

#%% find_ending_with_est
def find_ending_with_est(words=None, max_len=MAX_LEN):
    return find_all(words, func=lambda x: x.endswith('est') and len(x)<=max_len)

#%% find_ending_with_iest
def find_ending_with_iest(words=None, max_len=MAX_LEN):
    return find_all(words, func=lambda x: x.endswith('iest') and len(x)<=max_len)

#%% find_ending_with_ing
def find_ending_with_ing(words=None, max_len=MAX_LEN):
    return find_all(words, func=lambda x: x.endswith('ing') and len(x)<=max_len)

#%% find_ending_with_j
def find_ending_with_j(words=None, max_len=MAX_LEN):
    return find_all(words, func=lambda x: x.endswith('j') and len(x)<=max_len)

#%% find_ending_with_ness
def find_ending_with_ness(words=None, max_len=MAX_LEN):
    return find_all(words, func=lambda x: x.endswith('ness') and len(x)<=max_len)

#%% find_ending_with_q
def find_ending_with_q(words=None, max_len=MAX_LEN):
    return find_all(words, func=lambda x: x.endswith('q') and len(x)<=max_len)

#%% find_ending_with_ted
def find_ending_with_ted(words=None, max_len=MAX_LEN):
    return find_all(words, func=lambda x: x.endswith('ted') and len(x)<=max_len)

#%% find_ending_with_u
def find_ending_with_u(words=None, max_len=MAX_LEN):
    return find_all(words, func=lambda x: x.endswith('u') and len(x)<=max_len)

#%% find_ending_with_v
def find_ending_with_v(words=None, max_len=MAX_LEN):
    return find_all(words, func=lambda x: x.endswith('v') and len(x)<=max_len)

#%% find_ending_with_x
def find_ending_with_x(words=None, max_len=MAX_LEN):
    return find_all(words, func=lambda x: x.endswith('x') and len(x)<=max_len)

#%% find_ending_with_z
def find_ending_with_z(words=None, max_len=MAX_LEN):
    return find_all(words, func=lambda x: x.endswith('z') and len(x)<=max_len)

#%% Unit test
if __name__ == '__main__':
    unittest.main(module='dstauffman2.games.scrabble.tests.test_special', exit=False)
    doctest.testmod(verbose=False)
