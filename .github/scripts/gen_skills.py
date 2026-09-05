#!/usr/bin/env python3
"""Stack card: monochrome icon tiles, grouped, glowing faintly."""
import html, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from theme import *

OUT = sys.argv[1] if len(sys.argv) > 1 else "dist/skills.svg"
ICONS = json.load(open(os.path.join(os.path.dirname(__file__), "..", "assets", "icons.json")))

GROUPS = [
    ("LANGUAGES", ["c", "cplusplus", "python", "typescript", "javascript", "gnubash"]),
    ("SYSTEMS",   ["linux", "docker", "nginx", "git", "vim", "wireshark"]),
    ("WEB & DATA",["react", "nodedotjs", "php", "wordpress", "mariadb"]),
]

PAD, COLS, GAP = 34, 6, 12
TILE = (W - PAD * 2 - GAP * (COLS - 1)) / COLS      # ~106
TH = 74                                              # tile height
HEAD, SECTION_GAP = 30, 26
u = "s"

H = int(28 + sum(HEAD + TH + SECTION_GAP for _ in GROUPS) - SECTION_GAP + 18)

parts = [open_svg(H, "Tools and languages"), "<title>Stack</title>", defs(uid=u), clip(H, u),
         f'<g clip-path="url(#card{u})">', frame(H, u),
         orb(60, -20, 200, u, dur=13), orb(720, H, 200, u, dur=16, delay=4)]

y = 40
for title, slugs in GROUPS:
    parts.append(f'<text x="{PAD}" y="{y}" font-family="{MONO}" font-size="9.5" '
                 f'letter-spacing="3" fill="{DIM}">{html.escape(title)}</text>')
    parts.append(f'<line x1="{PAD + 110}" y1="{y-4}" x2="{W-PAD}" y2="{y-4}" stroke="{HAIR}"/>')
    y += 14
    for i, slug in enumerate(slugs):
        ic = ICONS.get(slug)
        if not ic:
            continue
        x = PAD + i * (TILE + GAP)
        # tile
        parts.append(f'<rect x="{x:.1f}" y="{y}" width="{TILE:.1f}" height="{TH}" rx="8" '
                     f'fill="#0e0e11" stroke="{LINE}"/>')
        # icon, simple-icons are 24x24 -> scale and centre
        s = 22 / 24
        ix = x + TILE / 2 - 11
        parts.append(f'<g transform="translate({ix:.1f},{y+16}) scale({s:.4f})" '
                     f'fill="{WHITE}" opacity="0.92"><path d="{ic["path"]}"/></g>')
        parts.append(f'<text x="{x + TILE/2:.1f}" y="{y + TH - 14}" font-family="{MONO}" '
                     f'font-size="9" fill="{MUTED}" text-anchor="middle">{html.escape(ic["label"])}</text>')
    y += TH + SECTION_GAP

parts += ["</g>", "</svg>"]
os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
open(OUT, "w").write("\n".join(parts) + "\n")
print(f"wrote {OUT} ({H}px tall)")
