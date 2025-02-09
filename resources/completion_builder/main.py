# General operations performed by the scripts found in this directory:
# 
# 1. Covert the function data found in func_data_list.txt to JSON, where each has:
#       "func_name" (String)
#       "req_param" (Array)
#       "opt_param" (Array)
#       "ellipsis" (Boolean)
#    ⮡ js.py ("json")
#
# 2. Build out completion strings for param-having functions
#    ⮡ cb.py ("completion builder")
# 
# 3. Covert the function metadata found in func_ref.xlsx to JSON
#    ⮡ ld.py ("load")
#       
# 4. Match completion strings to descriptions, categories, and function names
#    ⮡ mg.py ("merge")
# 
# 5. Build out completion strings for nullary functions
#       (Nullary functions are not included during the OCR which creates the *_data_list_raw.txt file.
#        Nullary functions are however included in the *_funcs_ref.xlsx file, so this is where they
#        are managed.)
#    ⮡ mg.py
#    
# 6. Remove TRUE() and FALSE() from consideration if present in *_funcs_ref.xlsx
#    ⮡ mg.py
# 
# 7. Run all subscripts (if toggle_rerun is enabled) and build out entire .sublime-completions file.
#    ⮡ main.py
# 
# NOTE: Not all `ellipsis == True` functions follow the same format, e.g.:
#       1. COUNTA~value1,[value2],...
#       2. COUNTIFS~criteria_range1,criteria1,...
#       Before running this script, clean formulas in *_funcs_data_list.txt that look like 2. to look like 1. using your best judgement. Find them using:
#           [^\]],\.{3}

# TODO: Allow this entire directory to switch between application specific information like the `scope` found in this file and
#       the file names used by all scripts instead of having to refactor a bunch of stuff every time.

import subprocess
import json

# Switch subscript versions as needed.
# These functions pass information through input/output files and sys.argv based on the value of `app`,
# so they can be used in any combination if that is maintained.
subscripts = ['js.py', 'cb.py', 'ld.py', 'mg.py']

# Takes values of 'excel', 'google', 'libre'
app = 'excel'

# Boolean-toggled rerun of subscripts
toggle_rerun = True

if toggle_rerun:
    print(f'App Config: {app}')
    for subscript in subscripts:
        print(f'Running {subscript}...')
        result = subprocess.run(['python3', subscript, app], check = True)
        if result.returncode != 0:
            print(f'Error occured while running {subscript}')
            break
        print(f'{subscript} completed successfully')

master_file = open(f'{app}_funcs_master.json', 'r')

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

dict_list = dict(scope = f'source.sheet.{app} - string - comment', completions = completions)

json_out = json.dumps(dict_list, indent = 4)

o = open('.sublime-completions', 'w')

o.write(json_out)
o.close()