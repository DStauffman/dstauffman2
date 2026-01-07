r"""
Copies changes any *.JPG to *.jpg and shows any missing numbers.

Notes
-----
#.  Written by David C. Stauffer in December 2013.

"""

# %% Imports
from pathlib import Path

import dstauffman2.imageproc as dip

# %% Test script
if __name__ == "__main__":
    folder = Path(r"C:\Users\DStauffman\Desktop\Camera")
    dip.rename_upper_ext(folder)
    dip.find_missing_nums(folder)
    # dip.find_unexpected_ext(folder)
    # dip.rename_old_picasa_files(folder)
    # dip.find_long_filenames(folder)
