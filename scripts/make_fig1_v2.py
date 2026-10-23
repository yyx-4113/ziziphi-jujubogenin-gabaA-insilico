#!/usr/bin/env python3
# Figure 1 v3 — (a) overview with 23.1 A separation, (b) BZ-site zoom (flumazenil,
# MODEL 1 only), (c) cavity zoom (jujubogenin). True zoom via explicit axis limits.
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = r"D:/2026.10/中药睡眠障碍脑肠轴"
FIGDIR = os.path.join(ROOT, "submission", "figures")
DOCK = os.path.join(ROOT, "docking")
MD = os.path.join(DOCK, "md_autodl")

def parse_ca(path, chains=("D", "E")):
    out = {}
    for line in open(path):
        if line.startswith("ATOM") and len(line) > 54:
            ch = line[21]
            if ch in chains and line[12:16].strip() == "CA":
                out.setdefault(ch, []).append(
                    (float(line[30:38]), float(line[38:46]), float(line[46:54])))
    return {k: np.array(v) for k, v in out.items()}

def parse_ligand_best_pose(path):
    """Parse ONLY the first (best) Vina MODEL from a pdbqt; single-pose pdb also fine."""
    lines = open(path).readlines()
    if not any(l.startswith("MODEL") for l in lines):
        # plain PDB, single pose
        return np.array([(float(l[30:38]), float(l[38:46]), float(l[46:54]))
                         for l in lines
                         if l.startswith(("ATOM", "HETATM")) and len(l) > 54], dtype=float)
    pts, in_first, seen_model = [], False, False
    for line in lines:
        if line.startswith("MODEL"):
            if seen_model:
                break          # second model -> stop
            seen_model = True
            in_first = True
            continue
        if line.startswith("ENDMDL"):
            break
        if in_first and line.startswith(("ATOM", "HETATM")) and len(line) > 54:
            pts.append((float(line[30:38]), float(line[38:46]), float(line[46:54])))
    return np.array(pts, dtype=float)

ca = parse_ca(os.path.join(MD, "protein_dimer.pdb"))
D, E = ca["D"], ca["E"]
flum = parse_ligand_best_pose(os.path.join(DOCK, "flum_BZ.pdbqt"))
juju = parse_ligand_best_pose(os.path.join(MD, "ligand_pose.pdb"))
print(f"flumazenil atoms (MODEL 1): {len(flum)}; jujubogenin atoms: {len(juju)}")
BZ = np.array([81.46, 119.93, 120.91])
CAV = juju.mean(axis=0)
dist = float(np.linalg.norm(CAV - BZ))
flum_c = flum.mean(axis=0)
print(f"flumazenil MODEL-1 centroid -> BZ centroid: {np.linalg.norm(flum_c - BZ):.2f} A")
print(f"cavity centroid -> BZ centroid: {dist:.2f} A")

AZ, EL = 49.0, 16.0
ZOOM_R = 16.0   # half-width of zoom panels (A)

def style_axis(ax, title, center, r=ZOOM_R):
    ax.set_xlim(center[0] - r, center[0] + r)
    ax.set_ylim(center[1] - r, center[1] + r)
    ax.set_zlim(center[2] - r, center[2] + r)
    ax.set_title(title, fontsize=10, pad=2)
    ax.set_xlabel("x (Å)", fontsize=7, labelpad=-4)
    ax.set_ylabel("y (Å)", fontsize=7, labelpad=-4)
    ax.set_zlabel("z (Å)", fontsize=7, labelpad=-4)
    ax.tick_params(labelsize=6, pad=-2)
    ax.view_init(elev=EL, azim=AZ)
    ax.set_box_aspect((1, 1, 1))

fig = plt.figure(figsize=(15, 5.6), constrained_layout=True)

# ---- (a) overview ---------------------------------------------------------
ax = fig.add_subplot(1, 3, 1, projection="3d")
ax.view_init(elev=EL, azim=AZ)
ax.scatter(D[:, 0], D[:, 1], D[:, 2], s=6, c="#4C72B0", alpha=0.45,
           label=r"$\alpha$1 (chain D)")
ax.scatter(E[:, 0], E[:, 1], E[:, 2], s=6, c="#55A868", alpha=0.45,
           label=r"$\gamma$2 (chain E)")
ax.scatter(flum[:, 0], flum[:, 1], flum[:, 2], s=26, c="#C44E52",
           edgecolor="k", linewidth=0.2, label="Flumazenil (BZ site)")
ax.scatter(juju[:, 0], juju[:, 1], juju[:, 2], s=26, c="#DD8452", marker="^",
           edgecolor="k", linewidth=0.2, label="Jujubogenin (cavity)")
ax.scatter(*BZ, s=110, c="red", marker="x", linewidths=2.2)
ax.scatter(*CAV, s=110, c="green", marker="x", linewidths=2.2)
ax.plot([BZ[0], CAV[0]], [BZ[1], CAV[1]], [BZ[2], CAV[2]], c="k", ls="--", lw=1.4)
mid = 0.5 * (BZ + CAV)
ax.text(mid[0], mid[1], mid[2] - 10, f"{dist:.1f} Å", fontsize=13, ha="center",
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="gray", alpha=0.9))
ax.text(BZ[0], BZ[1], BZ[2] + 11, "BZ site", fontsize=10, ha="center", color="red",
        fontweight="bold")
ax.text(CAV[0], CAV[1], CAV[2] + 11, "cavity", fontsize=10, ha="center",
        color="green", fontweight="bold")
ax.set_title("(a) Overview: two distinct sites", fontsize=11, pad=2)
ax.set_xlabel("x (Å)", fontsize=7, labelpad=-4)
ax.set_ylabel("y (Å)", fontsize=7, labelpad=-4)
ax.set_zlabel("z (Å)", fontsize=7, labelpad=-4)
ax.tick_params(labelsize=6, pad=-2)
ax.legend(fontsize=7, loc="upper left", framealpha=0.9)

# ---- (b) BZ-site zoom -----------------------------------------------------
ax = fig.add_subplot(1, 3, 2, projection="3d")
mD = np.linalg.norm(D - BZ, axis=1) < ZOOM_R
mE = np.linalg.norm(E - BZ, axis=1) < ZOOM_R
ax.scatter(D[mD, 0], D[mD, 1], D[mD, 2], s=16, c="#4C72B0", alpha=0.6)
ax.scatter(E[mE, 0], E[mE, 1], E[mE, 2], s=16, c="#55A868", alpha=0.6)
ax.scatter(flum[:, 0], flum[:, 1], flum[:, 2], s=60, c="#C44E52",
           edgecolor="k", linewidth=0.4, depthshade=False)
ax.scatter(*flum_c, s=140, c="red", marker="x", linewidths=2.4)
for (ch, num, lab, off) in [("D", 102, "α1 HIS102", (0, 0, -5.5)),
                            ("D", 205, "α1 SER205", (0, -6.5, 1.5)),
                            ("D", 203, "α1 VAL203", (0, 6.5, 1.5)),
                            ("E", 58, "γ2 TYR58", (0, -5.0, 5.0)),
                            ("E", 77, "γ2 PHE77", (0, 5.0, -4.0))]:
    pts = D if ch == "D" else E
    idx = num - (10 if ch == "D" else 25)
    p = pts[idx]
    ax.text(p[0] + off[0], p[1] + off[1], p[2] + off[2], lab, fontsize=7,
            ha="center", color="darkred", fontweight="bold")
style_axis(ax, "(b) Benzodiazepine site:\nflumazenil redock (−7.086 kcal/mol)", BZ)

# ---- (c) cavity zoom ------------------------------------------------------
ax = fig.add_subplot(1, 3, 3, projection="3d")
mD = np.linalg.norm(D - CAV, axis=1) < ZOOM_R
mE = np.linalg.norm(E - CAV, axis=1) < ZOOM_R
ax.scatter(D[mD, 0], D[mD, 1], D[mD, 2], s=16, c="#4C72B0", alpha=0.6)
ax.scatter(E[mE, 0], E[mE, 1], E[mE, 2], s=16, c="#55A868", alpha=0.6)
ax.scatter(juju[:, 0], juju[:, 1], juju[:, 2], s=60, c="#DD8452", marker="^",
           edgecolor="k", linewidth=0.4, depthshade=False)
ax.scatter(*CAV, s=140, c="green", marker="x", linewidths=2.4)
for (ch, num, lab, off) in [("D", 141, "α1 MET141", (0, 0, -5.5)),
                            ("E", 194, "γ2 ARG194", (0, -6.0, 2.5)),
                            ("E", 198, "γ2 LEU198", (0, 6.0, 2.5)),
                            ("E", 202, "γ2 SER202", (0, 2.0, 7.0))]:
    pts = D if ch == "D" else E
    idx = num - (10 if ch == "D" else 25)
    p = pts[idx]
    ax.text(p[0] + off[0], p[1] + off[1], p[2] + off[2], lab, fontsize=7,
            ha="center", color="darkgreen", fontweight="bold")
style_axis(ax, "(c) Candidate allosteric cavity:\njujubogenin docked pose (−8.324 kcal/mol)", CAV)

fig.savefig(os.path.join(FIGDIR, "Fig1_poses.png"), dpi=300)
fig.savefig(os.path.join(FIGDIR, "Fig1_poses.svg"))
plt.close(fig)
print("Fig1 v3 done.")
