"""Mark up the Gerbier letter: replace each cipher passage in Birch's text with its reading.
Writes ../letter-annotated.txt, ../ciphertext.txt, ../key.md.  usage: python3 build_entry.py"""
import os, re, collections
HERE = os.path.dirname(os.path.abspath(__file__)); UP = os.path.join(HERE, "..")
KEY = {1:'g',2:'g',3:'h',4:'h',5:'i',6:'i',7:'i',8:'i',10:'a',11:'a',12:'a',13:'a',14:'b',15:'b',16:'c',17:'c',18:'d',19:'d',
       20:'e',21:'e',22:'e',23:'e',24:'f',25:'f',26:'k',27:'l',28:'l',29:'m',30:'m',31:'n',32:'n',33:'o',34:'o',35:'o',36:'o',
       37:'p',38:'p',41:'r',42:'r',43:'s',44:'s',45:'t',46:'t',47:'u',48:'u',49:'u',50:'u',51:'w',52:'w',55:'y',56:'y',73:'e',77:'e'}
# reading for each cipher passage, in order; "t" = tentative or one figure differs from the key
READ = [("d","notes"),("t","receave"),("d","order"),("t","parliament"),("t","proffe[r] secret"),("t","prejudicial"),("d","treaty"),
 ("d","brybed"),("t","charitable"),("t","shedding"),("d","bloud"),("d","my lady mother"),("d","sisters"),("d","Bromley"),("d","Sackvile"),
 ("d","the seas"),("t","the Hague"),("d","heere"),("d","suspect"),("d","get over"),("d","credit"),("d","states affaires"),
 ("d","bookes written"),("t","commission"),("d","nature"),("d","allouwance"),("d","come over"),("d","get off"),("d","engaged"),
 ("d","venters"),("d","over"),("t","ripe"),("d","leave"),("d","lurch"),("d","wherewith"),("d","breathe"),("d","agitate"),
 ("d","accounte"),("d","dangerous"),("d","originall coppyes"),("d","bonds"),("d","faith"),("d","credit"),("d","safe conducte")]
NOT_CIPHER = {"229. 115.", "124", "109", "19."}   # code names for persons, and a date
def main():
    raw = open(os.path.join(UP, "raw_birch.txt"), encoding="utf-8").read()
    lines = raw.split("\n")
    body = "\n".join(lines[3:])
    runs, out, pos, k = [], [], 0, 0
    for m in re.finditer(r"(?:\b\d{1,3}\.\s*)+", body):
        g = m.group(0).strip()
        nums = [int(x) for x in re.findall(r"\d+", g)]
        if g in NOT_CIPHER or g.rstrip(".") in ("124", "109") or len(nums) < 2:
            continue
        kind, word = READ[k]; k += 1
        out.append(body[pos:m.start()]); runs.append(nums)
        sp = " " if body[m.end()-1] == " " else ""
        out.append("{%s|%s|%s}%s" % (kind, word, " ".join(map(str, nums)), sp)); pos = m.end()
    out.append(body[pos:])
    assert k == len(READ), (k, len(READ))
    text = "".join(out)
    pars = [p.strip() for p in re.split(r"\n", text) if p.strip()]
    hdr = ["# George Gerbier to his father Sir Balthazar Gerbier, London, 15/25 July 1653. Text from Birch, Thurloe State Papers vol. 1",
           "# (1742), pp. 352-354 (MS vol. iv, p. 212), with each cipher passage replaced by its reading.",
           "# Markup: {d|reading|cipher} deciphered; {t|reading|cipher} tentative, or one figure differs from the key.",
           "# 229, 115, 124 and 109 are code numbers for persons, left as printed; +, * and # are Birch's signs for further name symbols.", "",
           "=== George Gerbier to his father, London, 15/25 July 1653. (Birch, Thurloe State Papers vol. 1, pp. 352-354)"]
    open(os.path.join(UP, "letter-annotated.txt"), "w", encoding="utf-8").write("\n".join(hdr + pars) + "\n")
    allg = [n for r in runs for n in r]
    open(os.path.join(UP, "ciphertext.txt"), "w").write("# The 44 cipher passages, one per line, as printed by Birch.\n" + "\n".join(" ".join(map(str, r)) for r in runs) + "\n")
    # check: every figure's key value appears in the reading, flag mismatches
    bad = []
    for (kind, word), r in zip(READ, runs):
        dec = "".join(KEY.get(n, "?") for n in r); w = re.sub(r"[^a-z]", "", word.lower().replace("v", "u").replace("j","i"))
        if dec != w: bad.append((word, dec))
    c = collections.Counter(allg)
    rows = ["# Key", "", "One or more figures for each letter, in alphabetical order. 'Times' = occurrences in the letter.", "",
            "| Letter | Figures | Times |", "|---|---|---|"]
    by = collections.defaultdict(list)
    for n, v in sorted(KEY.items()): by[v].append(n)
    for v in sorted(by, key=lambda v: min(by[v]) if v not in "ghi" or min(by[v]) >= 10 else 0):
        rows.append("| %s | %s | %d |" % (v, ", ".join(map(str, by[v])), sum(c[n] for n in by[v])))
    rows += ["", "Figures 1-8 are extra homophones for g, h and i, placed before the main alphabet; 73 and 77 occur once each, for e.",
             "Figures 9, 39, 40, 53, 54 and 57-72 do not occur in this letter."]
    open(os.path.join(UP, "key.md"), "w", encoding="utf-8").write("\n".join(rows) + "\n")
    print(len(runs), "passages,", len(allg), "figures,", len(c), "distinct; differs from plain key in:", bad)
main()
