#!/usr/bin/env python3
"""Image + facts, on no background.

Both halves live in one SVG on purpose: two side-by-side <img> tags wrap onto
separate lines as soon as the README column is narrower than their combined
width, which it is on plenty of screens. One image cannot come apart.

The picture is the repo's own asset, deliberately not the GitHub avatar --
those two stay independent.
"""
import base64, os, re, sys, urllib.request
sys.path.insert(0, os.path.dirname(__file__))
from plain import *

HERE = os.path.dirname(__file__)
LOGIN = sys.argv[1] if len(sys.argv) > 1 else "slasfar"
OUT = sys.argv[2] if len(sys.argv) > 2 else "dist/identity.svg"
PIC = os.path.join(HERE, "..", "assets", "sadgejuice.png")

W, H = 800, 176
AV = 150
GAP = 30
TX = AV + GAP


def cursus():
    try:
        r = urllib.request.Request(f"https://badge.mediaplus.ma/levi/{LOGIN}",
                                   headers={"User-Agent": "profile-readme"})
        t = " ".join(re.findall(
            r">([^<>]{1,60})<",
            urllib.request.urlopen(r, timeout=45).read().decode("utf-8", "replace")))
        m = re.search(r"level\s+(\d+)\s*-\s*(\d+)\s*%", t, re.I)
        g = re.search(r"\b(Cadet|Member|Learner|Alumni|Transcender)\b", t, re.I)
        lvl = f"{int(m.group(1))}.{int(m.group(2)):02d}" if m else "—"
        return f"{(g.group(1).title() if g else 'Cadet')} &#183; level {lvl}"
    except Exception as e:
        print("cursus lookup failed:", e, file=sys.stderr)
        return "Cadet"


ROWS = [
    ("ROLE",   "Systems &amp; low-level engineering"),
    ("SCHOOL", "1337 Coding School &#183; 42 Network"),
    ("CURSUS", cursus()),
    ("BASED",  "Morocco"),
    ("NOW",    "ft_irc &#183; CPP modules &#183; Inception"),
]

# inlined as a data URI: an SVG loaded through <img> may not pull a remote href
data = base64.b64encode(open(PIC, "rb").read()).decode()

p = [svg(W, H, "Soufiane Lasfar"), "<title>Soufiane Lasfar</title>", STYLE,
     f'<image x="0" y="{(H-AV)//2}" width="{AV}" height="{AV}" '
     f'preserveAspectRatio="xMidYMid meet" href="data:image/png;base64,{data}"/>',
     f'<text x="{TX}" y="42" font-family="{DISPLAY}" font-size="33" letter-spacing="4.2" '
     f'class="pri">SOUFIANE LASFAR</text>',
     f'<rect x="{TX+1}" y="57" width="52" height="2" fill="{CRIM}"/>',
     f'<line x1="{TX+66}" y1="58" x2="{W}" y2="58" class="rule" stroke-width="1"/>']

y = 86
for k, v in ROWS:
    p.append(f'<text x="{TX}" y="{y}" font-family="{MONO}" font-size="9.5" font-weight="700" '
             f'letter-spacing="1.7" class="ter">{k}</text>')
    p.append(f'<text x="{TX+82}" y="{y}" font-family="{MONO}" font-size="12" class="sec">{v}</text>')
    y += 21

p.append("</svg>")
os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
open(OUT, "w").write("\n".join(p) + "\n")
print(f"wrote {OUT} ({W}x{H}) -> {os.path.getsize(OUT)/1024:.0f} KB")
