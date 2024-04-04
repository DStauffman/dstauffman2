"""Create PDF Books of different types."""

# %% Imports
from dstauffman2 import get_images_dir
from dstauffman2.imageproc import build_book

# %% Script
if __name__ == "__main__":
    folder = get_images_dir()
    names = ["black", "white", "gray_one", "gray_two", "gray_three", "red", "green", "blue"]
    images = {key: folder.joinpath(key + ".jpg") for key in names}
    files = list(images.values())

    dpi = 300
    border = dpi // 4
    height = 4*dpi
    width = 6*dpi
    background_color = (255, 255, 255)
    line_color = (0, 0, 0)

    # %% Full page
    # build_book(
    #     files,
    #     folder / "Full Page.pdf",
    #     height=12*dpi,
    #     width=12*dpi,
    #     photo_height=12*dpi,
    #     photo_width=12*dpi,
    #     border=None,
    #     layout="full",
    #     background_color=(0, 0, 0),
    #     line_color=(255, 255, 0),
    #     rotate="none",
    # )

    # %% Full 6x4
    # build_book(
    #     files,
    #     folder / "Full Horizontal.pdf",
    #     height=4*dpi,
    #     width=6*dpi,
    #     photo_height=4*dpi,
    #     photo_width=6*dpi,
    #     border=None,
    #     layout="full",
    #     background_color=(0, 0, 0),
    #     line_color=(255, 255, 0),
    #     rotate="Horizontal",
    # )

    # %% Full 4x6
    border = dpi // 4
    # Note: border not working on full page
    build_book(
        files,
        folder / "Full Vertical.pdf",
        height=6 * dpi,
        width=4 * dpi,
        photo_height=6 * dpi + 2 * border,
        photo_width=4 * dpi + 2 * border,
        border=border,
        layout="full",
        background_color=(0, 0, 0),
        line_color=(255, 255, 0),
        rotate="Vertical",
    )
