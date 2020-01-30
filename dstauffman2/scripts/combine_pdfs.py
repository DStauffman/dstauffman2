# -*- coding: utf-8 -*-
r"""
Script for combining some PDFs together.

Notes
-----
#.  Written by David C. Stauffer in June 2017.
"""

#%% Imports
import os

from PyPDF2 import PdfFileMerger

#%% Constants
folder = r'C:\Users\DStauffman\Documents\Lockheed_Martin\Security_Clearance'

#%% Script
if __name__ == '__main__':
    files = ['2019-01 - work_experience.pdf',
             '2019-01 - resume_references.pdf',
             ]

    merger = PdfFileMerger()
    for file in files:
        fullfile = os.path.join(folder, file)
        merger.append(fullfile)

    merger.write(os.path.join(folder, '2019-01 - Additional Work Experience plus references for Stauffer.pdf'))
