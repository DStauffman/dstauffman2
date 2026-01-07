r"""
Resizes all the photos within the given folder to a maximum height and width while maintaining the aspect ratio.

Notes
-----
#.  Written by David C. Stauffer in December 2013.

"""

# %% Imports
from pathlib import Path

import dstauffman2.imageproc as dip

# %% Test script
if __name__ == "__main__":
    folder = Path(r"E:\Pictures\eFrame\resized_1080p")
    dip.batch_resize(folder, max_width=1920, max_height=1080)
