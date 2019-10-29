import json
import requests
import time

# 设定起始结束年份参数
from_year = 2010 #设定起始年份
to_year = 2020 #设定结束年份（结束日期是上限值） from_year <= date < to_year

#定义输出年份+月份清单空队列
lm = []

# 循环生成年+月清单
for year in range(from_year,to_year):
    for mon in range(1,13): #月份
        mon_str = str(mon)
        if mon<10: # 月循环，1至9月前+'0'
            mon_str= '0' + mon_str
        ym = str(year) +mon_str
        lm.append(ym)
#调用节假日API
server_url = "http://www.easybots.cn/api/holiday.php?m=" # 节假日接口(工作日对应结果为 0, 休息日对应结果为 1, 节假日对应的结果为 2 )
req = requests.get(server_url + str(lm)) #调用网址及参数，结果集为Json
vop_data = json.loads(req.text) #Json转Dict

# 定义输出“日期，节假日类型”的Dict
ndict = dict()
# 按月循环将生成“日期，节假日类型”
for year in range(from_year,to_year):
    for mon in range(1,13): # 年循环
        mon_str = str(mon)
        if mon<10: # 1至9月前+'0'
            mon_str= '0' + mon_str

        ym = str(year) +mon_str
        v = vop_data[ym] #yyyyMM入参，取出某月Dict
        for k, val in v.items():
            new_k = ym + k #key值为yyyyMMdd
            ndict[new_k] = v[k] # 输出行为"yyyyMMdd:{1/2/3}"
print('resault is==')
print(ndict) #打印结果

#Dict转为DataFrame并转储至csv
import pandas as pd
df = pd.DataFrame.from_dict(ndict,orient='index', columns=['values'])
df2 = df.reset_index()
df2.to_csv('WORK_DAY.csv', index = False,index_label = False)