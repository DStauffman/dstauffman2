r"""
Test file for the `tictactoe.utils` module of the dstauffman2 code.  It is intented to contain test
cases to demonstrate functionaliy and correct outcomes for all the functions within the module.

Notes
-----
#.  Written by David C. Stauffer in January 2016.
"""

# %% Imports
import inspect
import os
import unittest

import matplotlib.pyplot as plt
import numpy as np

from dstauffman import Counter

import dstauffman2.games.tictactoe as ttt

# %% Aliases
o = ttt.PLAYER["o"]
x = ttt.PLAYER["x"]
n = ttt.PLAYER["none"]


# %% Functions - _make_board
def _make_board():
    r"""Makes a board and returns the figure and axis for use in testing."""
    plt.ioff()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlim(-0.5, 2.5)
    ax.set_ylim(-0.5, 2.5)
    ax.invert_yaxis()
    return (fig, ax)


# %% get_root_dir
class Test_get_root_dir(unittest.TestCase):
    r"""
    Tests the get_root_dir function with these cases:
        call the function
    """

    def test_function(self):
        filepath = inspect.getfile(ttt.get_root_dir)
        expected_root = os.path.split(filepath)[0]
        folder = ttt.get_root_dir()
        self.assertEqual(folder, expected_root)
        self.assertTrue(os.path.isdir(folder))


# %% calc_cur_move
class Test_calc_cur_move(unittest.TestCase):
    r"""
    Tests the _board_to_costs function with the following cases:
        Odd game, odd move
        Odd game, even move
        Even game, odd move
        Even game, even move
    """

    def setUp(self):
        self.odd_num  = 3
        self.even_num = 4
        self.o        = o
        self.x        = x

    def test_odd_odd(self):
        move = ttt.calc_cur_move(self.odd_num, self.odd_num)
        self.assertEqual(move, o)

    def test_odd_even(self):
        move = ttt.calc_cur_move(self.odd_num, self.even_num)
        self.assertEqual(move, x)

    def test_even_odd(self):
        move = ttt.calc_cur_move(self.even_num, self.odd_num)
        self.assertEqual(move, x)

    def test_even_even(self):
        move = ttt.calc_cur_move(self.even_num, self.even_num)
        self.assertEqual(move, o)


# %% check_for_win
class Test_check_for_win(unittest.TestCase):
    r"""
    Tests the check_for_win function with the following cases:
        No Moves
        No winner
        X wins
        O wins
        x wins multiple lines
        draw with no moves left
        draw with simultaneous wins
    """

    def setUp(self):
        self.board = np.full((3, 3), n, dtype=int)
        self.win_mask = np.zeros((3, 3), dtype=bool)

    def test_no_moves(self):
        (winner, win_mask) = ttt.check_for_win(self.board)
        self.assertEqual(winner, n)
        np.testing.assert_array_equal(win_mask, self.win_mask)

    def test_no_winner(self):
        self.board[0, 0] = x
        self.board[1, 1] = o
        (winner, win_mask) = ttt.check_for_win(self.board)
        self.assertEqual(winner, n)
        np.testing.assert_array_equal(win_mask, self.win_mask)

    def test_x_wins(self):
        self.board[0:3, 0] = x
        self.board[1:3, 1] = o
        self.win_mask[0:3, 0] = True
        (winner, win_mask) = ttt.check_for_win(self.board)
        self.assertEqual(winner, x)
        np.testing.assert_array_equal(win_mask, self.win_mask)

    def test_o_wins(self):
        self.board[2, 0:3] = o
        self.board[1, 0:2] = x
        self.win_mask[2, 0:3] = True
        (winner, win_mask) = ttt.check_for_win(self.board)
        self.assertEqual(winner, o)
        np.testing.assert_array_equal(win_mask, self.win_mask)

    def test_black_wins_mult(self):
        self.board[0, 0] = o
        self.board[0, 1] = o
        self.board[0, 2] = x
        self.board[1, 0] = o
        self.board[1, 1] = x
        self.board[1, 2] = o
        self.board[2, 0] = x
        self.board[2, 1] = x
        self.board[2, 2] = x
        (winner, win_mask) = ttt.check_for_win(self.board)
        self.assertEqual(winner, x)
        win_mask2 = self.board == x
        np.testing.assert_array_equal(win_mask, win_mask2)

    def test_draw_no_moves_left(self):
        self.board[0, 0] = o
        self.board[0, 1] = o
        self.board[0, 2] = x
        self.board[1, 0] = x
        self.board[1, 1] = x
        self.board[1, 2] = o
        self.board[2, 0] = o
        self.board[2, 1] = o
        self.board[2, 2] = x
        (winner, win_mask) = ttt.check_for_win(self.board)
        self.assertEqual(winner, ttt.PLAYER["draw"])
        np.testing.assert_array_equal(win_mask, self.win_mask)

    def test_draw_simult_wins(self):
        self.board[0, :] = o
        self.board[1, :] = x
        (winner, win_mask) = ttt.check_for_win(self.board)
        self.assertEqual(winner, ttt.PLAYER["draw"])
        win_mask2 = (self.board == x) | (self.board == o)
        np.testing.assert_array_equal(win_mask, win_mask2)


# %% find_moves
class Test_find_moves(unittest.TestCase):
    r"""
    Tests the find_moves function with the following cases:
        TBD
    """

    def setUp(self):
        self.board = np.zeros((3, 3), dtype=int)

    def test_no_wins(self):
        (white_moves, black_moves) = ttt.find_moves(self.board)
        self.assertEqual(white_moves[0], ttt.Move(1, 1))
        self.assertEqual(black_moves[0], ttt.Move(1, 1))

    def test_already_won(self):
        self.board[1, 0] = x
        self.board[1, 1] = x
        self.board[1, 2] = x
        with self.assertRaises(ValueError):
            ttt.find_moves(self.board)

    def test_o_place_to_win(self):
        self.board[2, 0] = o
        self.board[2, 1] = o
        (white_moves, black_moves) = ttt.find_moves(self.board)
        self.assertEqual(white_moves[0], ttt.Move(2, 2))
        self.assertEqual(black_moves[0], ttt.Move(2, 2))
        self.assertEqual(white_moves[0].power, 100)
        self.assertEqual(black_moves[0].power, 10)

    def test_wins_blocked(self):
        self.board[2, 0] = o
        self.board[2, 1] = o
        self.board[2, 2] = x
        (white_moves, black_moves) = ttt.find_moves(self.board)
        self.assertEqual(white_moves[0], ttt.Move(1, 1))
        self.assertEqual(black_moves[0], ttt.Move(1, 1))

    def test_no_valid_moves(self):
        self.board[0, 0] = x
        self.board[0, 1] = o
        self.board[0, 2] = x
        self.board[1, 0] = x
        self.board[1, 1] = o
        self.board[1, 2] = o
        self.board[2, 0] = o
        self.board[2, 1] = x
        self.board[2, 2] = o
        with self.assertRaises(AssertionError):
            ttt.find_moves(self.board)

    def test_x_place_to_win(self):
        self.board[0, 0] = x
        self.board[2, 2] = x
        (white_moves, black_moves) = ttt.find_moves(self.board)
        self.assertEqual(white_moves[0], ttt.Move(1, 1))
        self.assertEqual(black_moves[0], ttt.Move(1, 1))
        self.assertEqual(white_moves[0].power, 10)
        self.assertEqual(black_moves[0].power, 100)

    def test_same_win_square(self):
        self.board[0, 0] = x
        self.board[2, 2] = x
        self.board[1, 0] = o
        self.board[1, 2] = o
        (white_moves, black_moves) = ttt.find_moves(self.board)
        self.assertEqual(white_moves[0], ttt.Move(1, 1))
        self.assertEqual(black_moves[0], ttt.Move(1, 1))
        self.assertEqual(white_moves[0].power, 100)
        self.assertEqual(black_moves[0].power, 100)

    def test_one_from_win_move(self):
        self.board[0, 1] = o
        self.board[1, 2] = o
        self.board[1, 1] = x
        (white_moves, black_moves) = ttt.find_moves(self.board)
        self.assertEqual(white_moves[0], ttt.Move(0, 2))
        self.assertEqual(black_moves[0], ttt.Move(0, 2))
        self.assertEqual(white_moves[0].power, 6)
        self.assertEqual(black_moves[0].power, 5)

    def test_another_off_one_win(self):
        self.board[0, 0] = o
        self.board[0, 1] = x
        self.board[1, 2] = x
        (white_moves, black_moves) = ttt.find_moves(self.board)
        self.assertEqual(white_moves[0], ttt.Move(1, 1))
        self.assertEqual(black_moves[0], ttt.Move(1, 1))
        self.assertEqual(white_moves[0].power, 5)
        self.assertEqual(black_moves[0].power, 6)

    def test_double_win_in_two(self):
        self.board[0, 1] = o
        self.board[1, 2] = o
        self.board[1, 0] = x
        self.board[2, 1] = x
        (white_moves, black_moves) = ttt.find_moves(self.board)
        self.assertEqual(white_moves[0], ttt.Move(0, 2))
        self.assertEqual(black_moves[0], ttt.Move(2, 0))
        self.assertEqual(white_moves[0].power, 6)
        self.assertEqual(black_moves[0].power, 6)
        self.assertEqual(white_moves[1], ttt.Move(2, 0))
        self.assertEqual(black_moves[1], ttt.Move(0, 2))
        self.assertEqual(white_moves[1].power, 5)
        self.assertEqual(black_moves[1].power, 5)


# %% make_move
class Test_make_move(unittest.TestCase):
    r"""
    Tests the make_move function with the following cases:
        Nominal
    """

    def setUp(self):
        (self.fig, self.ax) = _make_board()
        self.board = np.full((3, 3), n, dtype=int)

    def test_first_and_second_move(self):
        board = self.board.copy()
        xc = 1
        yc = 0
        cur_move = Counter(0)
        cur_game = Counter(0)
        game_hist = [ttt.GameStats(1, o)]
        self.assertEqual(cur_move, 0)
        self.assertEqual(len(game_hist[0].move_list), 0)
        np.testing.assert_array_equal(board, self.board)
        ttt.make_move(self.ax, board, xc, yc, cur_move, cur_game, game_hist)
        self.assertEqual(cur_move, 1)
        self.assertEqual(len(game_hist[0].move_list), 1)
        self.board[1, 0] = o
        np.testing.assert_array_equal(board, self.board)
        yc = 1
        ttt.make_move(self.ax, board, xc, yc, cur_move, cur_game, game_hist)
        self.assertEqual(cur_move, 2)
        self.assertEqual(len(game_hist[0].move_list), 2)
        self.board[1, 1] = x
        np.testing.assert_array_equal(board, self.board)

    def test_inserting_move(self):
        board = self.board.copy()
        xc = 2
        yc = 2
        cur_move = Counter(1)  # 2 would be the next move, 1 makes this replace the last move
        cur_game = Counter(1)
        game_hist = [ttt.GameStats(1, o), ttt.GameStats(2, x)]
        game_hist[1].add_move(ttt.Move(0, 0))
        game_hist[1].add_move(ttt.Move(1, 1))  # setting a move that will be replaced
        board[0, 0] = x
        self.assertEqual(game_hist[1].num_moves, 2)
        ttt.make_move(self.ax, board, xc, yc, cur_move, cur_game, game_hist)
        self.assertEqual(cur_move, 2)
        self.assertEqual(cur_game, 1)
        self.board[0, 0] = x
        self.board[2, 2] = o
        np.testing.assert_array_equal(board, self.board)

    def tearDown(self):
        plt.close(self.fig)


# %% play_ai_game
class Test_play_ai_game(unittest.TestCase):
    r"""
    Tests the play_ai_game function with the following cases:
        Nominal (O to play first move)
    """

    def setUp(self):
        (self.fig, self.ax) = _make_board()
        self.board = np.full((3, 3), n, dtype=int)
        self.cur_move = Counter(0)
        self.cur_game = Counter(0)
        self.game_hist = [ttt.GameStats(1, o)]

    def test_nominal(self):
        # set AI options
        ttt.Options.x_is_computer = True
        ttt.Options.o_is_computer = True
        # play game
        board = self.board.copy()
        ttt.play_ai_game(self.ax, board, self.cur_move, self.cur_game, self.game_hist)
        self.board[1, 1] = o
        np.testing.assert_array_equal(board, self.board)
        self.assertEqual(self.cur_move, 1)
        self.assertEqual(self.cur_game, 0)

    def test_two_moves(self):
        # set AI options
        ttt.Options.x_is_computer = True
        ttt.Options.o_is_computer = True
        # play game
        board = self.board.copy()
        ttt.play_ai_game(self.ax, board, self.cur_move, self.cur_game, self.game_hist)
        self.assertEqual(self.cur_move, 1)
        self.assertEqual(self.cur_game, 0)
        ttt.play_ai_game(self.ax, board, self.cur_move, self.cur_game, self.game_hist)
        self.assertEqual(self.cur_move, 2)
        self.assertEqual(self.cur_game, 0)

    def test_no_ai(self):
        # set AI options
        ttt.Options.x_is_computer = False
        ttt.Options.o_is_computer = False
        # play game
        board = self.board.copy()
        ttt.play_ai_game(self.ax, board, self.cur_move, self.cur_game, self.game_hist)
        np.testing.assert_array_equal(board, self.board)
        self.assertEqual(self.cur_move, 0)
        self.assertEqual(self.cur_game, 0)

    def tearDown(self):
        plt.close(self.fig)


# %% create_board_from_moves
class Test_create_board_from_moves(unittest.TestCase):
    r"""
    Tests the create_board_From_moves function with the following cases:
        O to move first
        X to move first
    """

    def setUp(self):
        self.moves = [ttt.Move(0, 0), ttt.Move(1, 1), ttt.Move(2, 1)]
        self.board = np.full((3, 3), n, dtype=int)

    def test_o_first(self):
        first_player     = o
        self.board[0, 0] = o
        self.board[1, 1] = x
        self.board[2, 1] = o
        board = ttt.create_board_from_moves(self.moves, first_player)
        np.testing.assert_array_equal(board, self.board)

    def test_x_first(self):
        first_player = x
        self.board[0, 0] = x
        self.board[1, 1] = o
        self.board[2, 1] = x
        board = ttt.create_board_from_moves(self.moves, first_player)
        np.testing.assert_array_equal(board, self.board)


# %% Unit test execution
if __name__ == "__main__":
    unittest.main(exit=False)
