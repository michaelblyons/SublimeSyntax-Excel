import json

# Expected:
#   "FORECAST.ETS(${1:target_date}, ${2:values}, ${3:timeline}${4:${5/.+/, /}${5:[seasonality]}${6/.+/, /}${6:[data_completion]}${7/.+/, /}${7:[aggregation]}})"
#   "CHOOSECOLS(${1:array}, ${2:col_num1}${3:${4/.+/, /}${4:[col_num2], ...}})"

# Actual:
#   "FORECAST.ETS(${1:target_date}, ${2:values}, ${3:timeline}${4:${5/.+/, /}${5:[seasonality]}${6/.+/, /}${6:[data_completion]}${7/.+/, /}${7:[aggregation]}})"
#   "CHOOSECOLS(${1:array}, ${2:col_num1}${3:${4/.+/, /}${4:[col_num2], ...}})"

func_file = open('excel_funcs.json', 'r')

js = json.load(func_file)

func_file.close()

dict_list = []

for func in js:
    func_name = func.get('func_name')

    comp_str = func_name + '('

    param_id = 0

    req_param = func.get('req_param') 

    for req in req_param:
        param_id += 1

        if param_id > 1:
            comp_str += ', '

        comp_str += f'${{{param_id}:{req}}}'

    opt_param = func.get('opt_param')

    ellipsis = func.get('ellipsis')

    if opt_param:
        num_opt_param = len(opt_param)

        num_param = num_opt_param + len(req_param)

        param_id += 1

        comp_str += f'${{{param_id}:'

        for opt in opt_param:
            param_id += 1

            comp_str += f'${{{param_id}/.+/, /}}'

            if param_id == num_param + 1 and ellipsis == True:
                comp_str += f'${{{param_id}:[{opt}], ...}}'

            else:
                comp_str += f'${{{param_id}:[{opt}]}}'

        comp_str += '}'

    comp_str += ')'

    dict_list.append(dict(func_name = func_name, req_param = req_param, opt_param = opt_param, ellipsis = ellipsis, comp_str = comp_str))

    # Debug
    # if func_name == 'CHOOSECOLS':
    #     print(comp_str)

    #     break

json_out = json.dumps(dict_list, indent = 4)

o = open('excel_funcs_comp.json', 'w')

o.write(json_out)
o.close()
