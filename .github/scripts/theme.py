"""Shared visual language for the generated profile cards.

Everything is greyscale on near-black. Depth comes from blurred radial orbs
and hairline borders rather than colour, so the cards read as one system.
"""

W = 760                      # every card is this wide
INK = "#050506"              # page-black
PANEL = "#0b0b0d"            # card fill
LINE = "#1e1e22"             # hairline border
HAIR = "#141417"             # inner rules
WHITE = "#f5f5f7"
MUTED = "#8b8b93"
DIM = "#5c5c64"
RAMP = ["#f5f5f7", "#c3c3cb", "#94949d", "#6c6c75", "#4a4a52", "#2c2c33"]

MONO = "ui-monospace,SFMono-Regular,'JetBrains Mono',Menlo,monospace"
SANS = "'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"


def defs(orbs=(), glow=True, uid=""):
    """Radial 'blur' orbs + an optional soft glow filter."""
    g = [f'<radialGradient id="orb{uid}" cx="50%" cy="50%" r="50%">'
         f'<stop offset="0%" stop-color="#ffffff" stop-opacity="0.13"/>'
         f'<stop offset="55%" stop-color="#ffffff" stop-opacity="0.04"/>'
         f'<stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>'
         f'</radialGradient>']
    if glow:
        # a halo, not a smear: blur a dimmed copy and lay the crisp text over it
        g.append(f'<filter id="glow{uid}" x="-60%" y="-60%" width="220%" height="220%">'
                 f'<feGaussianBlur stdDeviation="7" result="b"/>'
                 f'<feComponentTransfer in="b" result="h">'
                 f'<feFuncA type="linear" slope="0.45"/></feComponentTransfer>'
                 f'<feMerge><feMergeNode in="h"/><feMergeNode in="SourceGraphic"/></feMerge>'
                 f'</filter>')
    g.append(f'<linearGradient id="sheen{uid}" x1="0" y1="0" x2="0" y2="1">'
             f'<stop offset="0%" stop-color="#ffffff" stop-opacity="0.05"/>'
             f'<stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>'
             f'</linearGradient>')
    return "<defs>" + "".join(g) + "</defs>"


def orb(cx, cy, r, uid="", dur=None, delay=0):
    """A soft blurred light source. Optionally breathes, very slowly."""
    a = ""
    if dur:
        a = (f'<animate attributeName="opacity" values="0.55;1;0.55" '
             f'dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/>')
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#orb{uid})">{a}</circle>'


def frame(h, uid=""):
    """Card background: black panel, hairline border, top sheen."""
    return (f'<rect x="0.5" y="0.5" width="{W-1}" height="{h-1}" rx="10" fill="{PANEL}" stroke="{LINE}"/>'
            f'<rect x="0.5" y="0.5" width="{W-1}" height="{min(h-1,120)}" rx="10" fill="url(#sheen{uid})"/>')


def open_svg(h, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" '
            f'viewBox="0 0 {W} {h}" role="img" aria-label="{label}">')


def clip(h, uid=""):
    """Keep orbs inside the rounded card."""
    return (f'<clipPath id="card{uid}"><rect x="0" y="0" width="{W}" height="{h}" rx="10"/></clipPath>')
