# See main.py for overview.

import json
import sys

app = sys.argv[1]

func_file = open(f'{app}_funcs_comp.json', 'r')

js_func = json.load(func_file)

func_file.close()

ref_file = open(f'{app}_funcs_ref.json', 'r')

js_ref = json.load(ref_file)

ref_file.close()

print('Length of Reference List: ' + str(len(js_ref)))
print('Length of Completions List: ' + str(len(js_func)))

# Goal: For each object in _ref,
#           if "is_nullary" == True:
#               (DONE) look for a matching function in _func and return the "comp_str" field, then load it into a new field for the current object in _ref.
#           if "is_nullary" == False:
#               generate a nullary-specific completion string using f'={func_name}()', then load it into a new field for the current object in _ref.

# Note: Drops the true and false functions to prevent them making their way into the final list.
js_ref = [ref for ref in js_ref if ref['func_name'] not in ['TRUE', 'FALSE']]
 
for ref in js_ref:
    func_name = ref.get('func_name')

    if ref.get('is_nullary'):
        ref['comp_str'] = f'={func_name}()'

    else:
        try:
            lookup = next(((func['comp_str'], func['ellipsis']) for func in js_func if func['func_name'] == func_name), None)
            ref['comp_str'] = lookup[0]
            ref['ellipsis'] = lookup[1]
        except:
            print("\nError when when matching comp_str for nonnullary function:")
            print(f'ref func_name: {func_name}')
            print(f'lookup: {lookup}')

print('Length of Master List: ' + str(len(js_ref)))

o = open(f'{app}_funcs_master.json', 'w')

json_out = json.dumps(js_ref, indent = 4)

o.write(json_out)
o.close()