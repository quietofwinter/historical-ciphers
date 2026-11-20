# usage: python3 -I build_ngram.py N out.bin file1 file2 ...   (letters a-z; j->i, v->u folded)
import sys, numpy as np, re
n=int(sys.argv[1]); out=sys.argv[2]
buf=[]
for p in sys.argv[3:]:
    t=open(p,encoding='latin-1').read().lower()
    t=t.replace('j','i').replace('v','u')
    buf.append(re.sub('[^a-z]','',t))
s=''.join(buf)
a=np.frombuffer(s.encode(),dtype=np.uint8).astype(np.int64)-97
idx=np.zeros(len(a)-n+1,dtype=np.int64)
for k in range(n): idx=idx*26+a[k:len(a)-n+1+k]
c=np.bincount(idx,minlength=26**n).astype(np.float64)
tot=c.sum()
lp=np.log10((c+0.02)/tot)
lp.astype(np.float32).tofile(out)
u=np.bincount(a,minlength=26)/len(a)
np.savetxt(out+'.uni',u)
print("letters",len(a),"ngrams",n,"nonzero",int((c>0).sum()),"floor",lp.min())
