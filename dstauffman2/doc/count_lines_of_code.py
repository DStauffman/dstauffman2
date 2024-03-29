r"""
Uses the CLOC utility to produce a lines of code count for the dstauffman and hesat repos.

Notes
-----
#.  Written by David C. Stauffer in April 2017.
#.  Updated by David C. Stauffer in March 2019 to process pyhesat.
"""

# %% Imports
import json
import os
import subprocess

from dstauffman import get_root_dir, make_conclusion, make_preamble


# %% Functions
def process_repo(name, root, tests, exclude):
    r"""
    Processes the given repository for a line of code count.

    Notes
    -----
    #.  All lines in the tests folder are considered "tests".
    #.  All lines in .tex, .xml, and .md files are considered "docs".
    """
    # hard-coded values
    langs = frozenset({"Python", "MATLAB", "DOS Batch", "Bourne Shell"})
    exclu = frozenset({"header", "SUM", "CSS", "HTML", "JSON", "JavaScript"})  # set(data.keys()) - langs - exclu - docs
    docs  = frozenset({"TeX", "XML", "Markdown"})
    types = frozenset({"blank", "comment", "code"})

    # get test folder results
    test_root = os.path.join(root, tests)
    command   = [cloc, test_root, "--json"]
    result    = subprocess.run(command, stdout=subprocess.PIPE)
    json_text = result.stdout.decode("utf-8")
    data      = json.loads(json_text)

    # check that nothing unexpected was found
    temp = set(data.keys()) - langs - exclu - docs
    assert len(temp) == 0, "Extra data was found: {}".format(temp)

    # get the total number of test lines of code
    lines = {"tests": sum(data["SUM"][x] for x in types)}
    files = {"tests": data["SUM"]["nFiles"]}

    # get root results with applied exclusions
    dirs = []
    for excl in exclude:
        dirs.append("-exclude_dir")
        dirs.append(excl)
    command   = [cloc, root, "--json"] + dirs
    result    = subprocess.run(command, stdout=subprocess.PIPE)
    json_text = result.stdout.decode("utf-8")
    data      = json.loads(json_text)

    # check that nothing unexpected was found
    assert len(set(data.keys()) - langs - exclu - docs) == 0

    # get the line counts
    # TODO: pull out the documentation lines from the rest
    lines["total"]   = sum(data["SUM"][subkey] for subkey in types) + lines["tests"]
    lines["code"]    = sum(data[key]["code"] for key in langs if key in data)
    lines["comment"] = sum(data[key]["comment"] for key in langs if key in data)
    lines["blank"]   = sum(data[key]["blank"] for key in langs if key in data)
    lines["docs"]    = sum(data[key][subkey] for key in docs for subkey in types if key in data)
    files["total"]   = data["SUM"]["nFiles"] + files["tests"]

    # organize output
    out = {"name": name, "lines": lines, "files": files}

    # print results
    print_results(**out)

    return out


# %% Functions - print_results
def print_results(name, lines, files):
    r"""Prints the results from the given dictionary."""
    print(f"******** {name} ********")
    print(f" Files: {files['total']}, ({100*files['tests']/files['total']:.1f}% tests)")
    print(f" Total lines of code: {lines['total']}")
    print('  Code: {} ({:.1f}%), Comments: {} ({:.1f}%), Blank: {} ({:.1f}%), Tests: {} ({:.1f}%), Documentation: {} ({:.1f}%)'.format(\
         lines['code'], 100*lines['code']/lines['total'], lines['comment'], 100*lines['comment']/lines['total'], \
         lines['blank'], 100*lines['blank']/lines['total'], lines['tests'], 100*lines['tests']/lines['total'], \
         lines['docs'], 100*lines['docs']/lines['total']))
    print('')


# %% Functions - combine_results
def combine_results(out1, out2):
    r"""Combines the results from the two given dictionaries."""
    out = {}
    for key in out1:
        if key == "name":
            out[key] = out1[key] + "+" + out2[key]
        else:
            out[key] = {}
            for subkey in out1[key]:
                out[key][subkey] = out1[key][subkey] + out2[key][subkey]
    return out


# %% Functions - print_latex_tables
def print_latex_tables(out, keys):
    r"""Prints the tables for inclusion in our LaTeX documents."""
    cols = ["total", "code", "comment", "blank", "tests", "docs"]

    text = []
    text += make_preamble('Count Lines of Code Breakdown','tab:cloc','lcccccc')
    text.append(r'        \textbf{Module} & \textbf{Total} & \textbf{Code} & \textbf{Comments} & \textbf{Blank} & \textbf{Tests} & \textbf{Documentation} \\ \midrule')
    for key in keys:
        lines = out[key]['lines']
        if '+' in key:
            name = 'total'
            midrule = ''
        else:
            name = key
            midrule = r' \midrule'
        values = ' & '.join('{}'.format(lines[x]) for x in cols)
        text.append(r'        \multirow{2}[3]{*}{\textbf{\texttt{' + name + r'}}} & ' + values + r' \\')
        #(100\%) & (36.0\%) & (28.6\%) & (22.4\%) & (9.3\%) & (3.7\%)
        values = ' & '.join('({:.1f}\\%)'.format(100*lines[x]/lines['total']) for x in cols)
        text.append(r'        & ' + values + r' \\' + midrule)
    text += make_conclusion()

    text = '\n'.join(text)
    print(text)

    return text


# %% Script
if __name__ == "__main__":
    # Constants
    # location of cloc utility
    root = os.path.sep.join(get_root_dir().split(os.path.sep)[:-2])
    cloc = os.path.join(root, "cloc-1.70.exe")
    # repositories to process
    repos = {k: {} for k in ["dstauffman", "hesat"]}

    # test folder and other exclusion settings
    repos["dstauffman"]["name"]    = "dstauffman"
    repos["dstauffman"]["root"]    = os.path.join(root, "dstauffman", "dstauffman")
    repos["dstauffman"]["tests"]   = "tests"
    repos["dstauffman"]["exclude"] = ["data", "images", "output", "results", "temp"]

    repos["hesat"]["name"]    = "hesat"
    repos["hesat"]["root"]    = os.path.join(root, "pyhesat", "hesat")
    repos["hesat"]["tests"]   = "tests"
    repos["hesat"]["exclude"] = ["data", "output"]

    # process repos
    out = {}
    for key in repos:
        out[key] = process_repo(**repos[key])

    # hesat and dstauffman
    out["hesat+dstauffman"] = combine_results(out["hesat"], out["dstauffman"])
    print_results(**out["hesat+dstauffman"])

    # print the LaTeX tables
    print_latex_tables(out, ["dstauffman", "hesat", "hesat+dstauffman"])
