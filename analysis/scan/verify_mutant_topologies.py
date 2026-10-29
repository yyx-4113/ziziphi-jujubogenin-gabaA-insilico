#!/usr/bin/env python3
"""Verify the in-silico mutant construction from the deposited starting coordinates.

§4.5 discloses that the tleap topology-build step returned a non-zero exit code
(exit = 1) for 5 of the 6 in-silico mutants, and justifies treating that as a
build warning rather than a failed substitution by an atom-count identity:

    receptor_atoms(mutant) == receptor_atoms(WT) - atom_difference(substitution)

This script checks that identity from the deposited files instead of from the
pipeline log, and cross-checks it two independent ways:

  1. rep1/complex_<MUT>.gro   -> total complex atoms (header line 2)
  2. mut_ddg_results.txt      -> "[<MUT>] index groups: receptor=NNNNN ligand=82"

Both must agree, and both must reproduce the substitution differences quoted in
the manuscript (MET->ALA 7, ARG->ALA 14, LEU->ALA 9, SER->ALA 1, VAL->ALA 6).

Exit code 0 = every check passed.
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))

WT_RECEPTOR = 10907          # gmx make_ndx "Group 1 (Protein)" on the WT tpr
LIGAND = 82                  # jujubogenin, JUB_GMX.gro

# name -> (substituted residue, expected atom difference WT - mutant)
MUTANTS = {
    "M141A": ("MET", 7),
    "M81A": ("MET", 7),
    "R194A": ("ARG", 14),
    "L198A": ("LEU", 9),
    "S202A": ("SER", 1),
    "V29A": ("VAL", 6),
}

fails = []


def chk(label, ok, detail=""):
    print("  %-58s %s   %s" % (label, "PASS" if ok else "FAIL", detail))
    if not ok:
        fails.append(label)


def gro_natoms(path):
    """Atom count from a .gro header (line 1 title, line 2 count)."""
    with io.open(path, encoding="utf-8", errors="replace") as fh:
        fh.readline()
        return int(fh.readline().split()[0])


def main():
    print("Mutant construction check — deposited starting coordinates\n")

    # --- index-group record (mut_ddg_results.txt) -----------------------------
    src = os.path.join(REPO, "analysis", "scan", "mut_ddg_results.txt")
    if not os.path.isfile(src):
        print("MISSING", src)
        return 1
    txt = io.open(src, encoding="utf-8", errors="replace").read()
    rec = {}
    for m in re.finditer(r"\[(\w+)\] index groups: receptor=(\d+) ligand=(\d+)", txt):
        rec[m.group(1)] = (int(m.group(2)), int(m.group(3)))
    chk("index-group record lists all six mutants", len(rec) == 6, "%d found" % len(rec))

    print("\n%-8s %-6s %-12s %-12s %-12s %-10s" %
          ("mutant", "sub", "receptor", "WT - mut", "expected", "complex"))
    for mu in sorted(MUTANTS):
        sub, diff = MUTANTS[mu]
        gro = os.path.join(HERE, "rep1", "complex_%s.gro" % mu)
        if not os.path.isfile(gro):
            chk("complex_%s.gro deposited" % mu, False)
            continue
        n_gro = gro_natoms(gro)

        if mu not in rec:
            chk("%s index record" % mu, False)
            continue
        n_rec, n_lig = rec[mu]

        # way 1: receptor from the index record vs WT minus substitution delta
        chk("%s receptor == WT - delta(%s->ALA)" % (mu, sub),
            WT_RECEPTOR - n_rec == diff,
            "%d - %d = %d (expected %d)" % (WT_RECEPTOR, n_rec, WT_RECEPTOR - n_rec, diff))

        # way 2: complex.gro atoms == receptor + ligand
        chk("%s complex.gro == receptor + ligand" % mu,
            n_gro == n_rec + n_lig,
            "%d == %d + %d" % (n_gro, n_rec, n_lig))

        chk("%s ligand is jujubogenin (82 atoms)" % mu, n_lig == LIGAND, str(n_lig))
        print("%-8s %-6s %-12d %-12d %-12d %-10d" %
              (mu, sub, n_rec, WT_RECEPTOR - n_rec, diff, n_gro))

    print()
    # --- the two MET->ALA mutants must be identical in atom count -------------
    if "M141A" in rec and "M81A" in rec:
        chk("both MET->ALA mutants share the same receptor count",
            rec["M141A"][0] == rec["M81A"][0],
            "%d vs %d" % (rec["M141A"][0], rec["M81A"][0]))

    print("\n%d checks failed" % len(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
