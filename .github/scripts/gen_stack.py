#!/usr/bin/env python3
"""The stack — one section, real full-colour brand marks, on no background.

Ordered low-level first, so it reads as a path from the metal outwards rather
than as an unsorted pile. Rows are centred and balanced, which is what stops a
17-item grid looking like it has a hole in the last row.
"""
import html, json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from plain import *

OUT = sys.argv[1] if len(sys.argv) > 1 else "dist/stack.svg"
ICONS = json.load(open(os.path.join(os.path.dirname(__file__), "..", "assets", "icons.json")))

ORDER = ["c", "cpp", "python", "bash", "linux", "vim", "git", "cmake", "docker",
         "nginx", "mariadb", "php", "wordpress", "javascript", "typescript",
         "nodejs", "react"]

W = 800
ICON, LABEL_DY, ROW_H = 36, 20, 78
PER_ROW = 9

keys = [k for k in ORDER if k in ICONS]
rows = [keys[i:i + PER_ROW] for i in range(0, len(keys), PER_ROW)]
# balance the rows so the last one is never a stub
if len(rows) == 2 and len(rows[1]) < len(rows[0]) - 1:
    half = math.ceil(len(keys) / 2)
    rows = [keys[:half], keys[half:]]

CELL = 80
H = len(rows) * ROW_H + 6

p = [svg(W, H, "Languages, systems and tools I work with"), "<title>Stack</title>", STYLE]

for r, row in enumerate(rows):
    span = len(row) * CELL
    x0 = (W - span) / 2
    y = r * ROW_H + 8
    for i, k in enumerate(row):
        ic = ICONS[k]
        cx = x0 + i * CELL + CELL / 2
        sc = ICON / max(ic["w"], ic["h"])
        dw, dh = ic["w"] * sc, ic["h"] * sc
        p.append(f'<g transform="translate({cx - dw/2:.2f},{y + (ICON - dh)/2:.2f}) '
                 f'scale({sc:.5f})">{ic["inner"]}</g>')
        p.append(f'<text x="{cx:.1f}" y="{y + ICON + LABEL_DY}" font-family="{MONO}" '
                 f'font-size="10" class="sec" text-anchor="middle">'
                 f'{html.escape(ic["label"])}</text>')

p.append("</svg>")
os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
open(OUT, "w").write("\n".join(p) + "\n")
print(f"wrote {OUT} ({W}x{H}) rows={[len(r) for r in rows]}")
