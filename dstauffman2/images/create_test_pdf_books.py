"""Create PDF Books of different types."""

# %% Imports
from dstauffman2 import get_images_dir
from dstauffman2.imageproc import build_book

# %% Script
if __name__ == "__main__":
    # %% Configuration
    folder = get_images_dir()
    names = ["black", "white", "gray_one", "gray_two", "gray_three", "red", "green", "blue"]
    images = {key: folder.joinpath(key + ".jpg") for key in names}
    files = list(images.values())
    dual_files = [[files[0], files[1]], [files[2], files[3]], [files[4], files[5]], [files[6], files[7]]]

    dpi = 300
    border = dpi // 4
    height = 4*dpi
    width = 6*dpi
    background_color = (255, 255, 255)
    line_color = (0, 0, 0)
    debug = True

    # %% Full page
    build_book(
        files,
        folder / "Full Page.pdf",
        height=12*dpi,
        width=12*dpi,
        photo_height=12*dpi,
        photo_width=12*dpi,
        border=0,
        layout="full",
        background_color=(0, 0, 0),
        line_color=(255, 255, 255),
        rotate="none",
        debug=debug,
    )

    # %% Full 6x4
    build_book(
        files,
        folder / "Full Horizontal.pdf",
        height=height,
        width=width,
        photo_height=height,
        photo_width=width,
        border=0,
        layout="full",
        background_color=(0, 0, 0),
        line_color=(255, 255, 255),
        rotate="Horizontal",
        debug=debug,
    )

    # %% Full 4x6
    border = dpi // 4
    build_book(
        files,
        folder / "Full Vertical.pdf",
        height=height + 2 * border,
        width=width + 2 * border,
        photo_height=height,
        photo_width=width,
        border=border,
        layout="full",
        background_color=(0, 0, 0),
        line_color=(255, 255, 255),
        rotate="Vertical",
        debug=debug,
    )

    # %% Dual 4x6
    # no border
    build_book(
        dual_files,
        folder / "Dual Horizontal.pdf",
        height=2 * height,
        width=width,
        photo_height=height,
        photo_width=width,
        border=0,
        layout="dual_4x6",
        background_color=(0, 0, 0),
        line_color=(255, 255, 255),
        rotate="Horizontal",
        debug=debug,
    )

    # %% Dual 4x6
    # with border
    this_files = [[files[0]], [files[1]], [files[2]], [files[3], files[5]], [files[5], files[7]], [files[4]], [files[6]]]
    build_book(
        this_files,
        folder / "Dual Horizontal Border.pdf",
        height=2 * height + 3 * border,
        width=width + 2 * border,
        photo_height=height,
        photo_width=width,
        border=border,
        layout="dual_4x6",
        background_color=(255, 255, 255),
        line_color=(63, 63, 63),
        rotate="None",
        debug=debug,
    )

    # %% Dual 4x6
    # with border and center offset
    this_files = [[files[0]], [files[1]], [files[2]], [files[3], files[5]], [files[5], files[7]], [files[4]], [files[6]]]
    build_book(
        this_files,
        folder / "Dual Horizontal Offset.pdf",
        height=2 * height + 3 * border,
        width=width + 5 * border,
        photo_height=height,
        photo_width=width,
        border=border,
        center_offset=3*border,
        layout="dual_4x6",
        background_color=(255, 255, 255),
        line_color=(63, 63, 63),
        rotate="None",
        debug=debug,
    )

    # %% Triplet 4x6
    # no border
    this_files = [[files[0], files[1]], [files[2], files[4]], [files[3], files[7], files[3]], [files[4], files[5]], [files[6], files[6]]]
    build_book(
        this_files,
        folder / "Triple Horizontal.pdf",
        height=3 * height,
        width=width,
        photo_height=height,
        photo_width=width,
        border=0,
        center_offset=0,
        layout="triple_4x6",
        background_color=(20, 20, 20),
        line_color=(191, 191, 191),
        rotate="None",
        debug=debug,
    )

    # %% Triplet 4x6
    # with border
    this_files = [[files[0], files[1]], [files[2], files[4]], [files[3], files[7], files[3]], [files[4], files[5]], [files[6], files[6]]]
    build_book(
        this_files,
        folder / "Triple Horizontal Border.pdf",
        height=3 * height + 4 * border,
        width=width + 2 * border,
        photo_height=height,
        photo_width=width,
        border=border,
        center_offset=0,
        layout="triple_4x6",
        background_color=(20, 20, 20),
        line_color=(191, 191, 191),
        rotate="None",
        debug=debug,
    )

    # %% Triplet 4x6
    # with border and center offset
    this_files = [[files[0], files[1]], [files[2], files[4]], [files[3], files[7], files[3]], [files[4], files[5]], [files[6], files[6]]]
    build_book(
        this_files,
        folder / "Triple Horizontal Offset.pdf",
        height=3 * height + 4 * border,
        width=width + 7 * border,
        photo_height=height,
        photo_width=width,
        border=border,
        center_offset=5 * border,
        layout="triple_4x6",
        background_color=(20, 20, 20),
        line_color=(191, 191, 191),
        rotate="None",
        debug=debug,
    )

    # %% Quad 4x6
    # no border horizontal

    # %% Quad 4x6
    # with border horizontal

    # %% Quad 4x6
    # with border horizontal and center offset

    # %% Quad 4x6
    # no border vertical

    # %% Quad 4x6
    # with border vertical

    # %% Quad 4x6
    # with border vertical and center offset
