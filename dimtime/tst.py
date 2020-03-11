import pandas as pd

# df_work = pd.read_csv("WORK_DAY.csv")
# df_work['is_work_day'] = df_work['values']
# df_work['index'] = df_work['index'].apply(lambda x: int(x))
# df_base = pd.read_csv("DIM_TIME.csv")
# df_base['date_int1'] =  df_base['id'].apply(lambda x:int(str(x).replace('-','')))
# del df_work['values']
# # df_base['id_trans'] = data['id'].apply(lambda x:str(x).replace('-',''))
# df_merge = pd.merge(df_base, df_work, how='left', left_on='date_int1', right_on='index')
# del df_merge['index']
#
# print(df_merge)
print('20200311'[0:8])