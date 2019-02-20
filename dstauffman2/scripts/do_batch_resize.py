# -*- coding: utf-8 -*-
r"""
THis script resizes all the photos within the given folder to a maximum height and width while
maintaining the aspect ratio.

Notes
-----
#.  Written by David C. Stauffer in December 2013.
"""

#%% Imports
import dstauffman2.imageproc as dip

#%% Test script
if __name__ == '__main__':
    folder = r'E:\Pictures\eFrame\resized_1080p'
    dip.batch_resize(folder, max_width=1920, max_height=1080)
