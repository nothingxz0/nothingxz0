#!/usr/bin/env python3
"""Hero card: name, role, and three slow-breathing light sources."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from theme import *

OUT = sys.argv[1] if len(sys.argv) > 1 else "dist/header.svg"
H = 208
u = "h"

body = f"""{open_svg(H, "Soufiane Lasfar — systems and low-level engineering")}
<title>Soufiane Lasfar</title>
{defs(uid=u)}
{clip(H, u)}
<g clip-path="url(#card{u})">
  {frame(H, u)}
  {orb(90, 30, 190, u, dur=11)}
  {orb(700, 200, 210, u, dur=14, delay=3)}
  {orb(390, 110, 150, u, dur=17, delay=6)}
  <g font-family="{MONO}">
    <text x="40" y="52" font-size="10.5" letter-spacing="3.4" fill="{DIM}">1337 CODING SCHOOL &#183; 42 NETWORK</text>
  </g>
  <g font-family="{SANS}">
    <text x="38" y="112" font-size="46" font-weight="700" letter-spacing="-1.4" fill="{WHITE}" filter="url(#glow{u})">Soufiane Lasfar</text>
  </g>
  <line x1="40" y1="136" x2="{W-40}" y2="136" stroke="{HAIR}"/>
  <g font-family="{MONO}" font-size="12" fill="{MUTED}">
    <text x="40" y="164">C &#183; C++ &#183; systems &#183; networks &#183; containers</text>
    <text x="{W-40}" y="164" text-anchor="end" fill="{DIM}">@nothingxz0</text>
  </g>
  <g font-family="{MONO}" font-size="10.5" fill="{DIM}">
    <text x="40" y="186">the layer where you own the memory, and every mistake in it</text>
  </g>
</g>
</svg>
"""
os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
open(OUT, "w").write(body)
print("wrote", OUT)
