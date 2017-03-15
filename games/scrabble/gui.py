# -*- coding: utf-8 -*-
r"""
GUI module file for the "scrabble" game.  It defines the GUI.

Notes
-----
#.  Written by David C. Stauffer in March 2017.
"""

#%% Imports
# normal imports
import doctest
import logging
from matplotlib.pyplot import Axes
from matplotlib.figure import Figure
import numpy as np
import sys
import unittest
# Qt imports
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QToolTip, QPushButton, QLabel, QMessageBox, \
    QMainWindow, QAction
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# model imports
from dstauffman2.games.scrabble.classes  import Options
from dstauffman2.games.scrabble.plotting import plot_board

#%% Logging options
# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)

#%% Option instance
OPTS = Options()

#%% Classes - ScrabbleGui
class ScrabbleGui(QMainWindow):
    r"""
    The Scrabble GUI.
    """
    def __init__(self, filename=None, board=None, cur_move=None, cur_game=None, game_hist=None):
        # call super method
        super().__init__()
        # call init method to instantiate the GUI
        self.init()

    #%% GUI initialization
    def init(self):
        r"""Initializes the GUI."""
        pass

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
