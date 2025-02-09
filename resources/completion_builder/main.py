# General operations performed by the scripts found in this directory:
# 
# 1. Covert the function data found in func_data_list.txt to JSON, where each has:
#       "func_name" (String)
#       "req_param" (Array)
#       "opt_param" (Array)
#       "ellipsis" (Boolean)
#
# 2. Build out completion strings for param-having functions
# 
# 4. Covert the function metadata found in func_ref.xlsx to JSON
# 
# 4. Match completion strings to descriptions, categories, and function names
# 
# 3. Build out completion strings for nullary functions
# 
# Last. Build out entire .sublime-completions file.
# 
# NOTE: Not all ellipsis == True functions follow the same format, e.g.:
#       1. COUNTA~value1,[value2],...
#       2. COUNTIFS~criteria_range1,criteria1,...
#       Before running this script, clean formulas that look like 2. to look like 1. using your best judgement and find using:
#           [^\]],\.{3}

# TODO: Allow this entire directory to switch between application specific information like the `scope` found in this file and
#       the file names used by all scripts instead of having to refactor a bunch of stuff every time.

import subprocess
import json

scripts = ['js.py', 'cb.py', 'ld.py', 'mg.py']

toggle_rerun = False

if toggle_rerun:
    for script in scripts:
        print(f'Running {script}...')
        result = subprocess.run(['python3', script], check = True)
        if result.returncode != 0:
            print(f'Error occured while running {script}')
            break
        print(f'{script} completed successfully')

master_file = open('func_master.json', 'r')

master_list = json.load(master_file)

master_file.close()

completions = []

for func in master_list:
    trigger = func.get('func_name')
    contents = func.get('comp_str')
    annotation = func.get('func_cat')
    details = func.get('func_desc')
    kind = 'function'
    completions.append(dict(trigger = trigger, contents = contents, annotation = annotation, details = details, kind = kind))

dict_list = dict(scope = 'source.sheet.excel - string - comment', completions = completions)

json_out = json.dumps(dict_list, indent = 4)

o = open('.sublime-completions', 'w')

o.write(json_out)
o.close()