#!/usr/bin/env python3
"""Recompute every binding free energy and every ddG in the manuscript from the
retained gmx_MMPBSA output files.

WHY THIS SCRIPT EXISTS
----------------------
Earlier rounds of this project recorded two quantities as "pipeline-log-only,
not re-derivable": (i) the wild-type 30-50 ns window value (-32.40 +- 1.73) and
(ii) the two independently seeded replica ddG values (D141A, E194A).  Both
verdicts were wrong.  The full remote working tree, including every
gmx_MMPBSA output file, had been packed into a local tar archive on 2026-10-23
(5.0 GB, 1022 members) that was not examined at the time.  Retrieving that
archive restored:

    analysis/wt/mmpbsa_wt_matched_30to50ns.dat   WT 30-50 ns window
    analysis/scan/rep1/mmpbsa_<MUT>.dat          all six first replicas
    analysis/scan/rep2/mmpbsa_<MUT>_rep2.dat     both second replicas

so that, as of this version, EVERY number in the alanine-scan table and in
Fig. 3 is backed by a retained output file and is recomputed by this script.

WHAT IS COMPUTED
----------------
    dG        :  DELTA TOTAL average, from the "Delta (Complex - Receptor -
                 Ligand)" block of each output
    SD(Prop.) :  the gmx_MMPBSA propagation-formula column (the uncertainty
                 quoted in the manuscript, see note below)
    ddG       =  dG(mutant) - dG(WT),  WT = 0-24.8 ns window = -38.06
    unc(ddG)  =  sqrt( SD(Prop.)_mutant^2 + SD(Prop.)_WT^2 )

NOTE ON THE UNCERTAINTY COLUMN
------------------------------
gmx_MMPBSA prints five columns for the delta block:
Average, SD(Prop.), SD, SEM(Prop.), SEM.  The manuscript quotes the SD(Prop.)
column (e.g. 4.29 for D141A) and propagates it; the plain "SD" column, the
sample standard deviation of the 100 per-frame binding energies, is larger
(7.03 for D141A, 6.45-12.00 across the six mutants) and is printed here as
well so that a reader can see which column was used.

Usage:
    python3 verify_all_dG_outputs.py [repo_analysis_dir]

Exit status is 0 only if every recomputed value matches the manuscript.
"""
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT = os.path.dirname(HERE)          # .../analysis

MUTS = ["D141A", "D81A", "E194A", "E198A", "E202A", "E29A"]

# ---- values printed in the manuscript (section 4.5 and Fig. 3) --------------
MANUSCRIPT = {
    "WT_0_24.8": (-38.06, 2.14),
    "WT_30_50": (-32.40, 1.73),
    "rep1": {"D141A": (-24.08, 4.29), "D81A": (-12.70, 3.46),
             "E194A": (-2.95, 2.61), "E198A": (-4.90, 9.78),
             "E202A": (-14.82, 0.95), "E29A": (-15.41, 1.73)},
    "rep2": {"D141A": (-10.62, 5.00), "E194A": (-24.55, 5.88)},
    "ddG": {"D141A": 13.98, "D81A": 25.36, "E194A": 35.11,
            "E198A": 33.16, "E202A": 23.24, "E29A": 22.65},
    "ddG_rep2": {"D141A": 27.44, "E194A": 13.51},
}

NUM = r"(-?\d+\.\d+)"
DELTA_TOTAL = re.compile(r"^ΔTOTAL\s+" + NUM + r"\s+" + NUM + r"\s+" + NUM)


def parse(path):
    """Return (dG, SD(Prop.), SD, nframes, 'Run on' line, structure file)."""
    dG = sdp = sd = None
    nframes = None
    run_on = struct = ""
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            if run_on == "" and line.startswith("| Run on"):
                run_on = line.strip("|\n").strip()
            if "Complex Structure file" in line and not struct:
                struct = line.split(":", 1)[1].strip()
            if nframes is None:
                g = re.search(r"Calculations performed using (\d+) complex frames", line)
                if g:
                    nframes = int(g.group(1))
            g = DELTA_TOTAL.match(line)
            if g:
                dG, sdp, sd = float(g.group(1)), float(g.group(2)), float(g.group(3))
    if dG is None:
        raise SystemExit("no DELTA TOTAL block found in %s" % path)
    return dG, sdp, sd, nframes, run_on, struct


def main():
    a = sys.argv[1] if len(sys.argv) > 1 else DEFAULT
    fails = []

    def chk(label, got, want, tol=0.006):
        ok = abs(got - want) <= tol
        if not ok:
            fails.append("%s: recomputed %.3f != manuscript %.3f" % (label, got, want))
        print("   %-42s %10.3f  (manuscript %8.2f)  %s"
              % (label, got, want, "OK" if ok else "MISMATCH"))

    print("=" * 92)
    print("WILD-TYPE REFERENCES  (both windows now backed by a retained output)")
    print("=" * 92)
    wt_ref, wt_sdp, wt_sd, n, run, st = parse(os.path.join(a, "wt", "mmpbsa_wt_100frames.dat"))
    print("  0-24.8 ns  %s" % os.path.join("wt", "mmpbsa_wt_100frames.dat"))
    print("             run %s | %d frames | structure %s" % (run, n, st))
    print("             per-frame sample SD = %.2f" % wt_sd)
    chk("dG(WT, 0-24.8 ns)", wt_ref, MANUSCRIPT["WT_0_24.8"][0])
    chk("SD(Prop.)", wt_sdp, MANUSCRIPT["WT_0_24.8"][1])

    wt2, wt2_sdp, wt2_sd, n2, run2, st2 = parse(
        os.path.join(a, "wt", "mmpbsa_wt_matched_30to50ns.dat"))
    print()
    print("  30-50 ns   %s" % os.path.join("wt", "mmpbsa_wt_matched_30to50ns.dat"))
    print("             run %s | %d frames | structure %s" % (run2, n2, st2))
    print("             per-frame sample SD = %.2f" % wt2_sd)
    chk("dG(WT, 30-50 ns)", wt2, MANUSCRIPT["WT_30_50"][0])
    chk("SD(Prop.)", wt2_sdp, MANUSCRIPT["WT_30_50"][1])
    print("  window dependence = %.2f kcal/mol (identity: shifts every ddG by "
          "the same amount)" % (wt2 - wt_ref))

    print()
    print("=" * 92)
    print("FIRST REPLICAS  (rep1, 20 ns each, 100 frames)")
    print("=" * 92)
    print("%-7s %10s %10s %10s %14s %12s" %
          ("mut", "dG", "SD(Prop.)", "SD", "ddG", "unc(ddG)"))
    rep1 = {}
    for m in MUTS:
        g, sdp, sd, nf, _, _ = parse(os.path.join(a, "scan", "rep1", "mmpbsa_%s.dat" % m))
        rep1[m] = (g, sdp, sd)
        ddg = g - wt_ref
        unc = math.sqrt(sdp ** 2 + wt_sdp ** 2)
        print("%-7s %10.2f %10.2f %10.2f %+14.2f %12.2f" % (m, g, sdp, sd, ddg, unc))
        chk("dG(%s)" % m, g, MANUSCRIPT["rep1"][m][0])
        chk("SD(Prop.)(%s)" % m, sdp, MANUSCRIPT["rep1"][m][1])
        chk("ddG(%s)" % m, ddg, MANUSCRIPT["ddG"][m], tol=0.02)

    print()
    print("=" * 92)
    print("INDEPENDENTLY SEEDED SECOND REPLICAS  (rep2, 20 ns each, 100 frames)")
    print("=" * 92)
    print("%-7s %10s %10s %10s %14s %12s %14s" %
          ("mut", "dG", "SD(Prop.)", "SD", "ddG", "unc(ddG)", "ddG - ddG(rep1)"))
    rep2 = {}
    for m in ("D141A", "E194A"):
        g, sdp, sd, nf, _, _ = parse(
            os.path.join(a, "scan", "rep2", "mmpbsa_%s_rep2.dat" % m))
        rep2[m] = (g, sdp, sd)
        ddg = g - wt_ref
        unc = math.sqrt(sdp ** 2 + wt_sdp ** 2)
        d1 = MANUSCRIPT["ddG"][m]
        print("%-7s %10.2f %10.2f %10.2f %+14.2f %12.2f %+14.2f"
              % (m, g, sdp, sd, ddg, unc, ddg - d1))
        chk("dG(%s rep2)" % m, g, MANUSCRIPT["rep2"][m][0])
        chk("SD(Prop.)(%s rep2)" % m, sdp, MANUSCRIPT["rep2"][m][1])
        chk("ddG(%s rep2)" % m, ddg, MANUSCRIPT["ddG_rep2"][m], tol=0.02)

    print()
    print("=" * 92)
    print("SENSITIVITY: the same table re-referenced to the 30-50 ns window")
    print("=" * 92)
    print("  (the wild-type reference enters ddG as an additive constant, so the")
    print("   ranking and every directional conclusion are unchanged)")
    for m in MUTS:
        print("   %-7s %+7.2f -> %+7.2f" % (m, rep1[m][0] - wt_ref, rep1[m][0] - wt2))

    print()
    print("=" * 92)
    if fails:
        print("FAILED (%d):" % len(fails))
        for f in fails:
            print("  -", f)
        sys.exit(1)
    print("ALL CHECKS PASSED")
    print("Every dG, every ddG, both wild-type windows and both independently")
    print("seeded replicas are recomputed here from retained gmx_MMPBSA output")
    print("files.  No value in section 4.5 or Fig. 3 depends on a pipeline log.")
    print("=" * 92)


if __name__ == "__main__":
    main()
