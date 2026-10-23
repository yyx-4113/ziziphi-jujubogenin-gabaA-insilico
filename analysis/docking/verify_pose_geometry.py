#!/usr/bin/env python3
"""Reproduce the Figure 1 pose-geometry claims from the deposited files.

Claims verified (manuscript Fig. 1 legend and section 2.2):

    * flumazenil, redocked into the crystal-defined benzodiazepine (BZ) site,
      has its best pose centroid 7.5 A from the BZ-site centroid;
    * jujubogenin, docked into the same BZ box, has its best pose centroid
      11.4 A from the BZ-site centroid;
    * the jujubogenin cavity pose (exploratory box) lies 23.1 A from the
      BZ-site centroid, and the flumazenil exploratory-box pose 22.9 A.

Definitions used here, stated explicitly so the numbers can be re-derived:

    BZ-site centroid      = the AutoDock Vina grid centre of the
                            crystal-validated BZ box, parsed from the
                            "Grid center:" line of flum_BZ_log.txt.  That
                            grid centre was placed on the C-alpha centroid
                            of the 13 residues that contact flumazenil in
                            the 6X3U co-crystal (listed below); the two
                            points differ by 0.27 A, so the choice does not
                            change any reported distance at the quoted
                            precision.  NOTE: box_center.txt in this
                            directory records the *exploratory cavity* box
                            centre (97.518, 105.844, 123.021), which lies
                            21.3 A from the BZ centroid; that offset is the
                            mis-centred-box failure mode documented in the
                            manuscript, and is not the BZ reference.
    pose centroid         = unweighted centroid of ALL atoms (hydrogens
                            included) of the first (best-scoring) MODEL in
                            each pdbqt.  This is the definition that
                            reproduces the four distances quoted in the
                            Fig. 1 legend; using heavy atoms only shifts
                            them by up to 0.6 A (flumazenil BZ pose:
                            8.11 A instead of 7.49 A).

The 13 crystallographic BZ contact residues of 6X3U (chain D = alpha-1,
chain E = gamma-2; assignment confirmed by the alpha-1 signature HIS102 /
SER205 on chain D and the gamma-2 signature TYR58 / PHE77 on chain E, and by
the co-crystallised flumazenil itself):

    D 100, 102, 159, 160, 203, 205, 206, 207, 210   (9 residues)
    E  58,  77,  79, 142                            (4 residues)

Usage:
    python3 verify_pose_geometry.py [docking_dir]

No third-party imports are required; only the Python standard library.
"""
import os
import sys

BZ_RESIDUES = ([("D", s) for s in (100, 102, 159, 160, 203, 205, 206, 207, 210)]
               + [("E", s) for s in (58, 77, 79, 142)])

POSES = [
    ("flum_BZ.pdbqt", "flumazenil, BZ box (20 A)", 7.5),
    ("juju_BZ.pdbqt", "jujubogenin, BZ box (20 A)", 11.4),
    ("flumazenil_tight.pdbqt", "flumazenil, exploratory cavity box (22 A)", 22.9),
    ("jujubogenin_tight.pdbqt", "jujubogenin, exploratory cavity box (22 A)", 23.1),
]


def read_first_model(path):
    """All-atom coordinates of the first MODEL block of a pdbqt file."""
    pts, seen, in_model = [], False, False
    with open(path) as fh:
        for line in fh:
            if line.startswith("MODEL"):
                if seen:
                    break
                seen = True
                in_model = True
                continue
            if line.startswith("ENDMDL"):
                break
            if not in_model or not line.startswith(("ATOM", "HETATM")):
                continue
            try:
                x, y, z = float(line[30:38]), float(line[38:46]), float(line[46:54])
            except ValueError:
                continue
            pts.append((x, y, z))
    return pts


def centroid(pts):
    n = len(pts)
    return tuple(sum(p[i] for p in pts) / n for i in range(3))


def dist(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5


def bz_ca_centroid(pdb_path):
    """C-alpha centroid of the 13 BZ contact residues, in the 6X3Z frame."""
    want = set(BZ_RESIDUES)
    cas = []
    with open(pdb_path) as fh:
        for line in fh:
            if not line.startswith("ATOM"):
                continue
            ch, seq, name = line[21], line[22:26].strip(), line[12:16].strip()
            if name == "CA" and (ch, seq) in {(c, str(n)) for c, n in want}:
                cas.append((float(line[30:38]), float(line[38:46]), float(line[46:54])))
    return cas


def parse_grid_centre(log_path):
    """Read the 'Grid center: X .. Y .. Z ..' line of a Vina log."""
    with open(log_path) as fh:
        for line in fh:
            if line.lower().startswith("grid center"):
                parts = line.replace(":", " ").split()
                # 'Grid center X 81.46 Y 119.93 Z 120.91'
                vals = [float(parts[i + 1]) for i in (2, 4, 6)]
                return tuple(vals)
    raise ValueError("no 'Grid center:' line in %s" % log_path)


def main():
    d = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
    print("=" * 86)
    print("Figure 1 pose geometry, recomputed from the deposited docking files")
    print("=" * 86)

    box = parse_grid_centre(os.path.join(d, "flum_BZ_log.txt"))
    print("BZ grid centre (flum_BZ_log.txt)     : %s" % (tuple(round(v, 2) for v in box),))

    cav_file = os.path.join(d, "box_center.txt")
    if os.path.exists(cav_file):
        with open(cav_file) as fh:
            cav = tuple(float(x) for x in fh.read().split())
        print("exploratory box centre (box_center.txt): %s  (%.2f A from BZ centroid)"
              % (tuple(round(v, 2) for v in cav), dist(cav, box)))

    pdbz = os.path.join(d, "structures", "6X3Z.pdb")
    cas = bz_ca_centroid(pdbz) if os.path.exists(pdbz) else []
    ref = centroid(cas) if cas else box
    if cas:
        print("13-residue BZ C-alpha centroid (6X3Z): %s  (n=%d CA)"
              % (tuple(round(v, 2) for v in ref), len(cas)))
        print("  difference between the two references: %.2f A" % dist(ref, box))
    print()

    print("%-38s %10s %10s %10s   %s" % ("pose", "centroid", "to grid", "to CA13", "manuscript"))
    print("-" * 86)
    ok = True
    for fname, label, expected in POSES:
        path = os.path.join(d, fname)
        if not os.path.exists(path):
            print("%-38s  MISSING (%s)" % (label, fname))
            ok = False
            continue
        c = centroid(read_first_model(path))
        d_grid, d_ca = dist(c, box), dist(c, ref)
        flag = "OK" if abs(d_grid - expected) <= 0.15 else "MISMATCH"
        if flag != "OK":
            ok = False
        print("%-38s %10s %9.2f %9.2f   %6.2f  %s"
              % (label, tuple(round(v, 1) for v in c), d_grid, d_ca, expected, flag))
    print()
    print("distances in A; 'to grid' uses the Vina grid centre, 'to CA13' the")
    print("C-alpha centroid of the 13 crystallographic flumazenil contact residues.")
    print("pose centroid = unweighted mean of all atoms of the best-scoring pose.")
    print("VERDICT:", "all four Figure 1 distances reproduced" if ok else "DISCREPANCY FOUND")


if __name__ == "__main__":
    main()
