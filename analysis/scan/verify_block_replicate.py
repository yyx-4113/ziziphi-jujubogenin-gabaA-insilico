#!/usr/bin/env python3
"""Artifact-backed internal replicate for the alanine scan.

WHY THIS SCRIPT EXISTS
----------------------
The manuscript (section 4.5, Fig. 3) quotes two *independently seeded* replica
values (M141A, R194A).  Those two numbers are recorded only in the archived
pipeline log (analysis/scan/mut_ddg_replica_results.txt); no trajectory, no
FINAL_RESULTS_MMPBSA output and no decomposition file was ever retrieved from
the compute host for the rep2 runs, so they cannot be recomputed from the
deposits.  That limitation is disclosed in the manuscript.

What *can* be recomputed from the deposits is an INTERNAL replicate: every
mutant decomposition file carries a per-frame binding free energy (the
`DELTAS:` section, 672 rows x 100 frames; the per-frame TOTAL sum equals
dG_bind for that frame).  Splitting that 100-frame series into independent
blocks therefore gives a replica-like precision estimate that is fully
re-derivable from the deposited file, with no new simulation.

WHAT IS COMPUTED
----------------
For each of the six mutants:
  1. full-run dG (mean, sample SD, naive SEM)            -- reproduces Table row
  2. block-averaged SEM (Flyvbjerg-Petersen style)       -- honest SEM for a
     correlated MD time series; the naive SD/sqrt(n) underestimates it
  3. half-trajectory blocks (frames 1-50, 51-100): mean +- SEM, and the
     half-to-half difference  -- this is the artifact-backed internal replicate
  4. quarter-trajectory blocks (4 x 25 frames): range (max-min)

Because the wild-type reference enters ddG only as an additive constant, the
half-to-half and quarter-to-quarter differences reported here are IDENTICAL
for dG and for ddG, whatever reference is chosen; they are therefore immune to
the choice of the -38.06 (0-24.8 ns) or -32.40 (30-50 ns) window.

Usage:
    python3 verify_block_replicate.py [allmode_dir]

Caveat stated in the manuscript and reproduced here: an internal block
replicate measures agreement BETWEEN BLOCKS OF ONE TRAJECTORY.  It is not a
substitute for an independently seeded replica, which probes a different
trajectory and is expected to be (and is) far less reproducible.
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

MUTS = ["M141A", "M81A", "R194A", "L198A", "S202A", "V29A"]
# pipeline-log values, for cross-reference only
LOG = {"M141A": -24.08, "M81A": -12.70, "R194A": -2.95,
       "L198A": -4.90, "S202A": -14.82, "V29A": -15.41}
# independently seeded replica (rep2) dG, pipeline log only, NOT recomputable
REP2 = {"M141A": -10.62, "R194A": -24.55}
WT_REF = -38.06   # 0-24.8 ns, artifact-backed (analysis/wt/mmpbsa_wt_100frames.dat)


def per_frame_dg(path):
    """Sum the DELTAS: section per frame -> list of per-frame dG_bind."""
    cur = None
    acc = {}
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
                acc[fr] = acc.get(fr, 0.0) + float(g.group(11))
    return [acc[k] for k in sorted(acc)]


def block_sem(x, b):
    """Block-average SEM estimator: sqrt(var(block means) / nblocks)."""
    n = len(x)
    m = n // b
    if m < 2:
        return float("nan")
    y = [st.mean(x[i * b:(i + 1) * b]) for i in range(m)]
    return math.sqrt(st.variance(y) / m)


def main():
    d = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DIR

    print("=" * 96)
    print("1. FULL-RUN dG AND BLOCK-AVERAGED (CORRELATION-AWARE) SEM")
    print("   recomputed from the DELTAS: section of decomp_<MUT>.dat (100 frames each)")
    print("=" * 96)
    print("%-7s %10s %8s %9s %9s %11s %11s %11s %11s"
          % ("mut", "dG", "SD", "naiveSEM", "log dG", "SEM b=2", "SEM b=5",
             "SEM b=10", "SEM b=20"))
    series, full = {}, {}
    for m in MUTS:
        x = per_frame_dg(os.path.join(d, "decomp_%s.dat" % m))
        series[m] = x
        sd = st.stdev(x)
        sem = sd / math.sqrt(len(x))
        full[m] = (st.mean(x), sd, sem)
        print("%-7s %10.3f %8.3f %9.3f %9.2f %11.3f %11.3f %11.3f %11.3f"
              % (m, st.mean(x), sd, sem, LOG[m],
                 block_sem(x, 2), block_sem(x, 5),
                 block_sem(x, 10), block_sem(x, 20)))

    print()
    print("=" * 96)
    print("2. INTERNAL REPLICATE: HALF-TRAJECTORY BLOCKS (frames 1-50 vs 51-100)")
    print("   the wild-type reference cancels in the difference, so the")
    print("   half-to-half difference is identical for dG and for ddG")
    print("=" * 96)
    print("%-7s %12s %12s %12s %14s %12s"
          % ("mut", "1st half", "2nd half", "|diff|", "diff unc.", "ddG 1st/2nd"))
    half = {}
    for m in MUTS:
        x = series[m]
        h1, h2 = x[:50], x[50:]
        m1, m2 = st.mean(h1), st.mean(h2)
        s1 = st.stdev(h1) / math.sqrt(len(h1))
        s2 = st.stdev(h2) / math.sqrt(len(h2))
        diff = m2 - m1
        unc = math.sqrt(s1 ** 2 + s2 ** 2)
        half[m] = (m1, m2, diff, unc)
        print("%-7s %12.3f %12.3f %12.3f %14.3f  %+6.2f/%+6.2f"
              % (m, m1, m2, abs(diff), unc, m1 - WT_REF, m2 - WT_REF))

    dh = [abs(half[m][2]) for m in MUTS]
    print()
    print("half-to-half |difference| across the six mutants: "
          "min %.2f  median %.2f  max %.2f kcal/mol"
          % (min(dh), st.median(dh), max(dh)))

    print()
    print("=" * 96)
    print("3. QUARTER-TRAJECTORY BLOCKS (4 x 25 frames): spread within one run")
    print("=" * 96)
    print("%-7s %10s %10s %10s %10s %12s" % ("mut", "q1", "q2", "q3", "q4", "range"))
    for m in MUTS:
        x = series[m]
        q = [st.mean(x[i * 25:(i + 1) * 25]) for i in range(4)]
        print("%-7s %10.2f %10.2f %10.2f %10.2f %12.2f"
              % (m, q[0], q[1], q[2], q[3], max(q) - min(q)))

    print()
    print("=" * 96)
    print("4. COMPARISON WITH THE INDEPENDENTLY SEEDED REPLICA (log-only)")
    print("=" * 96)
    print("%-7s %11s %11s %13s %13s %10s"
          % ("mut", "rep1 dG", "rep2 dG", "replica |diff|", "half |diff|", "ratio"))
    for m in ("M141A", "R194A"):
        r1 = LOG[m]
        r2 = REP2[m]
        print("%-7s %11.2f %11.2f %13.2f %13.2f %10.1f"
              % (m, r1, r2, abs(r2 - r1), abs(half[m][2]),
                 abs(r2 - r1) / abs(half[m][2]) if half[m][2] else float("nan")))
    print()
    print("Interpretation guard: the two quantities are NOT interchangeable.")
    print("  * half/quarter blocks = agreement between parts of ONE trajectory")
    print("    (artifact-backed, re-derivable, this script)")
    print("  * rep1 vs rep2 = agreement between TWO independently seeded")
    print("    trajectories (pipeline log only, not re-derivable)")


if __name__ == "__main__":
    main()
