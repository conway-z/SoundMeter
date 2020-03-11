#coding:utf-8
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
import pymysql
import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
# sys.path.append(curPath)

print("rootPath:"+rootPath)

from etl.conf.mysqlbi  import read_mysql_bi

# 参数获取
tb_name = sys.argv[1] # 获取参数：表名，如"ads_snd_cover_detail_mid" #sys.argv[1]
dt = sys.argv[2] # 获取台数：日期，如"20200218"
dt_num = sys.argv[3]  # 获取sql中日期参数的个数，如2

def main():
    # sql读取
    # sql文件夹路径
    sql_path = 'sql/' #+ '\\'
    # sql文件名， .sql后缀的
    sql_file = tb_name + '.sql' #
    # 读取 sql 文件文本内容
    sql = open(sql_path + sql_file, 'r', encoding='utf8')
    sqltxt = sql.readlines() # 此时 sqltxt 为 list 类型

    # 读取之后关闭文件
    sql.close()
    # list 转 str
    sql = "".join(sqltxt)

    # 删除语句
    sqlDel = "DELETE from  "+tb_name +" where date_format(data_date, '%%Y%%m%%d') = %s"

    # 数据库连接
    config = read_mysql_bi('local') # 读取数据库连接配置
    db = pymysql.connect(**config)
    cur = db.cursor() #设定游票
    ## 删除分区数据

    cur.execute(sqlDel,dt)
    ## 插入增量分区数据
    val_list = [dt] * int(dt_num)
    cur.execute(sql,val_list) #执行sql
    # print(sql)
    # print(cur.fetchall())
    print("处理完成：" + tb_name)
    # df = pd.(sql, con)
    db.commit() #提交sql
    cur.close() #游标关闭
    db.close()  #数据库连接关闭


if __name__ == "__main__":
    main()