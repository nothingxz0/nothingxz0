#!/usr/bin/env python3
"""Wrap the generated snake in the same card frame as everything else.

snk emits a bare, transparent SVG. Nesting it inside our frame keeps the
contribution graph from being the one element that floats loose on the page.
The inner <svg> keeps its own viewBox, and the CSS custom properties the
animation relies on inherit straight through.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from theme import *

SRC = sys.argv[1] if len(sys.argv) > 1 else "dist/snake.svg"
OUT = sys.argv[2] if len(sys.argv) > 2 else "dist/snake.svg"
PAD, u = 24, "n"

raw = open(SRC).read()
open_tag = re.search(r"<svg\b[^>]*>", raw).group(0)
vb = re.search(r'viewBox="([^"]+)"', open_tag).group(1)
sw, sh = (float(v) for v in vb.split()[2:4])   # aspect comes from the viewBox
inner = raw[len(open_tag):raw.rindex("</svg>")]

box_w = W - PAD * 2
box_h = round(box_w * sh / sw, 1)
H = int(box_h + PAD * 2)

out = f"""{open_svg(H, "Contribution graph being eaten by a snake")}
<title>Contributions</title>
{defs(uid=u, glow=False)}
{clip(H, u)}
<g clip-path="url(#card{u})">
  {frame(H, u)}
  {orb(80, 0, 170, u, dur=14)}
  {orb(700, H, 180, u, dur=17, delay=5)}
  <svg x="{PAD}" y="{PAD}" width="{box_w}" height="{box_h}" viewBox="{vb}">{inner}</svg>
</g>
</svg>
"""
os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
open(OUT, "w").write(out)
print(f"framed {SRC} -> {OUT} ({W}x{H})")
