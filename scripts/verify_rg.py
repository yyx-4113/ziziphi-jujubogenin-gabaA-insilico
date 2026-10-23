#!/usr/bin/env python3
"""Recompute the protein-alone radius of gyration from the retained
post-equilibration structure (npt.gro).

Motivation: the rg_nm column of rmsd_final.csv is a solvent-inclusive
quantity (all atoms of the system, protein + 203,406 water atoms + ions);
it is dominated by the solvent box and is NOT a measure of receptor
compactness. This script recovers the receptor's own radius of gyration
from the retained structure after periodic-boundary reassembly.

Usage:
    python verify_rg.py [path/to/npt.gro]

Requires: numpy only. Verified with Python 3.13 / numpy 2.x.
"""
import sys
import numpy as np

DEFAULT = r"D:/2026.10/中药睡眠障碍脑肠轴/docking/md_autodl/zss_md_results/npt.gro"

# Block layout of npt.gro (214,802 atoms), verified against the file:
#   atoms 0 .. 5458       chain D (alpha1, residues 10-347, 5,459 atoms incl. H)
#   atoms 5459 .. 10906   chain E (gamma2, residues 25-357, 5,448 atoms incl. H)
#   atoms 10907 .. 10988  ligand UB1 (82 atoms)
#   atoms 10989 .. 214394 water (67,802 molecules x 3 atoms)
#   atoms 214395 .. 214801 ions (198 Na+, 209 Cl-)
BLOCKS = {
    "chainD": (0, 5459),
    "chainE": (5459, 10907),
    "ligand": (10907, 10989),
    "water": (10989, 214395),
    "ions": (214395, 214802),
}


def read_gro(path):
    lines = open(path).read().splitlines()
    natom = int(lines[1])
    bv = [float(x) for x in lines[-1].split()]
    # GRO box line: v1x v2y v3z v1y v1z v2x v2z v3x v3y
    v1 = np.array([bv[0], bv[3], bv[4]])
    v2 = np.array([bv[5], bv[1], bv[6]])
    v3 = np.array([bv[7], bv[8], bv[2]])
    M = np.array([v1, v2, v3]).T          # columns are the box vectors
    xyz = []
    for line in lines[2:-1]:
        if len(line) < 45:
            continue
        xyz.append([float(line[20:28]), float(line[28:36]), float(line[36:44])])
    X = np.array(xyz)
    assert len(X) == natom, f"parsed {len(X)} atoms, header says {natom}"
    return X, M


def unwrap(P, Minv, M):
    """Sequential minimum-image reassembly of a contiguous atom block.

    Valid because consecutive atoms in a GROMACS coordinate file are bonded
    (or within the same residue), so every step is far below half the box.
    """
    P = P.copy()
    for i in range(1, len(P)):
        d = P[i] - P[i - 1]
        f = Minv @ d
        f = f - np.round(f)
        P[i] = P[i - 1] + M @ f
    return P


def radius_of_gyration(P):
    c = P.mean(axis=0)
    return float(np.sqrt(((P - c) ** 2).sum(axis=1).mean()))


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT
    X, M = read_gro(path)
    Minv = np.linalg.inv(M)

    # Reassemble the whole protein as ONE contiguous sequence. The D/E
    # junction consists of non-bonded interface atoms less than 1 nm apart,
    # so the minimum-image step across the junction places the two subunits
    # in their true relative position. Unwrapping the chains separately
    # would leave their relative periodic image undetermined.
    protein = unwrap(X[0:BLOCKS["chainE"][1]], Minv, M)
    nD = BLOCKS["chainD"][1] - BLOCKS["chainD"][0]
    D = protein[:nD]
    E = protein[nD:]
    P = protein

    print(f"file: {path}")
    print(f"box volume: {abs(np.linalg.det(M)):.1f} nm^3")
    print(f"Rg chain D (alpha1)   = {radius_of_gyration(D):.4f} nm")
    print(f"Rg chain E (gamma2)   = {radius_of_gyration(E):.4f} nm")
    print(f"Rg protein (D + E)    = {radius_of_gyration(P):.4f} nm")
    print(f"chain centroid distance = "
          f"{np.linalg.norm(D.mean(axis=0) - E.mean(axis=0)):.3f} nm")
    print()
    print("Reference: rmsd_final.csv rg_nm = 6.6118 +/- 0.0038 nm, which is a")
    print("solvent-inclusive system quantity and cannot be the protein value above.")


if __name__ == "__main__":
    main()
