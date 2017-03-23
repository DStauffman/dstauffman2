def f(a,b):
    if a==b: return 0
    d=0
    for i in range(len(a)):
        if a[i]==b[i]:
            continue
        else:
            d+=1
            if d>1: return 0
    return 1
def g(k,a):
    return [i for (i,t) in enumerate(a) if f(k,t)]
def stringsRearrangement(a):
    def s(k,v,l=0):
        d=0
        for i in g(k,v):
            n = v.pop(i)
            d = s(n,v,i)
            if d: return d
        else:
            if v:
                v.insert(l, k)
                d=0
            else:
                d=1
        return d
    for (j,t) in enumerate(a):
        w = [x for (i,x) in enumerate(a) if i!=j]
        if s(t,w): return 1
    return 0
