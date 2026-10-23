# This 30–50 ns wild-type MM-GBSA output is pending regeneration

The wild-type (WT) MM-GBSA reference used for the alanine-scan ΔΔG values in the manuscript
(ΔG = −32.40 ± 1.73 kcal/mol, §4.5) was computed over the continued WT trajectory's **30–50 ns
window** (input trajectory `wt_30to50ns_200ps.xtc` — 100 frames at 200 ps, built by trjconv
with `-b 30000 -e 50000 -dt 200` from the continued WT run).

The dedicated output of that calculation (`mmpbsa_wt_30to50ns.dat`) is **not yet present** in
this repository because it is being regenerated on the compute host. The 0–24.8 ns WT output
(`mmpbsa_wt_100frames.dat`, ΔG = −38.06 ± 2.14, the primary-window value reported in §3.3) is
already deposited here.

Action required before submission: regenerate `mmpbsa_wt_30to50ns.dat` on the compute host and
commit it to this directory. After that, the manuscript's Data availability statement and §4.5
transparency note become fully consistent with the deposited artifacts.
