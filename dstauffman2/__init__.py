r"""
The "dstauffman2" module is a collection of games, applications, extended utilities and miscellaneous documentation.

At least they are functions that I (David C. Stauffer) have found useful.  Your results may vary!

Notes
-----
#.  Pulled out of "dstauffman" module by David C. Stauffer in November 2016.

"""

# %% Imports
# fmt: off
from .parser  import main
from .paths   import get_root_dir, get_tests_dir, get_data_dir, get_images_dir, get_output_dir
from .version import version_info
# fmt: on

# %% Constants
__version__ = ".".join(str(x) for x in version_info)

# %% Unit test
if __name__ == "__main__":
    pass
