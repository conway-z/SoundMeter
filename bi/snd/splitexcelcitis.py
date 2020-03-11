import xlwt
import xlrd
import os
import sys
from xlutils.copy import copy;
"""
    读表
"""
dt =  sys.argv[1] #'20200226'
# dt = '20200217'
print('执行日期：' + dt)
startRowN = 3 #写文件时起始行
city_col_no = 2 # 城市列序号
dtPath = dt[4:]
pathRootHead = "C:/Users/newor/Desktop/bi/报表/"
pathRoot = pathRootHead + dtPath + "/tmp/" #根目录
print('文件目录：' +pathRoot)
#写文件定义：写入文件名主题，要抽取并拆分的城市，sheet名（目录清单）
fileWriteHead = pathRoot + '订单及机构信息报表_明细_'
sheetNameRDList = ['一、机构覆盖情况表-明细','二、供需模块订单情况表-明细','一、机构覆盖情况表-省联社-明细'] # 要读取的sheet页列表
sheetNameAddList = ['一','二','三'] #每张表写入sheet标题名数字前缀列表
cityList = ['杭州市','温州市'] # ['杭州市','温州市','嘉兴市','湖州市','绍兴市','金华市','衢州市','舟山市','台州市','丽水市']  #要抽取并拆分的城市
# ,'嘉兴市','湖州市','绍兴市','金华市','衢州市','舟山市','台州市','丽水市'
fileName =  pathRoot + "订单及机构信息报表_明细_地市_"+ dtPath + ".xlsx"

"""
    定义表格格式
"""
# 0、通用格式
# 居中
al = xlwt.Alignment()
al.horz = 2  # 设置水平居中
al.vert = 1  # 设置垂直居中
# 四周框线
borders = xlwt.Borders()
borders.left = 1
borders.right = 1
borders.top = 1
borders.bottom = 1
borders.bottom_colour=0x3A

# 1、表头格式
style0 = xlwt.XFStyle()  # 初始化样式
font = xlwt.Font()  # 为样式创建字体
font.name = '黑体'
font.bold = True  # 加黑
font.color_index = 4
font.height = 240
style0.font = font
style0.alignment = al #居中

# 2、 标题行格式
style1 = xlwt.XFStyle()  # 初始化样式
font = xlwt.Font()  # 为样式创建字体
font.name = '黑体'
# font.bold = True  # 加黑
font.color_index = 4
font.height = 180
style1.font = font
style1.alignment = al # 居中
style1.alignment.wrap = 1  # 自动换行
style11 = style1 # 不加框线
style1.borders = borders # 框线

# 3、 正文格式
style2 = xlwt.XFStyle()  # 初始化样式
font = xlwt.Font()  # 为样式创建字体
font.name = '宋体'
# font.bold = True  # 加黑
font.color_index = 4
font.height = 180
style2.font = font
style2.borders = borders # 框线

# 4、脚注格式
style3 = xlwt.XFStyle()  # 初始化样式
font = xlwt.Font()  # 为样式创建字体
font.name = '宋体'
font.bold = True  # 加黑
font.color_index = 4
font.height = 160
style3.font = font

# 读文件中各sheet页，抽取城市并按城市拆分
def read_excel(fileWrite, city, sheetNameRD, sheetNameWT, list_per_no):
    per = list_per_no[0] # 百分数位置
    mol = list_per_no[1] # 分子位置
    den = list_per_no[2] # 分母位置
    wb = xlrd.open_workbook(filename=fileName)#打开文件
    sheetRS = wb.sheet_by_name(sheetNameRD)#通过名字获取表格


    # 写表头
    if os.path.exists(fileWrite):

        # 打开需要操作的excel表
        f1 = xlrd.open_workbook(fileWrite, formatting_info=True)
        # 复制原有表
        f = copy(f1)
        # 新增sheet,参数是该sheet的名字，可自定义
        sheetw = f.add_sheet(sheetNameWT, cell_overwrite_ok=True)
    else:
        f = xlwt.Workbook()
        sheetw = f.add_sheet(sheetNameWT, cell_overwrite_ok=True) #创建sheet  , cell_overwrite_ok=True
    # 写第1行，表名
    row_0 = sheetRS.row_values(0)
    sheetw.write_merge(0, 0, 0, len(row_0) -1, row_0,style0)  # 合并行单元格
    # 写第2行，字段名
    row_1 = sheetRS.row_values(1)
    for i in range(0, len(row_1)):
        sheetw.write(1, i, row_1[i], style1)
    # 拆份地市
    ## 检索地市判断首次出现地市的行的行号
    nrows = sheetRS.nrows  # 行数
    fst_rowno = None
    for i in range(0, nrows):
        row_i = sheetRS.row_values(i)
        if row_i[city_col_no] == city:
            fst_rowno = i
            break
    ## 提取脚注, 最多识别最后5行
    footnoteList = []
    for i in range(nrows -5, nrows):
        row_i = sheetRS.row_values(i)
        if len(row_i[0]) > 10  and len(row_i[1]) < 2:
            footnoteList.append(row_i[0])
    # print(footnoteList)
    ## 检索地市提取行并写入地市对应excel
    row_sum = [0] * (len(row_1) -city_col_no + 1 ) # 合计项，累加
    row_end = 0
    for i in range(0, nrows):
      row_i = sheetRS.row_values(i)
      if row_i[city_col_no] == city:
        for j in range(0, len(row_1)):
            if j == per:
                per_val = '%.1f%%' % (row_i[j] * 100)
                sheetw.write(i - fst_rowno + startRowN, j, per_val, style2)
            else:
                sheetw.write(i - fst_rowno + startRowN, j, row_i[j], style2)

            # 迭代累加合计值行
            if j > city_col_no:
                sumij = row_sum[j-city_col_no]  + int(row_i[j])  #累加合计项
                row_sum[j-city_col_no] = sumij  # 更新合计值队列
                sheetw.write(city_col_no, j, sumij, style2) #第3行第三列开始填入
                row_end = i
    # 合计行百分比列计算并写入

    per_val = row_sum[mol-city_col_no] / row_sum[den- city_col_no]
    sheetw.write(startRowN-1,per,'%.2f%%' % (per_val * 100),style2)

    # 添加脚注
    if footnoteList:
        for i in range(0, len(footnoteList)):
            footnote = footnoteList[i]
            sheetw.write(row_end + 1 + i - fst_rowno + startRowN, 0, footnote, style3) # 尾行+1继续循环添加脚注
            print("添加脚注：" + sheetNameWT +footnote)

    #添加合计列前两格
    sheetw.write(2, 0, '合计', style1) #第1格s
    sheetw.write(2, 1, '--', style1)  # 第2格
    sheetw.col(0).width = 256*20 #首列列宽

    f.save(fileWrite) # 保存表
    print('创建'+city+'sheet页: '+sheetNameWT)

# 写目录sheet页
def write_cata(fileWrite, dt, sheetNameWTList):
    sheetNameWT = '目录'
    dt = str(dt)
    dtCN = '数据截止日期: ' + dt[0:4] + '年' + dt[4:6] + '月' + dt[6:] + '日'
    # 打开需要操作的excel表
    # 复制原有表
    f = xlwt.Workbook()
    # 新增sheet,参数是该sheet的名字，可自定义
    sheetw = f.add_sheet(sheetNameWT, cell_overwrite_ok=True)
    sheetw.write(0, 0, sheetNameWT, style0) #第1行
    sheetw.write(1, 0, dtCN) # 第2行
    for i in range(0, len(sheetNameWTList)):
        sheetw.write(2+i, 0, sheetNameWTList[i])  # 第2行
    sheetw.col(0).width = 256 * 40 #列宽调整
    f.save(fileWrite)

# 生成写入新表的sheet名列表
sheetNameWTList =  []
for i in range(0, len(sheetNameRDList)):
    sheetNameRD = sheetNameRDList[i]
    sheetNameWT = sheetNameAddList[i] + '、' + str.split(sheetNameRD, "、")[1]
    sheetNameWTList.append(sheetNameWT)

# 执行程序
for city in cityList:
    cityAbb = city.replace('市', '')
    fileWrite = fileWriteHead + cityAbb + dtPath+ '.xlsx' # 拼接写入文件名
    if os.path.exists(fileWrite):
        os.remove(fileWrite)
        print("删除旧文件：" + fileWrite)
    write_cata(fileWrite, dt, sheetNameWTList) #写入目录sheet
    print("新建文件：" + fileWrite)
    # 读文件中各sheet页，抽取城市并按城市拆分
    for i in range(0,len(sheetNameRDList)):
        sheetNameRD = sheetNameRDList[i]
        sheetNameWT = sheetNameWTList[i]

        list_per_no = [] # 定位百分比字段位置、分子分母位置
        sheet_no_cn = str.split(sheetNameWT,'、')[0]
        if sheet_no_cn == '一' or sheet_no_cn == '三':
            list_per_no = [6, 4, 3]
        elif   sheet_no_cn == '二':
            list_per_no = [7, 6, 3]
        read_excel(fileWrite, city, sheetNameRD, sheetNameWT, list_per_no)

# if __name__ == '__main__':
