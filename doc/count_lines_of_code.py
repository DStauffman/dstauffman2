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

#%% Functions
def process_repo(name, root, tests, exclude):
    r"""
    Processes the given repository for a line of code count.
    """
    # hard-coded values
    langs = frozenset({'Python', 'TeX', 'XML', 'MATLAB', 'Markdown', 'DOS Batch'})
    exclu = frozenset({'header', 'SUM'})

    # get test folder results
    test_root = os.path.join(root, tests)
    command   = [cloc, test_root, '--json']
    result    = subprocess.run(command, stdout=subprocess.PIPE)
    json_text = result.stdout.decode('utf-8')
    data      = json.loads(json_text)

    # check that nothing unexpected was found
    assert len(set(data.keys()) - langs - exclu) == 0

    # get the total number of test lines of code
    lines_tests = sum(data['SUM'][x] for x in ['blank', 'comment', 'code'])
    files_tests = data['SUM']['nFiles']

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
    assert len(set(data.keys()) - langs - exclu) == 0

    # get the line counts
    lines_total = sum(data['SUM'][x] for x in ['blank', 'comment', 'code']) + lines_tests
    lines_codes = data['SUM']['code']
    lines_commt = data['SUM']['comment']
    lines_blank = data['SUM']['blank']
    files_total = data['SUM']['nFiles'] + files_tests

    # organize output
    keys = ['name', 'lines_total', 'lines_codes', 'lines_tests', 'lines_commt', 'lines_blank', 'files_total', 'files_tests']
    temp = locals()
    out  = {key: temp[key] for key in keys}

    # print results
    print_results(out)

    return out

#%% Functions - print_results
def print_results(out):
    r"""Prints the results from the given dictionary."""
    print(f"******** {out['name']} ********")
    print(f" Files: {out['files_total']}, ({100*out['files_tests']/out['files_total']:.1f}% tests)")
    print(f" Total lines of code: {out['lines_total']}")
    print('  Code: {} ({:.1f}%), Tests: {} ({:.1f}%), Comments: {} ({:.1f}%), Blank: {} ({:.1f}%)'.format(\
         out['lines_codes'], 100*out['lines_codes']/out['lines_total'], \
         out['lines_tests'], 100*out['lines_tests']/out['lines_total'], \
         out['lines_commt'], 100*out['lines_commt']/out['lines_total'], \
         out['lines_blank'], 100*out['lines_blank']/out['lines_total']))
    print('')

#%% Functions - combine_results
def combine_results(out1, out2):
    r"""Combines the results from the two given dictionaries."""
    out = {}
    for key in out1:
        if key == 'name':
            out[key] = out1[key] + '+' + out2[key]
        else:
            out[key] = out1[key] + out2[key]
    return out

#%% Script
if __name__ == '__main__':
    # Constants
    # location of cloc utility
    cloc  = r'C:\Users\dcstauff\Documents\GitHub\cloc-1.70.exe'
    root  = r'C:\Users\dcstauff\Documents\GitHub'
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
    print_results(out['cromo+dstauffman'])

    # ghap and dstauffman
    out['ghap+dstauffman'] = combine_results(out['ghap'], out['dstauffman'])
    print_results(out['ghap+dstauffman'])
