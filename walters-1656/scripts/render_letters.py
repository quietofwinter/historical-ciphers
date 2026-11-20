"""Draw the two Walters letters with the deciphered text in colour and the cipher numbers beneath.

usage: python3 render_letters.py ../letters-annotated.txt ../images
"""
import re, sys, os
from PIL import Image, ImageDraw, ImageFont

SRC, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
f_txt, f_b, f_num = ImageFont.truetype(FONT, 26), ImageFont.truetype(BOLD, 26), ImageFont.truetype(MONO, 15)
f_head, f_leg = ImageFont.truetype(BOLD, 30), ImageFont.truetype(FONT, 20)
COL = {"p": (30, 30, 30), "d": (0, 92, 197), "t": (196, 102, 0), "u": (150, 150, 150)}
W, MARGIN = 1500, 60
LINE_H, NUM_H = 40, 20

def tokens(par):
    out = []
    for part in re.split(r"(\{[dtu]\|[^}]*\})", par):
        m = re.fullmatch(r"\{([dtu])\|([^}]*)\}", part)
        if m:
            kind, rest = m.group(1), m.group(2).split("|")
            if kind == "u":
                out.append(("u", "[" + rest[0] + "]", rest[0]))
            else:
                out.append((kind, rest[0], rest[1]))
        else:
            out += [("p", w, None) for w in part.split()]
    return out

def attach(toks):
    # glue punctuation that follows an annotated chunk onto it
    res = []
    for t in toks:
        if t[0] == "p" and res and res[-1][0] != "p" and re.fullmatch(r"[.,;:!?]+\S*", t[1]):
            k, txt, num, tail = res[-1]
            res[-1] = (k, txt, num, tail + t[1])
        else:
            res.append(t + (("",) if len(t) == 3 else ()))
    return res

def layout(paragraphs, draw):
    lines = []
    for par in paragraphs:
        cur, x = [], 0
        for kind, txt, num, tail in attach(tokens(par)):
            font = f_txt if kind == "p" else f_b
            w = draw.textlength(txt, font=font) + draw.textlength(tail, font=f_txt)
            if num and kind != "u":
                w = max(w, draw.textlength(num, font=f_num))
            gap = draw.textlength(" ", font=f_txt)
            if cur and x + gap + w > W - 2 * MARGIN:
                lines.append(cur); cur, x = [], 0
            if cur:
                x += gap
            cur.append((x, kind, txt, num, tail)); x += w
        lines.append(cur); lines.append(None)  # paragraph break
    return lines

def render(title, paragraphs, path):
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    lines = layout(paragraphs, probe)
    h = MARGIN + 92 + 50
    for ln in lines:
        h += 14 if ln is None else LINE_H + (NUM_H if any(k in "dt" for _, k, *_ in ln) else 0)
    img = Image.new("RGB", (W, h + MARGIN), (255, 255, 255))
    d = ImageDraw.Draw(img)
    main, _, ref = title.partition(" (")
    d.text((MARGIN, MARGIN), main, font=f_head, fill=COL["p"])
    if ref:
        d.text((MARGIN, MARGIN + 42), "(" + ref, font=f_leg, fill=COL["u"])
    y, lx = MARGIN + 82, MARGIN
    for k, lab in (("d", "deciphered"), ("t", "tentative reading"), ("u", "[still unread]")):
        d.rectangle((lx, y + 5, lx + 18, y + 23), fill=COL[k]); lx += 26
        d.text((lx, y), lab, font=f_leg, fill=COL["p"]); lx += d.textlength(lab, font=f_leg) + 34
    d.text((lx, y), "small numbers = the cipher as printed", font=f_leg, fill=COL["u"])
    y += 60
    for ln in lines:
        if ln is None:
            y += 14; continue
        ann = any(k in "dt" for _, k, *_ in ln)
        for x, kind, txt, num, tail in ln:
            font = f_txt if kind == "p" else f_b
            d.text((MARGIN + x, y), txt, font=font, fill=COL[kind])
            if tail:
                d.text((MARGIN + x + d.textlength(txt, font=font), y), tail, font=f_txt, fill=COL["p"])
            if num and kind != "u":
                d.text((MARGIN + x, y + LINE_H - 6), num, font=f_num, fill=COL[kind])
        y += LINE_H + (NUM_H if ann else 0)
    img.save(path)

blocks = re.split(r"^=== ", open(SRC, encoding="utf-8").read(), flags=re.M)
for i, b in enumerate(blocks[1:], 1):
    title, *body = b.strip().split("\n")
    pars = [l for l in body if l.strip() and not l.startswith("#")]
    render(title, pars, os.path.join(OUT, f"letter{i}-deciphered.png"))
    print("wrote", os.path.join(OUT, f"letter{i}-deciphered.png"))
