import functools

# 生成等差数列
def wholelist(begin,end):
    wl = []
    for i in range(begin,end):
        wl.append(i)
    return(wl)

# mex函数,最小的不属于这个集合的非负整数
def mex(sn):
    num = 0
    while True:
        if num not in sn:
            # print(num)
            break
        num += 1
    print(str(sn)+' '+ str(num))
    return(num)

def wipool(i):
    list2 = list1[0:i]
    xori = mex(list2)
    xorlist.append(xori)

from multiprocessing.pool import ThreadPool
# sn序列循环
xorlist = []
def snloop(sn):
    lensn = len(sn)
    # 循环获得sn前i个值的mex值
    # for i in range(lensn+1):
    #     snlist = sn[0:i]
    #     xorlist.append(mex(snlist))
    wi = wholelist(1,lensn+1)
    with ThreadPool(processes=2) as pool:
        pool.map(wipool, wi)
    xor =  functools.reduce(lambda x,y: x ^ y, xorlist) #异或和
    return(xor)

def F(data):
    return data

m=[]
np = int(input())
for _ in range(np):
    res = []
    n = int(input())
    n=1
    for _ in range(n):
        s = input()
        if s != '':
            strtemp = [int(j) for j in s.split()]
            res.append(strtemp)
        else:
            break
    list1 = res[0]
    xor = snloop(list1)  # 异或和结果值
    m.append(xor)
for i in m:
    print(F(i))