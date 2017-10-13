# -*- coding: utf-8 -*-
r"""
Test file to execute all the tests from the unittest library within the dstauffman2 code.

Notes
-----
#.  Written by David C. Stauffer in November 2016.
"""

#%% Imports
import sys
import unittest

from PyQt5.QtWidgets import QApplication

#%% Tests
if __name__ == '__main__':
    # open a qapp
    if QApplication.instance() is None:
        qapp = QApplication(sys.argv)
    else:
        qapp = QApplication.instance()
    # get a loader
    loader = unittest.TestLoader()
    # find all the test cases
    test_suite = loader.discover('dstauffman2.apps')
    test_suite.addTests(loader.discover('dstauffman2.archery'))
    test_suite.addTests(loader.discover('dstauffman2.games'))
    test_suite.addTests(loader.discover('dstauffman2.imageproc'))
    test_suite.addTests(loader.discover('dstauffman2.tests'))
    # run the tests
    unittest.TextTestRunner(verbosity=1).run(test_suite)
    # close the qapp
    qapp.closeAllWindows()
