# -*- coding: utf-8 -*-
r"""
Test file for the `scrabble.utils` module of the dstauffman2 code.  It is intented to contain test
cases to demonstrate functionaliy and correct outcomes for all the functions within the module.

Notes
-----
#.  Written by David C. Stauffer in March 2017.
"""

#%% Imports
import numpy as np
import unittest
import dstauffman2.games.scrabble as scrab

#%% Support
words = scrab.create_dict(scrab.get_enable_path())

#%% find_all_words
class Test_find_all_words(unittest.TestCase):
    r"""
    Tests the find_all_words function with the following cases:
        TBD

    Notes
    -----
    #.  Valid word lists provided by wordsolver.net

    """
    def setUp(self):
        self.tiles = ['w', 'o', 'r', 'd', 's']
        self.words = words
        self.out   = ['sword', 'words', 'dors', 'dows', 'rods', 'rows', 'sord', 'word', 'dor', \
            'dos', 'dow', 'ods', 'ors', 'rod', 'row', 'sod', 'sow', 'wos', 'do', 'od', 'or', 'os', \
            'ow', 'so', 'wo']

    def test_nominal(self):
        out = scrab.find_all_words(self.tiles, self.words)
        np.testing.assert_array_equal(out, self.out)

    def test_pattern(self):
        out = scrab.find_all_words(self.tiles, self.words, pattern=r'a..$')
        np.testing.assert_array_equal(out, ['draws', 'roads', 'sward', 'woads', 'daws', 'oars', \
            'rads', 'raws', 'sard', 'wads', 'ward', 'wars', 'ado', 'ads', 'ars'])

    def test_one_blank(self):
        tiles = ['a', 'b', 'c', '?']
        out = scrab.find_all_words(tiles, self.words)
        expected = ['bach', 'back', 'cabs', 'carb', 'crab', 'scab', \
            'aba', 'abo', 'abs', 'aby', 'ace', 'act', 'alb', 'arb', 'arc', 'baa', 'bad', 'bag', \
            'bah', 'bal', 'bam', 'ban', 'bap', 'bar', 'bas', 'bat', 'bay', 'boa', 'bra', 'cab', \
            'cad', 'cam', 'can', 'cap', 'car', 'cat', 'caw', 'cay', 'cob', 'cub', 'dab', 'fab', \
            'gab', 'jab', 'kab', 'lab', 'lac', 'mac', 'nab', 'oba', 'oca', 'pac', 'sab', 'sac', \
            'tab', 'vac', 'wab', \
            'aa', 'ab', 'ad', 'ae', 'ag', 'ah', 'ai', 'al', 'am', 'an', 'ar', 'as', 'at', 'aw', \
            'ax', 'ay', 'ba', 'be', 'bi', 'bo', 'by', 'da', 'fa', 'ha', 'ka', 'la', 'ma', 'na', \
            'pa', 'ta', 'ya', 'za']
        extra = set(expected) - set(out)
        print('Extra = ', sep='')
        print(extra)
        missing = set(out) - set(expected)
        print('Missing = ', sep='')
        print(missing)
        np.testing.assert_array_equal(out, expected)

    def test_two_blanks(self):
        tiles = ['x', 'z', 'z', '?', '?']
        out = scrab.find_all_words(tiles, self.words)
        expected = ['buzz', 'fizz', 'fuzz', 'jazz', 'razz', \
            'adz', 'axe', 'azo', 'biz', 'box', 'cox', 'coz', 'dex', 'dux', 'fax', 'fez', 'fix', \
            'fiz', 'fox', 'gox', 'hex', 'kex', 'lax', 'lex', 'lez', 'lox', 'lux', 'max', 'mix', \
            'nix', 'oxo', 'oxy', 'pax', 'pix', 'pox', 'pyx', 'rax', 'rex', 'sax', 'sex', 'six', \
            'sox', 'tax', 'tux', 'vex', 'vox', 'wax', 'wiz', 'xis', 'zag', 'zap', 'zas', 'zax', \
            'zed', 'zee', 'zek', 'zen', 'zep', 'zig', 'zin', 'zip', 'zit', 'zoa', 'zoo', \
            'aa', 'ab', 'ad', 'ae', 'ag', 'ah', 'ai', 'al', 'am', 'an', 'ar', 'as', 'at', 'aw', \
            'ax', 'ay', 'ba', 'be', 'bi', 'bo', 'by', 'da', 'de', 'di', 'do', 'ed', 'ef', 'eh', \
            'el', 'em', 'en', 'er', 'es', 'et', 'ex', 'fa', 'fe', 'fi', 'gi', 'go', 'ha', 'he', \
            'hi', 'hm', 'ho', 'id', 'if', 'in', 'is', 'it', 'jo', 'ka', 'ki', 'la', 'li', 'lo', \
            'ma', 'me', 'mi', 'mm', 'mo', 'mu', 'my', 'na', 'ne', 'no', 'nu', 'od', 'oe', 'of', \
            'oh', 'oi', 'om', 'on', 'op', 'or', 'os', 'ow', 'ox', 'oy', 'pa', 'pe', 'pi', 'qi', \
            're', 'sh', 'si', 'so', 'ta', 'ti', 'to', 'uh', 'um', 'un', 'up', 'us', 'ut', 'we',
            'wo', 'xi', 'xu', 'ya', 'ye', 'yo', 'za']
        extra = set(expected) - set(out)
        print('Extra = ', sep='')
        print(extra)
        missing = set(out) - set(expected)
        print('Missing = ', sep='')
        print(missing)
        np.testing.assert_array_equal(out, expected)

#%% Unit test execution
if __name__ == '__main__':
    unittest.main(exit=False)
