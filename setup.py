r"""
Packaging setup file for Pypi and installation via pip.

Notes
-----
#.  Written by David C. Stauffer in January 2019.
"""

# %% Import
from pathlib import Path

from setuptools import setup


# %% Support functions - readme
def readme():
    r"""Opens the README.rst file for additional descriptions."""
    filename = Path(__file__).resolve().parent / "README.rst"
    with open(filename) as file:
        return file.read()


# %% Support functions - get_version
def get_version():
    r"""Reads the version information from the library."""
    filename = Path(__file__).resolve().parent.joinpath("dstauffman2", "version.py")
    with open(filename) as file:
        text = file.read()
    for line in text.splitlines():
        if line.startswith("version_info = "):
            return line.split("(")[1].split(")")[0].replace(", ", ".")
    raise RuntimeError("Unable to load version information.")


# %% Setup
setup(
    name="dstauffman2",
    version=get_version(),
    description="Vaguely useful Python utilities, plus a playground for games and miscelllaneous code.",
    long_description=readme(),
    keywords="dstauffman dstauffman2 games playground spyder configuration",
    url="https://github.com/dstauffman/dstauffman2",
    author="David C. Stauffer",
    author_email="dstauffman@yahoo.com",
    license="LGPLv3",
    packages=["dstauffman2"],
    package_data={"dstauffman2": ["py.typed"]},
    install_requires=[
        "dstauffman",
        "h5py",
        "matplotlib",
        "numpy",
        "pandas",
        "PyQt5",
        "pytest",
        "scipy",
        "slog",
    ],
    python_requires=">=3.8",
    include_package_data=True,
    zip_safe=False,
)
