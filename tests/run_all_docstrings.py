# -*- coding: utf-8 -*-
r"""
Test file to execute all the docstrings within the dstauffman2 code.

Notes
-----
#.  Written by David C. Stauffer in March 2015.
"""

#%% Imports
import doctest
import os

from dstauffman2 import get_root_dir

#%% Locals
verbose = False

#%% Execution
if __name__ == '__main__':
    folder = get_root_dir() # TODO: include subfolders...
    files  = [f for f in os.listdir(folder) if f.endswith('.py') and not f.startswith('__')]
    for file in files:
        if verbose:
            print('')
            print('******************************')
            print('******************************')
            print('Testing "{}":'.format(file))
        doctest.testfile(os.path.join(folder, file), report=True, verbose=verbose, module_relative=True)
