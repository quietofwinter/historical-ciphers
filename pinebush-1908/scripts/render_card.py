"""Redraw the 1908 Pine Bush postcard cipher line by line, with each symbol drawn as it looks on the card
and its letter beneath (blue = read, orange = covered by the postmark and reconstructed). Also prints the letter counts
used in key.md.

usage: python3 render_card.py ../images/card-deciphered.png
"""
import sys
from collections import Counter
from PIL import Image, ImageDraw, ImageFont

OUT = sys.argv[1] if len(sys.argv) > 1 else "card-deciphered.png"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
f_let, f_head, f_leg = ImageFont.truetype(BOLD, 22), ImageFont.truetype(BOLD, 28), ImageFont.truetype(FONT, 19)

# Lines of the card. Lower case = covered by the postmark (reconstructed); "#" = P.M. written in clear.
LINES = ["MUST disappo-", "INT YOU", "AGAIN FOR", "I AM LEAVING", "ON # TRAIN",
         "FOR GREYCOURT", "WILL WRITE", "FROM THERE"]

BLUE, ORANGE, INK, GREY = (0, 92, 197), (196, 102, 0), (40, 40, 40), (150, 150, 150)
S = 34  # symbol cell size

def glyph(d, ch, x, y, col):
    """Draw the symbol for letter ch in a cell with top-left (x, y)."""
    w = 3
    L, R, T, B, cx, cy = x + 4, x + S - 4, y + 4, y + S - 4, x + S // 2, y + S // 2
    line = lambda *p: d.line(p, fill=col, width=w)
    if ch == "A":
        line(L, cy, R, cy)
    elif ch == "I":
        line(L, cy, R, cy); line(R - 4, cy - 10, R - 4, cy + 10)
    elif ch == "U":
        line(L, cy, R, cy); line(L + 3, cy - 10, L + 3, cy + 10); line(R - 3, cy - 10, R - 3, cy + 10)
    elif ch == "Y":
        line(L, cy, R, cy)
        for xx in (L + 7, cx, R - 7):
            line(xx, cy - 10, xx, cy + 10)
    elif ch == "C":
        line(L, cy, R, cy)
        d.ellipse([cx - 2, cy - 11, cx + 2, cy - 7], fill=col); d.ellipse([cx - 2, cy + 7, cx + 2, cy + 11], fill=col)
    elif ch == "E":
        d.arc([L + 4, cy - 12, R - 4, cy + 6], 180, 360, fill=col, width=w); line(L, cy + 8, R, cy + 8)
    elif ch == "N":
        d.arc([L + 2, T + 4, R - 2, B + 14], 180, 360, fill=col, width=w)
    elif ch == "O":
        d.arc([L + 2, T - 14, R - 2, B - 4], 0, 180, fill=col, width=w)
    elif ch == "F":
        d.arc([L + 4, T - 12, R - 4, cy + 2], 0, 180, fill=col, width=w)
        line(L + 2, cy + 6, R - 2, cy + 6); line(L + 2, cy + 11, R - 2, cy + 11)
    elif ch == "G":
        line(L + 4, T, L + 4, B); line(L + 4, B, R, B)
    elif ch == "S":
        line(L, cy - 6, R - 4, cy - 6); line(R - 4, cy - 6, R - 4, cy + 10)
    elif ch == "H":
        line(L, cy - 4, R, cy - 4); line(L, cy + 4, R, cy + 4); line(cx + 6, T + 2, cx - 6, B - 2)
    elif ch == "R":
        d.rectangle([L + 3, T + 5, R - 3, B - 5], outline=col, width=w)
    elif ch == "T":
        d.rectangle([L + 3, T + 5, R - 3, B - 5], outline=col, width=w)
        line(L + 3, T + 5, R - 3, B - 5); line(L + 3, B - 5, R - 3, T + 5)
    elif ch == "L":
        line(L, cy, R, cy); d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], outline=col, width=w)
    elif ch == "M":
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], outline=col, width=w); line(cx, T, cx, B); line(L + 2, cy, R - 2, cy)
    elif ch == "V":
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], outline=col, width=w); line(L, cy, R, cy)
    elif ch == "W":
        line(L + 2, T + 2, R - 2, B - 2); line(L + 2, B - 2, R - 2, T + 2)
    else:  # covered or unread: a dotted box
        for k in range(L, R, 6):
            d.point([(k, T + 4), (k, B - 4)], fill=col)

def main():
    pad, gap, lh = 50, 18, 92
    width = 1380
    img = Image.new("RGB", (width, 150 + lh * len(LINES) + 90), "white")
    d = ImageDraw.Draw(img)
    d.text((pad, 30), "Postcard, Pine Bush, N.Y., 31 August 1908, to Miss Florence Mieler, Crawford, N.Y.", font=f_head, fill=INK)
    d.text((pad, 75), "Cipher redrawn from the card, letter beneath each symbol.", font=f_leg, fill=GREY)
    y = 130
    for ln in LINES:
        x = pad
        for word in ln.split():
            if word == "#":
                d.text((x, y + 4), "P.M.", font=f_head, fill=INK); x += 80 + gap; continue
            cont = word.endswith("-")
            for ch in word.rstrip("-"):
                covered = ch.islower()
                col = ORANGE if covered else BLUE
                glyph(d, ch.upper() if not covered else "?", x, y, GREY if covered else INK)
                tw = d.textlength(ch.upper(), font=f_let)
                d.text((x + (S - tw) / 2, y + S + 6), ch.upper(), font=f_let, fill=col)
                x += S + 4
            if not cont:
                d.text((x - 2, y + 8), ",", font=f_head, fill=GREY)
            x += gap + 10
        y += lh
    d.text((pad, y + 10), "Signed \"H\" in ordinary script.  Blue = read.  Orange = under the postmark, reconstructed.",
           font=f_leg, fill=INK)
    img.save(OUT)
    seen = Counter(c for ln in LINES for w in ln.split() if w != "#" for c in w.rstrip("-") if c.isupper())
    print(OUT, dict(sorted(seen.items())))

main()
