import os
from dstauffman import find_tabs

root_folder = r'C:\Users\DStauffman\Documents\GitHub'
trailing = True
list_all = False
eol = '\n'

find_tabs(os.path.join(root_folder, 'matlab'), trailing=trailing, list_all=list_all, check_eol=eol)
find_tabs(os.path.join(root_folder, 'matlab2'), trailing=trailing, list_all=list_all, check_eol=eol)
find_tabs(os.path.join(root_folder, 'hesat'), trailing=trailing, list_all=list_all, check_eol=eol)
