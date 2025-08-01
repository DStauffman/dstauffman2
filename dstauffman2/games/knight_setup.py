from Cython.Build import cythonize
from distutils.core import setup
import numpy

setup(
    name="Knight app",
    ext_modules=cythonize("knight2.pyx", include_path=[numpy.get_include()]),
)
