import numpy
from Cython.Build import cythonize
from distutils.core import setup

setup(
    name = "Knight app",
    ext_modules = cythonize('knight2.pyx', include_path=[numpy.get_include()]),
)
