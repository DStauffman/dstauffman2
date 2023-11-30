"""
Splits the given pages of a PDF file into a new output file.

Notes
-----
#.  Written by David C. Stauffer in February 2018.
"""

# %% Imports
from PyPDF2 import PdfFileReader, PdfFileWriter

# %% Constants
src_file = r"C:\Users\DStauffman\Downloads\member_list_2019-08-27_04-53.pdf"
out_file = r"C:\Users\DStauffman\Downloads\member_list_2019-08-27_page{}.pdf"
pages = [0, 1, 2, 3, 4, 5]

# %% Script
if __name__ == "__main__":
    # open the source file
    with open(src_file, "rb") as file:
        # get reader and writers
        reader = PdfFileReader(file)
        # read each desired page and send it to the writer
        for page in pages:
            writer = PdfFileWriter()
            writer.addPage(reader.getPage(page))
            # write out the accumulated pages to disk
            with open(out_file.format(page + 1), "wb") as out:
                writer.write(out)
