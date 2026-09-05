"""Helpers for the no-background badges.

These sit directly on the README, so they must not paint a ground: the page
behind them is white for some viewers and near-black for others. Text colour
is therefore set in CSS and swapped on prefers-color-scheme, which an SVG
still honours when it is loaded through <img>.
"""

# the purple of the drink in the picture -- the one accent in the system
ACCENT = "#8153f2"

DISPLAY = ("'Iowan Old Style','Palatino Linotype',Palatino,'Book Antiqua',"
           "'URW Palladio L',Georgia,'Times New Roman',serif")
MONO = ("ui-monospace,'SF Mono',SFMono-Regular,Menlo,Consolas,"
        "'Liberation Mono','DejaVu Sans Mono',monospace")

# GitHub's own light/dark text ramps, so the badges sit natively on either theme
STYLE = (
    "<style>"
    ".pri{fill:#1f2328}.sec{fill:#59636e}.ter{fill:#818b98}.rule{stroke:#d1d9e0}"
    "@media (prefers-color-scheme:dark){"
    ".pri{fill:#e6edf3}.sec{fill:#9198a1}.ter{fill:#656c76}.rule{stroke:#3d444d}}"
    "</style>"
)


def svg(w, h, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" fill="none" '
            f'text-rendering="geometricPrecision" role="img" aria-label="{label}">')
