import re
def load_tokens(paths):
    """Return list of token streams per file: ints 10-99 are letters; 'B' marks a break (code sign, plaintext, unknown)."""
    out=[]
    for p in paths:
        toks=[]
        for l in open(p,encoding="utf-8"):
            if l.startswith("#"): continue
            for t in re.split(r"[\s.|,;:]+",l.strip()):
                if not t: continue
                u=t.rstrip("?")
                if re.fullmatch(r"\d{2}",u) and 10<=int(u)<=99: toks.append(int(u))
                elif re.fullmatch(r"[A-Z#]{1,2}|TRI|SQ|j",u): toks.append("K"+u)
                elif re.fullmatch(r"\d+",u): toks.append("C"+u)
                else: toks.append("B")
        out.append(toks)
    return out
def segments(streams,minlen=1):
    segs=[]
    for toks in streams:
        cur=[]
        for t in toks:
            if isinstance(t,int): cur.append(t)
            else:
                if len(cur)>=minlen: segs.append(cur)
                cur=[]
        if len(cur)>=minlen: segs.append(cur)
    return segs
