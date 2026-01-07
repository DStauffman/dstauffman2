r"""
Runs the Scrabble GUI.

Written by David C. Stauffer in March 2017.

"""

# %% Imports
import sys

from qtpy.QtWidgets import QApplication

from dstauffman2.games.scrabble import ScrabbleGui

# %% Execution
if __name__ == "__main__":
    # Runs the GUI application
    qapp = QApplication(sys.argv)
    # instatiates the GUI
    gui = ScrabbleGui()
    gui.show()
    # exits and returns the code on close of all main application windows
    sys.exit(qapp.exec_())
