r"""
File containing useful custom iPython magic commands.

Notes
-----
#.  Written by David C. Stauffer in March 2017.
#.  This file is best placed in the iPython startup folder, somewhere like:
    C:\Users\DStauffman\.ipython\profile_default\startup ~or~
    C:\Programs\WinPython-64bit-3.6.1.0Qt5\settings\.ipython\profile_default\startup

"""

# %% Imports
from IPython.core.magic import register_line_magic


# %% Custom Magic Commands - reload_ghap
@register_line_magic
def reload_ghap(line):
    r"""Force reloading of `ghap` module."""
    from dstauffman import reload_package
    import ghap

    reload_package(ghap)


# %% Custom Magic Commands - reload_ghap
@register_line_magic
def reload_cromo(line):
    r"""Force reloading of `cromo` module."""
    from dstauffman import reload_package
    import cromo

    reload_package(cromo)


# %% Custom Magic Commands - reload_dstauffman
@register_line_magic
def reload_dstauffman(line):
    r"""Force reloading of `dstauffman` module."""
    import dstauffman

    dstauffman.reload_package(dstauffman)


# %% Custom Magic Commands - cc
@register_line_magic
def cc(line):
    r"""Like Matlab CC command."""
    from IPython import get_ipython
    import dstauffman
    import ghap

    dstauffman.reload_package(ghap, disp_reloads=False)
    dstauffman.reload_package(dstauffman, disp_reloads=False)
    get_ipython().magic("%reset -f")
    get_ipython().magic("%clear")


del reload_ghap, reload_cromo, reload_dstauffman, cc
