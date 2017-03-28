# -*- coding: utf-8 -*-
r"""
File containing useful custom iPython magic commands.

Notes
-----
#.  Written by David C. Stauffer in March 2017.
#.  This file is best placed in the iPython startup folder, somewhere like:
    C:\Users\DStauffman\.ipython\profile_default\startup
"""

#%% Imports
from IPython.core.magic import register_line_magic
from dstauffman import reload_package

#%% Custom Magic Commands - reload_ghap
@register_line_magic
def reload_ghap(line):
    r"""Force reloading of `ghap` module."""
    import ghap
    reload_package(ghap)

#%% Custom Magic Commands - reload_ghap
@register_line_magic
def reload_cromo(line):
    r"""Force reloading of `cromo` module."""
    import cromo
    reload_package(cromo)

#%% Custom Magic Commands - reload_ghap
@register_line_magic
def reload_dstauffman(line):
    r"""Force reloading of `dstauffman` module."""
    import dstauffman
    reload_package(dstauffman)
