"""Verify the Sec. 3.1 site-assignment geometry: the 25 jujubogenin contact residues
versus the 13 classical benzodiazepine (BZ) contact residues.

Manuscript claim under test (Sec. 3.1):
  "This set shares no residue with the classical BZ set (alpha1 PHE100, HIS102,
   SER159, TYR160, VAL203, SER205, SER206, THR207, TYR210; gamma2 TYR58, ALA79,
   PHE77, THR142), and the two groups are also spatially separate: every one of the
   25 residues lies more than 12 A from the centroid of the BZ site (the mean Calpha
   position of those 13 residues; closest approach 14.8 A, gamma2 Asp192), and the
   closest residue-to-residue approach between the two sets is 11.0 A Calpha-Calpha
   (gamma2 Asp192 to gamma2 Tyr58)."

Both metrics are computed strictly WITHIN the deposited 6X3Z coordinates
(analysis/docking/structures/6X3Z.pdb), chains D = alpha1 and E = gamma2 (chain
assignment by signature residues: alpha1 = HIS102 + SER205, gamma2 = TYR58 + PHE77;
see analysis/docking/docking_results.md). The script also re-checks every residue
NAME in both lists against the deposited structure.

If the simulated alpha1/gamma2 dimer is present locally (data/wt_100ns/protein_dimer.pdb,
not deposited: it is coordinate-identical to 6X3Z chains D+E), the script additionally
reports the raw-coordinate Calpha RMSD between the two and repeats the metrics in the
dimer; the expected result is RMSD 0.000 A and identical distances.

An earlier version of this check mixed coordinates from the simulated dimer and the
crystal pentamer. That happens to be harmless here because the dimer IS the crystal
D+E chains (verified: 0.000 A over 671 common Calpha), but the mixing is not done in
this script.

Output (from the deposited coordinates alone):
  min CA-CA between the sets ........ 11.01 A  (gamma2 Asp192 <-> gamma2 Tyr58)
  min heavy-atom between the sets ...  5.44 A  (E192 N <-> E58 OH)
  min CA to BZ-site centroid ........ 14.75 A  (gamma2 Asp192)
  contacts within 12 A of a BZ residue: 2/25 (E192, E193); within 11 A: 0/25
  => "all 25 more than 12 A from the BZ-site centroid"  holds
  => "all 25 more than 11 A CA-CA from any BZ residue" holds
  => "all 25 more than 12 A CA-CA from any BZ residue" does NOT hold (this is why
     the manuscript states the metric explicitly)

Usage:  python3 verify_bz_separation.py
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PDB_CRYSTAL = os.path.join(HERE, "..", "docking", "structures", "6X3Z.pdb")
# optional local cross-check; not part of the repository
PDB_DIMER = os.path.join(HERE, "..", "..", "..", "data", "wt_100ns", "protein_dimer.pdb")

# --- residue sets exactly as listed in manuscript Sec. 3.1 ----------------------
CONTACT = (
    [("D", n) for n in (58, 140, 141, 142, 143, 144, 280, 281, 282)]
    + [("E", n) for n in (192, 193, 194, 195, 196, 197, 198, 199, 201, 202,
                          203, 204, 230, 232, 356, 357)]
)
BZ = (
    [("D", n) for n in (100, 102, 159, 160, 203, 205, 206, 207, 210)]
    + [("E", n) for n in (58, 79, 77, 142)]
)
CONTACT_NAMES = {
    ("D", 58): "MET", ("D", 140): "PRO", ("D", 141): "MET", ("D", 142): "HIS",
    ("D", 143): "LEU", ("D", 144): "GLU", ("D", 280): "VAL", ("D", 281): "ALA",
    ("D", 282): "TYR",
    ("E", 192): "ASP", ("E", 193): "THR", ("E", 194): "ARG", ("E", 195): "SER",
    ("E", 196): "TRP", ("E", 197): "ARG", ("E", 198): "LEU", ("E", 199): "TYR",
    ("E", 201): "PHE", ("E", 202): "SER", ("E", 203): "PHE", ("E", 204): "VAL",
    ("E", 230): "SER", ("E", 232): "ARG", ("E", 356): "TYR", ("E", 357): "LEU",
}
BZ_NAMES = {
    ("D", 100): "PHE", ("D", 102): "HIS", ("D", 159): "SER", ("D", 160): "TYR",
    ("D", 203): "VAL", ("D", 205): "SER", ("D", 206): "SER", ("D", 207): "THR",
    ("D", 210): "TYR",
    ("E", 58): "TYR", ("E", 79): "ALA", ("E", 77): "PHE", ("E", 142): "THR",
}


def parse_pdb(path):
    """Return {(chain, resseq): {'ca': (x,y,z) or None, 'heavy': [(name,x,y,z)],
    'resname': str}}. Insertion codes are ignored (first occurrence wins)."""
    residues = {}
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if line[:6] not in ("ATOM  ", "HETATM"):
                continue
            if line[16] not in (" ", "A"):
                continue
            name = line[12:16].strip()
            resname = line[17:20].strip()
            chain = line[21]
            try:
                resseq = int(line[22:26])
            except ValueError:
                continue
            try:
                xyz = (float(line[30:38]), float(line[38:46]), float(line[46:54]))
            except ValueError:
                continue
            elem = line[76:78].strip()
            d = residues.setdefault((chain, resseq),
                                    {"ca": None, "heavy": [], "resname": resname})
            if name == "CA" and d["ca"] is None:
                d["ca"] = xyz
            is_h = elem == "H" or (elem == "" and name.startswith("H"))
            if not is_h:
                d["heavy"].append((name,) + xyz)
    return residues


def dist(a, b):
    return math.sqrt(sum((a[t] - b[t]) ** 2 for t in range(3)))


def min_pairwise(ca, cb):
    best = (float("inf"), -1, -1)
    for i, a in enumerate(ca):
        for j, b in enumerate(cb):
            d = dist(a, b)
            if d < best[0]:
                best = (d, i, j)
    return best


def check_names(residues, expected, label):
    bad = [(k, w, residues.get(k, {}).get("resname")) for k, w in expected.items()
           if residues.get(k, {}).get("resname") != w]
    print(f"  residue-name check ({label}): {len(expected) - len(bad)}/{len(expected)}"
          + (f"  MISMATCH: {bad}" if bad else "  OK"))


def analyse(label, residues):
    print(f"\n===== {label} =====")
    ca_a = [(k, residues[k]["ca"]) for k in CONTACT
            if k in residues and residues[k]["ca"]]
    ca_b = [(k, residues[k]["ca"]) for k in BZ
            if k in residues and residues[k]["ca"]]
    print(f"  contact residues with CA: {len(ca_a)}/{len(CONTACT)}; "
          f"BZ residues with CA: {len(ca_b)}/{len(BZ)}")
    if len(ca_a) != len(CONTACT) or len(ca_b) != len(BZ):
        print("  -> residue set incomplete in this structure; aborting")
        return None

    d, i, j = min_pairwise([c for _, c in ca_a], [c for _, c in ca_b])
    print(f"M1  min CA-CA between the sets: {d:.2f} A  "
          f"({ca_a[i][0][0]}{ca_a[i][0][1]} <-> {ca_b[j][0][0]}{ca_b[j][0][1]})")

    heavy_a = [(k, a) for k in CONTACT for a in residues[k]["heavy"]]
    heavy_b = [(k, a) for k in BZ for a in residues[k]["heavy"]]
    d2, i2, j2 = min_pairwise([a[1:] for _, a in heavy_a], [b[1:] for _, b in heavy_b])
    print(f"M2  min heavy-atom distance:   {d2:.2f} A  "
          f"({heavy_a[i2][0][0]}{heavy_a[i2][0][1]} {heavy_a[i2][1][0]} <-> "
          f"{heavy_b[j2][0][0]}{heavy_b[j2][0][1]} {heavy_b[j2][1][0]})")

    cen = tuple(sum(c[t] for c in (x[1] for x in ca_b)) / len(ca_b) for t in range(3))
    best3 = min((dist(c, cen), k) for k, c in ca_a)
    print(f"M3  min CA distance to the BZ-site centroid (mean of {len(ca_b)} BZ CA): "
          f"{best3[0]:.2f} A at {best3[1][0]}{best3[1][1]}")

    per = sorted((min(dist(c, residues[kk]["ca"]) for kk in BZ), k) for k, c in ca_a)
    n12 = sum(1 for dm, _ in per if dm <= 12.0)
    n11 = sum(1 for dm, _ in per if dm <= 11.0)
    print(f"M4  closest five contact residues (CA-CA to the nearest BZ residue): "
          + ", ".join(f"{k[0]}{k[1]} {dm:.2f}" for dm, k in per[:5]))
    print(f"    within 12 A: {n12}/{len(per)};  within 11 A: {n11}/{len(per)}")
    print(f"    all 25 beyond 12 A of the BZ-site centroid: "
          f"{best3[0] > 12.0}")
    print(f"    all 25 beyond 11 A CA-CA from any BZ residue: {n11 == 0}")
    print(f"    all 25 beyond 12 A CA-CA from any BZ residue: {n12 == 0}")
    return per[0]


def main():
    if not os.path.exists(PDB_CRYSTAL):
        sys.exit(f"missing deposited structure: {PDB_CRYSTAL}")
    cry = parse_pdb(PDB_CRYSTAL)
    print(f"Loaded {os.path.relpath(PDB_CRYSTAL, HERE)}: "
          f"{len(cry)} residues, chains "
          + ", ".join(sorted({ch for ch, _ in cry})))

    print("\nResidue-name integrity check against the manuscript lists")
    check_names(cry, CONTACT_NAMES, "25 contact residues")
    check_names(cry, BZ_NAMES, "13 BZ residues")

    r = analyse("6X3Z crystal (chains D = alpha1, E = gamma2)", cry)

    if os.path.exists(PDB_DIMER):
        dim = parse_pdb(PDB_DIMER)
        common = [k for k in cry if k in dim and cry[k]["ca"] and dim[k]["ca"]]
        if common:
            ss = sum(dist(cry[k]["ca"], dim[k]["ca"]) ** 2 for k in common) / len(common)
            print(f"\nRaw-coordinate CA RMSD vs the local simulated dimer "
                  f"({len(common)} common CA): {math.sqrt(ss):.3f} A")
        analyse("simulated alpha1/gamma2 dimer (local cross-check)", dim)
    else:
        print("\n(local simulated dimer not present; skipped, metrics above use the "
              "deposited crystal coordinates only)")

    print("\n===== verdict =====")
    if r:
        print(f"  closest contact-BZ CA-CA separation = {r[0]:.2f} A at "
              f"{r[1][0]}{r[1][1]}; the manuscript states both metrics explicitly "
              f"because '>12 A' holds only for the site-centroid metric.")


if __name__ == "__main__":
    sys.exit(main())
