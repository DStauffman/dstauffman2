"""
Splits the given pages of a PDF file into a new output file.

Notes
-----
#.  Written by David C. Stauffer in February 2018.

"""

# %% Imports
from pypdf import PdfReader, PdfWriter

# %% Constants
src_file = r"C:\Users\DStauffman\Documents\GitHub\dstauffman2\Clarinet 3.pdf"
out_file = r"C:\Users\DStauffman\Documents\GitHub\dstauffman2\Clarinet_3_subset_print.pdf"
pages = [1, 2, 3, 4, None, 5, 6, 13, 14]  # pages is one based, instead of default python zero based
compress = True

# %% Script
if __name__ == "__main__":
    # open the source file
    with open(src_file, "rb") as file:
        # get reader and writers
        reader = PdfReader(file)
        # read each desired page and send it to the writer
        writer = PdfWriter()
        for page_num in pages:
            if page_num is None:
                writer.add_blank_page()
                continue
            this_page = reader.pages[page_num - 1]
            if compress:
                this_page.compress_content_streams()
            writer.add_page(this_page)
        # write out the accumulated pages to disk
        with open(out_file, "wb") as out:
            writer.write(out)
