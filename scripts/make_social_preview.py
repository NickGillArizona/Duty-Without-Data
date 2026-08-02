"""Generate the repository social-preview card (PNG + SVG source).

A restrained typographic card: the Note's title, subtitle, author, and
publication status on a solid ivory background — no statistics, no
slogans, no imagery. GitHub's recommended canvas is 1280 x 640 under
1 MB, uploaded manually at Settings -> Social preview; the committed
files record the design so the upload is reproducible.

Outputs (assets/):
  social-preview.png
  social-preview-source.svg

Usage: python scripts/make_social_preview.py
"""
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(REPO_ROOT, "assets")

W, H, DPI = 1280, 640, 100

IVORY = "#faf8f3"
NAVY = "#1f3a5f"
INK = "#3a3f45"
MUTED = "#62666d"
RUST = "#9a4f35"

SERIF = ["Georgia", "Times New Roman", "serif"]
SANS = ["Segoe UI", "Arial", "sans-serif"]


def build(fig):
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    fig.patch.set_facecolor(IVORY)

    x = 92
    ax.text(x, 418, "DUTY WITHOUT DATA", fontsize=46, color=NAVY,
            fontfamily=SERIF, fontweight="bold", va="baseline")
    ax.text(x, 352, "Disability Fair Housing and the Record-Dependent Right",
            fontsize=23, color=NAVY, fontfamily=SERIF, fontstyle="italic",
            va="baseline")
    ax.plot([x, x + 620], [305, 305], color=RUST, linewidth=2.2,
            solid_capstyle="butt")
    ax.text(x, 246, "Nicholas Gill · Forthcoming, Arizona Law Review (2026)",
            fontsize=17, color=INK, fontfamily=SANS, va="baseline")
    ax.text(x, 108, "Legal argument · evidence · replication",
            fontsize=14, color=MUTED, fontfamily=SANS, va="baseline")


def main():
    os.makedirs(ASSETS_DIR, exist_ok=True)
    for name, meta in (
        ("social-preview.png", None),
        ("social-preview-source.svg", {"Date": None}),
    ):
        fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI)
        build(fig)
        out = os.path.join(ASSETS_DIR, name)
        kwargs = {"facecolor": IVORY}
        if meta is not None:
            kwargs["metadata"] = meta
        fig.savefig(out, **kwargs)
        plt.close(fig)
        print(f"wrote assets/{name}")


if __name__ == "__main__":
    main()
