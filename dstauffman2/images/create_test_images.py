"""Create some test images for use in PDF book-making."""

# %% Imports
from pathlib import Path

from PIL import Image

from dstauffman2 import get_images_dir

# %% Constants
_C = tuple[int, int, int]

# %% Functions - draw_gradient
def draw_gradient(width: int, height: int, color_one: _C, color_two: _C, direction: str) -> Image:
    base = Image.new("RGB", (width, height), color_one)
    top = Image.new("RGB", (width, height), color_two)
    mask = Image.new("L", (width, height))
    mask_data = []
    if direction.lower() == "horizontal":
        for y in range(height):
            mask_data += [int(255 * (y / height))] * width
    elif direction.lower() == "vertical":
        for y in range(height):
            mask_data += [int(255 * (x / width)) for x in range(width)]
    else:
        raise ValueError(f"Unexpected direction: {direction}")
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base


# %% Functions
def create_test_images(folder: Path, *, width: int = 4*300, height: int = 6*300, dpi: int = 300) -> None:
    """Create a bunch of simple images for use in testing."""
    # create black image
    black = Image.new("RGB", (width, height))
    black.paste((0, 0, 0), (0, 0, width, height))
    black.save(folder / "black.jpg", dpi=(dpi, dpi))

    # create white image
    white = Image.new("RGB", (width, height))
    white.paste((255, 255, 255), (0, 0, width, height))
    white.save(folder / "white.jpg", dpi=(dpi, dpi))

    # create different DPI gray image
    gray1 = Image.new("RGB", (width // 3, height // 3))
    gray1.paste((63, 63, 63), (0, 0, width // 3, height // 3))
    gray1.save(folder / "gray_one.jpg", dpi=(dpi // 3, dpi // 3))

    # create skinning gray image
    gray2 = Image.new("RGB", (width, height // 3 * 2))
    gray2.paste((127, 127, 127), (0, 0, width, height))
    gray2.save(folder / "gray_two.jpg", dpi=(dpi, dpi))

    # create fat gray image
    gray3 = Image.new("RGB", (width // 3 * 2, height))
    gray3.paste((191, 191, 191), (0, 0, width, height))
    gray3.save(folder / "gray_three.jpg", dpi=(dpi, dpi))

    # create small red image with gradient
    red = draw_gradient(width, height, (255, 0, 0), (63, 0, 0), "Horizontal")
    red.save(folder / "red.jpg", dpi=(dpi, dpi))

    # create large green image with gradient
    green = draw_gradient(width, height, (0, 255, 0), (0, 63, 0), "Vertical")
    green.save(folder / "green.jpg", dpi=(dpi, dpi))

    # create square blue image with gradient
    blue = draw_gradient(width, width, (0, 0, 255), (0, 0, 63), "Horizontal")
    blue.save(folder / "blue.jpg", dpi=(dpi, dpi))


# %% Script
if __name__ == "__main__":
    create_test_images(get_images_dir())
