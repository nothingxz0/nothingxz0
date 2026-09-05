#!/usr/bin/env python3
"""Name + facts, on no background, to sit beside the avatar."""
import html, os, re, sys, urllib.request
sys.path.insert(0, os.path.dirname(__file__))
from plain import *

LOGIN = sys.argv[1] if len(sys.argv) > 1 else "slasfar"
OUT = sys.argv[2] if len(sys.argv) > 2 else "dist/identity.svg"
W, H = 596, 170


def cursus():
    try:
        r = urllib.request.Request(f"https://badge.mediaplus.ma/levi/{LOGIN}",
                                   headers={"User-Agent": "profile-readme"})
        t = " ".join(re.findall(r">([^<>]{1,60})<",
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

p = [svg(W, H, "Soufiane Lasfar"), "<title>Soufiane Lasfar</title>", STYLE,
     f'<text x="0" y="36" font-family="{DISPLAY}" font-size="33" letter-spacing="4.3" '
     f'class="pri">SOUFIANE LASFAR</text>',
     f'<rect x="1" y="50" width="52" height="2" fill="{CRIM}"/>',
     f'<line x1="66" y1="51" x2="{W}" y2="51" class="rule" stroke-width="1"/>']

y = 80
for k, v in ROWS:
    p.append(f'<text x="0" y="{y}" font-family="{MONO}" font-size="9.5" font-weight="700" '
             f'letter-spacing="1.7" class="ter">{k}</text>')
    p.append(f'<text x="82" y="{y}" font-family="{MONO}" font-size="12" class="sec">{v}</text>')
    y += 21

p.append("</svg>")
os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
open(OUT, "w").write("\n".join(p) + "\n")
print(f"wrote {OUT} ({W}x{H})")
