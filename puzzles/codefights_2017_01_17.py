# -*- coding: utf-8 -*-
r"""
Codefight challenge (stringsRearrangement), 2017-01-17, by DStauffman.
"""

#%% Imports
import doctest
import unittest

#%% Functions - is_str_one_off
def is_str_one_off(str1, str2):
    r"""
    Determines if strings are only one character different from one another.

    Parameters
    ----------
    str1 : str
        First string
    str2 : str
        Second string

    Returns
    -------
    unnamed : bool
        Whether strings are one off from each other

    Examples
    --------

    >>> print(is_str_one_off('abc', 'axc'))
    True

    >>> print(is_str_one_off('abc', 'cba'))
    False

    """
    # check that the lengths are the same
    assert len(str1) == len(str2)
    # do a simple test to see if everything is the same
    if str1 == str2:
        return False
    # keep a counter of differences
    diff = 0
    # loop through the characters
    for ix in range(len(str1)):
        # if the characters are the same, then continue to the next one
        if str1[ix] == str2[ix]:
            continue
        else:
            # if not the same, increment the counter
            diff += 1
            # check for too many differences
            if diff > 1:
                return False
    # if you got here, then there is exactly one difference and it's a good result
    return True

#%% Functions - find_one_offs
def find_one_offs(key, input_array):
    r"""
    Finds the one-off paths within the list.

    Parameters
    ----------
    key : char
        Input key to use when finding elements that are one character away
    input_array : list
        List of fixed length character strings for which to compare to the key

    Returns
    -------
    out : list
        Element numbers that are one character off from the given key

    Examples
    --------

    >>> print(find_one_offs('abc', ['abc', 'aac', 'aby']))
    [1, 2]

    """
    # save the indices in the input where they are only one off from the key
    out = [ix for (ix, this_str) in enumerate(input_array) if is_str_one_off(key, this_str)]
    return out

#%% Functions - stringsRearrangement
def stringsRearrangement(input_array):
    r"""
    Finds out if there is a viable path from one string to the next.

    Parameters
    ----------
    input_array : list
        List of fixed length character strings for which to decide if there is a one string change

    Returns
    -------
    has_path : bool
        Flag for whether the list has a one character path

    Examples
    --------

    >>> print(stringsRearrangement(['ab', 'bb', 'aa']))
    True

    >>> print(stringsRearrangement(['aba', 'bbb', 'bab']))
    False

    """
    def recursive_solver(key, items, last=0):
        r"""
        Recursive path solver.
            Using a current key and list, deterimen if there is a next move
            If there is, take it and shorten list
            If list is empty, we found a path
            If list is not empty, recursively continue
            If there is not a path, reverse the last step
        """
        # find valid next steps
        possible_steps = find_one_offs(key, items)
        for this_step in possible_steps:
            # if any steps, take the first one and continue recursively
            new_key = items.pop(this_step)
            done = recursive_solver(new_key, items, last=this_step)
            if done:
                # solution was found
                return done
        else:
            # if no valid steps, determine if we are done or need to backtrack
            if items:
                # backtrack
                items.insert(last, key)
                return False
            else:
                # success
                return True
        # no steps and no backtracking
        return False

    # solve wrapper
    for (i, this_key) in enumerate(input_array):
        # build a working list of everything except the current starting point
        working_list = [value for (j, value) in enumerate(input_array) if j != i]
        # recursively solve puzzle
        has_path = recursive_solver(this_key, working_list)
        if has_path:
            return True
    return False

#%% Tests - is_str_one_off
class Test_is_str_one_off(unittest.TestCase):
    r"""
    Tests the is_str_one_off function with the following cases:
        TBD
    """
    def test_nominal(self):
        self.assertTrue(is_str_one_off('aaa', 'aab'))
        self.assertTrue(is_str_one_off('aaa', 'aba'))
        self.assertTrue(is_str_one_off('aaa', 'baa'))
        self.assertTrue(is_str_one_off('ccc', 'cbc'))

    def test_char_jumps(self):
        self.assertTrue(is_str_one_off('aaa', 'aac'))
        self.assertTrue(is_str_one_off('ccc', 'cac'))

    def test_not_true(self):
        self.assertFalse(is_str_one_off('cc', 'bb'))
        self.assertFalse(is_str_one_off('cccc', 'dddd'))
        self.assertFalse(is_str_one_off('ccc', 'dce'))

    def test_equal(self):
        self.assertFalse(is_str_one_off('a', 'a'))

    def test_wrong_len(self):
        with self.assertRaises(AssertionError):
            is_str_one_off('aaa', 'aa')

#%% Tests - find_one_offs
class Test_find_one_offs(unittest.TestCase):
    r"""
    Tests the find_one_offs function with the following cases:
        TBD
    """
    def test_nominal(self):
        ix = find_one_offs('ccc', ['ccd', 'cdc', 'dcc', 'ddd', 'bbb', 'bcc', 'cbc', 'ccb', 'ccc'])
        self.assertListEqual(ix, [0, 1, 2, 5, 6, 7])

#%% Tests - stringsRearrangement
class Test_stringsRearrangement(unittest.TestCase):
    r"""
    Tests the stringsRearrangement function with the following cases:
        TBD
    """
    def test_simple1(self):
        self.assertTrue(stringsRearrangement(['aa', 'ab', 'bb']))

    def test_simple2(self):
        self.assertTrue(stringsRearrangement(['aa', 'bb', 'ba']))

    def test_simple3(self):
        self.assertFalse(stringsRearrangement(['aa', 'ab', 'ee']))

    def test_1(self):
        self.assertFalse(stringsRearrangement(['aba', 'bbb', 'bab']))

    def test_2(self):
        self.assertTrue(stringsRearrangement(['ab', 'bb', 'aa']))

    def test_3(self):
        self.assertFalse(stringsRearrangement(['q', 'q']))

    def test_4(self):
        self.assertTrue(stringsRearrangement(['zzzzab', 'zzzzbb', 'zzzzaa']))

    def test_5(self):
        self.assertFalse(stringsRearrangement(['ab', 'ad', 'ef', 'eg']))

    def test_6(self):
        self.assertFalse(stringsRearrangement(['abc', 'abx', 'axx', 'abc']))

    def test_7(self):
        self.assertTrue(stringsRearrangement(['abc', 'abx', 'axx', 'abx', 'abc']))

    def test_8(self):
        self.assertTrue(stringsRearrangement(['f', 'g', 'a', 'h']))

    def test_repeats(self):
        self.assertTrue(stringsRearrangement(['abc', 'xbc', 'xxc', 'xbc', 'aby', 'ayy', 'aby']))

#%% Script
if __name__ == '__main__':
    # execute unit tests
    unittest.main(module='dstauffman2.puzzles.codefights_2017_01_17', exit=False)
    # execute doctests
    doctest.testmod(verbose=False)
