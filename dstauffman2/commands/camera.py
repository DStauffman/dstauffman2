r"""
Functions related to processing photos from my digital camera.

Notes
-----
#.  Written by David C. Stauffer in December 2020.
"""

#%% Imports
import argparse
import doctest
import os
from typing import List
import unittest

from dstauffman2.imageproc import batch_resize, find_long_filenames, find_missing_nums, \
    find_unexpected_ext, rename_old_picasa_files, rename_upper_ext

#%% Functions - parse_photos
def parse_photos(input_args: List[str]) -> argparse.Namespace:
    r"""
    Parser for the photos command.

    Parameters
    ----------
    input_args : list of str
        Input arguments as passed to sys.argv for this command

    Returns
    -------
    args : class Namespace
        Arguments as parsed by argparse.parse_args

    Notes
    -----
    #.  Written by David C. Stauffer in December 2020.

    Examples
    --------
    >>> from dstauffman2.commands import parse_photos
    >>> input_args = ['.']
    >>> args = parse_photos(input_args)
    >>> print(args)
    Namespace(folder='.', upper=False, missing=False, unexpected_ext=False, picasa=False, long=False, resize=False, pause=False)

    """
    parser = argparse.ArgumentParser(prog='dcs2 photos', description='Batch processes digital photos.')

    parser.add_argument('folder', help='Folder to search for source files')

    parser.add_argument('-u', '--upper', help='Rename uppercase extensions to lowercase.', action='store_true')

    parser.add_argument('-m', '--missing', help='Display any missing file numbers.', action='store_true')

    parser.add_argument('-x', '--unexpected-ext', help='Find any unexpected file extensions in the folder(s).', action='store_true')

    parser.add_argument('-c', '--picasa', help='Rename any old picasa ini files', action='store_true')

    parser.add_argument('-l', '--long', help='Find long filenames', action='store_true')

    parser.add_argument('-r', '--resize', help='Resize the photos to max width and height', action='store_true')  # TODO: group with two other arguments

    parser.add_argument('-p', '--pause', help='Pause within the python environment at the end of execution.', action='store_true')

    args = parser.parse_args(input_args)
    return args

#%% Functions - execute_photos
def execute_photos(args: argparse.Namespace) -> int:
    r"""
    Executes the photo processing commands.

    Parameters
    ----------
    args : class argparse.Namespace, with fields:
        .docstrings : bool
        .verbose : bool

    Returns
    -------
    return_code : int
        Return code for whether the command executed cleanly

    Notes
    -----
    #.  Written by David C. Stauffer in December 2020.

    Examples
    --------
    >>> from dstauffman2.commands import execute_photos
    >>> from argparse import Namespace
    >>> args = Namespace(folder='.', long=False, missing=False, pause=False, picasa=False, resize=False, unexpected_ext=False, upper=False)
    >>> execute_photos(args) # doctest: +SKIP

    """
    # alias options
    folder    = os.path.abspath(args.folder)
    upper     = args.upper
    missing   = args.missing
    unexpect  = args.unexpected_ext
    picasa    = args.picasa
    list_long = args.long
    resize    = args.resize
    pause     = args.pause

    if upper:
        rename_upper_ext(folder)
    if missing:
        find_missing_nums(folder)
    if list_long:
        find_long_filenames(folder)
    if unexpect:
        find_unexpected_ext(folder)
    if picasa:
        rename_old_picasa_files(folder)
    if resize:
        batch_resize(folder, max_width=1024, max_height=768)
    if pause:
        breakpoint()

#%% Unit test
if __name__ == '__main__':
    unittest.main(module='dstauffman2.tests.test_commands_camera', exit=False)
    doctest.testmod(verbose=False)
