import sys
from pyhive import hive
import json
import os
import pandas as pd
import numpy as np

conn = hive.Connection(host = '0.0.0.0', port = 10000, username = 'thienbinhdinh98', database='default')
inputTerm = ""
for i in range(1, len(sys.argv)):
    if(i == len(sys.argv)-1):
        inputTerm+= sys.argv[i]
    else:
        inputTerm += sys.argv[i] + " "
new_term = inputTerm.replace('\n', '')
query = ''' SELECT click_map FROM searchTerm WHERE term == "%s"'''%(new_term)
df = pd.read_sql(query, conn)
res =  dict(df["click_map"])
for i in res:
    js = json.loads(res[i])

print(js, flush = True)
