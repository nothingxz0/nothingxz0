#!/usr/bin/env python3
"""Avatar + facts, on no background.

Both halves live in one SVG on purpose. Two side-by-side <img> tags wrap onto
separate lines as soon as the README column is narrower than their combined
width, which it is on a lot of screens. One image cannot come apart.

The avatar is re-fetched and embedded on every run, so changing the GitHub
profile picture updates this badge within a day, on its own.
"""
import base64, html, os, re, sys, urllib.request
sys.path.insert(0, os.path.dirname(__file__))
from plain import *

LOGIN = sys.argv[1] if len(sys.argv) > 1 else "slasfar"
OUT = sys.argv[2] if len(sys.argv) > 2 else "dist/identity.svg"
UID = os.environ.get("GH_UID", "72560375")

W, H = 800, 172
AV = 172                     # avatar box
GAP = 26
TX = AV + GAP                # where the text column starts


def fetch(url, timeout=45):
    r = urllib.request.Request(url, headers={"User-Agent": "profile-readme"})
    with urllib.request.urlopen(r, timeout=timeout) as f:
        return f.read(), f.headers.get("Content-Type", "image/jpeg")


def avatar():
    """Inline the avatar as a data URI -- camo will not follow a remote ref
    from inside an SVG, so it has to travel with the file."""
    try:
        raw, ctype = fetch(f"https://avatars.githubusercontent.com/u/{UID}?s=344")
        if "png" in ctype:
            mime = "image/png"
        elif "webp" in ctype:
            mime = "image/webp"
        else:
            mime = "image/jpeg"
        return f"data:{mime};base64," + base64.b64encode(raw).decode(), len(raw)
    except Exception as e:
        print("avatar fetch failed:", e, file=sys.stderr)
        return None, 0


def cursus():
    try:
        raw, _ = fetch(f"https://badge.mediaplus.ma/levi/{LOGIN}")
        t = " ".join(re.findall(r">([^<>]{1,60})<", raw.decode("utf-8", "replace")))
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

data, nbytes = avatar()

p = [svg(W, H, "Soufiane Lasfar"), "<title>Soufiane Lasfar</title>", STYLE,
     f'<defs><clipPath id="av"><rect x="0" y="0" width="{AV}" height="{AV}" rx="10"/></clipPath></defs>']

if data:
    p.append(f'<image x="0" y="0" width="{AV}" height="{AV}" clip-path="url(#av)" '
             f'preserveAspectRatio="xMidYMid slice" href="{data}"/>')

p += [
    f'<text x="{TX}" y="40" font-family="{DISPLAY}" font-size="33" letter-spacing="4.2" '
    f'class="pri">SOUFIANE LASFAR</text>',
    f'<rect x="{TX+1}" y="55" width="52" height="2" fill="{CRIM}"/>',
    f'<line x1="{TX+66}" y1="56" x2="{W}" y2="56" class="rule" stroke-width="1"/>',
]

y = 84
for k, v in ROWS:
    p.append(f'<text x="{TX}" y="{y}" font-family="{MONO}" font-size="9.5" font-weight="700" '
             f'letter-spacing="1.7" class="ter">{k}</text>')
    p.append(f'<text x="{TX+82}" y="{y}" font-family="{MONO}" font-size="12" class="sec">{v}</text>')
    y += 21

p.append("</svg>")
os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
open(OUT, "w").write("\n".join(p) + "\n")
print(f"wrote {OUT} ({W}x{H}) avatar={nbytes}B -> {os.path.getsize(OUT)/1024:.0f} KB")
