#!/usr/bin/env python3
"""Reproduce the six alanine-scan dG values from the deposited decomposition files.

Claim being verified (manuscript section 4.5 / Data availability):
    "The six mutant dG values in the table above are re-derivable from those
     deposits: each decomp_<mutant>.dat file carries a per-frame, per-residue
     decomposition (the DELTAS: section, 672 rows x 100 frames), and summing
     the TOTAL column within each frame and averaging over the 100 frames
     reproduces the tabulated value to within 1.06 kcal/mol (RMS 0.75,
     Pearson r = 0.9998); the recomputation is scripted as
     analysis/scan/verify_ddg_from_decomp.py."

File layout of allmode/decomp_<MUT>.dat (verified by header inspection):

    line 3        Complex:     67200 rows = 100 frames x 672 residues
                                per-residue COMPLEX energies
    line 67208    Receptor:    67100 rows = 100 frames x 671 residues
                                per-residue RECEPTOR energies
    line 134311   Ligand:         100 rows = 100 frames x 1 ligand
                                TDC of the ligand, NO free-energy offset
                                (Internal ~= 95.8, the ligand's bonded energy)
    line 134414   DELTAS:      67200 rows = 100 frames x 672 residues
                                per-residue BINDING contribution.
                                The ligand row carries Internal = 0.0, i.e. the
                                free-ligand energy is already subtracted.

Identity under test (single-trajectory MM-GBSA):

    sum over the DELTAS: section, per frame  ==  dG_bind for that frame

Usage:
    python3 verify_ddg_from_decomp.py [allmode_dir]

Expected output: a table of recomputed dG (mean, SD, SEM over 100 frames) beside
the values recorded in ../mut_ddg_results.txt, plus agreement statistics.

Caveat stated in the manuscript and reproduced here: the WILD-TYPE reference
dG = -32.40 +- 1.73 kcal/mol (30-50 ns window) is NOT re-derivable from any
deposited file; its dedicated MM-GBSA output was never pulled back from the
compute host and must be regenerated per ../wt/REGENERATE_WT_30to50ns.md.
The two replica ddG values (+21.78, +7.85) are likewise log-only.
"""
import math
import os
import re
import statistics as st
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DIR = os.path.join(HERE, "allmode")

ROW = re.compile(
    r"^(\d+),([RL]):([A-Z0-9]+):([A-Z0-9]{2,4}):(\d+),"
    r"(-?[\d.]+),(-?[\d.]+),(-?[\d.]+),(-?[\d.]+),(-?[\d.]+),(-?[\d.]+)\s*$"
)
SEC = re.compile(r"^(Complex|Receptor|Ligand|DELTAS):")

MUTS = ["D141A", "D81A", "E194A", "E198A", "E202A", "E29A"]
# values recorded in the archived pipeline log (mut_ddg_results.txt)
LOG = {"D141A": -24.08, "D81A": -12.70, "E194A": -2.95,
       "E198A": -4.90, "E202A": -14.82, "E29A": -15.41}
LOGSD = {"D141A": 4.29, "D81A": 3.46, "E194A": 2.61,
         "E198A": 9.78, "E202A": 0.95, "E29A": 1.73}


def recompute(path):
    """Sum the DELTAS: section per frame; return (mean, sd, sem, nframes)."""
    cur = None
    per_frame = {}
    with open(path) as f:
        for line in f:
            s = SEC.match(line)
            if s:
                cur = s.group(1)
                continue
            if cur != "DELTAS":
                continue
            g = ROW.match(line)
            if g:
                fr = int(g.group(1))
                per_frame[fr] = per_frame.get(fr, 0.0) + float(g.group(11))
    v = [per_frame[k] for k in sorted(per_frame)]
    return st.mean(v), st.stdev(v), st.stdev(v) / len(v) ** 0.5, len(v)


def main():
    d = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DIR
    print("=" * 88)
    print("dG_bind recomputed from the DELTAS: section of allmode/decomp_<MUT>.dat")
    print("=" * 88)
    print("%-7s %7s %11s %7s %7s %10s %8s %9s %7s"
          % ("mut", "frames", "recomputed", "SD", "SEM", "log value",
             "log SD", "residual", "z"))
    res = {}
    for m in MUTS:
        mean, sd, sem, n = recompute(os.path.join(d, "decomp_%s.dat" % m))
        resid = mean - LOG[m]
        z = resid / math.sqrt(sem ** 2 + (LOGSD[m] / 20.0) ** 2)
        res[m] = mean
        print("%-7s %7d %11.3f %7.3f %7.3f %10.2f %8.2f %+9.3f %+7.2f"
              % (m, n, mean, sd, sem, LOG[m], LOGSD[m], resid, z))

    print()
    print("=" * 88)
    print("AGREEMENT STATISTICS")
    print("=" * 88)
    rr = [res[m] - LOG[m] for m in MUTS]
    print("max |residual| = %.3f kcal/mol" % max(abs(x) for x in rr))
    print("RMS residual   = %.3f kcal/mol" % math.sqrt(sum(x * x for x in rr) / len(rr)))
    print("mean signed    = %+.3f kcal/mol" % st.mean(rr))
    mx, my = st.mean([res[m] for m in MUTS]), st.mean([LOG[m] for m in MUTS])
    r = (sum((res[m] - mx) * (LOG[m] - my) for m in MUTS)
         / math.sqrt(sum((res[m] - mx) ** 2 for m in MUTS)
                     * sum((LOG[m] - my) ** 2 for m in MUTS)))
    print("Pearson r      = %.6f (n = 6)" % r)
    print("ranking identical to log: %s"
          % ([m for m in sorted(MUTS, key=lambda k: res[k])]
             == [m for m in sorted(MUTS, key=lambda k: LOG[k])]))

    print()
    print("=" * 88)
    print("SENSITIVITY OF ddG TO THE (LOG-ONLY) WILD-TYPE REFERENCE")
    print("=" * 88)
    for label, wt in [("-32.40 (30-50 ns, log-only)", -32.40),
                      ("-38.06 (0-24.8 ns, artifact-backed)", -38.06)]:
        vals = {m: res[m] - wt for m in MUTS}
        print("  WT %-38s -> " % label
              + "  ".join("%s %+6.2f" % (m, vals[m]) for m in MUTS))
    print("  The reference enters every ddG as an additive constant, so the")
    print("  ranking and the signs are invariant to it.")


if __name__ == "__main__":
    main()
