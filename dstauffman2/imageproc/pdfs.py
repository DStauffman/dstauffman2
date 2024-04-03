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
import unittest

from PIL import Image, ImageDraw

# %% Constants
_C = tuple[int, int, int]
_OC = None | _C


# %% Functions - _should_rotate
def _should_rotate(page_height: int, page_width: int, image_height: int, image_width: int) -> bool:
    """Determine if an image should be rotated or not."""
    if page_height == page_width or image_height == image_width:
        return False
    if page_height > page_width and image_height < image_width:
        return True
    if page_height < page_width and image_height > image_width:
        return True
    return False


# %% Functions - _resize_image
def _resize_image(image: Image, width: int, height: int) -> Image:
    """Resize the image, which will also upsample if necessary."""
    image.thumbnail((width, height), Image.Resampling.LANCZOS)  # Note: will not increase size
    if image.size[0] < width and image.size[1] < height:
        ratio = max(image.size[0] / width, image.size[1] / height)
        new_size = (int(round(image.size[0] / ratio)), int(round(image.size[1] / ratio)))
        image = image.resize(new_size, Image.Resampling.LANCZOS)
    assert image.size[0] == width or image.size[1] == height, "Must be full size."
    return image


# %% Functions - _build_full_page
def _build_full_page(this_image: Image, *, width: int, height: int, background_color: _C) -> Image:
    """Builds a full page from the given image."""
    new_image = Image.new("RGB", (width, height))
    new_image.paste(background_color, (0, 0, width, height))
    this_image = _resize_image(this_image, width, height)
    offset_x = (width - this_image.size[0]) // 2
    offset_y = (height - this_image.size[1]) // 2
    new_image.paste(this_image, (offset_x, offset_y))
    return new_image


# %% Functions - _build_dual_page
def _build_dual_page():
    pass


# %% Functions - _build_triplet_page
def _build_triplet_page(new_image: Image, images: list[Image], *, width: int, height: int, border: int, background_color: _C, right: bool) -> Image:
    """Add up to three photos to the given page."""
    is_horizontal = [image.size[0] >= image.size[1] for image in images]
    offset1 = border
    offset2 = 2 * border + height
    offset3 = 3 * border + 2 * height
    offset_left = border
    offset_right = 6 * border  # full page width - border - width
    offset_delta = width - height
    offset_half = 3*border + 3*height - width  # full page height - border - width
    if all(is_horizontal):
        assert len(images) == 3, "Expect three images if all horizontal."
    else:
        assert len(images) == 2, "Expect two images if any are vertical."

    if is_horizontal[0]:
        offsets = (offset_right, offset1) if right else (offset_left, offset1)
    else:
        offsets = (offset_right, offset1) if right else (offset_left + offset_delta, offset1)
    new_image.paste(images[0], offsets)
    if is_horizontal[0]:
        if is_horizontal[1]:
            offsets = (offset_right, offset2) if right else (offset_left, offset2)
        else:
            offsets = (offset_right, offset_half) if right else (offset_left + offset_delta, offset_half)
    else:
        if is_horizontal[1]:
            offsets = (offset_right, offset3) if right else (offset_left, offset3)
        else:
            offsets = (offset_right, offset_half) if right else (offset_left + offset_delta, offset_half)
    new_image.paste(images[1], offsets)
    if all(is_horizontal):
        offsets = (offset_right, offset3) if right else (offset_left, offset3)
        new_image.paste(images[2], offsets)

    return new_image


# %% Functions - _build_full_12x12
def _build_full_12x12(
    files: list[Path], *, height: int, width: int, background_color: _C, line_color: _OC, rotate: bool
) -> tuple[Image, list[Image]]:
    """Create full pages for book."""
    num_images = len(files)
    book_pages = []
    assert len(files) % 2 == 0, "Expecting an even number of images."
    page = 1
    for ix, file in enumerate(files):
        print(f" Processing image {ix+1} of {num_images}, Page {page}, ({file})")
        this_image = Image.open(file)
        if rotate and _should_rotate(height, width, this_image.size[1], this_image.size[0]):
            this_image = this_image.rotate(90, expand=1)
        new_image = _build_full_page(this_image, width=width, height=height, background_color=background_color)
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
            if line_color is not None:
                draw = ImageDraw.Draw(full)
                draw.line((width, 0, width, height), fill=line_color, width=1)
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
    background_color: _C,
    line_color: _OC,
    rotate: bool,
) -> tuple[Image, list[Image]]:
    """Create dual pages for book."""
    num_images = len(files)
    book_pages = []
    page = 1
    for ix, file in enumerate(files):
        print(f" Processing image {ix+1} of {num_images}, Page {page}, ({file})")
        this_image = Image.open(file)
        if rotate and _should_rotate(height, width, this_image.size[1], this_image.size[0]):
            this_image = this_image.rotate(90, expand=1)
        new_image = _build_full_page(this_image, width=width, height=height, background_color=background_color)
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
            if line_color is not None:
                draw = ImageDraw.Draw(full)
                draw.line((width, 0, width, height), fill=line_color, width=1)
            book_pages.append(full)
            page += 1

    return book, book_pages


# %% Functions - _build_triplet_4x6
def _build_triplet_4x6(
    files: list[list[Path]],
    *,
    height: int,
    width: int,
    photo_height: int,
    photo_width: int,
    border: int,
    background_color: _C,
    line_color: _OC,
    rotate: bool,
) -> tuple[Image, list[Image]]:
    """Create triplet pages for book."""
    num_images = sum(len(page) for page in files)
    book_pages = []
    page = 0
    ix = 0
    is_right = False
    for subfiles in files:
        page += 1
        is_right = not is_right
        images = []
        for file in subfiles:
            print(f" Processing image {ix+1} of {num_images}, Page {page}, ({file})")
            this_image = Image.open(file)
            if this_image.size[0] >= this_image.size[1]:
                images.append(_resize_image(this_image, width=photo_width, height=photo_height))
            else:
                images.append(_resize_image(this_image, width=photo_height, height=photo_width))
            ix += 1

        new_image = Image.new("RGB", (width, height))
        new_image.paste(background_color, (0, 0, width, height))
        _build_triplet_page(new_image, images, width=photo_width, height=photo_height, border=border, right=is_right, background_color=background_color)
        if page == 1:
            # first page, just keep image
            book = new_image
        elif ix == num_images - 1:
            # last page, which should be single, so save it
            book_pages.append(new_image)
        elif not is_right:
            # save for next loop
            left = new_image
        else:
            full = Image.new("RGB", (2*width, height))
            full.paste(left, (0, 0))
            full.paste(new_image, (width, 0))
            if line_color is not None:
                draw = ImageDraw.Draw(full)
                draw.line((width, 0, width, height), fill=line_color, width=1)
            book_pages.append(full)

    return book, book_pages


# %% Functions - build_book
def build_book(
    files: list[Path | list[Path]],
    pdf_filename: Path,
    *,
    width: int = 300*12,
    height: int = 300*12,
    photo_width: int = 300*12,
    photo_height: int = 300*12,
    border: int = 0,
    dpi: int = 300,
    layout: str = "full",
    background_color: _C = (0, 0, 0),
    line_color: _OC = None,
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
    photo_width : int
        Photo width in pixels
    photo_height : int
        Photo height in pixels
    dpi : int
        Pixels per inch
    layout : str
        Layout of pages, from {"full", "dual_4x6", "triple_4x6"}
    background_color : tuple[int, int, int]
        Background color as integer RGB, default is black
    line_color : tuple[int, int, int], optional
        Line color between side by side pages, if None, then no line
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
            files,
            height=height,
            width=width,
            background_color=background_color,
            line_color=line_color,
            rotate=rotate,
        )
    elif layout == "dual_4x6":
        book, book_pages = _build_dual_4x6(files)
    elif layout in {"triple_4x6",}:
        book, book_pages = _build_triplet_4x6(
            files,
            height=height,
            width=width,
            photo_width=photo_width,
            photo_height=photo_height,
            border=border,
            background_color=background_color,
            line_color=line_color,
            rotate=rotate,
        )
    else:
        raise ValueError(f"Unexpected layout: {layout}")

    if bool(files):
        # TODO: metadata not saving?
        book.save(pdf_filename, save_all=True, append_images=book_pages, metadata=meta, dpi=(dpi, dpi))
        print(f"Book saved to: {pdf_filename}")


# %% Unit test
if __name__ == "__main__":
    unittest.main(module="dstauffman2.imageproc.test_pdfs", exit=False)
    doctest.testmod(verbose=False)
