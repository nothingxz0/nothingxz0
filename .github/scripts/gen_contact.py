#!/usr/bin/env python3
"""Contact buttons — hand-drawn, not shields.io.

Two halves like a classic badge, but on our own palette: the mark and the
service on the left, the handle on the right, split by a hairline with the
ember tick that runs through the rest of the profile.

These carry their own dark ground on purpose. They are buttons, so they should
read as objects on the page rather than as loose text, and a fixed dark chip
looks deliberate on GitHub light as well as dark.
"""
import html, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from plain import *

OUTDIR = sys.argv[1] if len(sys.argv) > 1 else "dist"
MARKS = json.load(open(os.path.join(os.path.dirname(__file__), "..", "assets", "marks.json")))

H = 46
PADX = 16          # outer padding
ICON = 17
ICON_GAP = 9
MID_GAP = 15       # space either side of the divider
LBL_SIZE, LBL_TRACK = 10, 1.9
VAL_SIZE, VAL_TRACK = 12.5, 0.3
MONO_ADV = 0.605   # worst-case-safe advance ratio across the mono stack

FILL, EDGE = "#0b0f16", "#232b38"
LBL_FILL, VAL_FILL = "#8a919c", "#e6edf3"

BADGES = [
    ("github", "github", "GITHUB", "nothingxz0"),
    ("intra42", "42", "42 INTRA", "slasfar"),
]


def text_w(s, size, track):
    return len(s) * (size * MONO_ADV + track)


for name, mark_key, label, value in BADGES:
    mk = MARKS[mark_key]
    lw = text_w(label, LBL_SIZE, LBL_TRACK)
    vw = text_w(value, VAL_SIZE, VAL_TRACK)
    left = PADX + ICON + ICON_GAP + lw
    divx = left + MID_GAP
    W = divx + MID_GAP + vw + PADX

    icon_scale = ICON / 24
    iy = (H - ICON) / 2

    p = [svg(round(W), H, f"{label} — {value}"),
         f"<title>{label} — {value}</title>",
         f'<rect x="0.5" y="0.5" width="{W-1:.1f}" height="{H-1}" rx="9" '
         f'fill="{FILL}" stroke="{EDGE}"/>',
         # the ember tick, same accent as the rule on the identity badge
         f'<rect x="0" y="{H/2-9:.1f}" width="2.5" height="18" rx="1.25" fill="{CRIM}"/>',
         f'<g transform="translate({PADX},{iy:.1f}) scale({icon_scale:.5f})" fill="{VAL_FILL}">'
         f'<path d="{mk["path"]}"/></g>',
         f'<text x="{PADX + ICON + ICON_GAP:.1f}" y="{H/2 + 3.5:.1f}" font-family="{MONO}" '
         f'font-size="{LBL_SIZE}" font-weight="700" letter-spacing="{LBL_TRACK}" '
         f'fill="{LBL_FILL}">{html.escape(label)}</text>',
         f'<line x1="{divx:.1f}" y1="12" x2="{divx:.1f}" y2="{H-12}" stroke="{EDGE}"/>',
         f'<text x="{divx + MID_GAP:.1f}" y="{H/2 + 4.5:.1f}" font-family="{MONO}" '
         f'font-size="{VAL_SIZE}" letter-spacing="{VAL_TRACK}" '
         f'fill="{VAL_FILL}">{html.escape(value)}</text>',
         "</svg>"]

    os.makedirs(OUTDIR, exist_ok=True)
    path = os.path.join(OUTDIR, f"contact_{name}.svg")
    open(path, "w").write("\n".join(p) + "\n")
    print(f"wrote {path} ({round(W)}x{H})")
