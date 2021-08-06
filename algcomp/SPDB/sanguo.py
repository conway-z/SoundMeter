def group(items):
    rd1=[]
    rd2=[]
    for it in range(len(items)):
        if items[it]=='a':
            rd1.append(it)
        else:
            rd2.append(it)
    n = 0
    for i in range(len(rd2)):
        if len(rd2)!=0:
            for p in range(len(rd2)):
                if rd1[i]<rd2[p]:
                    n=n+1
                    rd2.remove(rd2[p])
                    break
    n=n*2
    print(n)
res = []
n = int(input())

for _ in range(n*2):
    si = input()
    if si!='':
        strtemp = [j for j in si.split()]
        res.append(strtemp[0])
    else:
        break
for v in res :
    if not str(v).isdigit():
        group(v)