r"""
dstauffman python commands.

Notes
-----
#.  Written by David C. Stauffer in March 2020.
"""

#%% Imports
from dstauffman2.commands.camera   import parse_photos, execute_photos
from dstauffman2.commands.help     import print_help, print_version, parse_help, execute_help, \
                                              parse_version, execute_version
from dstauffman2.commands.runtests import parse_tests, execute_tests, parse_coverage, \
                                              execute_coverage

#%% Unittest
if __name__ == '__main__':
    pass
