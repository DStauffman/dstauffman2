r"""
Test file to execute all the tests from the unittest library within the dstauffman2 code.

Notes
-----
#.  Written by David C. Stauffer in November 2016.
"""

# %% Imports
import sys

from PyQt5.QtWidgets import QApplication
import pytest

from dstauffman2 import get_root_dir

# %% Tests
if __name__ == "__main__":
    # open a qapp
    if QApplication.instance() is None:
        qapp = QApplication(sys.argv)
    else:
        qapp = QApplication.instance()
    # run the tests
    pytest.main([get_root_dir()])
    # close the qapp
    qapp.closeAllWindows()
