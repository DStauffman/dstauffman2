r"""
Parser used to parse all commands from the terminal and pass to the revelant command functions.

Notes
-----
#.  Written by David C. Stauffer in March 2020.
#.  Copied from dstauffman into dstauffman2 by David C. Stauffer in May 2020.
"""

# %% Imports
from __future__ import annotations

import argparse
import doctest
import sys
from typing import List, Optional, Tuple
import unittest

from slog import ReturnCodes

# %% Constants
_VALID_COMMANDS = frozenset({"batch_rename", "find_words", "help", "photos", "man", "tests", "version"})


# %% Functions - _print_bad_command
def _print_bad_command(command: str) -> None:
    r"""Prints to the command line when a command name is not understood."""
    print('Command "{}" is not understood.'.format(command))


# %% Functions - main
def main() -> int:
    r"""Main function called when executed using the command line api."""
    try:
        (command, args) = parse_wrapper(sys.argv[1:])
    except ValueError:
        _print_bad_command(" ".join(sys.argv[1:]))
        return ReturnCodes.bad_command
    rc = execute_command(command, args)
    return sys.exit(rc)


# %% Functions - parse_wrapper
def parse_wrapper(args: List[str]) -> Tuple[str, argparse.Namespace]:
    r"""Wrapper function to parse out the command name from the rest of the arguments."""
    # check for no command option
    if len(args) >= 1:
        command = args[0]
    else:
        command = "help"
    # check for alternative forms of help with the base dcs command
    if command in {"--help", "-h"}:
        command = "help"
    elif command in {"--version", "-v"}:
        command = "version"
    # pass the command and remaining arguments to the command parser
    parsed_args = parse_commands(command, args[1:])
    return (command, parsed_args)


# %% Functions - parse_commands
def parse_commands(command: str, args: List[str]) -> argparse.Namespace:
    r"""
    Splits the parsing based on the name of the command.

    Parameters
    ----------
    command : str
        Name of command to parse
    args : list
        Command line arguments

    Returns
    -------
    parsed_args : class argparse.Namespace
        Parsed arguments ready to be passed to command to execute

    Examples
    --------
    >>> from dstauffman import parse_commands
    >>> command = 'help'
    >>> args = []
    >>> parsed_args = parse_commands(command, args)

    """
    # delayed import of commands
    import dstauffman2.commands as commands

    # check for valid commands
    if command in _VALID_COMMANDS:
        # If valid, then parse the arguments with the appropiate method, so help calls parse_help etc.
        func = getattr(commands, "parse_" + command)
        parsed_args: argparse.Namespace = func(args)
    else:
        raise ValueError('Unexpected command "{}".'.format(command))
    return parsed_args


# %% Functions - execute_command
def execute_command(command: str, args: argparse.Namespace) -> int:
    r"""Executes the given command."""
    # delayed import of commands
    import dstauffman2.commands as commands

    # check for valid commands
    if command in _VALID_COMMANDS:
        # If valid, then call the appropriate method, so help calls execute_help etc.
        func = getattr(commands, "execute_" + command)
        rc: Optional[int] = func(args)
    else:
        _print_bad_command(command)
        rc = ReturnCodes.bad_command
    if rc is None:
        rc = ReturnCodes.clean
    return rc


# %% Unit test
if __name__ == "__main__":
    unittest.main(module="dstauffman2.tests.test_parser", exit=False)
    doctest.testmod(verbose=False)
