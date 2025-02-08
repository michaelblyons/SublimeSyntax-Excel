import subprocess
import json

# TODO: Allow this entire directory to switch between application specific information like the `scope` found in this file and
#       the file names used by all scripts instead of having to refactor a bunch of stuff every time.

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