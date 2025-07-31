r"""
Test file for the `parser` module of the "dstauffman2" library.

Notes
-----
#.  Written by David C. Stauffer in March 2020.

"""

# %% Imports
import unittest

from slog import capture_output

import dstauffman2 as dcs2


# %% _VALID_COMMANDS
class Test__VALID_COMMANDS(unittest.TestCase):
    r"""Tests the _VALID_COMMANDS enumerator for expected values."""

    def test_nominal(self) -> None:
        self.assertIn("find_words", dcs2.parser._VALID_COMMANDS)
        self.assertIn("help", dcs2.parser._VALID_COMMANDS)
        self.assertIn("tests", dcs2.parser._VALID_COMMANDS)
        self.assertIn("version", dcs2.parser._VALID_COMMANDS)


# %% parser._print_bad_command
class Test_parser__print_bad_command(unittest.TestCase):
    r"""
    Tests the parser._print_bad_command function with the following cases:
        Nominal
    """

    def test_nominal(self) -> None:
        with capture_output() as ctx:
            dcs2.parser._print_bad_command("garbage")
        output = ctx.get_output()
        ctx.close()
        self.assertEqual(output, 'Command "garbage" is not understood.')


# %% main
class Test_main(unittest.TestCase):
    r"""
    Tests the main function with the following cases:
        TBD
    """

    pass  # TODO: write this


# %% parse_wrapper
class Test_parse_wrapper(unittest.TestCase):
    r"""
    Tests the parse_wrapper function with the following cases:
        TBD
    """

    pass


# %% parse_commands
class Test_parse_commands(unittest.TestCase):
    r"""
    Tests the parse_commands function with the following cases:
        TBD
    """

    pass


# %% execute_command
class Test_execute_command(unittest.TestCase):
    r"""
    Tests the execute_command function with the following cases:
        TBD
    """

    pass


# %% Unit test execution
if __name__ == "__main__":
    unittest.main(exit=False)
