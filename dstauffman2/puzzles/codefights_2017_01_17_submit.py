r"""Codefight challenge (stringsRearrangement), 2017-01-17, by DStauffman."""


# %% Functions - is_str_one_off
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
    >>> from dstauffman2.puzzles.codefights_2017_01_17 import *
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


# %% Functions - find_one_offs
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
    >>> from dstauffman2.puzzles.codefights_2017_01_17 import *
    >>> print(find_one_offs('abc', ['abc', 'aac', 'aby']))
    [1, 2]

    """
    # save the indices in the input where they are only one off from the key
    out = [ix for (ix, this_str) in enumerate(input_array) if is_str_one_off(key, this_str)]
    return out


# %% Functions - stringsRearrangement
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
    >>> from dstauffman2.puzzles.codefights_2017_01_17 import *
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
    for i, this_key in enumerate(input_array):
        # build a working list of everything except the current starting point
        working_list = [value for (j, value) in enumerate(input_array) if j != i]
        # recursively solve puzzle
        has_path = recursive_solver(this_key, working_list)
        if has_path:
            return True
    return False
