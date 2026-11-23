import re,math,sys
from collections import Counter
sys.path.insert(0,".")
from key29 import K,NAMES
K[66]='i'
CAP={"N":"ch","D":"ch","W":"ss","P":"ss","Z":"st","O":"st","j":"sch","X":"sch","Y":"ei","G":"ei","S":"au","F":"au","H":"ll","L":"t","A":"t","R":"mm","M":"mm","E":"mm","C":"mm","B":"ff","T":"ff"}
txt=open("lm/emg.txt").read().lower()
txt=txt.replace("v","u").replace("j","i").replace("ä","a").replace("ö","o").replace("ü","u")
W=Counter(re.findall(r"[a-z]+",txt))
for w in "und ich der die das nicht noch nach auch mit von zu auf bei sein werden haben ist wie so oder aber dass sich man uns euer gnaden armee regiment compagnie volck reuter knechte obrist general feldmarschall soldaten pferde geld reichsthaler gulden tausend hundert quartier marsch tractat friede frieden convoy werbung recrute salvum conductum avisiert schreiben brief patente patenten herr herrn fürst graf konig konigs kayser churfurst landgraf commissarius commissar staadische holland wesel cassel koln hamburg lubeck regensburg wurzburg bischof statthalter gesandten guarnison guarnisonen dalwig eberstein ordre abfertigung".split(): W[w]+=50
tot=sum(W.values()); maxlen=16
def cost(w):
    c=W.get(w,0)
    return -math.log(c/tot) if c else 12+3.0*len(w)
def segment(s):
    n=len(s); best=[0.0]+[1e18]*n; bp=[0]*(n+1)
    for i in range(1,n+1):
        for j in range(max(0,i-maxlen),i):
            v=best[j]+cost(s[j:i])
            if v<best[i]: best[i]=v; bp[i]=j
    out=[]; i=n
    while i>0: out.append(s[bp[i]:i]); i=bp[i]
    return " ".join(reversed(out))
def render(f):
    lines=[]
    for l in open(f"../transcription/{f}.txt",encoding="utf-8"):
        if l.startswith("#"): continue
        pieces=[]
        for i,part in enumerate(l.strip().split("|")):
            if i%2: pieces.append(("P",part.strip())); continue
            buf=""
            for t in part.split("."):
                u=t.strip().rstrip("?")
                if not u: continue
                if u.isdigit() and int(u) in K: buf+=K[int(u)]
                elif u in CAP: buf+=CAP[u]
                else:
                    if buf: pieces.append(("C",buf)); buf=""
                    pieces.append(("N",NAMES.get(int(u),"["+u+"]") if u.isdigit() else "{"+u+"}"))
            if buf: pieces.append(("C",buf))
        lines.append(pieces)
    # join cipher across line breaks
    flat=[p for ln in lines for p in ln]
    merged=[]
    for p in flat:
        if merged and p[0]=="C" and merged[-1][0]=="C": merged[-1]=("C",merged[-1][1]+p[1])
        else: merged.append(p)
    out=[]
    for kind,s in merged:
        if kind=="C": out.append(segment(s))
        elif kind=="P": out.append("«"+s+"»")
        else: out.append(s)
    return " ".join(out)
if __name__=="__main__":
    print(render(sys.argv[1])[:2500])
