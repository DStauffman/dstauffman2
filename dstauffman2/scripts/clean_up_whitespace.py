"""Clean-up the whitespace in the given folder."""

# %% Imports
from pathlib import Path

from drepo import find_repo_issues

# %% Settings
root_folder = Path(r"C:\Users\DStauffman\Documents\GitHub")
trailing = True
list_all = False
eol = "\n"

# %% Script
if __name__ == "__main__":
    find_repo_issues(root_folder.joinpath("matlab"), trailing=trailing, list_all=list_all, check_eol=eol)
    find_repo_issues(root_folder.joinpath("matlab2"), trailing=trailing, list_all=list_all, check_eol=eol)
    find_repo_issues(root_folder.joinpath("hesat"), trailing=trailing, list_all=list_all, check_eol=eol)
