# -*- coding: utf-8 -*-
r"""
Utils module file for the "dstauffman2" library.  It contains generic utilities that can be
independently defined and used by other modules.

Notes
-----
#.  Written by David C. Stauffer in November 2016.
"""

#%% Imports
import doctest
import os
import unittest

#%% Functions - get_root_dir
def get_root_dir():
    r"""
    Returns the folder that contains this source file and thus the root folder for the whole code.

    Returns
    -------
    folder : str
        Location of the folder that contains all the source files for the code.

    Notes
    -----
    #.  Written by David C. Stauffer in March 2015.

    Examples
    --------

    >>> from dstauffman2 import get_root_dir
    >>> folder = get_root_dir()

    """
    # this folder is the root directory based on the location of this file (utils.py)
    folder = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    return folder

#%% Functions - get_tests_dir
def get_tests_dir():
    r"""
    Returns the default test folder location.

    Returns
    -------
    folder : str
        Location of the folder that contains all the test files for the code.

    Notes
    -----
    #.  Written by David C. Stauffer in March 2015.

    Examples
    --------

    >>> from dstauffman2 import get_tests_dir
    >>> folder = get_tests_dir()

    """
    # this  folder is the 'tests' subfolder
    folder = os.path.join(get_root_dir(), 'tests')
    return folder

#%% Functions - get_data_dir
def get_data_dir():
    r"""
    Returns the default data folder location.

    Returns
    -------
    folder : str
        Location of the default folder for storing the code data.

    Notes
    -----
    #.  Written by David C. Stauffer in April 2015.

    Examples
    --------

    >>> from dstauffman2 import get_data_dir
    >>> folder = get_data_dir()

    """
    # this folder is the 'data' subfolder
    folder = os.path.join(get_root_dir(), 'data')
    return folder

#%% Functions - get_images_dir
def get_images_dir():
    r"""
    Returns the default data folder location.

    Returns
    -------
    folder : str
        Location of the default folder for storing the code data.

    Notes
    -----
    #.  Written by David C. Stauffer in April 2015.

    Examples
    --------

    >>> from dstauffman2 import get_images_dir
    >>> folder = get_images_dir()

    """
    # this folder is the 'images' subfolder
    folder = os.path.join(get_root_dir(), 'images')
    return folder

#%% Functions - get_output_dir
def get_output_dir():
    r"""
    Returns the default output folder location.

    Returns
    -------
    folder : str
        Location of the default folder for storing the code data.

    Notes
    -----
    #.  Written by David C. Stauffer in January 2016.

    Examples
    --------

    >>> from dstauffman2 import get_output_dir
    >>> folder = get_output_dir()

    """
    # this folder is the 'images' subfolder
    folder = os.path.join(get_root_dir(), 'results')
    return folder

#%% Unit test
if __name__ == '__main__':
    unittest.main(module='dstauffman2.tests.test_utils', exit=False)
    doctest.testmod(verbose=False)
