r"""
Renumbers the pictures in the given folder with a new prefix.

Notes
-----
#.  Written by David C. Stauffer in December 2018.
"""

#%% Imports
import re

import dstauffman2.imageproc as dip

#%% Test script
if __name__ == '__main__':
    # folder to process
    folder = r'C:\Users\DStauffman\Downloads\Chrome'

    name = re.match(r'.* - (?P<name>\w* \w*) - \w', folder)

    # command
    if name:
        dip.number_files(folder, prefix='Misc - ' + name['name'] + ' ', start=1, digits=3)

    # checks
    dip.rename_upper_ext(folder)
    dip.find_missing_nums(folder)
    dip.find_unexpected_ext(folder)