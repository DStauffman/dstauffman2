r"""
Plotting module file for the "scrabble" game.  It defines the plotting functions.

Notes
-----
#.  Written by David C. Stauffer in March 2017.
"""

# %% Imports
import doctest
import unittest

from matplotlib.patches import Rectangle

from dstauffman2.games.scrabble.constants import COLOR


# %% plot_board
def plot_board(ax, board):
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
    >>> from dstauffman2.games.scrabble import plot_board, Board
    >>> import matplotlib.pyplot as plt
    >>> plt.ioff()
    >>> fig = plt.figure()
    >>> ax = fig.add_subplot(111, aspect="equal")
    >>> ax.invert_yaxis()
    >>> board = Board()
    >>> board.played = board.played[:119] + "sword" + board.played[124:]
    >>> plot_board(ax, board)
    >>> plt.show(block=False) # doctest: +SKIP

    >>> plt.close(fig)

    """
    # get board details and size limits
    spots = board.board.split("\n")
    m     = len(spots[0])
    n     = len(spots)
    hs    = 0.5
    xmin  = 0 - hs
    xmax  = m - 1 + hs
    ymin  = 0 - hs
    ymax  = n - 1 + hs
    tiles = board.played.split("\n")

    # fill background
    ax.add_patch(Rectangle((-xmin-1, -ymin-1), xmax-xmin, ymax-ymin, facecolor=COLOR["board"], \
        edgecolor=None))

    # draw horizontal lines
    for i in range(0, n + 1):
        ax.plot([i - hs, i - hs], [ymin, ymax], color=COLOR["edge"], linewidth=1)
    # draw vertical lines
    for i in range(0, m + 1):
        ax.plot([xmin, xmax], [i - hs, i - hs], color=COLOR["edge"], linewidth=1)

    # loop through and place pieces
    for i in range(m):
        for j in range(n):
            this_spot = spots[i][j]
            plot_tile(ax, j, i, this_spot, color=COLOR[this_spot], textcolor=COLOR["board_text"])
            this_tile = tiles[i][j]
            if this_tile != " ":
                plot_letter(ax, j, i, this_tile, color=COLOR["tile"], textcolor=COLOR["tile_text"])

    # make sure the limits are good
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)


# %% plot_tile
def plot_tile(ax, x, y, piece, size=1, color=(0, 0, 0), textcolor=(1, 1, 1)):
    map_ = {".": "", "d": "DL", "D": "DW", "t": "TL", "T": "TW", "s": ""}
    text = map_[piece]
    if text:
        ax.annotate(text, xy=(x, y), xycoords="data", horizontalalignment="center", \
            verticalalignment="center", fontsize=10, color=textcolor)
    ax.add_patch(Rectangle((x-size/2, y-size/2), size, size, facecolor=color, edgecolor=None))


# %% plot_letter
def plot_letter(ax, x, y, letter, size=1, color=(0, 0, 0), textcolor=(1, 1, 1)):
    text = letter.upper()
    ax.annotate(text, xy=(x, y), xycoords="data", horizontalalignment="center", \
        verticalalignment="center", fontsize=15, color=textcolor)
    ax.add_patch(Rectangle((x-size/2, y-size/2), size, size, facecolor=color, edgecolor=None))


# %% plot_draw_stats
def plot_draw_stats(ax, counts, tiles, move):
    pass


# %% plot_move_strength
def plot_move_strength(ax, move, pot_moves):
    pass


# %% display_tile_bag
def display_tile_bag(lne, counts, tiles):
    pass


# %% Unit Test
if __name__ == "__main__":
    unittest.main(module="dstauffman2.games.scrabble.tests.test_plotting", exit=False)
    doctest.testmod(verbose=False)
