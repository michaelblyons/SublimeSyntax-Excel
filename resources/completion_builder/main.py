#! /usr/bin/env python3

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
