#!/usr/bin/env python3
"""Render a minimal 42 cursus badge.

Pulls the current level from badge42 (the only public source that speaks to
the intra API without OAuth credentials) and redraws it in our own style,
so the card stays current without anyone touching this repo.
"""
import html
import re
import sys
import urllib.request

LOGIN = sys.argv[1] if len(sys.argv) > 1 else "slasfar"
OUT = sys.argv[2] if len(sys.argv) > 2 else "dist/42.svg"
SRC = f"https://badge.mediaplus.ma/levi/{LOGIN}"

BG, LINE, FG, MUTED, BAR = "#0d1117", "#21262d", "#e6edf3", "#7d8590", "#e6edf3"


def scrape():
    req = urllib.request.Request(SRC, headers={"User-Agent": "profile-readme"})
    svg = urllib.request.urlopen(req, timeout=45).read().decode("utf-8", "replace")
    text = " ".join(re.findall(r">([^<>]{1,60})<", svg))

    m = re.search(r"level\s+(\d+)\s*-\s*(\d+)\s*%", text, re.I)
    level, pct = (int(m.group(1)), int(m.group(2))) if m else (0, 0)

    g = re.search(r"\b(Cadet|Member|Learner|Alumni|Transcender|Pisciner)\b", text, re.I)
    grade = g.group(1).title() if g else "Cadet"

    n = re.search(r"\b([A-Z][a-z]+ [A-Z][a-z]+)\b", text)
    return level, pct, grade, (n.group(1) if n else LOGIN)


def render(level, pct, grade, name):
    W, H, PAD = 460, 132, 24
    bar_w = W - PAD * 2
    fill = round(bar_w * pct / 100, 1)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="42 cursus: level {level}.{pct:02d}, {grade}">
  <title>42cursus — level {level}.{pct:02d} ({grade})</title>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="6" fill="{BG}" stroke="{LINE}"/>
  <g font-family="ui-monospace,SFMono-Regular,'JetBrains Mono',Menlo,monospace">
    <text x="{PAD}" y="34" font-size="11" letter-spacing="2.4" fill="{MUTED}">42CURSUS</text>
    <text x="{W - PAD}" y="34" font-size="11" letter-spacing="2.4" fill="{MUTED}" text-anchor="end">{html.escape(grade.upper())}</text>
    <text x="{PAD}" y="66" font-size="21" fill="{FG}">{html.escape(name)}</text>
    <text x="{W - PAD}" y="66" font-size="21" fill="{FG}" text-anchor="end">{level}.{pct:02d}</text>
    <rect x="{PAD}" y="84" width="{bar_w}" height="6" rx="3" fill="{LINE}"/>
    <rect x="{PAD}" y="84" width="{fill}" height="6" rx="3" fill="{BAR}"/>
    <text x="{PAD}" y="118" font-size="10.5" fill="{MUTED}">intra.42.fr/users/{html.escape(LOGIN)}</text>
    <text x="{W - PAD}" y="118" font-size="10.5" fill="{MUTED}" text-anchor="end">{pct}% to level {level + 1}</text>
  </g>
</svg>
"""


level, pct, grade, name = scrape()
import os
os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
open(OUT, "w").write(render(level, pct, grade, name))
print(f"wrote {OUT}: {name} — level {level}.{pct:02d} ({grade})")
