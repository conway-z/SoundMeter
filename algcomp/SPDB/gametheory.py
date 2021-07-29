import sys
import numpy as np
import functools
n1 = int(sys.stdin.readline().strip()) # 数据组数
n2 = int(sys.stdin.readline().strip()) # 数列长度
line = sys.stdin.readline().strip() # 数列(长度=n2)

# mex函数,最小的不属于这个集合的非负整数
def mex(sn):
    if len(sn) == 1:
        out = 0
    else:
        minsn = int(min(sn))
        maxsn = int(max(sn))
        snwhole = np.arange(minsn, maxsn,1)
        diff = set(snwhole).difference(sn) # 数组差值
        if len(diff) == 0:
            out = maxsn + 1
        else:
            out =  min(diff)
    return(out)
n2 =7
# sn序列循环
def snloop(n2,sn):
    snlist = []
    xorlist = []
    for si in sn:
        si = int(si)
        snlist.append(si)
        print("sn:"+str(snlist) + " mex:" + str(mex(snlist)))
        xorlist.append(mex(snlist))
    xor =  functools.reduce(lambda x,y: x ^ y, xorlist)
    print("xorlist:" + str(xorlist) + "xor:" + str(xor))


sn = line.split()
snloop(n2,sn)
