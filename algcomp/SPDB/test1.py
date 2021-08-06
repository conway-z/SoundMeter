a = '3' * 3
x =2333
lin = list(str(x))

def incd(x,d):
    out = list((map(lambda x: (x,int(x) ** int(d)), lin)))
    print(str(out))

incd(lin,2)