#!/usr/bin/env python3
"""Stack card — real full-colour brand marks on dark tiles."""
import html, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from theme import *

OUT = sys.argv[1] if len(sys.argv) > 1 else "dist/skills.svg"
ICONS = json.load(open(os.path.join(os.path.dirname(__file__), "..", "assets", "icons.json")))

GROUPS = [
    ("LANGUAGES",  ["c", "cpp", "python", "typescript", "javascript", "bash"]),
    ("SYSTEMS",    ["linux", "docker", "nginx", "git", "vim", "cmake"]),
    ("WEB & DATA", ["react", "nodejs", "php", "wordpress", "mariadb"]),
]

COLS, GAP = 6, 12
TILE = (W - PAD * 2 - GAP * (COLS - 1)) / COLS
TH = 82
ICON = 30
GROUP_GAP = 22
u = "s"

H = int(56 + sum(26 + TH + GROUP_GAP for _ in GROUPS) - GROUP_GAP + 10)

p = [head(H, "Languages, systems and web tools"), "<title>Stack</title>",
     plate_defs(H, u), f'<g clip-path="url(#clip{u})">', plate(H, u), eyes(u),
     eyebrow(62, 32.5, "STACK"),
     eyebrow(W - PAD, 32.5, "WHAT I REACH FOR", anchor="end", fill=GHOST)]

y = 74
for title, keys in GROUPS:
    p.append(eyebrow(PAD, y, html.escape(title), fill=DIM, size=9.5, track=2.2))
    p.append(f'<line x1="{PAD + len(title)*8.2 + 16:.0f}" y1="{y-3.5}" x2="{W-PAD}" '
             f'y2="{y-3.5}" stroke="{FAINT}"/>')
    y += 12
    for i, k in enumerate(keys):
        ic = ICONS.get(k)
        if not ic:
            continue
        x = PAD + i * (TILE + GAP)
        p.append(f'<rect x="{x:.1f}" y="{y}" width="{TILE:.1f}" height="{TH}" rx="4" '
                 f'fill="{WELL}" stroke="{LINE}"/>')
        sc = ICON / max(ic["w"], ic["h"])
        dw, dh = ic["w"] * sc, ic["h"] * sc
        ix = x + TILE / 2 - dw / 2
        iy = y + 19 + (ICON - dh) / 2
        p.append(f'<g transform="translate({ix:.2f},{iy:.2f}) scale({sc:.5f})">{ic["inner"]}</g>')
        p.append(f'<text x="{x + TILE/2:.1f}" y="{y + TH - 14}" font-family="{MONO}" '
                 f'font-size="9.5" fill="{MUTED}" text-anchor="middle">'
                 f'{html.escape(ic["label"])}</text>')
    y += TH + GROUP_GAP

p += ["</g>", border(H), "</svg>"]
os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
open(OUT, "w").write("\n".join(p) + "\n")
print(f"wrote {OUT} ({H}px)")
