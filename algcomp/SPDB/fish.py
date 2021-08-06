def  nice(B):
    m = []
    tmdic = {}
    tndic = {}
    for A in B:
        if len(A) == 3:
            if tmdic.get(A[1]) and A[0] == '0':
                tmdic[A[1]] = tmdic[A[1]] + 1
                # print(dictm)
            elif tmdic.get(A[1]) and A[0] == '1':
                tmdic[A[1]] = tmdic[A[1]] - 1
                # print(dictm)
            else:
                tmdic[A[1]] = 1
                # print(dictm)
            if tndic.get(A[2]) and A[0] == '0':
                tndic[A[2]] = tndic[A[2]] + 1
            elif tndic.get(A[2]) and A[0] == '1':
                tndic[A[2]] = tndic[A[2]] - 1
                # print(dictn)
            else:
                tndic[A[2]] = 1
                # print(dictn)
        elif len(A) == 2:
            if A[0] == '2':
                if tmdic.get(A[1]) == None:
                    m.append(0)
                else:
                    m.append(tmdic.get(A[1]))
            elif A[0] == '3':
                m.append(tndic.get(A[1]))
    return m
def F(data):
    return data

m=[]
np = int(input())
for _ in range(np):
    res = []
    n = int(input())
    for _ in range(n):
        s = input()
        if s != '':
            strtemp = [j for j in s.split()]
            res.append(strtemp)
        else:
            break
    n=nice(res)
    for i in n:
        m.append(i)
for i in m:
    print(F(i))
