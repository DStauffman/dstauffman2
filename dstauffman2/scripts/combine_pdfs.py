r"""
Script for combining some PDFs together.

Notes
-----
#.  Written by David C. Stauffer in June 2017.

"""

# %% Imports
from pathlib import Path

from pypdf import PdfWriter

# %% Constants
folder = Path(r"C:\Users\DStauffman\Desktop\print\pdf")

# %% Script
if __name__ == "__main__":
    files = ["Kari_page1.pdf", "Kari_pages_2_4.pdf", "Kari_page5.pdf", "Kari_page6.pdf"]

    merger = PdfWriter()
    for file in files:
        fullfile = folder / file
        merger.append(fullfile)

    merger.write(folder / "Kari Adoption Contract (Signed).pdf")
