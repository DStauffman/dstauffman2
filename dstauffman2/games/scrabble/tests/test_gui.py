r"""
Test file for the `scrabble.gui` module of the dstauffman2 code.  It is intented to contain test
cases to demonstrate functionaliy and correct outcomes for all the functions within the module.

Notes
-----
#.  Written by David C. Stauffer in March 2017.

"""

# %% Imports
import sys
import unittest

from PyQt5 import QtCore
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication, QPushButton

import dstauffman2.games.scrabble as scrab

# %% Unit test execution
if __name__ == "__main__":
    unittest.main(exit=False)

# %% Unit test execution
if __name__ == "__main__":
    # open a qapp
    if QApplication.instance() is None:
        qapp = QApplication(sys.argv)
    else:
        qapp = QApplication.instance()
    # run the tests
    unittest.main(exit=False)
    # close the qapp
    qapp.closeAllWindows()
