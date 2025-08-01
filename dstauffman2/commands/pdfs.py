r"""
Functions related to processing photos from my digital camera.

Notes
-----
#.  Written by David C. Stauffer in December 2020.

"""

# %% Imports
import argparse
import doctest
import os
from typing import List, Tuple
import unittest

from pypdf import PdfMerger, PdfReader, PdfWriter


# %% Functions - split_pdf
def split_pdf(src_file: str, pages: Tuple[int], out_file: str = "out.pdf") -> None:
    r"""Splits a given PDF file into pieces."""
    # open the source file
    with open(src_file, "rb") as file:
        # get reader and writers
        reader = PdfReader(file)
        # read each desired page and send it to the writer
        for page in pages:
            writer = PdfWriter()
            writer.addPage(reader.getPage(page))
            # write out the accumulated pages to disk
            with open(out_file.format(page + 1), "wb") as out:
                writer.write(out)


# %% Functions - combine_pdf
def combine_pdf(folder: str, files: List[str], out_file: str = "out.pdf"):
    r"""Combines the given files into a master file"""
    merger = PdfMerger()
    out_file = out_file if os.path.pathsep in out_file else os.path.join(folder, out_file)
    for file in files:
        fullfile = os.path.join(folder, file)
        merger.append(fullfile)
    merger.write(out_file)


# %% Functions - parse_pdf
def parse_pdf(input_args: List[str]) -> argparse.Namespace:
    r"""
    Parser for the PDF command.

    Parameters
    ----------
    input_args : list of str
        Input arguments as passed to sys.argv for this command

    Returns
    -------
    args : class Namespace
        Arguments as parsed by argparse.parse_args

    Notes
    -----
    #.  Written by David C. Stauffer in December 2020.

    Examples
    --------
    >>> from dstauffman2.commands import parse_pdf`
    >>> input_args = ['split', '.', '-s', 'test.pdf', '-o', 'page1.pdf']
    >>> args = parse_pdf(input_args)
    >>> print(args)
    Namespace(folder='.', upper=False, missing=False, unexpected_ext=False, picasa=False, long=False, resize=False)

    """
    parser = argparse.ArgumentParser(prog="dcs2 pdf", description="PDF processing.")

    parser.add_argument("command", help="PDF command to run, from {combine, split}.", choices={"combine", "split"})

    parser.add_argument("folder", help="Folder to search for source files")

    parser.add_argument("-o", "--output", help="Output file to write the results to.", default="out.pdf", type="int")

    parser.add_argument("-s", "--source", help="Source file(s) to use in the command.")

    parser.add_argument("-p", "--pages", nargs="+", help="Pages to split into the output file.", required=False)

    args = parser.parse_args(input_args)
    return args


# %% Functions - execute_pdf
def execute_pdf(args: argparse.Namespace) -> int:
    r"""
    Executes the PDF processing commands.

    Parameters
    ----------
    args : class argparse.Namespace, with fields:
        .docstrings : bool
        .verbose : bool

    Returns
    -------
    return_code : int
        Return code for whether the command executed cleanly

    Notes
    -----
    #.  Written by David C. Stauffer in December 2020.

    Examples
    --------
    >>> from dstauffman2.commands import execute_photos
    >>> from argparse import Namespace
    >>> args = Namespace(folder='.', long=False, missing=False, picasa=False, resize=False, unexpected_ext=False, upper=False)
    >>> execute_photos(args) # doctest: +SKIP

    """
    # alias options
    # fmt: off
    command  = args.command
    folder   = os.path.abspath(args.folder)
    src_file = args.src_file
    out_file = args.out_file
    pages    = args.pages
    # fmt: on

    if command == "split":
        split_pdf(src_file=src_file, pages=pages, out_file=out_file)
    elif command == "combine":
        combine_pdf(folder=folder, files=src_file, out_file=out_file)


# %% Unit test
if __name__ == "__main__":
    unittest.main(module="dstauffman2.tests.test_commands_pdf", exit=False)
    doctest.testmod(verbose=False)
