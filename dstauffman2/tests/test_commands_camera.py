r"""
Test file for the `commands.camera` module of the "dstauffman2" library.  It is intented to contain
test cases to demonstrate functionaliy and correct outcomes for all the functions within the module.

Notes
-----
#.  Written by David C. Stauffer in December 2020.
"""

#%% Imports
import argparse
import unittest
from unittest.mock import patch

import dstauffman2 as dcs2
import dstauffman2.commands as commands

#%% commands.parse_photos
class Test_parse_photos(unittest.TestCase):
    r"""
    Tests the parse_photos function with the following cases:
        Nominal
    """
    def setUp(self):
        self.folder = dcs2.get_root_dir()
        self.expected = argparse.Namespace()
        self.expected.folder = self.folder
        self.expected.upper = False
        self.expected.missing = False
        self.expected.unexpected_ext = False
        self.expected.picasa = False
        self.expected.long = False
        self.expected.resize = False
        self.expected.pause = False

    def test_nominal(self):
        args = commands.parse_photos([self.folder])
        self.assertEqual(args, self.expected)

    def test_upper(self):
        self.expected.upper = True
        args = commands.parse_photos([self.folder, '-u'])
        self.assertEqual(args, self.expected)

    def test_missing(self):
        self.expected.missing = True
        args = commands.parse_photos([self.folder, '-m'])
        self.assertEqual(args, self.expected)

    def test_unexpected(self):
        self.expected.unexpected_ext = True
        args = commands.parse_photos([self.folder, '-x'])
        self.assertEqual(args, self.expected)

    def test_picasa(self):
        self.expected.picasa = True
        args = commands.parse_photos([self.folder, '-c'])
        self.assertEqual(args, self.expected)

    def test_long(self):
        self.expected.long = True
        args = commands.parse_photos([self.folder, '-l'])
        self.assertEqual(args, self.expected)

    def test_resize(self):
        self.expected.resize = True
        args = commands.parse_photos([self.folder, '-r'])
        self.assertEqual(args, self.expected)

    def test_pause(self):
        self.expected.pause = True
        args = commands.parse_photos([self.folder, '-p'])
        self.assertEqual(args, self.expected)

#%% commands.execute_photos
class Test_execute_photos(unittest.TestCase):
    r"""
    Tests the execute_photos function with the following cases:
        Nominal
        TBD
    """
    def setUp(self):
        self.folder = dcs2.get_root_dir()
        self.args = argparse.Namespace(folder=self.folder, upper=False, missing=False, unexpected_ext=False, \
            picasa=False, long=False, resize=False, pause=False)

    def test_nominal(self):
        commands.execute_photos(self.args)

    @patch('dstauffman2.commands.camera.rename_upper_ext')
    def test_upper(self, mocker):
        self.args.upper = True
        commands.execute_photos(self.args)
        mocker.assert_called_once_with(self.folder)

    @patch('dstauffman2.commands.camera.find_missing_nums')
    def test_missing(self, mocker):
        self.args.missing = True
        commands.execute_photos(self.args)
        mocker.assert_called_once_with(self.folder)

    @patch('dstauffman2.commands.camera.find_long_filenames')
    def test_long(self, mocker):
        self.args.long = True
        commands.execute_photos(self.args)
        mocker.assert_called_once_with(self.folder)

    @patch('dstauffman2.commands.camera.find_unexpected_ext')
    def test_unexpected(self, mocker):
        self.args.unexpected_ext = True
        commands.execute_photos(self.args)
        mocker.assert_called_once_with(self.folder)

    @patch('dstauffman2.commands.camera.rename_old_picasa_files')
    def test_picasa(self, mocker):
        self.args.picasa = True
        commands.execute_photos(self.args)
        mocker.assert_called_once_with(self.folder)

    @patch('dstauffman2.commands.camera.batch_resize')
    def test_resize(self, mocker):
        self.args.resize = True
        commands.execute_photos(self.args)
        mocker.assert_called_once_with(self.folder, max_width=1024, max_height=768)

    @patch('dstauffman2.commands.camera.breakpoint')
    def test_pause(self, mocker):
        self.args.pause = True
        commands.execute_photos(self.args)
        mocker.assert_called_once_with()

#%% Unit test execution
if __name__ == '__main__':
    unittest.main(exit=False)
