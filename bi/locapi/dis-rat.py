import requests
import math
import json
import pandas as pd
import pandas as pd
import numpy as np
import math
import difflib

# dfr = pd.read_excel("bi/locapi/dfout-merge.xlsx", sheet_name='Sheet1')
# dfl =  pd.read_excel("bi/locapi/dfout-addr.xlsx",sheet_name = 'Sheet1')
# dfout = pd.merge(dfl,dfr,on='orgid',how='left')
# dfout.to_excel('bi/locapi/dfout-addrloc.xlsx')
df = pd.read_excel("dfout-addrloc.xlsx", sheet_name = 'Sheet1')


def string_similar(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()

def dis_map(series):
    dis_n = ""
    orgid = series['orgid']
    ct = series['ct']
    dis_0 = series['dis_0']
    addr_0 = series['addr']
    dis_x = series['district_x'] # addr
    dis_y = series['district_y'] # gaode
    addr_y = series['addr_y']  # gaode
    dis_z = series['district_z'] # baidu
    addr_z = series['addr_z']  # baidu
    # print(type(dis_0),dis_0)
    area_list = ['滨江区','淳安县','富阳区','拱墅区','建德市','江干区','临安区','钱塘新区','上城区','桐庐县','西湖区','下城区','萧山区','余杭区']
    # print(addr_0, str(dis_z), dis_y)
    # if str(dis_z) == "nan":
    #     dis_z = dis_y
    # if dis_z in area_list:
    #     if dis_z == dis_y:
    #        dis_n = dis_z
    #     else:
    #         rat_z = string_similar(addr_z,addr_0)
    #         rat_y = string_similar(addr_y,addr_0)
    #         if rat_z > rat_y:
    #             dis_n = dis_z
    #         else:
    #             dis_n = dis_y
    # else:
    #     dis_n = dis_x

    ### 用出现次数最多
    a = [dis_z,dis_y,dis_x]
    dis_n = max(a, key=a.count)
    if str(dis_n) == "" or str(dis_n) == "nan":
        dis_n = dis_0
    return dis_n

df[['ct','dis_0']]=df[['ct','dis_0']].fillna('n')
df = df[(df['ct']== '杭州市') & (df['samecol'] == 'F')]
df["dis_n"] = df.apply(dis_map,axis=1)
df.to_excel('dfout-addrloc-t.xlsx')
