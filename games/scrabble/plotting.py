# -*- coding: utf-8 -*-
r"""
Plotting module file for the "scrabble" game.  It defines the plotting functions.

Notes
-----
#.  Written by David C. Stauffer in March 2017.
"""

#%% Imports
import doctest
from matplotlib.patches import Rectangle, Wedge, Polygon
import unittest
from dstauffman2.games.scrabble.constants import COLOR

#%% plot_board
def plot_board(ax, board, played):
    r"""
    Plots the board.

    Parameters
    ----------
    ax : object
        Axis to plot on
    board : str
        Board layout

    Examples
    --------

    >>> from dstauffman2.games.scrabble import plot_board, BOARD
    >>> import matplotlib.pyplot as plt
    >>> plt.ioff()
    >>> fig = plt.figure()
    >>> ax = fig.add_subplot(111, aspect='equal')
    >>> _ = ax.set_xlim(-0.5, 14.5)
    >>> _ = ax.set_ylim(-0.5, 14.5)
    >>> ax.invert_yaxis()
    >>> board = BOARD
    >>> plot_board(ax, board)
    >>> plt.show(block=False) # doctest: +SKIP

    >>> plt.close()

    """
    # get axes limits
    rows = board.strip().split('\n')
    m = len(rows[0])
    n = len(rows)
    s = 0.5
    xmin = 0 - s
    xmax = m - 1 + s
    ymin = 0 - s
    ymax = n - 1 + s

    # fill background
    ax.add_patch(Rectangle((-xmin-1, -ymin-1), xmax-xmin, ymax-ymin, facecolor=COLOR['board'], \
        edgecolor=None))

    # draw horizontal lines
    for i in range(1, n):
        ax.plot([i-s, i-s], [ymin, ymax], color=COLOR['edge'], linewidth=1)
    # draw vertical lines
    for i in range(1, m):
        ax.plot([xmin, xmax], [i-s, i-s], color=COLOR['edge'], linewidth=1)

    # loop through and place pieces
    for i in range(m):
        for j in range(n):
            plot_tile(ax, i, j, rows[i][j])

#%% plot_tile
def plot_tile(ax, x, y, piece, size=1, color=(0, 0, 0)):
    map_ = {'.': '', 'd': 'DL', 'D':'DW', 't': 'TL', 'T': 'TW', 's': ''}
    text = map_[piece]
    if text:
        pass
    # TODO: finish function

#%% plot_letter
def plot_letter(ax, x, y, letter, size=1, color=(0.8, 0.8, 0)):
    pass

#%% Unit Test
if __name__ == '__main__':
    unittest.main(module='dstauffman2.games.scrabble.tests.test_plotting', exit=False)
    doctest.testmod(verbose=False)
