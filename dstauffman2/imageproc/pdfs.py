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
DEBUG_COLOR: _C = (255, 0, 0)  # (255, 255, 0)
DEBUG_WIDTH: int = 3


# %% Functions - _should_rotate
def _should_rotate(rotate: str, *, height: int, width: int) -> bool:
    """Determine if an image should be rotated or not."""
    assert rotate.lower() in {"none", "horizontal", "vertical", "horizontal_clockwise", "vertical_clockwise"}
    if rotate.lower() == "none":
        return False
    if height == width:
        return False
    if rotate.lower().startswith("vertical") and height < width:
        return True
    if rotate.lower().startswith("horizontal") and height > width:
        return True
    return False


# %% Functions - _resize_image
def _resize_image(image: Image.Image, *, width: int, height: int) -> Image.Image:
    """Resize the image, which will also upsample if necessary."""
    # Note: thumbnial will not increase size
    image.thumbnail((width, height), Image.Resampling.LANCZOS)
    if image.size[0] < width and image.size[1] < height:
        # This code is to upscale as necessary
        ratio = max(image.size[0] / width, image.size[1] / height)
        new_size = (int(round(image.size[0] / ratio)), int(round(image.size[1] / ratio)))
        image = image.resize(new_size, Image.Resampling.LANCZOS)
    assert image.size[0] == width or image.size[1] == height, "Must be full size."
    return image


# %% Functions - _build_full_page
def _build_full_page(this_image: Image.Image, *, width: int, height: int, background_color: _C, border: int, debug: bool) -> Image.Image:
    """Builds a full page from the given image."""
    new_image = Image.new("RGB", (width, height))
    new_image.paste(background_color, (0, 0, width, height))
    this_image = _resize_image(this_image, width=width - 2 * border, height=height - 2 * border)
    offset_x = (width - this_image.size[0]) // 2
    offset_y = (height - this_image.size[1]) // 2
    new_image.paste(this_image, (offset_x, offset_y))
    if debug:
        draw = ImageDraw.Draw(new_image)
        draw.rectangle((border, border, border + width, border + height), outline=DEBUG_COLOR, width=DEBUG_WIDTH)
    return new_image


# %% Functions - _build_dual_page
def _build_dual_page(
    new_image: Image.Image,
    images: list[Image.Image],
    *,
    width: int,
    height: int,
    border: int,
    center_offset: int,
    background_color: _C,
    right: bool,
    debug: bool,
) -> Image.Image:
    """Add up to three photos to the given page."""
    is_horizontal = [image.size[0] >= image.size[1] for image in images]
    offset1 = border
    offset2 = 2 * border + height
    offset_left = border
    offset_right = border + center_offset
    offset_delta = width - height
    if all(is_horizontal):
        assert len(images) == 2, "Expect two images if all horizontal."
    else:
        assert len(images) == 1, "Expect one image if any are vertical."

    if is_horizontal[0]:
        assert is_horizontal[1]
        offsets = (offset_right, offset1) if right else (offset_left, offset1)
        new_image.paste(images[0], offsets)
        if debug:
            draw = ImageDraw.Draw(new_image)
            draw.rectangle((offsets[0], offsets[1], offsets[0] + width, offsets[1] + height), outline=DEBUG_COLOR, width=DEBUG_WIDTH)  # fmt: skip
        offsets = (offset_right, offset2) if right else (offset_left, offset2)
        new_image.paste(images[1], offsets)
        if debug:
            draw = ImageDraw.Draw(new_image)
            draw.rectangle((offsets[0], offsets[1], offsets[0] + width, offsets[1] + height), outline=DEBUG_COLOR, width=DEBUG_WIDTH)  # fmt: skip
    else:
        if right:
            offsets = (offset_right, offset1 + offset_delta // 2)
        else:
            offsets = (offset_left + offset_delta, offset1 + offset_delta // 2)
        new_image.paste(images[0], offsets)
        if debug:
            draw = ImageDraw.Draw(new_image)
            draw.rectangle((offsets[0], offsets[1], offsets[0] + height, offsets[1] + width), outline=DEBUG_COLOR, width=DEBUG_WIDTH)  # fmt: skip

    return new_image


# %% Functions - _build_triplet_page
def _build_triplet_page(
    new_image: Image.Image,
    images: list[Image.Image],
    *,
    width: int,
    height: int,
    border: int,
    center_offset: int,
    background_color: _C,
    right: bool,
    debug: bool,
) -> Image.Image:
    """Add up to three photos to the given page."""
    is_horizontal = [image.size[0] >= image.size[1] for image in images]
    offset1 = border
    offset2 = 2 * border + height
    offset3 = 3 * border + 2 * height
    offset_left = border
    offset_right = border + center_offset
    offset_delta = width - height
    offset_half = 3 * border + 3 * height - width  # full page height - border - width
    if all(is_horizontal):
        assert len(images) == 3, "Expect three images if all horizontal."
    else:
        assert len(images) == 2, "Expect two images if any are vertical."

    if is_horizontal[0]:
        offsets = (offset_right, offset1) if right else (offset_left, offset1)
    else:
        offsets = (offset_right, offset1) if right else (offset_left + offset_delta, offset1)
    new_image.paste(images[0], offsets)
    if debug:
        draw = ImageDraw.Draw(new_image)
        temp = (width, height) if is_horizontal[0] else (height, width)
        draw.rectangle((offsets[0], offsets[1], offsets[0] + temp[0], offsets[1] + temp[1]), outline=DEBUG_COLOR, width=DEBUG_WIDTH)  # fmt: skip
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
    if debug:
        draw = ImageDraw.Draw(new_image)
        temp = (width, height) if is_horizontal[1] else (height, width)
        draw.rectangle((offsets[0], offsets[1], offsets[0] + temp[0], offsets[1] + temp[1]), outline=DEBUG_COLOR, width=DEBUG_WIDTH)  # fmt: skip
    if all(is_horizontal):
        offsets = (offset_right, offset3) if right else (offset_left, offset3)
        new_image.paste(images[2], offsets)
        if debug:
            draw = ImageDraw.Draw(new_image)
            draw.rectangle((offsets[0], offsets[1], offsets[0] + width, offsets[1] + height), outline=DEBUG_COLOR, width=DEBUG_WIDTH)  # fmt: skip

    return new_image


# %% Functions - _build_quad_page
def _build_quad_page(
    new_image: Image.Image,
    images: list[Image.Image],
    *,
    width: int,
    height: int,
    border: int,
    center_offset: int,
    background_color: _C,
    right: bool,
    debug: bool,
) -> Image.Image:
    """Add up to four photos to the given page in a 2x2 grid."""

    def _add_image(new_image: Image.Image, this_image: Image.Image, offsets: tuple[int, int], debug: bool, is_horizontal: bool):
        new_image.paste(this_image, offsets)
        if debug:
            draw = ImageDraw.Draw(new_image)
            big = max(width, height)
            sml = min(width, height)
            temp = (big, sml) if is_horizontal else (sml, big)
            draw.rectangle((offsets[0], offsets[1], offsets[0] + temp[0], offsets[1] + temp[1]), outline=DEBUG_COLOR, width=DEBUG_WIDTH)  # fmt: skip

    is_horizontal = [image.size[0] >= image.size[1] for image in images]
    offset1 = border
    offset2 = 2 * border + height
    offset_left1 = border
    offset_right1 = border + center_offset
    offset_left2 = 2 * border + width
    offset_right2 = 2 * border + width + center_offset
    assert len(images) == 4, "Expect four images in quad layout."
    offsets = (offset_right1, offset1) if right else (offset_left1, offset1)
    _add_image(new_image, images[0], offsets, debug, is_horizontal[0])
    offsets = (offset_right2, offset1) if right else (offset_left2, offset1)
    _add_image(new_image, images[1], offsets, debug, is_horizontal[1])
    offsets = (offset_right1, offset2) if right else (offset_left1, offset2)
    _add_image(new_image, images[2], offsets, debug, is_horizontal[2])
    offsets = (offset_right2, offset2) if right else (offset_left2, offset2)
    _add_image(new_image, images[3], offsets, debug, is_horizontal[3])
    new_image.paste(images[3], offsets)

    return new_image


# %% Functions - _build_single_page
def _build_single_page(
    files: list[Path],
    *,
    height: int,
    width: int,
    border: int,
    background_color: _C,
    line_color: _OC,
    rotate: str,
    debug: bool,
) -> tuple[Image.Image, list[Image.Image]]:
    """Create single image pages for book."""
    num_images = len(files)
    book_pages = []
    assert len(files) % 2 == 0, "Expecting an even number of images."
    page = 1
    for ix, file in enumerate(files):
        print(f" Processing image {ix+1} of {num_images}, Page {page}, ({file})")
        this_image: Image.Image = Image.open(file)
        if _should_rotate(rotate, height=this_image.size[1], width=this_image.size[0]):
            if rotate.lower().endswith("clockwise"):
                this_image = this_image.rotate(-90, expand=1)
            else:
                this_image = this_image.rotate(90, expand=1)
        new_image = _build_full_page(
            this_image, width=width, height=height, background_color=background_color, border=border, debug=debug
        )
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
            full = Image.new("RGB", (2 * width, height))
            full.paste(left, (0, 0))
            full.paste(new_image, (width, 0))
            if line_color is not None:
                draw = ImageDraw.Draw(full)
                draw.line((width, 0, width, height), fill=line_color, width=1)
            book_pages.append(full)
            page += 1

    return book, book_pages


# %% Functions - _build_multipage
def _build_multipage(
    files: list[list[Path]],
    *,
    layout: str,
    height: int,
    width: int,
    photo_height: int,
    photo_width: int,
    border: int,
    center_offset: int,
    background_color: _C,
    line_color: _OC,
    rotate: str,
    debug: bool,
) -> tuple[Image.Image, list[Image.Image]]:
    """Create multi-image pages for book."""
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
            this_image: Image.Image = Image.open(file)
            if _should_rotate(rotate, height=this_image.size[1], width=this_image.size[0]):
                if rotate.lower().endswith("clockwise"):
                    this_image = this_image.rotate(-90, expand=1)
                else:
                    this_image = this_image.rotate(90, expand=1)
            if this_image.size[0] > this_image.size[1] and photo_width < photo_height:
                this_image = _resize_image(this_image, width=photo_height, height=photo_width)
            elif this_image.size[0] < this_image.size[1] and photo_width > photo_height:
                this_image = _resize_image(this_image, width=photo_height, height=photo_width)
            else:
                this_image = _resize_image(this_image, width=photo_width, height=photo_height)
            images.append(this_image)
            ix += 1

        new_image = Image.new("RGB", (width, height))
        new_image.paste(background_color, (0, 0, width, height))
        if layout.startswith("dual"):
            _build_dual_page(
                new_image,
                images,
                width=photo_width,
                height=photo_height,
                border=border,
                center_offset=center_offset,
                right=is_right,
                background_color=background_color,
                debug=debug,
            )
        elif layout.startswith("trip"):
            _build_triplet_page(
                new_image,
                images,
                width=photo_width,
                height=photo_height,
                border=border,
                center_offset=center_offset,
                right=is_right,
                background_color=background_color,
                debug=debug,
            )
        elif layout.startswith("quad"):
            _build_quad_page(
                new_image,
                images,
                width=photo_width,
                height=photo_height,
                border=border,
                center_offset=center_offset,
                right=is_right,
                background_color=background_color,
                debug=debug,
            )
        else:
            raise ValueError(f"Unexpected layout: {layout}")
        if page == 1:
            # first page, just keep image
            book = new_image
            continue
        if not is_right:
            # save for next loop
            left = new_image
            if ix < num_images:
                # not the last page, then continue
                continue
            # is the last page, and it's only the left, then save
            book_pages.append(new_image)
            break
        full = Image.new("RGB", (2 * width, height))
        full.paste(left, (0, 0))
        full.paste(new_image, (width, 0))
        if line_color is not None:
            draw = ImageDraw.Draw(full)
            draw.line((width, 0, width, height), fill=line_color, width=1)
        book_pages.append(full)

    return book, book_pages


# %% Functions - build_book
def build_book(
    files: list[Path] | list[list[Path]],
    pdf_filename: Path,
    *,
    width: int = 300 * 12,
    height: int = 300 * 12,
    photo_width: int = 300 * 12,
    photo_height: int = 300 * 12,
    border: int = 0,
    dpi: int = 300,
    layout: str = "full",
    center_offset: int = 0,
    background_color: _C = (0, 0, 0),
    line_color: _OC = None,
    rotate: str = "None",
    debug: bool = False,
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
    border: int
        Border width in pixels
    dpi : int
        Pixels per inch
    layout : str
        Layout of pages, from {"full", "dual_4x6", "triple_4x6"}
    center_offset : int
        The offset from center in pixels
    background_color : tuple[int, int, int]
        Background color as integer RGB, default is black
    line_color : tuple[int, int, int], optional
        Line color between side by side pages, if None, then no line
    rotate : str, optional, default is "None"
        Whether to rotate the photo to maximize its size on the page,
        from {"None", "Horizontal", "Vertical", "horizontal_clockwise", "vertical_clockwise"}
    debug : bool, optional, default is False
        Whether to print debug information

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
        book, book_pages = _build_single_page(
            files,  # type: ignore[arg-type]
            height=height,
            width=width,
            border=border,
            background_color=background_color,
            line_color=line_color,
            rotate=rotate,
            debug=debug,
        )
    elif layout in {"dual_4x6", "triple_4x6", "quad_4x6"}:
        book, book_pages = _build_multipage(
            files,  # type: ignore[arg-type]
            layout=layout,
            height=height,
            width=width,
            photo_width=photo_width,
            photo_height=photo_height,
            border=border,
            center_offset=center_offset,
            background_color=background_color,
            line_color=line_color,
            rotate=rotate,
            debug=debug,
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
