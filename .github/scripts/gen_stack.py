#!/usr/bin/env python3
"""Things I master — real full-colour brand marks, on no background."""
import html, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from plain import *

OUT = sys.argv[1] if len(sys.argv) > 1 else "dist/stack.svg"
ICONS = json.load(open(os.path.join(os.path.dirname(__file__), "..", "assets", "icons.json")))

GROUPS = [
    ("LANGUAGES",  ["c", "cpp", "python", "typescript", "javascript", "bash"]),
    ("SYSTEMS",    ["linux", "docker", "nginx", "git", "vim", "cmake"]),
    ("WEB & DATA", ["react", "nodejs", "php", "wordpress", "mariadb"]),
]

W = 800
COLS, GAP = 6, 14
CELL = (W - GAP * (COLS - 1)) / COLS
ICON, CH = 34, 62
GROUP_GAP = 26

H = int(sum(20 + CH + GROUP_GAP for _ in GROUPS) - GROUP_GAP + 6)

p = [svg(W, H, "Languages, systems and web tools"), "<title>Stack</title>", STYLE]

y = 12
for title, keys in GROUPS:
    p.append(f'<text x="0" y="{y}" font-family="{MONO}" font-size="9.5" font-weight="700" '
             f'letter-spacing="2.2" class="ter">{html.escape(title)}</text>')
    p.append(f'<line x1="{len(title)*8.4 + 14:.0f}" y1="{y-3.5}" x2="{W}" y2="{y-3.5}" '
             f'class="rule" stroke-width="1"/>')
    y += 20
    for i, k in enumerate(keys):
        ic = ICONS.get(k)
        if not ic:
            continue
        cx = i * (CELL + GAP) + CELL / 2
        sc = ICON / max(ic["w"], ic["h"])
        dw, dh = ic["w"] * sc, ic["h"] * sc
        p.append(f'<g transform="translate({cx - dw/2:.2f},{y + (ICON - dh)/2:.2f}) '
                 f'scale({sc:.5f})">{ic["inner"]}</g>')
        p.append(f'<text x="{cx:.1f}" y="{y + ICON + 17}" font-family="{MONO}" font-size="10" '
                 f'class="sec" text-anchor="middle">{html.escape(ic["label"])}</text>')
    y += CH + GROUP_GAP

p.append("</svg>")
os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
open(OUT, "w").write("\n".join(p) + "\n")
print(f"wrote {OUT} ({W}x{H})")
