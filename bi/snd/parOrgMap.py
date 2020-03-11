# -*-coding:utf-8-*-
import pandas as pd
"""
input file:
    含银行简称，检索银行关键字的银行清单： bank_list_head.csv
    2.1机构覆盖信息.csv
output file: bank_join.csv
output column: bank_name_short --机构简称，用于报表展示   
"""
# 文件配置
rootPath = "C:/Users/Administrator/Desktop/desk/shuqin/py/"
parFile = "bank_list_head.csv"
bankListFile = "2_1机构覆盖信息.csv"
saveFile ="bank_join.csv"
csvBank = pd.read_csv(rootPath  + bankListFile, encoding="gbk", header=0) #.head(10)
dfBank = pd.DataFrame(csvBank) #,columns=['prov,city','bank_code','bank_name','bank_name_abb']
csvPar = pd.read_csv(rootPath  + parFile, encoding="gbk", header=0, index_col=0)
dfPar = pd.DataFrame(csvPar)
# 创建输出DF
df_map = pd.DataFrame(columns=['bank_name_join', 'bank_name_short'])
# 用检索词匹配银行名称，并输出银行总行简称
for item in dfBank.iterrows():
        for r in dfPar.iterrows():
            bankHeadqtName = item[1]['zorganization_name'] #总行名称
            bankName = item[1]['bank_name_join'] #银行名称
            searchKey = r[1]['search_key'] # 检索词
            bankNameShort = r[1]['bank_name_short'] + ''
            findName = "" # 用于检索的银行名, 优先用总行

            if bankHeadqtName is None:
                findName = bankNameShort
            else:
                findName = bankName
            #检索银行简称并输出DataFrame
            if findName.find(searchKey) >=0:
                dataAdd = [[bankName, bankNameShort]]
                df_add = pd.DataFrame(data=dataAdd,columns=['bank_name_join', 'bank_name_short'])
                df_map = df_map.append(df_add, ignore_index=True)
                break
            print(searchKey, findName)
# 连接DataFrame, 合并简称
dfOut = dfBank.join(df_map.set_index('bank_name_join'), on='bank_name_join')
dfOut.to_csv(rootPath + saveFile, encoding='utf_8_sig')
