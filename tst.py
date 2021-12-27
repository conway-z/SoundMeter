import pandas as pd
dfsradd = pd.read_excel("locapi/files/dfout-merge.xlsx", sheet_name='Sheet1')
# dfsradd['dislist'] = dfsradd['dislist'].str.split(',')
# dfsradd['dislist'] =dfsradd['dislist'].apply(lambda x: max(x,key=x.count))
#     # dfsradd.apply(lambda x: max(x['dislist'],key=x['dislist'].count))
# # max(dfout3['dislist'],key=dfout3['dislist'].count)
print(dfsradd[['orgid','dislist']])
