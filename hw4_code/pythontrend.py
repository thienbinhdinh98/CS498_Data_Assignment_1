import sys
from pyhive import hive
import json
import os
import pandas as pd
import numpy as np

conn = hive.Connection(host = '0.0.0.0', port = 10000, username = 'thienbinhdinh98', database='default')
cur = conn.cursor()
inputTerm = ""
for i in range(1, len(sys.argv)):
    if(i == len(sys.argv)-1):
        inputTerm+= sys.argv[i]
    else:
        inputTerm += sys.argv[i] + " "
new_term = inputTerm.replace('\n', '')
query = ''' SELECT sum(val) FROM (select term, temp.val as val FROM searchTerm LATERAL VIEW EXPLODE(click_map) temp as URL, val WHERE term = "%s") as new GROUP by term ''' %(new_term)
df = pd.read_sql(query, conn);

res =dict( df['_c0'])
for i in res:
    num = res[i]
print(num, flush = True)
