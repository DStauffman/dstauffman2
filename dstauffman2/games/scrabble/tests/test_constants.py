r"""
Test file for the `scrabble.constants` module of the dstauffman2 code.  It is intented to contain
test cases to demonstrate functionaliy and correct outcomes for all the functions within the module.

Notes
-----
#.  Written by David C. Stauffer in March 2017.
"""

# %% Imports
import unittest

import dstauffman2.games.scrabble as scrab


# %% Test Letters
class Test_letters(unittest.TestCase):
    r"""
    Tests the letter sets for valid settings.
    """

    def setUp(self):
        self.letters    = scrab.LETTERS
        self.vowels     = scrab.VOWELS
        self.consonants = scrab.CONSONANTS

    def test_letters(self):
        for num in range(ord("a"), ord("z") + 1):
            letter = chr(num)
            self.assertIn(letter, self.letters)
        self.assertIn("?", self.letters)
        for num in range(ord("A"), ord("Z") + 1):
            letter = chr(num)
            self.assertNotIn(letter, self.letters)

    def test_vowels(self):
        c = 0
        for letter in "aeiou":
            if letter in self.vowels:
                c += 1
        self.assertEqual(c, 5)
        self.assertEqual(c, len(self.vowels))

    def test_consonants(self):
        c = 0
        for num in range(ord("a"), ord("z") + 1):
            letter = chr(num)
            if letter not in self.vowels:
                if letter in self.consonants:
                    c += 1
                cap_letter = str.upper(letter)
                self.assertNotIn(cap_letter, self.consonants)
        self.assertEqual(c, 26 - 5)
        self.assertEqual(c, len(self.consonants))
        self.assertIn("y", self.consonants)


# %% Letter point values
# test that each letter has a value
# test that sets are equal

# %% Tile counts
# test that each letter has a count
# test that sets are equal

# %% Colors
# test that are colors are valid tuples or hex codes
# test that all symbols have colors defined


# %% Boards
class Test_boards(unittest.TestCase):
    r"""
    Tests all the given boards for validity.
    """

    def setUp(self):
        self.boards = [scrab.WWF_BOARD, scrab.WWF_SMALL_BOARD, scrab.SCRAB_BOARD]

    def test_valid(self):
        for board in self.boards:
            scrab.validate_board(board)


# %% Defaults
class Test_defaults(unittest.TestCase):
    r"""
    Tests that the defaults are valid.
    """

    def setUp(self):
        self.board  = scrab.BOARD
        self.scores = scrab.SCORES
        self.counts = scrab.COUNTS
        self.dict   = scrab.DICT

    def test_board(self):
        pass

    def test_scores(self):
        pass

    def test_counts(self):
        pass

    def test_dict(self):
        pass


# %% Unit test execution
if __name__ == "__main__":
    unittest.main(exit=False)
