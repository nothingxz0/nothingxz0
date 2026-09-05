"""Shared visual language for the generated profile cards.

Taken from the avatar: a hooded skull in near-total darkness, lit only by two
crimson eyes. So the ground is genuinely black, the little light there is falls
from above-left, and crimson is rationed.

Two rules keep the set coherent:
  * plate() draws the same ground on every card -- black, with haze confined to
    fixed-size corner squares so a short card and a tall one look identical.
  * eyes() sits at the same coordinates on every card. Down a README it forms a
    vertical registration column, and that column is the identity.
"""

W = 800
PAD = 28
R = 10

# ── ground ───────────────────────────────────────────────────────────────
VOID  = "#05070c"       # the floor
CARD  = "#080b12"       # nested panel
WELL  = "#0c1017"       # recessed furniture: icon tiles, bar tracks
HAZE  = "#1b2130"       # corner haze, never at full opacity
HAZE_R = 200            # fixed px: identical corners on every card
LINE  = "#151a24"       # card border, dividers
FAINT = "#0f131b"       # internal rules
TRACK = "#0e1219"       # unfilled bar remainder

# ── ink ──────────────────────────────────────────────────────────────────
BONE   = "#dfe4ec"
MUTED  = "#8a919c"
DIM    = "#5b6473"
GHOST  = "#3f4756"

# ── crimson: the eyes. Budget is two elements per card, and only the eyes glow ──
CRIM_HOT  = "#ff5a5a"
CRIM      = "#ff1a26"
CRIM_DEEP = "#8f0d15"
CRIM_GLOW = "#ff2b34"

# cold neutral ramp, largest series first; rank-1 may be overridden to crimson
RAMP = ["#aab3c0", "#7e8798", "#5c6473", "#424a58", "#2e3542", "#1e2430"]

# A tracked serif in caps carries the one display string. Every generated README
# card in existence renders in Segoe UI / Roboto, so dropping sans is the cheapest
# single move that stops these reading as template furniture.
# single quotes inside: these are interpolated into double-quoted SVG attributes
DISPLAY = ("'Iowan Old Style','Palatino Linotype',Palatino,'Book Antiqua',"
           "'URW Palladio L',Georgia,'Times New Roman',serif")
MONO = ("ui-monospace,'SF Mono',SFMono-Regular,Menlo,Consolas,"
        "'Liberation Mono','DejaVu Sans Mono',monospace")


def head(h, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" '
            f'viewBox="0 0 {W} {h}" preserveAspectRatio="xMidYMid meet" '
            f'text-rendering="geometricPrecision" role="img" aria-label="{label}">')


def plate_defs(h, uid):
    """Corner haze + the eye bloom. Nothing else emits light."""
    g = []
    for tag, cx, cy in (("tl", 0, 0), ("tr", 1, 0), ("bl", 0, 1), ("br", 1, 1)):
        g.append(
            f'<radialGradient id="hz{tag}{uid}" cx="{cx}" cy="{cy}" r="1">'
            f'<stop offset="0" stop-color="{HAZE}" stop-opacity="1"/>'
            f'<stop offset="0.55" stop-color="{HAZE}" stop-opacity="0.34"/>'
            f'<stop offset="1" stop-color="{HAZE}" stop-opacity="0"/>'
            f'</radialGradient>')
    # sRGB is mandatory: the linearRGB default washes the bloom out and
    # renders differently in Firefox than in Chrome
    g.append(f'<filter id="eye{uid}" x="-500%" y="-500%" width="1100%" height="1100%" '
             f'color-interpolation-filters="sRGB">'
             f'<feGaussianBlur in="SourceGraphic" stdDeviation="1.6" result="b1"/>'
             f'<feGaussianBlur in="SourceGraphic" stdDeviation="5.5" result="b2"/>'
             f'<feMerge><feMergeNode in="b2"/><feMergeNode in="b1"/></feMerge>'
             f'</filter>')
    g.append(f'<clipPath id="clip{uid}"><rect x="0" y="0" width="{W}" height="{h}" rx="{R}"/></clipPath>')
    return "<defs>" + "".join(g) + "</defs>" + _style()


def _style():
    # out of phase by 0.7s: perfectly synced dots read as a recording light,
    # slightly offset they read as alive
    return ("<style>"
            "@keyframes breathe{0%,100%{opacity:.55}50%{opacity:1}}"
            ".eL{animation:breathe 5.2s ease-in-out infinite}"
            ".eR{animation:breathe 5.2s ease-in-out infinite;animation-delay:-.7s}"
            "@media (prefers-reduced-motion:reduce){.eL,.eR{animation:none;opacity:.85}}"
            "</style>")


def plate(h, uid):
    """The shared ground. Haze is asymmetric -- light falls from above-left,
    toward where the eyes sit. Symmetric weights read as an inset box-shadow."""
    r = HAZE_R
    return (
        f'<rect x="0" y="0" width="{W}" height="{h}" fill="{VOID}"/>'
        f'<rect x="0" y="0" width="{r}" height="{r}" fill="url(#hztl{uid})" opacity="0.30"/>'
        f'<rect x="{W-r}" y="0" width="{r}" height="{r}" fill="url(#hztr{uid})" opacity="0.22"/>'
        f'<rect x="0" y="{h-r}" width="{r}" height="{r}" fill="url(#hzbl{uid})" opacity="0.13"/>'
        f'<rect x="{W-r}" y="{h-r}" width="{r}" height="{r}" fill="url(#hzbr{uid})" opacity="0.13"/>'
    )


def border(h):
    return (f'<rect x="0.5" y="0.5" width="{W-1}" height="{h-1}" rx="{R-0.5}" '
            f'fill="none" stroke="{LINE}"/>')


def eyes(uid, cy=28, lx=30, rx=44):
    """The motif. Same coordinates on every card -- a registration mark, and
    the bullet that opens the eyebrow. The only glowing thing in the system."""
    return (
        f'<g filter="url(#eye{uid})" opacity="0.85">'
        f'<circle class="eL" cx="{lx}" cy="{cy}" r="2.2" fill="{CRIM_GLOW}"/>'
        f'<circle class="eR" cx="{rx}" cy="{cy}" r="2.2" fill="{CRIM_GLOW}"/></g>'
        f'<circle cx="{lx}" cy="{cy}" r="1.5" fill="{CRIM}"/>'
        f'<circle cx="{rx}" cy="{cy}" r="1.5" fill="{CRIM}"/>'
        f'<circle cx="{lx}" cy="{cy}" r="0.7" fill="{CRIM_HOT}"/>'
        f'<circle cx="{rx}" cy="{cy}" r="0.7" fill="{CRIM_HOT}"/>'
    )


def eyebrow(x, y, text, anchor="start", fill=DIM, size=10, track=1.8):
    return (f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="{size}" '
            f'font-weight="700" letter-spacing="{track}" fill="{fill}" '
            f'text-anchor="{anchor}">{text}</text>')
