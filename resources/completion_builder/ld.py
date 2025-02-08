import json
import pandas as pd

# Must use na_filter = False to prevent the func_name field of the NA() function's object being set to null.
ref_file = pd.read_excel('func_ref.xlsx', sheet_name = 'Sheet1', na_filter = False).to_json(orient = 'records', indent = 4)

o = open('excel_funcs_ref.json', 'w')

o.write(ref_file)