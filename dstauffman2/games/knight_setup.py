"""Use Cython to build the code into a standalone app."""

from Cython.Build import cythonize  # type: ignore[import-not-found]
from distutils.core import setup  # type: ignore[import-not-found]
import numpy

setup(
    name="Knight app",
    ext_modules=cythonize("knight2.pyx", include_path=[numpy.get_include()]),
)
