r"""
Test file for the `help` module of the "dstauffman2.commands" library.

Notes
-----
#.  Written by David C. Stauffer in March 2020.

"""

# %% Imports
import argparse
import unittest

from slog import capture_output

import dstauffman2.commands as commands


# %% commands.print_help
class Test_commands_print_help(unittest.TestCase):
    r"""
    Tests the commands.print_help function with the following cases:
        Nominal
    """

    def setUp(self) -> None:
        self.expected_header = "###########\ndstauffman2\n###########\n"

    def test_nominal(self) -> None:
        with capture_output() as ctx:
            commands.print_help()
        output = ctx.get_output()
        ctx.close()
        self.assertEqual(output[0:36], self.expected_header)


# %% commands.parse_help
class Test_commands_parse_help(unittest.TestCase):
    r"""
    Tests the commands.parse_help function with the following cases:
        Nominal
    """

    def setUp(self) -> None:
        self.args: list[str] = []
        self.expected = argparse.Namespace()

    def test_nominal(self) -> None:
        args = commands.parse_help(self.args)
        self.assertEqual(args, self.expected)


# %% commands.execute_help
class Test_commands_execute_help(unittest.TestCase):
    r"""
    Tests the commands.execute_help function with the following cases:
        Nominal
    """

    def setUp(self) -> None:
        self.args = argparse.Namespace()
        self.expected_header = "###########\ndstauffman2\n###########\n"

    def test_nominal(self) -> None:
        with capture_output() as ctx:
            commands.execute_help(self.args)
        output = ctx.get_output()
        ctx.close()
        self.assertEqual(output[0:36], self.expected_header)


# %% Unit test execution
if __name__ == "__main__":
    unittest.main(exit=False)
