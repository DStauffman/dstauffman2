"""
The "brick" file solves the 3D red and gray brick puzzle that I have.
(I don't actually remember the original name of the puzzle.)

Notes
-----
#.  Written by David C. Stauffer in June 2015 after he crashed his bike and had nothing to do for a bit.
"""

# %% Imports
from datetime import datetime
import doctest
import os
import shutil

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Line3DCollection, Poly3DCollection
import numpy as np

from dstauffman import Opts, setup_dir, setup_plots

from dstauffman2 import get_root_dir

# %% Hard-coded values
N = 0  # Null cube - not defined
R = 1  # Red cube
G = 2  # Gray cube
E = 3  # Either (unknown color, used for center cube)
# Number of unique pieces in the game
NUM_PIECES = 9
# Size of the overall puzzle
SIZE_PIECES = (3, 3, 3)
# Pre-determined solution color pattern
soln = np.array([[[R, G, R], [G, G, G], [R, G, R]], [[R, G, R], [G, E, G], [R, G, R]], [[R, G, R], [G, G, G], [R, G, R]]])
# Pieces 1-9
p1 = np.array([[[R, N, N], [N, N, N], [N, N, N]], [[R, N, N], [N, N, N], [N, N, N]], [[R, N, N], [N, N, N], [N, N, N]]])
p2 = np.array([[[N, N, N], [N, N, N], [N, N, N]], [[R, G, N], [N, N, N], [N, N, N]], [[R, N, N], [N, N, N], [N, N, N]]])
p3 = np.array([[[N, N, N], [N, N, N], [N, N, N]], [[N, N, N], [G, N, N], [N, G, N]], [[R, N, N], [N, N, N], [N, N, N]]])
p4 = np.array([[[N, N, N], [N, G, N], [N, N, N]], [[N, N, N], [R, N, N], [N, N, N]], [[G, N, N], [N, N, N], [N, N, N]]])
p5 = np.array([[[N, N, N], [N, N, N], [N, N, N]], [[N, G, N], [G, N, N], [N, N, N]], [[G, N, N], [N, N, N], [N, N, N]]])
p6 = np.array([[[N, N, N], [N, N, N], [N, N, N]], [[N, N, G], [N, N, N], [N, N, N]], [[R, G, N], [N, N, N], [N, N, N]]])
p7 = np.array([[[N, N, N], [N, N, N], [N, N, N]], [[R, N, N], [N, R, N], [N, N, N]], [[R, N, N], [N, N, N], [N, N, N]]])
p8 = np.array([[[N, N, R], [N, N, N], [N, N, N]], [[N, G, N], [N, N, N], [N, N, N]], [[R, N, N], [N, N, N], [N, N, N]]])
p9 = np.array([[[N, N, N], [N, N, N], [N, N, N]], [[N, G, N], [N, N, N], [N, N, N]], [[G, N, G], [N, N, N], [N, N, N]]])
# combine all the pieces into a list
pieces = [p1, p2, p3, p4, p5, p6, p7, p8, p9]


# %% Functions - _get_color
def _get_color(value):
    r"""
    Gets the color based on the given numeric value.

    Parameters
    ----------
    value : int
        Numeric enumerated value corresponding to the color of the cube

    Returns
    -------
    color : str
        Color specifying for use in plotting

    Notes
    -----
    #.  Written by David C. Stauffer in June 2015.

    Examples
    --------
    >>> from dstauffman2.games.brick import _get_color, R
    >>> color = _get_color(R)
    >>> print(color)
    r

    """
    if value == N:
        color = "none"
    elif value == R:
        color = "r"
    elif value == G:
        color = "#cccccc"
    elif value == E:
        color = "k"
    else:
        raise ValueError("Unexpected color code.")
    return color


# %% Functions - _support_rot_piece
def _support_rot_piece():
    r"""
    Calculates the maps for rotating the pieces.

    Notes
    -----
    #.  Written by David C. Stauffer in June 2015.
    #.  This function is not intended to be used, but is reference for where the maps came from
        for rotating the pieces.
    """
    # start indices
    x = np.arange(0, 27).reshape(SIZE_PIECES)
    # rot 1
    y1 = np.zeros(SIZE_PIECES, dtype=int)
    for i in range(3):
        for j in range(3):
            y1[:, i, j] = x[:, 2 - j, i]
    # rot 2
    y2 = np.zeros(SIZE_PIECES, dtype=int)
    for i in range(3):
        for j in range(3):
            y2[j, :, i] = x[i, :, 2 - j]
    # rot 3
    y3 = np.zeros(SIZE_PIECES, dtype=int)
    for i in range(3):
        for j in range(3):
            y3[i, j, :] = x[2 - j, i, :]


# %% Functions - _draw_cube
def _draw_cube(ax, xs=0, ys=0, zs=0, color="k"):
    r"""
    Draws a 3D plot of the cube at a possibly shifted position, with a given color.

    Parameters
    ----------
    ax : matplotlib.pyplot.figure.axis
        Axis to draw the cube on, axis must be a 3D projection
    xs : int, optional
        Amount to shift the cube in the X direction
    ys : int, optional
        Amount to shift the cube in the Y direction
    zs : int, optional
        Amount to shift the cube in the Z direction
    color : str, optional
        Color code to use to override the default of black

    Notes
    -----
    #.  Written by David C. Stauffer in June 2015.

    Examples
    --------
    >>> from dstauffman2.games.brick import _draw_cube
    >>> import matplotlib.pyplot as plt
    >>> plt.ioff()
    >>> fig = plt.figure()
    >>> ax = fig.add_subplot(111, projection='3d')
    >>> _draw_cube(ax)
    >>> plt.show(block=False) # doctest: +SKIP

    Close the plot
    >>> plt.close(fig)

    """
    #               face 1     face 2     face 3     face 4     face 5     face 6
    x = np.array([[0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 1, 1], [0, 0, 1, 1], [0, 0, 0, 0], [1, 1, 1, 1]]) + xs
    y = np.array([[0, 0, 1, 1], [0, 0, 1, 1], [0, 0, 0, 0], [1, 1, 1, 1], [0, 1, 1, 0], [0, 1, 1, 0]]) + ys
    z = np.array([[0, 0, 0, 0], [1, 1, 1, 1], [0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 1, 1], [0, 0, 1, 1]]) + zs
    # loop through the 6 faces of the cube
    for i in range(len(x)):
        # collect the four vertices for each face
        verts = np.array([x[i], y[i], z[i]]).T
        # create a 3D poly shape and set the desired colors
        poly = Poly3DCollection([verts], facecolors=color, edgecolors="k")
        line = Line3DCollection([verts], colors="k", linewidths=0.6, linestyles=":")
        # add the shape to the specified axis
        ax.add_collection3d(poly)
        ax.add_collection3d(line)


def _check_seams(piece_combos, this_soln):
    r"""
    Checks that the solution set is physically able to be built based on where the seams
    on the individual pieces are located.

    Parameters
    ----------
    piece_combos : list of (3,3,3) ndarray of int
        All the possible piece combinations
    this_soln : ndarray of len 9
        The indices into piece_combos to pull out which ones are in this solution

    Returns
    -------
    is_valid : bool
        True if all the seams are non-overlapping, otherwise False

    Notes
    -----
    #.  Written by David C. Stauffer in June 2015.

    Examples
    --------
    >>> from dstauffman2.games.brick import apply_solution_to_combos, pieces, get_all_positions, R, \
    ...     soln, solve_puzzle, _check_seams
    >>> soln[1,1,1] = R
    >>> combos = [get_all_positions(piece) for piece in pieces]
    >>> piece_combos = [apply_solution_to_combos(soln, this_combo) for this_combo in combos]
    >>> soln_pieces = solve_puzzle(piece_combos)
    >>> is_valid = _check_seams(piece_combos, soln_pieces[0])
    >>> print(is_valid)
    False

    """
    # intiailize a set for use later
    seams = set()
    # build this list of all diagonally adjacent cubes to check
    permutations = [(1,1,0),(1,-1,0),(-1,1,0),(-1,-1,0),(1,0,1),(1,0,-1),(-1,0,1),(-1,0,-1), \
        (0,1,1),(0,1,-1),(0,-1,1),(0,-1,-1)]
    # loop through the piecese
    for p in range(NUM_PIECES):
        # alias this piece
        this_piece = piece_combos[p][this_soln[p]]
        # initialize a list
        this_list = []
        # loop through each piece in the 3x3x3 grid
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    # see if this piece is not null
                    if this_piece[i, j, k] != N:
                        # go through all the possibly adjacent cubes
                        for perm in permutations:
                            # see if this adjacent cube is within the 3x3x3 bounds
                            if not set((i + perm[0], j + perm[1], k + perm[2])) - {0, 1, 2}:
                                # check if this valid adjacent cube is not null
                                if this_piece[i + perm[0], j + perm[1], k + perm[2]] != N:
                                    # append this seam to the list
                                    this_list.append((2 * np.array([i, j, k]) + np.array(perm)) / 2)
        # make a set of the seams that were found (eliminates duplicates within one piece)
        this_set = set(tuple(x) for x in this_list)
        # see if any of the seams overlap with a previous piece
        intersect = seams & this_set
        if intersect:
            # if the seams overlap, then this is not valid and you can exit
            return False
        else:
            # if they don't overlap, then combine the sets and go to the next piece
            seams = seams | this_set
    return True


# %% Functions - solve_center
def solve_center(pieces):
    r"""
    Solve for the color of the center piece.

    Parameters
    ----------
    pieces : list of 3x3x3 int array
        All 9 pieces

    Returns
    -------
    center : int
        The color of the center piece

    Notes
    -----
    #.  Written by David C. Stauffer in June 2015.

    Examples
    --------
    >>> from dstauffman2.games.brick import solve_center, pieces
    >>> center = solve_center(pieces)
    >>> print(center)
    1

    """
    # initialize the unknown answer
    center = E
    p_red  = 0
    p_gry  = 0
    # count the numbers of red and gray pieces in the known solution
    s_red  = np.count_nonzero(soln.ravel() == R)
    s_gry  = np.count_nonzero(soln.ravel() == G)
    # count the numbers of red and gray pieces in the total collection of pieces
    p_red = np.count_nonzero(np.array([x.ravel() for x in pieces]) == R)
    p_gry = np.count_nonzero(np.array([x.ravel() for x in pieces]) == G)
    # find the differences
    d_red = p_red - s_red
    d_gry = p_gry - s_gry
    # if exactly one difference in one color, and nothing in the other, then the solution is found
    if d_red == 0 and d_gry == 1:
        center = G
    elif d_red == 1 and d_gry == 0:
        center = R
    elif d_red == 0 and d_gry == 0:
        # Already solved and this function was called again, so return the current center color
        center = soln[1, 1, 1]
    else:
        raise ValueError("Unable to solve for center color.")
    return center


# %% Functions - rot_piece
def rot_piece(piece, axis):
    r"""
    Rotates the piece about the given axis.

    Parameters
    ----------
    piece : (3,3,3) ndarray of int
        Puzzle piece
    axis : int
        Axis to rotate about (assumed to be a positive 90 degree rotation)

    Notes
    -----
    #.  Written by David C. Stauffer in June 2015.

    Examples
    --------
    >>> from dstauffman2.games.brick import rot_piece, N, R
    >>> import numpy as np
    >>> piece = np.array([\
    ...    [[R, N, N],[N, N, N],[N, N, N]], \
    ...    [[R, N, N],[N, N, N],[N, N, N]], \
    ...    [[R, N, N],[N, N, N],[N, N, N]]])
    >>> axis = 1
    >>> new_piece = rot_piece(piece, axis)
    >>> print(new_piece)
    [[[0 0 0]
      [0 0 0]
      [0 0 0]]
    <BLANKLINE>
     [[0 0 0]
      [0 0 0]
      [0 0 0]]
    <BLANKLINE>
     [[1 1 1]
      [0 0 0]
      [0 0 0]]]

    """
    # build the correct map based on the given axis
    if axis == 0:
        map_ = np.array([6, 3, 0, 7, 4, 1, 8, 5, 2, 15, 12, 9, 16, 13, 10, 17, 14, 11, 24, 21, 18, 25, 22, 19, 26, 23, 20])
    elif axis == 1:
        map_ = np.array([2, 11, 20, 5, 14, 23, 8, 17, 26, 1, 10, 19, 4, 13, 22, 7, 16, 25, 0, 9, 18, 3, 12, 21, 6, 15, 24])
    elif axis == 2:
        map_ = np.array([18, 19, 20, 9, 10, 11, 0, 1, 2, 21, 22, 23, 12, 13, 14, 3, 4, 5, 24, 25, 26, 15, 16, 17, 6, 7, 8])
    else:
        # throw an error for any unexpected axes
        raise ValueError("Unexpected axis to rotate.")
    # rotate the piece by using the map and return
    new_piece = piece.ravel()[map_].reshape(3, 3, 3)
    return new_piece


# %% Functions - trans_piece
def trans_piece(piece, axis, step):
    r"""
    Translates the piece in the given axis by the given number of steps.

    Parameters
    ----------
    piece : (3,3,3) ndarray of int
        Piece layout
    axis : int
        Axis to translate along
    step :
        Number of steps to tranlate along axis

    Returns
    -------
    new_piece : 3x3x3 int array or None
        New piece location, None means the translation was not valid

    Notes
    -----
    #.  Written by David C. Stauffer in June 2015.

    Examples
    --------
    >>> from dstauffman2.games.brick import trans_piece, R, N
    >>> import numpy as np
    >>> piece = np.array([\
    ...    [[R, N, N],[N, N, N],[N, N, N]], \
    ...    [[R, N, N],[N, N, N],[N, N, N]], \
    ...    [[R, N, N],[N, N, N],[N, N, N]]])
    >>> axis = 1
    >>> step = 1
    >>> new_piece = trans_piece(piece, axis, step)
    >>> print(new_piece)
    [[[0 0 0]
      [1 0 0]
      [0 0 0]]
    <BLANKLINE>
     [[0 0 0]
      [1 0 0]
      [0 0 0]]
    <BLANKLINE>
     [[0 0 0]
      [1 0 0]
      [0 0 0]]]

    """
    # initialize piece
    new_piece = piece.copy()
    # find axis
    if axis == 0:
        # loop through number of steps
        for i in range(step):
            # determine if the step is valid
            if np.any(new_piece[2, :, :] != N):
                return None
            # make the step
            new_piece[2, :, :] = new_piece[1, :, :]
            new_piece[1, :, :] = new_piece[0, :, :]
            new_piece[0, :, :] = N
    elif axis == 1:
        for i in range(step):
            if np.any(new_piece[:, 2, :] != N):
                return None
            new_piece[:, 2, :] = new_piece[:, 1, :]
            new_piece[:, 1, :] = new_piece[:, 0, :]
            new_piece[:, 0, :] = N
    elif axis == 2:
        for i in range(step):
            if np.any(new_piece[:, :, 2] != N):
                return None
            new_piece[:, :, 2] = new_piece[:, :, 1]
            new_piece[:, :, 1] = new_piece[:, :, 0]
            new_piece[:, :, 0] = N
    else:
        raise ValueError("Unexpected value for axis = {}.".format(axis))
    return new_piece


# %% Functions - get_all_positions
def get_all_positions(piece):
    r"""
    Gets all the possible positions for the given piece.

    This function determines all the possible positions by first rotating about all three axes,
    then shifting up to two 2 steps in either direction, then rotating again, and then shifting again.

    Parameters
    ----------
    piece : (3,3,3) ndarray of int
        Piece layout

    Returns
    -------
    all_pos : list of (3,3,3) ndarray of int
        List of all possible position and orientations of the given piece.

    Notes
    -----
    #.  Written by David C. Stauffer in June 2015.
    #.  This does not take into account the solution color pattern, that is done afterwards.

    Examples
    --------
    >>> from dstauffman2.games.brick import get_all_positions, R, N
    >>> import numpy as np
    >>> piece = np.array([\
    ...    [[R, N, N],[N, N, N],[N, N, N]], \
    ...    [[R, N, N],[N, N, N],[N, N, N]], \
    ...    [[R, N, N],[N, N, N],[N, N, N]]])
    >>> all_pos = get_all_positions(piece)
    >>> print(len(all_pos))
    27

    """

    def _rotations(all_pos):
        r"""
        Rotates the list of pieces about all 24 possible 3D orientations.

        Notes
        -----
        #.  Modifies `all_pos` in-place.
        """
        # loop through the current list (use index to avoid infinite loops while growing in place)
        for i in range(len(all_pos)):
            this_pos = all_pos[i]
            # rotate four times about the first axis
            for j in range(4):
                this_pos = rot_piece(this_pos, axis=0)
                # keep the first 3, the 4th puts you back at the beginning
                if j < 3:
                    all_pos.append(this_pos)
            for k in range(3):
                # now rotate once about the 2nd axis and repeat
                this_pos = rot_piece(this_pos, axis=1)
                for j in range(4):
                    this_pos = rot_piece(this_pos, axis=0)
                    all_pos.append(this_pos)
            # rotate once more to get back to original
            this_pos = rot_piece(this_pos, axis=1)
            # then rotate once about the 3rd axis and four times about the first
            this_pos = rot_piece(this_pos, axis=2)
            for j in range(4):
                this_pos = rot_piece(this_pos, axis=0)
                all_pos.append(this_pos)
            # then rotate twice about the 3rd axis, and then four times about the first
            for k in range(2):
                this_pos = rot_piece(this_pos, axis=2)
            for j in range(4):
                this_pos = rot_piece(this_pos, axis=0)
                all_pos.append(this_pos)

    def _translations(all_pos):
        r"""
        Translates the list of pieces up to two spaces in either direction along all three axes.

        Notes
        -----
        #.  Written by David C. Stauffer in June 2015.
        #.  Modifies `all_pos` in-place.
        """
        # translate all rotations
        for i in range(len(all_pos)):
            this_rot = all_pos[i]
            # about all 3 axes
            for axis in range(3):
                # up to two steps in each direction
                for step in [-2, -1, 1, 2]:
                    # get the new position
                    new_pos = trans_piece(this_rot, axis, step)
                    # if it's not None, then the translation was successful, and this piece should be kept
                    if new_pos is not None:
                        all_pos.append(new_pos)

    def _keep_unique(all_pos):
        r"""
        Keeps only the unique permutations from all possible piece layouts.

        Notes
        -----
        #.  Written by David C. Stauffer in 2015.
        #.  Does not take symmetry into account.
        """
        # convert to N positions by 27 element linear array
        all_rows = np.array([x.ravel() for x in all_pos])
        # find the unique rows
        uniq_rows = np.unique(all_rows, axis=0)
        # convert back to N element list of 3x3x3 pieces
        pieces = []
        for i in range(uniq_rows.shape[0]):
            pieces.append(uniq_rows[i, :].reshape(SIZE_PIECES))
        return pieces

    # initialize a new list
    all_pos = []
    # get the starting piece and append it to the list
    all_pos.append(piece.copy())
    # repeat this process three times to get all the possible combinations of rotations and translations
    for i in range(3):
        # go through rotations (produces up to 24x orientations)
        _rotations(all_pos)
        # keep unique ones
        all_pos = _keep_unique(all_pos)
        # go through translations (produces up to 12x translations)
        _translations(all_pos)
        # keep unique ones
        all_pos = _keep_unique(all_pos)
    return all_pos


# %% Functions - plot_cube
def plot_cube(piece, title=None, opts=None):
    r"""
    Plots the given cube as a 3D plot.

    Parameters
    ----------
    cube : (3,3,3) ndarray of int
        Piece layout
    title : str, optional
        Title to put on the plot and use to save to disk
    opts : class dstauffman.Opts, optional
        Plotting options

    Returns
    -------
    fig : class matplotlib.pyplot.figure
        Figure handle

    Notes
    -----
    #.  Written by David C. Stauffer in June 2015.

    Examples
    --------
    >>> from dstauffman2.games.brick import plot_cube, R, N
    >>> import numpy as np
    >>> piece = np.array([\
    ...    [[R, N, N],[N, N, N],[N, N, N]], \
    ...    [[R, N, N],[N, N, N],[N, N, N]], \
    ...    [[R, N, N],[N, N, N],[N, N, N]]])
    >>> fig = plot_cube(piece, title='Test Plot')

    Close plot
    >>> import matplotlib.pyplot as plt
    >>> plt.close(fig)

    """
    # check for opts
    if opts is None:
        opts = Opts()
    # turn interactive plotting off
    plt.ioff()
    # create the figure
    fig = plt.figure()
    # create the axis
    ax = fig.add_subplot(111, projection="3d")
    # TODO: put back once MPL is fixed: ax.set_aspect('equal')
    # set the title
    if title is not None:
        fig.canvas.manager.set_window_title(title)
        ax.set_title(title)
    # draw each of the 27 cubes
    for i in range(3):
        for j in range(3):
            for k in range(3):
                _draw_cube(ax, xs=i, ys=j, zs=k, color=_get_color(piece[i, j, k]))

    # set the limits
    ax.set_xlim3d(-1, 4)
    ax.set_ylim3d(-1, 4)
    ax.set_zlim3d(-1, 4)

    # Turn the tick labels off
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zticklabels([])

    # configure the plot
    setup_plots(fig, opts)

    # return the resulting figure handle
    return fig


# %% Functions - print_combos
def print_combos(piece_combos, text):
    r"""
    Print the possible combos.

    Parameters
    ----------
    piece_combos : list of (3,3,3) ndarray of int
        All the possible piece combinations

    Notes
    -----
    #.  Written by David C. Stauffer in June 2015.

    Examples
    --------
    >>> from dstauffman2.games.brick import print_combos, pieces, get_all_positions
    >>> piece_combos = [get_all_positions(piece) for piece in pieces]
    >>> text = 'testing'
    >>> print_combos(piece_combos, text) # doctest: +ELLIPSIS
    Piece 1 has 27 testing combinations
    Piece 2 has ... testing combinations
    Piece 3 has ... testing combinations
    Piece 4 has ... testing combinations
    Piece 5 has ... testing combinations
    Piece 6 has ... testing combinations
    Piece 7 has ... testing combinations
    Piece 8 has ... testing combinations
    Piece 9 has ... testing combinations
    <BLANKLINE>

    """
    for i in range(NUM_PIECES):
        print("Piece {} has {} {} combinations".format(i + 1, len(piece_combos[i]), text))
    print("")


# %% Functions - apply_solution_to_combos
def apply_solution_to_combos(soln, combos):
    r"""
    Applies the known solution to restrict the piece combinations to only those that fit.

    Parameters
    ----------
    soln : (3,3,3) ndarray of int
        Solution
    combos : list of (3,3,3) ndarray of int
        Possible piece combinations

    Returns
    -------
    valid : list of (3,3,3) ndarray of int
        Valid piece combinations based on solution

    Notes
    -----
    #.  Written by David C. Stauffer in June 2015.

    Examples
    --------
    >>> from dstauffman2.games.brick import apply_solution_to_combos, pieces, get_all_positions, soln, solve_center
    >>> soln[1,1,1] = solve_center(pieces)
    >>> combos = [get_all_positions(piece) for piece in pieces]
    >>> valid = apply_solution_to_combos(soln, combos[0])
    >>> print(len(combos[0]))
    27
    >>> print(len(valid))
    4

    """
    # convert combos to 2D array
    all_rows = np.array([x.ravel() for x in combos])
    # convert solution to vector
    soln_row = soln.ravel()
    # compare the pieces to the solution
    valid_ix = np.flatnonzero(np.all((all_rows == soln_row) | (all_rows == N), axis=1))
    # save only the valid combinations and return
    valid = [combos[x] for x in valid_ix]
    return valid


# %% Functions - solve_puzzle
def solve_puzzle(piece_combos, stop_at_first=False, check_seams=True):
    r"""
    Solves the puzzle once all the possible piece combinations have been found.

    Parameters
    ----------
    piece_combos : list of (3,3,3) ndarray of int
        Piece combinations
    stop_at_first : bool, optional (False)
        Stop at the first valid solution
    check_seams : bool, optional (True)
        Check the physical seams to make sure the puzzle can be assembled

    Returns
    -------
    soln_pieces : list of ndarray
        Indices to the combinations for each piece that solve the puzzle

    Notes
    -----
    #.  Written by David C. Stauffer in June 2015.

    Examples
    --------
    >>> from dstauffman2.games.brick import apply_solution_to_combos, pieces, get_all_positions, R, \
    ...     soln, solve_puzzle
    >>> soln[1,1,1] = R
    >>> combos = [get_all_positions(piece) for piece in pieces]
    >>> piece_combos = [apply_solution_to_combos(soln, this_combo) for this_combo in combos]
    >>> soln_pieces = solve_puzzle(piece_combos)
    >>> print(soln_pieces[0])
    [ 0  4 14  3  5 23  5  4  0]

    """

    def _get_solution_sum(level):
        soln_sum = r_comb[0][i0]
        if level >= 1:
            soln_sum = soln_sum + r_comb[1][i1]
        if level >= 2:
            soln_sum = soln_sum + r_comb[2][i2]
        if level >= 3:
            soln_sum = soln_sum + r_comb[3][i3]
        if level >= 4:
            soln_sum = soln_sum + r_comb[4][i4]
        if level >= 5:
            soln_sum = soln_sum + r_comb[5][i5]
        if level >= 6:
            soln_sum = soln_sum + r_comb[6][i6]
        if level >= 7:
            soln_sum = soln_sum + r_comb[7][i7]
        return soln_sum

    # initialize output
    soln_pieces = []
    # r_comb = [cube.ravel() for cube in this_piece for this_piece in piece_combos]
    r_comb = []
    for i in range(NUM_PIECES):
        temp = []
        for j in range(len(piece_combos[i])):
            temp.append(piece_combos[i][j].ravel())
        r_comb.append(np.array(temp))
    for i0 in range(len(r_comb[0])):
        # check for all possible combinations of the next piece that work.
        soln1 = _get_solution_sum(0) * r_comb[1]
        ix1 = np.flatnonzero(np.sum(soln1, axis=1) == 0)
        # if no pieces work, then continue to the next base piece
        if ix1.shape[0] == 0:
            continue
        # otherwise continue down the spiral of pieces
        for i1 in ix1:
            soln2 = _get_solution_sum(1) * r_comb[2]
            ix2 = np.flatnonzero(np.sum(soln2, axis=1) == 0)
            if ix2.shape[0] == 0:
                continue
            for i2 in ix2:
                soln3 = _get_solution_sum(2) * r_comb[3]
                ix3 = np.flatnonzero(np.sum(soln3, axis=1) == 0)
                if ix3.shape[0] == 0:
                    continue
                for i3 in ix3:
                    soln4 = _get_solution_sum(3) * r_comb[4]
                    ix4 = np.flatnonzero(np.sum(soln4, axis=1) == 0)
                    if ix4.shape[0] == 0:
                        continue
                    for i4 in ix4:
                        soln5 = _get_solution_sum(4) * r_comb[5]
                        ix5 = np.flatnonzero(np.sum(soln5, axis=1) == 0)
                        if ix5.shape[0] == 0:
                            continue
                        for i5 in ix5:
                            soln6 = _get_solution_sum(5) * r_comb[6]
                            ix6 = np.flatnonzero(np.sum(soln6, axis=1) == 0)
                            if ix6.shape[0] == 0:
                                continue
                            for i6 in ix6:
                                soln7 = _get_solution_sum(6) * r_comb[7]
                                ix7 = np.flatnonzero(np.sum(soln7, axis=1) == 0)
                                if ix7.shape[0] == 0:
                                    continue
                                for i7 in ix7:
                                    soln8 = _get_solution_sum(7) * r_comb[8]
                                    ix8 = np.flatnonzero(np.sum(soln8, axis=1) == 0)
                                    if ix8.shape[0] == 0:
                                        continue
                                    # potential solution found, but must check seams!
                                    this_soln = np.array([i0, i1, i2, i3, i4, i5, i6, i7, ix8[0]])
                                    if check_seams:
                                        is_valid = _check_seams(piece_combos, this_soln)
                                    else:
                                        is_valid = True
                                    if is_valid:
                                        # append any valid solutions
                                        soln_pieces.append(this_soln)
                                        if stop_at_first:
                                            return soln_pieces
    return soln_pieces


# %% Funccions - discard_symmetric_duplicates
def discard_symmetric_duplicates(soln_pieces, piece_combos):
    r"""Discards solutions that are only rotations of other solutions."""

    def _make_equal_solns(piece):
        # initialize output and counter
        pieces_array = np.empty((27, 8), dtype=int)
        counter = 0
        # create a temp variable to use
        temp_piece = piece.copy()
        # store the original position
        pieces_array[:, 0] = temp_piece.ravel()
        counter += 1
        # create all possible permutations
        for i in range(4):
            temp_piece = rot_piece(temp_piece, axis=0)
            if i < 3:
                pieces_array[:, counter] = temp_piece.ravel()
                counter += 1
        # rotate 180 degrees
        temp_piece = rot_piece(temp_piece, axis=1)
        temp_piece = rot_piece(temp_piece, axis=1)
        # repeat rotations
        for i in range(4):
            pieces_array[:, counter] = temp_piece.ravel()
            temp_piece = rot_piece(temp_piece, axis=0)
            counter += 1
        return pieces_array

    # initialize the output variable
    reduced_soln_pieces = []
    # append the first solution, it's unique by definition, with an if block in case no solutions were found
    if soln_pieces:
        reduced_soln_pieces.append(soln_pieces[0])
    # loop through the remaining pieces
    for i in range(1, len(soln_pieces)):
        if np.all(np.prod(soln_pieces[i] - np.array(reduced_soln_pieces), axis=1) == 0):
            # solution has at least one piece matching another answer, so it can't be strictly
            # symmetric and thus must be new.
            reduced_soln_pieces.append(soln_pieces[i])
        else:
            # solution may be a symmetric copy
            # TODO: might not be, put additional test here!!!
            pass
    return reduced_soln_pieces


# %% Functions - test_docstrings
def test_docstrings():
    r"""Tests the docstrings within this file."""
    file = os.path.join(get_root_dir(), "games", "brick.py")
    doctest.testfile(file, report=True, verbose=False, module_relative=True)


# %% Main script
if __name__ == "__main__":
    # flags for running code
    run_tests    = True
    make_plots   = True
    make_soln    = True

    if run_tests:
        # Run docstring test
        test_docstrings()

    if make_soln:
        # Create and set Opts
        date = datetime.now()
        opts = Opts()
        opts.case_name = "Brick"
        opts.save_path = os.path.join(get_root_dir(), "results", date.strftime("%Y-%m-%d") + "_brick")
        opts.save_plot = True
        opts.show_plot = False
        if make_plots:
            setup_dir(opts.save_path, rec=True)

        # Solve for the center color
        soln[1, 1, 1] = solve_center(pieces)

        if make_plots:
            # plot the cube
            plot_cube(soln, title="Final Solution", opts=opts)

        # find all possible orientations of all pieces
        all_piece_combos = []
        for this_piece in pieces:
            all_piece_combos.append(get_all_positions(this_piece))

        # Print the total combinations before simplifying to the solution
        print_combos(all_piece_combos, "total")

        # Solve for only the valid piece combinations
        piece_combos = [apply_solution_to_combos(soln, this_piece_combos) for this_piece_combos in all_piece_combos]

        # Print the total combinations after simplifying to the solution
        print_combos(piece_combos, "valid")

        # Plot all the piece combinations and save to disk
        if make_plots:
            for i in range(NUM_PIECES):
                for j, this_piece in enumerate(piece_combos[i]):
                    plot_cube(this_piece, title="P{} position {}".format(i + 1, j + 1), opts=opts)
                    for this_fig in plt.get_fignums():
                        plt.close(this_fig)

        # sort pieces by their number of combinations
        num_combos = [len(x) for x in piece_combos]
        sort_ix = np.argsort(num_combos)
        piece_combos = [piece_combos[x] for x in sort_ix]

        # solve puzzle
        soln_pieces_all = solve_puzzle(piece_combos)

        # discard duplicates based on symmetry
        soln_pieces = discard_symmetric_duplicates(soln_pieces_all, piece_combos)

        # verify solution
        for ix, this_soln in enumerate(soln_pieces):
            soln2 = 0
            for i in range(NUM_PIECES):
                soln2 = soln2 + piece_combos[i][this_soln[i]]
            np.testing.assert_array_equal(soln, soln2)

        # print/save solution sets
        unsort_ix = np.argsort(sort_ix)
        for j in range(len(soln_pieces)):
            if make_plots:
                setup_dir(os.path.join(opts.save_path, "soln{}".format(j + 1)))
            print("Solution #{}".format(j + 1))
            for i in range(NUM_PIECES):
                print("Piece {}, position {}".format(i + 1, soln_pieces[j][unsort_ix[i]] + 1))
                if make_plots:
                    old_name = os.path.join(opts.save_path, '{} - P{} position {}.png'.format(opts.case_name, i+1, soln_pieces[j][unsort_ix[i]]+1))
                    new_name = os.path.join(opts.save_path, 'soln{}'.format(j+1), '{} - P{} position {}.png'.format(opts.case_name, i+1, soln_pieces[j][unsort_ix[i]]+1))
                    shutil.copyfile(old_name, new_name)
            print("")
            if make_plots:
                old_name = os.path.join(opts.save_path, '{} - Final Solution.png'.format(opts.case_name))
                new_name = os.path.join(opts.save_path, 'soln{}'.format(j+1), '{} - Final Solution.png'.format(opts.case_name))
                shutil.copyfile(old_name, new_name)
