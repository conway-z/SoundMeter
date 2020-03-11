# dimdate 
## 日期维度生成-dimdate
1. dimDate.py生成基础表DIM_TIME，农历日期调用lunar.py
2. workDay.py生成假日识别码，生成文件WORK_DAY.py

# bi
## 报表2.1自动识别银行简称
### 程序名
- `parOrgMap.py`
### 文件处理
- 导入`2.1 机构覆盖信息`报表，添加一列`ybj_bank_join`。EXCEL方法：`=IF(LEN(E2)<5,F13,E2)`
也可以在数据库中添加好，优先用银保监持证机构名称，如果该值空则取供需系统银行名称
- 另存为`2_1机构覆盖信息.csv`（原文件名不改动默认是这个另存名称）
- 将py文件夹保存在本机，文件夹要包含但不限于：`bank_list_head.csv`,
### 程序执行
- `parOrgMap.py`中，配置文件根路径rootPath
- 执行`parOrgMap.py`
### 文件输出及编辑
- 输出文件：`bank_join.csv`
- 找到`bank_name_short`列为空的，去掉非银行的机构
- 确认其它`bank_name_short`所匹配出的简称是否正确
## 自动拆分“订单及机构信息报表”省局各市局明细
### 程序名
- `SplitExcelCitis.py`
### 配置目录
- 打开`SplitExcelCitis.py`，修改`pathRoot`参数为自己`报表根目录`。例:`pathRoot = c:/bi/reports`
- 省局文件如`订单及机构信息报表_分局.xlsx`应存储在`报表根目录+短日期`目录中。
- 例：`报表根目录`路径为`c:/bi/reports/`;`短日期`路径为`2017`,完整文件目录为`c:/bi/reports/2017/订单及机构信息报表_分局.xlsx`
### 执行方式
- 带参数脚本执行
- 命令行：`{程序地址:{pyPyth\}} {长日期}`
- 例(windows cmd)：`python c:\python\bi\SplitExcelCitis.py 20200217`
- 注意，日期格式应为`{yyyyMMdd}`
### 文件生成方式
- 程序执行后，会自动在省局同目录下，即`{报表根目录}/{短日期}`中生成各地市分局明细表格

