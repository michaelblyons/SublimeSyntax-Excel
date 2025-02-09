# See main.py for overview.

import json
import pandas as pd
import sys

app = sys.argv[1]

# Must use na_filter = False to prevent the func_name field of the NA() function's object being set to null.
ref_file = pd.read_excel(f'{app}_funcs_ref.xlsx', sheet_name = 'Sheet1', na_filter = False).to_json(orient = 'records', indent = 4)

o = open(f'{app}_funcs_ref.json', 'w')

o.write(ref_file)