# Wild-type MM-GBSA artifacts

| File | Window | ΔTOTAL (kcal/mol) | Status |
|---|---|---|---|
| `mmpbsa_wt_100frames.dat` (= `analysis/md/mmpbsa_r3.dat`) | 0–24.8 ns, 100 frames | −38.06 ± 2.14 (per-frame SD 4.04) | deposited, verified |
| `mmpbsa_wt_matched_30to50ns.dat` | 30–50 ns, 100 frames | −32.40 ± 1.73 (per-frame SD 5.73) | **deposited, verified** |

Both wild-type windows are now backed by a retained gmx_MMPBSA output. The 0–24.8 ns value is the
binding-energy result of §3.3 and the reference for every ΔΔG in §4.5; the 30–50 ns value is
reported as a convergence and window-sensitivity check (a 5.66 kcal/mol window dependence).

**Where the 30–50 ns output came from.** It was recovered on 2026-10-24 from a local 5.0 GB tar
archive of the remote working tree (`zss_md_remote_20261023.tar`, packed 2026-10-23 12:04). Inside
the archive it sits at `_mmpbsa_r3/mmpbsa_wt_matched.dat` and is identified by its header: run
2026-10-20 07:57:57, structure file `/root/wt_rebuild/md_ref.tpr` (the reference used to cut the
30–50 ns subset), 100 complex frames, receptor mask `:1-671`, ligand mask `:672`. Its ΔTOTAL
(−32.40 ± 1.73) matches the archived pipeline log (`analysis/scan/mut_ddg_results.txt`: "WT
reference ΔG = -32.40 ± 1.73 kcal/mol (recomputed, matched 30-50ns window)") to both quoted
digits, mean and SD.

The input trajectory (`wt_30to50ns_200ps.xtc`, 100 extracted frames at 200 ps) is retained in the
author's project directory and SHA-256 verified, so the calculation remains fully re-runnable.

**→ `REGENERATE_WT_30to50ns.md`** still carries the verbatim original command line, the input
hashes, the ligand-topology rebuild step, and a control run that must reproduce the deposited
0–24.8 ns result (−38.06 ± 2.14). It is now an independent cross-check rather than the only route
to the number.
