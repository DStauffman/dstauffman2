r"""
Script for combining some PDFs together.

Notes
-----
#.  Written by David C. Stauffer in June 2017.

"""

# %% Imports
from pathlib import Path

from pypdf import PdfMerger

# %% Constants
folder = Path(r"C:\Users\DStauffman\Documents\Lockheed_Martin\Security_Clearance")

# %% Script
if __name__ == "__main__":
    files = ["2019-01 - work_experience.pdf", "2019-01 - resume_references.pdf"]

    merger = PdfMerger()
    for file in files:
        fullfile = folder / file
        merger.append(fullfile)

    merger.write(folder / "2019-01 - Additional Work Experience plus references for Stauffer.pdf")
