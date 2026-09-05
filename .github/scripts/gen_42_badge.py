#!/usr/bin/env python3
"""42 cursus card.

Level comes from badge42, the only public source that reaches the intra API
without OAuth credentials; we just redraw it, so the card stays current
without anyone editing this repo.
"""
import html, os, re, sys, urllib.request
sys.path.insert(0, os.path.dirname(__file__))
from theme import *

LOGIN = sys.argv[1] if len(sys.argv) > 1 else "slasfar"
OUT = sys.argv[2] if len(sys.argv) > 2 else "dist/42.svg"
H, u = 152, "f"


def scrape():
    req = urllib.request.Request(f"https://badge.mediaplus.ma/levi/{LOGIN}",
                                 headers={"User-Agent": "profile-readme"})
    svg = urllib.request.urlopen(req, timeout=45).read().decode("utf-8", "replace")
    t = " ".join(re.findall(r">([^<>]{1,60})<", svg))
    m = re.search(r"level\s+(\d+)\s*-\s*(\d+)\s*%", t, re.I)
    level, pct = (int(m.group(1)), int(m.group(2))) if m else (0, 0)
    g = re.search(r"\b(Cadet|Member|Learner|Alumni|Transcender|Pisciner)\b", t, re.I)
    n = re.search(r"\b([A-Z][a-z]+ [A-Z][a-z]+)\b", t)
    return level, pct, (g.group(1).title() if g else "Cadet"), (n.group(1) if n else LOGIN)


level, pct, grade, name = scrape()
bar_w = W - PAD * 2
fill = bar_w * pct / 100

svg = f"""{head(H, f"42cursus level {level}.{pct:02d}, {grade}")}
<title>42cursus — level {level}.{pct:02d} ({grade})</title>
{plate_defs(H, u)}
<g clip-path="url(#clip{u})">
  {plate(H, u)}
  {eyes(u)}
  {eyebrow(62, 32.5, "42CURSUS")}
  {eyebrow(W - PAD, 32.5, html.escape(grade.upper()), anchor="end", fill=GHOST)}

  <text x="{PAD}" y="86" font-family="{DISPLAY}" font-size="27" letter-spacing="3.4"
        fill="{BONE}">{html.escape(LOGIN.upper())}</text>
  <text x="{W-PAD}" y="86" font-family="{MONO}" font-size="31" font-weight="500"
        letter-spacing="-0.3" fill="{BONE}" text-anchor="end">{level}.{pct:02d}</text>

  <rect x="{PAD}" y="104" width="{bar_w}" height="4" rx="1" fill="{TRACK}"/>
  <rect x="{PAD}" y="104" width="{fill:.1f}" height="4" rx="1" fill="{CRIM}" fill-opacity="0.88"/>

  <text x="{PAD}" y="133" font-family="{MONO}" font-size="10.5" fill="{DIM}"
    >intra.42.fr/users/{html.escape(LOGIN)}</text>
  <text x="{W-PAD}" y="133" font-family="{MONO}" font-size="10.5" fill="{DIM}"
    text-anchor="end">{pct}% to level {level+1}</text>
</g>
{border(H)}
</svg>
"""
os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
open(OUT, "w").write(svg)
print(f"wrote {OUT}: {name} — level {level}.{pct:02d} ({grade})")
