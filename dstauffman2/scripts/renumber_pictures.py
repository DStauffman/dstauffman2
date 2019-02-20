# -*- coding: utf-8 -*-
r"""
This script renumbers the pictures in the given folder with a new prefix.

Notes
-----
#.  Written by David C. Stauffer in December 2018.
"""

#%% Imports
import dstauffman2.imageproc as dip

#%% Test script
if __name__ == '__main__':
    # folder to process
    folder = r'C:\Users\DStauffman\Downloads\Chrome'

    # command
    dip.number_files(folder, prefix='misc ', start=1, digits=3)

    # checks
    dip.rename_upper_ext(folder)
    dip.find_missing_nums(folder)
    dip.find_unexpected_ext(folder)