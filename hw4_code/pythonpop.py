import sys
from pyhive import hive
import json
import os
import pandas as pd
import numpy as np

conn = hive.Connection(host = '0.0.0.0', port = 10000, username = 'thienbinhdinh98', database='default')
inputURL = ""
for i in range(1, len(sys.argv)):
    if(i == len(sys.argv)-1):
        inputURL+= sys.argv[i]
    else:
        inputURL += sys.argv[i] + " "
new_url = inputURL.replace('\n', '')
query = ''' select sum(val) from (select click_map["%s"] as val from searchTerm where click_map["%s"] is not NULL) as new'''%(new_url, new_url)
df = pd.read_sql(query, conn)

res = dict(df['_c0'])
for i in res:
    num =  res[i]
print(num)
