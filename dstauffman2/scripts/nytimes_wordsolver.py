"""
Example script for how to solve one of the puzzles in the New York Times Sunday paper.

Notes
-----
#.  Written by David C. Stauffer in April 2020.
"""

#%% Imports
from dstauffman2.games.scrabble import create_dict, find_all, find_all_words, get_dict_path

#%% Script
if __name__ == '__main__':
    # Tiles to use
    tiles = ['a', 'c', 'e', 'i', 'o', 't', 'v']

    # Allow repeated tiles?
    # TODO: should make this a flag to the solver
    all_tiles = tiles + tiles + tiles

    # Letters that must exist
    # (must have a v)
    pattern = '.*v.*'

    # Length restrictions
    # (must be at least 5 letters)
    func = lambda x: len(x) >= 5

    # get a list of all possible words
    filename = get_dict_path()
    words    = create_dict(filename)

    # find all the words that match the pattern
    temp = find_all_words(all_tiles, words, pattern='.*v.*')

    # apply the additional restrictions
    solution = find_all(temp, func=lambda x: len(x) >= 5)

    # print the solution
    print(solution)

    # score the solution
    # (one point per word, 3 points if all letters used)
    score = sum([1 if len(set(x)) < len(tiles) else 3 for x in solution])
    print('{} Words for a final score of {} points!'.format(len(solution), score))
