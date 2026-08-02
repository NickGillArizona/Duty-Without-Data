"""Shared SVG primitives for the committed figure generators.

This module carries the palette, guard, and SVG-fragment helpers that
scripts/make_fig1.py imports. Figures are plain SVG text assembled in
memory: pure standard library, no plotting dependencies, deterministic
output (no timestamps), so regenerated files diff clean when inputs are
unchanged. Guard checks abort with a nonzero exit if a source value
drifts from the value cited in the Note beyond rounding tolerance, so a
stale or regenerated artifact cannot silently change a published figure.

This module is a library; run `python scripts/make_fig1.py` to generate
the published Figure 1 pair.
"""
import os
import sys
from xml.sax.saxutils import escape

import config

FIGURES_DIR = os.path.join(config.RESULTS_DIR, "figures")

# GitHub Primer palette values so the figures read natively on github.com
# in both color modes. The README embeds each pair via <picture> with a
# prefers-color-scheme source.
PALETTES = {
    "light": {
        "text": "#1f2328",
        "muted": "#57606a",
        "grid": "#d0d7de",
        "axis": "#8c959f",
        "blue": "#0969da",
        "orange": "#bc4c00",
        "green": "#1a7f37",
        "purple": "#8250df",
        "on_series": "#ffffff",
    },
    "dark": {
        "text": "#e6edf3",
        "muted": "#8b949e",
        "grid": "#30363d",
        "axis": "#6e7681",
        "blue": "#58a6ff",
        "orange": "#f0883e",
        "green": "#3fb950",
        "purple": "#d2a8ff",
        "on_series": "#0d1117",
    },
}

FONT = "Helvetica, Arial, sans-serif"


def fail(msg):
    print(f"GUARD FAILURE: {msg}")
    sys.exit(1)


def guard(label, actual, expected, tol=0.1):
    """Abort if a source value drifts from the Note-cited value."""
    if abs(actual - expected) > tol:
        fail(f"{label}: source value {actual} != expected {expected} (tol {tol})")


def fmt1(x):
    return f"{x:.1f}"


def svg_open(w, h, title):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="{w}" height="{h}" role="img">\n'
        f"  <title>{title}</title>\n"
        f'  <g font-family="{FONT}">\n'
    )


SVG_CLOSE = "  </g>\n</svg>\n"


def text(x, y, s, size, fill, anchor="start", weight=None, style=None):
    w = f' font-weight="{weight}"' if weight else ""
    st = f' font-style="{style}"' if style else ""
    # Escape XML character data: a raw "<" (e.g. "p < 0.0001") makes the SVG
    # unparseable, and browsers refuse to render invalid SVG in <img>.
    return (
        f'    <text x="{x}" y="{y}" font-size="{size}" fill="{fill}" '
        f'text-anchor="{anchor}"{w}{st}>{escape(str(s))}</text>\n'
    )


def line(x1, y1, x2, y2, stroke, width=1, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'    <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{width}"{d}/>\n'


def rect(x, y, w, h, fill, rx=2):
    return f'    <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" rx="{rx}"/>\n'


def circle(cx, cy, r, fill):
    return f'    <circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>\n'


def polyline(points, stroke, width=2.5):
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    return f'    <polyline points="{pts}" fill="none" stroke="{stroke}" stroke-width="{width}"/>\n'
