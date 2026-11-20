import numpy as np, random, math, sys
lg=np.fromfile('model/nl5.bin',dtype=np.float32)
L=[[int(x) for x in l.split()] for l in open('deBruyne/ct.txt')]
syms=sorted({x for l in L for x in l})
def score(key):
    s=0.0
    for l in L:
        p=[key[x] for x in l]
        for i in range(len(p)-4):
            s+=lg[(((p[i]*26+p[i+1])*26+p[i+2])*26+p[i+3])*26+p[i+4]]
    return s
letters=list(range(26))
random.seed(int(sys.argv[1]))
best=None
for r in range(int(sys.argv[2])):
    perm=random.sample(letters,26); key={s:perm[i] for i,s in enumerate(syms)}
    spare=perm[len(syms):]
    cur=score(key); T=3.0
    N=40000
    for it in range(N):
        T=3.0*(1-it/N)+0.05
        k2=dict(key); sp=list(spare)
        a=random.choice(syms)
        if random.random()<0.5:
            b=random.choice(syms); k2[a],k2[b]=k2[b],k2[a]
        else:
            j=random.randrange(len(sp)); k2[a],sp[j]=sp[j],k2[a]
        sc=score(k2)
        if sc>=cur or random.random()<math.exp((sc-cur)/T): key,spare,cur=k2,sp,sc
    txt=' / '.join(''.join(chr(97+key[x]) for x in l) for l in L)
    print("%.1f"%cur, txt); sys.stdout.flush()
    if best is None or cur>best[0]: best=(cur,dict(key),txt)
print("BEST %.1f"%best[0]); print({s:chr(97+v) for s,v in sorted(best[1].items())}); print(best[2])
