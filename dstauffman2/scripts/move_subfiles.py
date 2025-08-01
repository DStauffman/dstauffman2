"""
Moves the files from any folders up to the root level.

Notes
-----
#.  Written by David C. Stauffer in December 2018.

"""

# %% Imports
import os
import shutil

# %% Script
if __name__ == "__main__":
    folder = r"C:\Users\DStauffman\Desktop\Camera"

    for this_sub in os.listdir(folder):
        this_full_sub = os.path.join(folder, this_sub)
        if os.path.isdir(this_full_sub):
            for this_file in os.listdir(this_full_sub):
                filename = os.path.join(this_full_sub, this_file)
                if os.path.isfile(filename):
                    print('Moving "{}" to "{}".'.format(filename, os.path.join(folder, this_file)))
                    shutil.move(filename, os.path.join(folder, this_file))
