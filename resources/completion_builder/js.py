# Plan
# 1. (DONE) Covert the function data to JSON, where each has:
#       "func_name" (String)
#       "req_param" (Array)
#       "opt_param" (Array)
#       "ellipsis" (Boolean)
# 2. (DONE) Write code to build out completion strings for param-having functions
# 
# 3. Write code to build out completion strings for nullary functions
# 
# 4. Write code to match completion strings to descriptions, categories, and function names(?)
# 
# Last. Write code to build out entire .sublime-completions file.
# 
# NOTE: Not all ellipsis == True functions follow the same format, e.g.:
#       1. COUNTA~value1,[value2],...
#       2. COUNTIFS~criteria_range1,criteria1,...
#       Before running this script, clean formulas that look like 2. to look like 1. using your best judgement and find using:
#           [^\]],\.{3}

import json
import re

func_file = 'func_data_list.txt'

with open(func_file, 'r') as file:
    func_list = [line.strip() for line in file]

# Debug
# func_list = ['CALL~register_id,[argument1],...']

dict_list = []

for line in func_list:
    func_name = line.split('~')[0]

    param_str = line.split('~')[1]

    param_list = param_str.split(',')

    req_param = []

    opt_param = []

    ellipsis = False

    for param in param_list:
        if param[0] == '[':
            opt_param.append(re.sub(r'[\[\]]', '', param))

        elif param[0] == '.':
            ellipsis = True

        else:
            req_param.append(param)

    func_dict = dict(func_name = func_name, req_param = req_param, opt_param = opt_param, ellipsis = ellipsis)

    dict_list.append(func_dict)

json_out = json.dumps(dict_list, indent = 4)

o = open('excel_funcs.json', 'w')

o.write(json_out)
o.close()