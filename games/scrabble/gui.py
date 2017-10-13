# -*- coding: utf-8 -*-
r"""
GUI module file for the "scrabble" game.  It defines the GUI.

Notes
-----
#.  Written by David C. Stauffer in March 2017.
"""

#%% Imports
import doctest
import os
import pickle
import sys
import unittest

from matplotlib import colors
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.pyplot import Axes
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QAction, QApplication, QGridLayout, QHBoxLayout, QLabel, QLineEdit, \
    QMainWindow, QPushButton, QToolTip, QVBoxLayout, QWidget

from dstauffman import pprint_dict
from dstauffman2.games.scrabble.classes import Board, Move
from dstauffman2.games.scrabble.constants import COLOR, COUNTS, DICT, SCORES
from dstauffman2.games.scrabble.plotting import display_tile_bag, plot_board, plot_draw_stats, \
    plot_move_strength
from dstauffman2.games.scrabble.utils import get_root_dir

#%% Classes - GuiSettings
class GuiSettings(object):
    r"""
    Settings that capture the current state of the GUI.
    """
    def __init__(self):
        self.board     = Board()
        self.dict_name = DICT
        self.words     = {}
        self.scores    = SCORES
        self.counts    = COUNTS
        self.tiles     = ''
        self.move_list = []
        self.move      = Move()
        self.pot_moves = []

    def pprint(self, indent=2, align=True):
        r"""Prints all the settings outs."""
        pprint_dict(self.__dict__, name=self.__class__.__name__, indent=indent, align=align)

    @staticmethod
    def load(filename):
        r"""Loads a instance of the class from a given filename."""
        with open(filename, 'rb') as file:
            gui_settings = pickle.load(file)
        assert isinstance(gui_settings, GuiSettings)
        return gui_settings

    def save(self, filename):
        r"""Saves an instance of the class to the given filename."""
        with open(filename, 'wb') as file:
            pickle.dump(self, file)

#%% Classes - ScrabbleGui
class ScrabbleGui(QMainWindow):
    r"""
    The Scrabble GUI.
    """
    # Create GUI setting defaults for the class
    gui_settings = GuiSettings()

    def __init__(self):
        # call super method
        super().__init__()
        # call init method to instantiate the GUI
        self.init()

    #%% GUI initialization
    def init(self):
        r"""Initializes the GUI."""
        # Check to see if the Default profile exists, and if so load it, else create it
        folder = get_root_dir()
        filename = os.path.join(folder, 'Default.pkl')
        if os.path.isfile(filename): # pragma: no cover
            self.gui_settings = GuiSettings.load(filename)
        else: # pragma: no cover
            self.gui_settings.save(filename)

        # initialize time
        self.time = QtCore.QTimer(self)

        # properties
        QToolTip.setFont(QtGui.QFont('SanSerif', 10))

        # alias some colors
        tile_color = colors.to_hex(COLOR['tile'])

        # Central Widget
        self.gui_widget  = QWidget(self)
        self.setCentralWidget(self.gui_widget)

        # Panels
        self.grp_tiles  = QWidget()
        self.grp_moves  = QWidget()
        self.grp_left   = QWidget()
        self.grp_center = QWidget()
        self.grp_right  = QWidget()
        self.grp_main   = QWidget()

        #%% Layouts
        layout_gui    = QVBoxLayout(self.gui_widget)
        layout_main   = QHBoxLayout(self.grp_main)
        layout_left   = QVBoxLayout(self.grp_left)
        layout_center = QVBoxLayout(self.grp_center)
        layout_right  = QVBoxLayout(self.grp_right)
        layout_tiles  = QHBoxLayout(self.grp_tiles)
        layout_moves  = QGridLayout(self.grp_moves)

        for layout in [layout_gui, layout_main, layout_left, layout_center, layout_right, layout_tiles, layout_moves]:
            layout.setAlignment(QtCore.Qt.AlignCenter)

        #%% Labels
        lbl_title      = QLabel('Scrabble & Words With Friends Cheater')
        lbl_tile_bag   = QLabel('Tile Bag')
        lbl_draw_stats = QLabel('Draw Stats')
        lbl_strength   = QLabel('Move Strength')
        lbl_moves      = QLabel('Best Moves')

        for label in [lbl_title, lbl_tile_bag, lbl_draw_stats, lbl_strength, lbl_moves]:
            label.setAlignment(QtCore.Qt.AlignCenter)

        #%% Text Edit Boxes
        self.lne_tile_bag = QLineEdit('')

        #%% Axes
        # board
        fig = Figure(figsize=(4.2, 4.2), dpi=100, frameon=False)
        self.board_canvas = FigureCanvas(fig)
        #self.board_canvas.setParent(self.grp_center) # TODO: layout instead?
        self.board_canvas.mpl_connect('button_release_event', lambda event: self.mouse_click_callback(event))
        self.board_axes = Axes(fig, [0., 0., 1., 1.])
        self.board_axes.invert_yaxis()
        fig.add_axes(self.board_axes)

        # draw stats
        fig = Figure(figsize=(2.2, 1.1), dpi=100, frameon=False)
        self.draw_stats_canvas = FigureCanvas(fig)
        #self.draw_stats_canvas.setParent(self.grp_left) # TODO: layout instead?
        self.draw_stats_axes = Axes(fig, [0., 0., 1., 1.])
        fig.add_axes(self.draw_stats_axes)

        # move strength
        fig = Figure(figsize=(2.2, 2.2), dpi=100, frameon=False)
        self.strength_canvas = FigureCanvas(fig)
        #self.strength_canvas.setParent(self.grp_right) # TODO: layout instead?
        self.strength_axes = Axes(fig, [0., 0., 1., 1.])
        fig.add_axes(self.strength_axes)

        #%% Buttons
        self.btn_play = QPushButton('PLAY')
        self.btn_play.setToolTip('Ploy the current move.')
        self.btn_play.setMaximumWidth(200)
        self.btn_play.setStyleSheet('color: black; background-color: #00bfbf; font: bold;')
        self.btn_play.clicked.connect(self.btn_play_func)

        for ix in range(7):
            temp = QPushButton('')
            temp.setMaximumWidth(20)
            temp.setStyleSheet(f'color: black; background-color: {tile_color};')
            temp.clicked.connect(lambda state, x=ix: self.btn_tile_func(x))
            setattr(self, f'btn_tile{ix}', temp)

        for ix in range(10):
            temp = QPushButton('')
            temp.setMaximumWidth(20)
            temp.setStyleSheet(f'color: black; background-color: {tile_color};')
            temp.clicked.connect(lambda state, x=ix: self.btn_move_func(x))
            setattr(self, f'btn_move{ix}', temp)

        #%% Populate Widgets
        # tiles
        layout_tiles.addWidget(self.btn_tile0)
        layout_tiles.addWidget(self.btn_tile1)
        layout_tiles.addWidget(self.btn_tile2)
        layout_tiles.addWidget(self.btn_tile3)
        layout_tiles.addWidget(self.btn_tile4)
        layout_tiles.addWidget(self.btn_tile5)
        layout_tiles.addWidget(self.btn_tile6)

        # best moves
        layout_moves.addWidget(self.btn_move0, 0, 0)
        layout_moves.addWidget(self.btn_move1, 0, 1)
        layout_moves.addWidget(self.btn_move2, 0, 2)
        layout_moves.addWidget(self.btn_move3, 0, 3)
        layout_moves.addWidget(self.btn_move4, 0, 4)
        layout_moves.addWidget(self.btn_move5, 1, 0)
        layout_moves.addWidget(self.btn_move6, 1, 1)
        layout_moves.addWidget(self.btn_move7, 1, 2)
        layout_moves.addWidget(self.btn_move8, 1, 3)
        layout_moves.addWidget(self.btn_move9, 1, 4)

        # left
        layout_left.addWidget(lbl_tile_bag)
        layout_left.addWidget(self.lne_tile_bag)
        layout_left.addWidget(lbl_draw_stats)
        layout_left.addWidget(self.draw_stats_canvas)

        # center
        layout_center.addWidget(self.board_canvas)
        layout_center.addWidget(self.grp_tiles)

        # right
        layout_right.addWidget(lbl_strength)
        layout_right.addWidget(self.strength_canvas)
        layout_right.addWidget(lbl_moves)
        layout_right.addWidget(self.grp_moves)
        layout_right.addWidget(self.btn_play)

        # main
        layout_main.addWidget(self.grp_left)
        layout_main.addWidget(self.grp_center)
        layout_main.addWidget(self.grp_right)

        # main GUI
        layout_gui.addWidget(lbl_title)
        layout_gui.addWidget(self.grp_main)

        #%% File Menu
        # actions - new game
        act_new_game = QAction('New Game', self)
        act_new_game.setShortcut('Ctrl+N')
        act_new_game.setStatusTip('Starts a new game.')
        act_new_game.triggered.connect(self.act_new_game_func)
        # actions - options
        act_options = QAction('Options', self)
        act_options.setShortcut('Ctrl+O')
        act_options.setStatusTip('Opens the advanced option settings.')
        act_options.triggered.connect(self.act_options_func)
        # actions - quit game
        act_quit = QAction('Exit', self)
        act_quit.setShortcut('Ctrl+Q')
        act_quit.setStatusTip('Exits the application.')
        act_quit.triggered.connect(self.close)

        # menubar
        self.statusBar()
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(act_new_game)
        file_menu.addAction(act_options)
        file_menu.addAction(act_quit)

        #%% Finalization
        # Call wrapper to initialize GUI
        self.wrapper()

        # GUI final layout properties
        self.center()
        self.setWindowTitle('Cheater GUI')
        self.setWindowIcon(QtGui.QIcon(os.path.join(get_root_dir(), 'scrabble.png')))
        self.show()

    #%% Wrapper
    def wrapper(self):
        r"""
        Acts as a wrapper to everything the GUI needs to do.
        """
        # plot the board
        plot_board(self.board_axes, self.gui_settings.board)
        # display tile bag
        display_tile_bag(self.lne_tile_bag, self.gui_settings.counts, self.gui_settings.tiles)
        # display draw statistic
        plot_draw_stats(self.draw_stats_axes, self.gui_settings.counts, self.gui_settings.tiles, \
            self.gui_settings.move)
        # Show current move strength
        plot_move_strength(self.strength_axes, self.gui_settings.move, self.gui_settings.pot_moves)

    #%% Other callbacks - closing
    def closeEvent(self, event):
        r"""Things in here happen on GUI closing."""
        event.accept()

    #%% Other callbacks - center the GUI on the screen
    def center(self):
        r"""Makes the GUI centered on the active screen."""
        frame_gm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        center_point = QApplication.desktop().screenGeometry(screen).center()
        frame_gm.moveCenter(center_point)
        self.move(frame_gm.topLeft())

    #%% Other callbacks - Play Button
    def btn_play_func(self):
        r"""Plays the current move."""
        pass

    def btn_tile_func(self, tile):
        r"""Function for button click."""
        pass

    def btn_move_func(self, move):
        r"""Function for move click."""
        pass

    def btn_new_function(self):
        r"""Function that executes on new game button press."""

    #%% Menu action callbacks
    def act_new_game_func(self):
        r"""Function that executes on new game menu selection."""
        # reset Gui Settings

        # call GUI wrapper
        self.wrapper()

    def act_options_func(self):
        r"""Function that executes on options menu selection."""
        pass # TODO: write this

#%% Unit Test
if __name__ == '__main__':
    # open a qapp
    if QApplication.instance() is None:
        qapp = QApplication(sys.argv)
    else:
        qapp = QApplication.instance()
    # run the tests
    unittest.main(module='dstauffman2.games.scrabble.tests.test_gui', exit=False)
    doctest.testmod(verbose=False)
    # close the qapp
    qapp.closeAllWindows()
