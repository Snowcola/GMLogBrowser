import pandas as pd
from pathlib import Path
import os
path = Path("C:\\Users\\u7j9\\ATCO Group\\O365Grp_Measurement Management - Instrumentation Priority Work")
files = list(path.glob('*.xlsx'))

file_names = [
    "ACCID",
    "CKEQM",
    "CKEVC",
    "CKHUC_TRUSG",
    "TRCID"
]

pfiles = []

for name in file_names:

    for f in files:
        print(f'checking {name} in {f.name}')
        if name in f.name:
            print(f"match for {name}")
            pfiles.append(f)
            files.remove(f)
            continue
            

print(*pfiles, sep='\n')

for i, item in enumerate(pfiles):
    pfiles[i] = pd.read_excel(item)

result = pd.concat(pfiles, keys=file_names, sort=True)
result.index.rename(names=['Job_type', 'id'], inplace=True)
result.reset_index(col_level=1, col_fill='job_type', inplace=True)
result.set_index(result['Service Point'], inplace=True)
result.sort_index(inplace=True)
result['Dispatched to:'] = result['Dispatched to:'] + result['dispatched to:']
result['Problem/Comment'] = result['PROBLEM'] + result['Comment'] + result['comments'] 
cols = ['Job_type', 'Job','AMR', 'Instrument', 'Meter Location','Grid','Address','Operation Centre',  'Create Date',
         'High Use',  
       'Tech', 'Ventyx ID',  'Dispatched to:','Problem/Comment']
result = result[cols]
print(result.head())
print(result.columns)
x = result.to_excel('inst_jobs_simple.xlsx')
os.startfile('inst_jobs_simple.xlsx')