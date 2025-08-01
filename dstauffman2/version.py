r"""
Functions related to version history.

Notes
-----
#.  Written by David C. Stauffer in January 2021.

"""

# %% Constants
version_info = (1, 2, 0)

# Below is data about the minor release history for potential use in deprecating older support.
# For inspiration, see: https://numpy.org/neps/nep-0029-deprecation_policy.html

data = """Jan 4, 2021: dstauffman2 1.0
Nov 2, 2023: dstauffman2 1.1
Jul 31, 2025: dstauffman2 1.2
"""

# Historical notes:
# v1.0 Inital Release
# v1.1 Support Python standards for black, isort, flake8, pylint, and mypy.
# v1.2 Convert to uv instead of poetry.
