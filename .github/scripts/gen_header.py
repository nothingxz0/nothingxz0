#!/usr/bin/env python3
"""Hero card. One display string, one rule, no ornament."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from theme import *

OUT = sys.argv[1] if len(sys.argv) > 1 else "dist/header.svg"
H, u = 220, "h"

svg = f"""{head(H, "Soufiane Lasfar — C, C++, systems, networks, containers")}
<title>Soufiane Lasfar</title>
{plate_defs(H, u)}
<g clip-path="url(#clip{u})">
  {plate(H, u)}
  {eyes(u)}
  {eyebrow(62, 32.5, "1337 CODING SCHOOL &#183; 42 NETWORK")}
  {eyebrow(W - PAD, 32.5, "@NOTHINGXZ0", anchor="end", fill=GHOST)}

  <text x="{PAD}" y="106" font-family="{DISPLAY}" font-size="42" letter-spacing="5.9"
        fill="{BONE}">SOUFIANE LASFAR</text>
  <text x="{PAD}" y="134" font-family="{DISPLAY}" font-size="15" letter-spacing="1.5"
        fill="{MUTED}">C &#183; C++ &#183; SYSTEMS &#183; NETWORKS &#183; CONTAINERS</text>

  <line x1="{PAD}" y1="158" x2="{W-PAD}" y2="158" stroke="{FAINT}"/>

  <text x="{PAD}" y="184" font-family="{MONO}" font-size="12.5" fill="{MUTED}"
    >the layer where you own the memory, and every mistake in it</text>
  <text x="{PAD}" y="203" font-family="{MONO}" font-size="10.5" fill="{DIM}"
    >currently: ft_irc &#183; CPP modules &#183; Inception</text>
</g>
{border(H)}
</svg>
"""
os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
open(OUT, "w").write(svg)
print("wrote", OUT)
