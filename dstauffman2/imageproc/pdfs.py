r"""
PDF related functions for the "dstauffman2" library.

Contains a collection of functions for building, spliting, and combining PDF files.

Notes
-----
#.  Written by David C. Stauffer in March 2024.
"""  # pylint: disable=C0326

# %% Imports
import datetime
import doctest
from pathlib import Path
from typing import Any
import unittest

from PIL import Image


# %% Functions - _should_rotate
def _should_rotate(page_height: int, page_width: int, image_height: int, image_width: int) -> bool:
    if page_height == page_width or image_height == image_width:
        return False
    if page_height > page_width and image_height < image_width:
        return True
    if page_height < page_width and image_height > image_width:
        return True
    return False


# %% Functions - _build_full_12x12
def _build_full_12x12(
    files: list[Path], *, height: int, width: int, dpi: int, background_color: tuple[int, int, int], rotate: bool
) -> tuple[Any, Any]:
    # Create PDF of images
    num_images = len(files)
    book_pages = []
    assert len(files) % 2 == 0, "Expecting an even number of images."
    page = 1
    for ix, file in enumerate(files):
        print(f" Processing image {ix+1} of {num_images}, Page {page}, ({file})")
        this_image = Image.open(file)
        if rotate and _should_rotate(height, width, this_image.size[1], this_image.size[0]):
            this_image = this_image.rotate(90, expand=1)
        new_image = Image.new("RGB", (width, height))
        new_image.paste(background_color, (0, 0, width, height))
        this_image.thumbnail((width, height), Image.Resampling.LANCZOS)  # Note: will not increase size
        if this_image.size[0] < width and this_image.size[1] < height:
            ratio = max(this_image.size[0] / width, this_image.size[1] / height)
            new_size = (int(round(this_image.size[0] / ratio)), int(round(this_image.size[1] / ratio)))
            this_image = this_image.resize(new_size, Image.Resampling.LANCZOS)
        assert this_image.size[0] == width or this_image.size[1] == height, "Must be full size."
        offset_x = (width - this_image.size[0]) // 2
        offset_y = (height - this_image.size[1]) // 2
        new_image.paste(this_image, (offset_x, offset_y))
        if ix == 0:
            # first page, just keep image
            book = new_image
            page += 1
        elif ix == num_images - 1:
            # last page, which should be single, so save it
            book_pages.append(new_image)
            page += 1
        elif ix % 2 == 1:
            # save for next loop
            left = new_image
        else:
            full = Image.new("RGB", (2*width, height))
            full.paste(left, (0, 0))
            full.paste(new_image, (width, 0))
            book_pages.append(full)
            page += 1

    return book, book_pages


# %% Functions - _build_dual_4x6
def _build_dual_4x6(
    files: list[Path],
    *,
    height: int,
    width: int,
    photo_height: int,
    photo_width: int,
    border: int,
    dpi: int,
    background_color: tuple[int, int, int],
) -> tuple[Any, Any]:
    pass


# %% Functions - build_book
def build_book(
    files: list[Path | list[Path]],
    pdf_filename: Path,
    *,
    width: int = 300*12,
    height: int = 300*12,
    photo_width: int = 300*12,
    photo_height: int = 300*12,
    dpi: int = 300,
    layout: str = "full",
    background_color: tuple[int, int, int] = (0, 0, 0),
    rotate: bool = False,
) -> None:
    """
    Creates the PDF file from the given images.

    Parameters
    ----------
    files : list[pathlib.Path | list[pathlib.Path]]
        List of files to use to create PDF
    pdf_filename : Path
        Output filename to create the PDF
    width : int
        Page width in pixels
    height : int
        Page height in pixels
    dpi : int
        Pixels per inch
    layout : str | list[str]
        Layout, or list of layout per page
    background_color : tuple[int, int, int]
        Background color as integer RGB, default is black
    rotate : bool, optional, default is False
        Whether to rotate the photo to maximize its size on the page

    Notes
    -----
    #.  Written by David C. Stauffer in March 2024.

    Examples
    --------
    >>> from dstauffman2.imageproc import build_book
    >>> files = []

    """
    # create the metadata
    meta: dict[str, str | datetime.datetime] = {}
    meta["Title"] = "PDF Figures"
    meta["Author"] = "David C. Stauffer"
    meta["CreationDate"] = datetime.datetime.now()
    meta["ModDate"] = meta["CreationDate"]

    print(f"Making Book: {pdf_filename}")
    if layout == "full":
        book, book_pages = _build_full_12x12(
            files, height=height, width=width, dpi=dpi, background_color=background_color, rotate=rotate
        )
    elif layout == "dual_4x6":
        book, book_pages = _build_dual_4x6(files)
    elif layout in {"triple_4x6",}:
        raise NotImplementedError("Not yet implemented.")
    else:
        raise ValueError(f"Unexpected layout: {layout}")

    if bool(files):
        # TODO: metadata not saving?
        book.save(pdf_filename, save_all=True, append_images=book_pages, metadata=meta, dpi=(dpi, dpi))


# %% Unit test
if __name__ == "__main__":
    unittest.main(module="dstauffman2.imageproc.test_pdfs", exit=False)
    doctest.testmod(verbose=False)
