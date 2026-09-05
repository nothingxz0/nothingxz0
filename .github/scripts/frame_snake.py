#!/usr/bin/env python3
"""Wrap the generated snake in the shared card so it is not the one loose element.

The inner <svg> keeps its own viewBox; the CSS custom properties the animation
relies on inherit straight through.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from theme import *

SRC = sys.argv[1] if len(sys.argv) > 1 else "dist/snake.svg"
OUT = sys.argv[2] if len(sys.argv) > 2 else "dist/snake.svg"
u = "n"

raw = open(SRC).read()
tag = re.search(r"<svg\b[^>]*>", raw).group(0)
vb = re.search(r'viewBox="([^"]+)"', tag).group(1)
sw, sh = (float(v) for v in vb.split()[2:4])
inner = raw[len(tag):raw.rindex("</svg>")]

box_w = W - PAD * 2
box_h = round(box_w * sh / sw, 1)
H = int(box_h + PAD + 54)

out = f"""{head(H, "Contribution graph being eaten by a snake")}
<title>Contributions</title>
{plate_defs(H, u)}
<g clip-path="url(#clip{u})">
  {plate(H, u)}
  {eyes(u)}
  {eyebrow(62, 32.5, "CONTRIBUTIONS")}
  {eyebrow(W - PAD, 32.5, "LAST 12 MONTHS", anchor="end", fill=GHOST)}
  <svg x="{PAD}" y="54" width="{box_w}" height="{box_h}" viewBox="{vb}">{inner}</svg>
</g>
{border(H)}
</svg>
"""
os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
open(OUT, "w").write(out)
print(f"framed {SRC} -> {OUT} ({W}x{H})")
