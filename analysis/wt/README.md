# Wild-type MM-GBSA artifacts

| File | Window | ΔTOTAL (kcal/mol) | Status |
|---|---|---|---|
| `mmpbsa_wt_100frames.dat` (= `analysis/md/mmpbsa_r3.dat`) | 0–24.8 ns, 100 frames | −38.06 ± 2.14 | deposited, verified |
| `mmpbsa_wt_30to50ns.dat` | 30–50 ns, 100 frames | −32.40 ± 1.73 (expected) | **missing — regeneration recipe below** |

The 30–50 ns value is the wild-type reference for every ΔΔG in the manuscript's §4.5. It was
computed on the compute host on 2026-10-20 (see `analysis/scan/mut_ddg_results.txt`, line 3)
but its output file was never pulled back. The input trajectory
(`wt_30to50ns_200ps.xtc`, 101 frames) is retained and SHA-256 verified in the author's
project directory, so the calculation is fully re-runnable.

**→ `REGENERATE_WT_30to50ns.md`** contains the verbatim original command line, the input
hashes, the ligand-topology rebuild step, and a mandatory control run that must reproduce
the archived 0–24.8 ns result (−38.06 ± 2.14) before the 30–50 ns number may be trusted.

Until that file exists, the manuscript carries a transparency note in §4.5 and the Data
availability statement names the value as pending deposition. Do not remove those notes
before the artifact is committed here.
