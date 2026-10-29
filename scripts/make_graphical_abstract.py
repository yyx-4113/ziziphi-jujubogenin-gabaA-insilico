#!/usr/bin/env python3
"""Render the JMGM-mandatory Graphical Abstract at exactly 531 x 1328 px.

JMGM (Journal of Molecular Graphics and Modelling, Elsevier) requires a
Graphical Abstract of 531 x 1328 px. This script draws a single, honest
schematic summarising the paper's two-site finding:

  * flumazenil occupies the crystallographically defined benzodiazepine (BZ)
    site (validated by re-dock);
  * an exploratory search places jujubogenin in a distinct candidate cavity at
    the alpha1/gamma2 interface, 23.1 A from the BZ site, with 25 contacts that
    share none with the classical BZ set.

The interface model contains NO membrane, NO M4, NO beta2, and NO bound GABA;
every value is a computational prediction, not a measured affinity/efficacy.

Output:
  figures/GraphicalAbstract.png  (531 x 1328 px, opaque white background, RGB)
  figures/GraphicalAbstract.svg  (vector source)
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, FancyArrowPatch
import matplotlib.patheffects as pe
from PIL import Image
import os

HERE = os.path.dirname(os.path.abspath(__file__))
FIGDIR = os.path.join(os.path.dirname(HERE), "figures")
os.makedirs(FIGDIR, exist_ok=True)
PNG = os.path.join(FIGDIR, "GraphicalAbstract.png")
SVG = os.path.join(FIGDIR, "GraphicalAbstract.svg")

W, H = 531, 1328
RED = "#c0392b"      # flumazenil / BZ site
ORANGE = "#e67e22"   # jujubogenin / candidate cavity
INK = "#1a1a1a"
ACCENT = "#2c3e50"

fig = plt.figure(figsize=(W / 100.0, H / 100.0), dpi=100)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.axis("off")

def t(x, y, s, size=10, color=INK, weight="normal", style="normal", ha="center"):
    ax.text(x, y, s, fontsize=size, color=color, fontweight=weight,
            fontstyle=style, ha=ha, va="center", family="DejaVu Sans")

# ---- Title block ---------------------------------------------------------
t(265, 1300, r"Jujubogenin and the GABA$_A$ $\alpha$1/$\gamma$2 interface",
  size=13.5, weight="bold")
t(265, 1274, "a candidate allosteric cavity", size=14, weight="bold")
t(265, 1249, "(membrane-absent in silico model - no lipid bilayer)",
  size=9, style="italic", color="#555555")

# ---- Two-site schematic (symmetric about x = 265.5) ----------------------
cx_l, cx_r, cy = 138, 398, 1000
ax.add_patch(Circle((cx_l, cy), 100, fill=True, facecolor="#f5b7b1",
                    edgecolor=RED, linewidth=2.5))
t(cx_l, cy + 12, "BZ site", size=12, weight="bold", color=RED)
t(cx_l, cy - 18, "flumazenil", size=11, weight="bold")
ax.add_patch(FancyBboxPatch((cx_r - 100, cy - 100), 200, 200,
                            boxstyle="round,pad=0,rounding_size=24",
                            fill=True, facecolor="#fad7a0",
                            edgecolor=ORANGE, linewidth=2.5))
t(cx_r, cy + 34, r"$\alpha$1/$\gamma$2", size=12, weight="bold", color=ORANGE)
t(cx_r, cy + 12, "candidate cavity", size=11, weight="bold", color=ORANGE)
t(cx_r, cy - 16, "jujubogenin", size=11, weight="bold")
t(cx_l, 1148, "Benzodiazepine site", size=10.5, weight="bold")
t(cx_l, 1128, "(classical, 13 contacts)", size=8.5, color="#444444")
t(cx_r, 1148, "Candidate allosteric cavity", size=10.5, weight="bold")
t(cx_r, 1128, "(25 contacts, 0 shared with BZ)", size=8.5, color="#444444")
t(cx_l, 858, "Vina -7.09 kcal/mol", size=8.5, color="#444444")
t(cx_l, 838, "crystal-validated re-dock (6X3U)", size=8, color="#444444")
t(cx_r, 858, "Vina -8.32 kcal/mol", size=8.5, color="#444444")
t(cx_r, 838, "exploratory search", size=8, color="#444444")
# Distance arrow cleanly between the two shape edges + readable white-backed label
ax.add_patch(FancyArrowPatch((cx_l + 102, cy), (cx_r - 102, cy),
                            arrowstyle="-|>", mutation_scale=15,
                            linewidth=2, color=ACCENT))
ax.text(268, 1044, "23.1 \u00c5", fontsize=10, color=ACCENT,
        fontweight="bold", ha="center", va="center", family="DejaVu Sans",
        path_effects=[pe.withStroke(linewidth=2.6, foreground="white")])

t(265, 788, "25 cavity contacts; none shared with the classical BZ set",
  size=9.5, color="#333333")

# ---- Divider -------------------------------------------------------------
ax.plot([40, 491], [756, 756], color="#bbbbbb", linewidth=1)

# ---- Key findings --------------------------------------------------------
t(265, 716, "Key findings", size=12, weight="bold")
bullets = [
    "Jujubogenin does NOT preferentially occupy the BZ site",
    "Stable cavity pose: 24.8 ns (ligand RMSD 0.42 \u00b1 0.10 \u00c5)",
    "MM-GBSA \u0394G = -38.06 \u00b1 2.14 kcal/mol (no entropy term)",
    "25 cavity contacts; 0 overlap with the classical BZ set",
    "Site preference unestablished - cavity-targeted re-dock needed",
]
y = 676
for b in bullets:
    t(55, y, "- " + b, size=10, ha="left")
    y -= 52

# ---- Divider -------------------------------------------------------------
ax.plot([40, 491], [420, 420], color="#bbbbbb", linewidth=1)

# ---- Footer / honesty statement ------------------------------------------
t(265, 382, "In silico computational study - all values are predictions, not",
  size=9.5, color="#333333")
t(265, 342, "measured affinity, efficacy, or function.", size=9.5, color="#333333")
t(265, 302, "Membrane-absent model: \u03b1\u2013\u03b3 interface simulated in water;",
  size=9.5, color="#333333")
t(265, 262, "no lipid bilayer, no M4, no \u03b2 subunit, no bound GABA.",
  size=9.5, color="#333333")

fig.savefig(SVG, dpi=100, facecolor="white", pad_inches=0)
fig.savefig(PNG, dpi=100, facecolor="white", pad_inches=0)
im = Image.open(PNG).convert("RGBA")
bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
out = Image.alpha_composite(bg, im).convert("RGB")
out.save(PNG)
print("Wrote", PNG, out.size, out.mode)
print("Wrote", SVG)
