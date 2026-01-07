r"""
Test file to execute all the tests from the unittest library within the tictactoe code using nose.

Notes
-----
#.  Written by David C. Stauffer in January 2016.

"""

# %% Imports
import sys

from qtpy.QtWidgets import QApplication
import pytest

# %% Script
if __name__ == "__main__":
    # open a qapp
    if QApplication.instance() is None:
        qapp = QApplication(sys.argv)
    else:
        qapp = QApplication.instance()  # type: ignore[assignment]
    # run the tests
    pytest.main()
    # close the qapp
    qapp.closeAllWindows()
