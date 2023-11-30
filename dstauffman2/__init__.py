r"""
The "dstauffman2" module is a collection of games, applications, extended utilities and
miscellaneous documentation that I (David C. Stauffer) have found useful.

Notes
-----
#.  Pulled out of "dstauffman" module by David C. Stauffer in November 2016.
"""

#%% Imports
from .parser  import main
from .paths   import get_root_dir, get_tests_dir, get_data_dir, get_images_dir, get_output_dir
from .version import version_info

# %% Constants
__version__ = ".".join(str(x) for x in version_info)

# %% Unit test
if __name__ == "__main__":
    pass
