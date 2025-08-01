r"""
Copies in the raw files based on the time stamps from the given jpg's.

Notes
-----
#.  Written by David C. Stauffer in December 2018.

"""

# %% Imports
from dstauffman2.imageproc import get_raw_file_from_datetime

# %% Test script
if __name__ == "__main__":
    folder = r"C:\Users\DStauffman\Desktop\Camera\Washington"
    raw_folder = r"C:\Users\DStauffman\Desktop\Camera\raw"
    (missed, possibly_wrong) = get_raw_file_from_datetime(folder, raw_folder, dry_run=False)
