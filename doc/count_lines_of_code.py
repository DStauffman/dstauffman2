# -*- coding: utf-8 -*-
r"""
This script uses the CLOC utility to produce a lines of code count for the cromo, dstauffman, and
ghap repositories.

Notes
-----
#.  Written by David C. Stauffer in April 2017.
"""

#%% Imports
import os
import json
import subprocess
from dstauffman import get_root_dir

#%% Functions
def process_repo(name, root, tests, exclude):
    r"""
    Processes the given repository for a line of code count.

    Notes
    -----
    #.  All lines in the tests folder are considered "tests".
    #.  All lines in .tex, .xml, and .md files are considered "docs".
    """
    # hard-coded values
    langs = frozenset({'Python', 'MATLAB', 'DOS Batch'})
    exclu = frozenset({'header', 'SUM'})
    docs  = frozenset({'TeX', 'XML', 'Markdown'})
    types = frozenset({'blank', 'comment', 'code'})

    # get test folder results
    test_root = os.path.join(root, tests)
    command   = [cloc, test_root, '--json']
    result    = subprocess.run(command, stdout=subprocess.PIPE)
    json_text = result.stdout.decode('utf-8')
    data      = json.loads(json_text)

    # check that nothing unexpected was found
    assert len(set(data.keys()) - langs - exclu - docs) == 0

    # get the total number of test lines of code
    lines = {'tests': sum(data['SUM'][x] for x in types)}
    files = {'tests': data['SUM']['nFiles']}

    # get root results with applied exclusions
    dirs = []
    for excl in exclude:
        dirs.append('-exclude_dir')
        dirs.append(excl)
    command   = [cloc, root, '--json'] + dirs
    result    = subprocess.run(command, stdout=subprocess.PIPE)
    json_text = result.stdout.decode('utf-8')
    data      = json.loads(json_text)

    # check that nothing unexpected was found
    assert len(set(data.keys()) - langs - exclu - docs) == 0

    # get the line counts
    # TODO: pull out the documentation lines from the rest
    lines['total']   = sum(data['SUM'][subkey] for subkey in types) + lines['tests']
    lines['code']    = sum(data[key]['code'] for key in langs if key in data)
    lines['comment'] = sum(data[key]['comment'] for key in langs if key in data)
    lines['docs']    = sum(data[key][subkey] for key in docs for subkey in types if key in data)
    lines['blank']   = sum(data[key]['blank'] for key in langs if key in data)
    files['total']   = data['SUM']['nFiles'] + files['tests']

    # organize output
    out = {'name': name, 'lines': lines, 'files': files}

    # print results
    print_results(**out)

    return out

#%% Functions - print_results
def print_results(name, lines, files):
    r"""Prints the results from the given dictionary."""
    print(f"******** {name} ********")
    print(f" Files: {files['total']}, ({100*files['tests']/files['total']:.1f}% tests)")
    print(f" Total lines of code: {lines['total']}")
    print('  Code: {} ({:.1f}%), Comments: {} ({:.1f}%), Blank: {} ({:.1f}%), Tests: {} ({:.1f}%), Documentation: {} ({:.1f}%)'.format(\
         lines['code'], 100*lines['code']/lines['total'], lines['tests'], 100*lines['tests']/lines['total'], \
         lines['comment'], 100*lines['comment']/lines['total'], lines['blank'], 100*lines['blank']/lines['total'], \
         lines['docs'], 100*lines['docs']/lines['total']))
    print('')

#%% Functions - combine_results
def combine_results(out1, out2):
    r"""Combines the results from the two given dictionaries."""
    out = {}
    for key in out1:
        if key == 'name':
            out[key] = out1[key] + '+' + out2[key]
        else:
            out[key] = {}
            for subkey in out1[key]:
                out[key][subkey] = out1[key][subkey] + out2[key][subkey]
    return out

#%% Script
if __name__ == '__main__':
    # Constants
    # location of cloc utility
    root  = os.path.sep.join(get_root_dir().split(os.path.sep)[:-1])
    cloc  = os.path.join(root, 'cloc-1.70.exe')
    # repositories to process
    repos = {k:{} for k in ['cromo', 'dstauffman', 'ghap']}

    # test folder and other exclusion settings
    repos['cromo']['name']    = 'cromo'
    repos['cromo']['root']    = os.path.join(root, 'cromo')
    repos['cromo']['tests']   = 'tests'
    repos['cromo']['exclude'] = ['output']

    repos['dstauffman']['name']    = 'dstauffman'
    repos['dstauffman']['root']    = os.path.join(root, 'dstauffman')
    repos['dstauffman']['tests']   = 'tests'
    repos['dstauffman']['exclude'] = ['data', 'images', 'output', 'results' ,'temp']

    repos['ghap']['name']    = 'ghap'
    repos['ghap']['root']    = os.path.join(root, 'ghap')
    repos['ghap']['tests']   = 'tests'
    repos['ghap']['exclude'] = ['data', 'output']

    # process repos
    out = {}
    for key in repos:
        out[key] = process_repo(**repos[key])

    # cromo and dstauffman
    out['cromo+dstauffman'] = combine_results(out['cromo'], out['dstauffman'])
    print_results(**out['cromo+dstauffman'])

    # ghap and dstauffman
    out['ghap+dstauffman'] = combine_results(out['ghap'], out['dstauffman'])
    print_results(**out['ghap+dstauffman'])
