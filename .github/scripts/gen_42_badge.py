#!/usr/bin/env python3
"""42 cursus card.

Reads the current level from badge42, which is the only public source that
reaches the intra API without OAuth credentials, then redraws it in our own
style so the card stays current without anyone editing this repo.
"""
import html, os, re, sys, urllib.request
sys.path.insert(0, os.path.dirname(__file__))
from theme import *

LOGIN = sys.argv[1] if len(sys.argv) > 1 else "slasfar"
OUT = sys.argv[2] if len(sys.argv) > 2 else "dist/42.svg"
H, PAD, u = 148, 34, "f"


def scrape():
    req = urllib.request.Request(f"https://badge.mediaplus.ma/levi/{LOGIN}",
                                 headers={"User-Agent": "profile-readme"})
    svg = urllib.request.urlopen(req, timeout=45).read().decode("utf-8", "replace")
    text = " ".join(re.findall(r">([^<>]{1,60})<", svg))
    m = re.search(r"level\s+(\d+)\s*-\s*(\d+)\s*%", text, re.I)
    level, pct = (int(m.group(1)), int(m.group(2))) if m else (0, 0)
    g = re.search(r"\b(Cadet|Member|Learner|Alumni|Transcender|Pisciner)\b", text, re.I)
    n = re.search(r"\b([A-Z][a-z]+ [A-Z][a-z]+)\b", text)
    return level, pct, (g.group(1).title() if g else "Cadet"), (n.group(1) if n else LOGIN)


level, pct, grade, name = scrape()
bar_w = W - PAD * 2
fill = bar_w * pct / 100

svg = f"""{open_svg(H, f"42cursus level {level}.{pct:02d}, {grade}")}
<title>42cursus — level {level}.{pct:02d} ({grade})</title>
{defs(uid=u)}
{clip(H, u)}
<g clip-path="url(#card{u})">
  {frame(H, u)}
  {orb(70, 20, 170, u, dur=12)}
  {orb(690, 150, 180, u, dur=15, delay=5)}
  <g font-family="{MONO}" font-size="9.5" letter-spacing="3" fill="{DIM}">
    <text x="{PAD}" y="36">42CURSUS</text>
    <text x="{W-PAD}" y="36" text-anchor="end">{html.escape(grade.upper())}</text>
  </g>
  <text x="{PAD}" y="76" font-family="{SANS}" font-size="27" font-weight="600"
        letter-spacing="-0.5" fill="{WHITE}" filter="url(#glow{u})">{html.escape(name)}</text>
  <text x="{W-PAD}" y="76" font-family="{MONO}" font-size="27" fill="{WHITE}"
        text-anchor="end" filter="url(#glow{u})">{level}.{pct:02d}</text>
  <rect x="{PAD}" y="97" width="{bar_w}" height="5" rx="2.5" fill="#1a1a1f"/>
  <rect x="{PAD}" y="97" width="{fill:.1f}" height="5" rx="2.5" fill="{WHITE}"/>
  <g font-family="{MONO}" font-size="10" fill="{DIM}">
    <text x="{PAD}" y="126">intra.42.fr/users/{html.escape(LOGIN)}</text>
    <text x="{W-PAD}" y="126" text-anchor="end">{pct}% to level {level+1}</text>
  </g>
</g>
</svg>
"""
os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
open(OUT, "w").write(svg)
print(f"wrote {OUT}: {name} — level {level}.{pct:02d} ({grade})")
