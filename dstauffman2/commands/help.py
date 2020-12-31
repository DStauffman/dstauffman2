r"""
Functions related to `help` command.

Notes
-----
#.  Written by David C. Stauffer in March 2020.
"""

#%% Imports
import argparse
import doctest
from importlib import metadata
import os
from typing import List
import unittest

from dstauffman import ReturnCodes
from dstauffman2.paths import get_root_dir

#%% Functions - print_help
def print_help() -> int:
    r"""
    Prints the contents of the README.rst file.

    Returns
    -------
    return_code : int
        Return code for whether the help file was successfully loaded

    Examples
    --------
    >>> from dstauffman2.commands import print_help
    >>> print_help() # doctest: +SKIP

    """
    help_file = os.path.join(get_root_dir(), '..', 'README.rst')
    if not os.path.isfile(help_file): # pragma: no cover
        print(f'Warning: help file at "{help_file}" was not found.')
        return ReturnCodes.bad_help_file
    with open(help_file) as file:
        text = file.read()
    print(text)
    return ReturnCodes.clean

#%% Functions - print_version
def print_version() -> int:
    r"""Prints the version of the library.

    Returns
    -------
    return_code : int
        Return code for whether the version was successfully read

    Examples
    --------
    >>> from dstauffman2.commands import print_version
    >>> print_version()  # doctest: +SKIP

    """
    try:
        version = metadata.version('dstauffman2')
        return_code = ReturnCodes.clean
    except:
        version = 'unknown'
        return_code = ReturnCodes.bad_version
    print(version)
    return return_code

#%% Functions - parse_help
def parse_help(input_args: List[str]) -> argparse.Namespace:
    r"""
    Parser for help command.

    Parameters
    ----------
    input_args : list of str
        Input arguments as passed to sys.argv for this command

    Returns
    -------
    args : class Namespace
        Arguments as parsed by argparse.parse_args

    Examples
    --------
    >>> from dstauffman2.commands import parse_help
    >>> input_args = []
    >>> args = parse_help(input_args)
    >>> print(args)
    Namespace()

    """
    parser = argparse.ArgumentParser(prog='dcs2 help')

    args = parser.parse_args(input_args)
    return args

#%% Functions - parse_version
def parse_version(input_args: List[str]) -> argparse.Namespace:
    r"""
    Parser for version command.

    Parameters
    ----------
    input_args : list of str
        Input arguments as passed to sys.argv for this command

    Returns
    -------
    args : class Namespace
        Arguments as parsed by argparse.parse_args

    Examples
    --------
    >>> from dstauffman2.commands import parse_version
    >>> input_args = []
    >>> args = parse_version(input_args)
    >>> print(args)
    Namespace()

    """
    parser = argparse.ArgumentParser(prog='dcs2 version')

    args = parser.parse_args(input_args)
    return args

#%% Functions - execute_help
def execute_help(args: argparse.Namespace) -> int:
    r"""
    Executes the help command.

    Parameters
    ----------
    args : class Namespace
        Arguments as parsed by argparse.parse_args, in this case they can be empty or ommitted

    Returns
    -------
    return_code : int
        Return code for whether the command completed successfully

    Examples
    --------
    >>> from dstauffman2.commands import execute_help
    >>> args = []
    >>> execute_help(args) # doctest: +SKIP

    """
    return_code = print_help()
    return return_code

#%% Functions - execute_version
def execute_version(args: argparse.Namespace) -> int:
    r"""
    Executes the version command.

    Parameters
    ----------
    args : class Namespace
        Arguments as parsed by argparse.parse_args, in this case they can be empty or ommitted

    Returns
    -------
    return_code : int
        Return code for whether the command completed successfully

    Examples
    --------
    >>> from dstauffman2.commands import execute_version
    >>> args = []
    >>> execute_version(args) # doctest: +SKIP

    """
    return_code = print_version()
    return return_code

#%% Unit test
if __name__ == '__main__':
    unittest.main(module='dstauffman2.tests.test_commands_help', exit=False)
    doctest.testmod(verbose=False)
