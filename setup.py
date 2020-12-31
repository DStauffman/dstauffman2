r"""
Packaging setup file for Pypi and installation via pip.

Notes
-----
#.  Written by David C. Stauffer in January 2019.
"""

#%% Import
import os

from setuptools import setup

#%% Support functions
def readme():
    r"""Opens the README.rst file for additional descriptions."""
    filename = os.path.join(os.path.dirname(__file__), 'README.rst')
    with open(filename) as file:
        return file.read()

#%% Setup
setup(
    name='dstauffman2',
    version='1.0.0',
    description='Vaguely useful Python utilities, plus a playground for games and miscelllaneous code.',
    long_description=readme(),
    keywords='dstauffman dstauffman2 games playground spyder configuration',
    url='https://github.com/dstauffman/dstauffman2',
    author='David C. Stauffer',
    author_email='dstauffman@yahoo.com',
    license='LGPLv3',
    packages=['dstauffman2'],
    package_data={'dstauffman2': ['py.typed']},
    install_requires=[
        'h5py',
        'matplotlib',
        'numpy',
        'pandas',
        'PyQt5',
        'scipy',
    ],
    python_requires='>=3.8',
    include_package_data=True,
    zip_safe=False)
