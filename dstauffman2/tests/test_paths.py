r"""
Test file for the `paths` module of the "dstauffman2" library.

Notes
-----
#.  Written by David C. Stauffer in March 2015.

"""

# %% Imports
import inspect
import os
import pathlib
import unittest

import dstauffman2 as dcs2


# %% get_root_dir
class Test_get_root_dir(unittest.TestCase):
    r"""
    Tests the get_root_dir function with the following cases:
        call the function
    """

    def test_function(self) -> None:
        filepath = inspect.getfile(dcs2.get_root_dir.__wrapped__)
        expected_root = pathlib.Path(os.path.split(filepath)[0])
        folder = dcs2.get_root_dir()
        self.assertEqual(folder, expected_root)
        self.assertTrue(folder.is_dir())


# %% get_tests_dir
class Test_get_tests_dir(unittest.TestCase):
    r"""
    Tests the get_tests_dir function with the following cases:
        call the function
    """

    def test_function(self) -> None:
        folder = dcs2.get_tests_dir()
        self.assertEqual(str(folder), os.path.join(str(dcs2.get_root_dir()), "tests"))  # noqa: PTH118


# %% get_data_dir
class Test_get_data_dir(unittest.TestCase):
    r"""
    Tests the get_data_dir function with the following cases:
        call the function
    """

    def test_function(self) -> None:
        folder = dcs2.get_data_dir()
        self.assertEqual(str(folder), os.path.join(str(dcs2.get_root_dir()), "data"))  # noqa: PTH118


# %% get_images_dir
class Test_get_images_dir(unittest.TestCase):
    r"""
    Tests the get_images_dir function with the following cases:
        call the function
    """

    def test_function(self) -> None:
        folder = dcs2.get_images_dir()
        self.assertEqual(str(folder), os.path.join(str(dcs2.get_root_dir()), "images"))  # noqa: PTH118


# %% get_output_dir
class Test_get_output_dir(unittest.TestCase):
    r"""
    Tests the get_output_dir function with the following cases:
        call the function
    """

    def test_function(self) -> None:
        folder = dcs2.get_output_dir()
        self.assertEqual(str(folder), os.path.join(str(dcs2.get_root_dir()), "results"))  # noqa: PTH118


# %% Unit test execution
if __name__ == "__main__":
    unittest.main(exit=False)
