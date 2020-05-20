# -*- coding: utf-8 -*-
r"""
Test file for the `commands.help` module of the "dstauffman" library.  It is intented to contain
test cases to demonstrate functionaliy and correct outcomes for all the functions within the module.

Notes
-----
#.  Written by David C. Stauffer in March 2020.
"""

#%% Imports
import argparse
import unittest

from dstauffman import capture_output

import dstauffman2.commands as commands

#%% commands.print_help
class Test_commands_print_help(unittest.TestCase):
    r"""
    Tests the commands.print_help function with the following cases:
        Nominal
    """
    def setUp(self):
        self.expected_header = '###########\ndstauffman2\n###########\n'

    def test_nominal(self):
        with capture_output() as out:
            commands.print_help()
        output = out.getvalue().strip()
        out.close()
        self.assertEqual(output[0:36], self.expected_header)

#%% commands.parse_help
class Test_commands_parse_help(unittest.TestCase):
    r"""
    Tests the commands.parse_help function with the following cases:
        Nominal
    """
    def setUp(self):
        self.args = []
        self.expected = argparse.Namespace()

    def test_nominal(self):
        args = commands.parse_help(self.args)
        self.assertEqual(args, self.expected)

#%% commands.execute_help
class Test_commands_execute_help(unittest.TestCase):
    r"""
    Tests the commands.execute_help function with the following cases:
        Nominal
    """
    def setUp(self):
        self.args = argparse.Namespace()
        self.expected_header = '###########\ndstauffman2\n###########\n'

    def test_nominal(self):
        with capture_output() as out:
            commands.execute_help(self.args)
        output = out.getvalue().strip()
        out.close()
        self.assertEqual(output[0:36], self.expected_header)

#%% Unit test execution
if __name__ == '__main__':
    unittest.main(exit=False)
