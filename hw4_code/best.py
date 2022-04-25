import sys
from pyhive import hive
import json
import os
import pandas as pd
import numpy as np

conn = hive.Connection(host = '0.0.0.0', port = 10000, username = 'thienbinhdinh98', database='default')
inputSite = ""
for i in range(1, len(sys.argv)):
    if(i == len(sys.argv)-1):
        inputSite+= sys.argv[i]
    else:
        inputSite += sys.argv[i] + " "
new_site = inputSite.replace('\n', '')
query = ''' select term from (select term, sum(val) as sm, max(curr) as cur from (select *, click_map["%s"] as curr from searchTerm where click_map["%s"] is not NULL) as new LATERAL VIEW EXPLODE(click_map) temp as URL, val group by term) as new2 where cur/sm >= 0.05 '''%(new_site, new_site)
df = pd.read_sql(query, conn)
res =  dict(df["term"])
ans = ""
count = 0
for i in res:
    if(count != len(res)-1):
        ans += res[i] + ','
    else:
        ans += res[i]
    count+=1

print(ans, flush = True)
