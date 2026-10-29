# ziziphi-jujubogenin-gabaA-insilico

**Reproducibility package for:** "Jujubogenin does not preferentially engage the GABA_A benzodiazepine site: an in silico study of a candidate allosteric cavity at the α1/γ2 interface (membrane-absent model)" (single-author, purely computational study).

**Author:** Yongxin Yang — Department of Anesthesiology, The Second Affiliated Hospital of Fujian University of Traditional Chinese Medicine, Fuzhou, Fujian 350003, China. ORCID 0009-0004-9698-6552.

## What this repository contains

This is a **computational-only** study. No animals, humans, tissues, or wet-lab measurements were used. The repository provides the full analysis code, input structures, and all derived products needed to reproduce every reported number. Raw all-atom MD trajectories are >1.5 GB, above the per-file size limit of the hosting platform, so they are not deposited here; the deposited code and derived products are sufficient to reproduce all reported values without the raw trajectories. A frozen copy of this repository is archived at Zenodo: 10.5281/zenodo.23602221 (https://doi.org/10.5281/zenodo.23602221).

```
analysis/
  docking/   four Vina logs (juju_BZ, flum_BZ, jujubogenin_tight, flumazenil_tight),
             the four best poses as pdbqt, docking_results.md, box_center.txt,
             structures/ (6X3Z.pdb, 6X3U.pdb, rec_ok.pdbqt),
             verify_pose_geometry.py (reproduces the Fig. 1 pose-geometry distances)
  md/        MD metrics (rmsd_final.csv/json), MM-GBSA (mmpbsa_r3.dat), interaction energies (interaction_energy_summary.json, contact_residue_energy.json), post-equilibration structure (npt.gro)
  scan/      alanine-scan ΔΔG tables (mut_ddg_results.txt, mut_ddg_replica_results.txt), post_summary.txt, diag_summary.json,
             cross-map matrices (crossmap_*.csv),
             allmode/decomp_<MUT>.dat  (6 × 9.6 MB, complete per-residue MM-GBSA decompositions,
                                        100 frames × 672 residues × 4 sections),
             rep1/mmpbsa_<MUT>.dat     (6 × gmx_MMPBSA output, the six first-replica ΔG),
             rep1/complex_<MUT>.gro    (6 × starting coordinates as built by tleap,
                                        unsolvated complex; underpins the §4.5
                                        build-warning note),
             rep2/mmpbsa_<MUT>_rep2.dat + gmx_MMPBSA_<MUT>_rep2.log
                                       (2 × independently seeded second replicas, M141A and R194A),
             verify_all_dG_outputs.py  (recomputes EVERY ΔG and ΔΔG of §4.5 / Fig. 3 from
                                        wt/, rep1/ and rep2/ — the single entry point),
             verify_mutant_topologies.py (checks the §4.5 atom-count identity from
                                        rep1/complex_<MUT>.gro and mut_ddg_results.txt),
             verify_ddg_from_decomp.py (reproduces the six ΔG values from allmode/),
             verify_block_replicate.py (auxiliary: half- and quarter-trajectory block
                                        agreement within each deposited run),
             verify_bz_separation.py (reproduces the §3.1 contact-set / BZ-set separation
                                     geometry from structures/6X3Z.pdb: 11.0 Å closest Cα–Cα,
                                     all 25 contacts beyond 12 Å of the BZ-site centroid)
  wt/        0–24.8 ns wild-type MM-GBSA output (mmpbsa_wt_100frames.dat), the 30–50 ns output
             (mmpbsa_wt_matched_30to50ns.dat), the recovered 0–24.8 ns output text
             (WT_MMGBSA_OUTPUT_0to24.8ns.txt), and the 30–50 ns regeneration recipe; see wt/README.md
figures/     Fig. 1–3 (PNG + SVG) and their generation scripts
scripts/     md2docx.py (manuscript → DOCX), verify_rg.py (protein radius of gyration), figure-generation scripts
manuscript/  manuscript_ZSS_insilico_v3.0.md (source), manuscript.md (submission copy), manuscript.docx (rendered)
```

## How to reproduce

1. **Docking** (AutoDock Vina 1.2.7): see `analysis/docking/` logs. The BZ-corrected box is centred on [81.46, 119.93, 120.91] (20 Å); the exploratory mis-centred box is centred on [97.518, 105.844, 123.021] (22 Å).
2. **MD** (GROMACS 2024.5, amber99sb-ildn, GAFF2/AM1-BCC ligand): `analysis/md/` holds the derived metrics; `verify_rg.py` recomputes the protein-alone radius of gyration from `npt.gro` (3.46 nm). The 3.46 nm is the receptor's own radius of gyration, recovered from the retained post-equilibration structure `npt.gro` after minimum-image reassembly (see `scripts/verify_rg.py`); the trajectory's `rg_nm` column is solvent-inclusive (~6.6 nm) and the naive un-imaged protein Rg is ~8.1 nm, so periodic-boundary reassembly is mandatory. To recompute from the trajectory: `gmx trjconv -pbc whole -center` then `gmx gyrate` on the protein-only index group.
3. **MM-GBSA** (gmx_MMPBSA 1.6.5, igb=5, saltcon 0.150 M, 100 frames, no entropy term) and **energy-group** interaction energies: `analysis/md/`.
4. **Alanine scan** (six 20 ns mutant re-simulations plus two independently seeded second
   replicas, M141A and R194A): `analysis/scan/`. Run
   `python3 analysis/scan/verify_all_dG_outputs.py`, which reads the retained gmx_MMPBSA
   outputs in `analysis/wt/`, `analysis/scan/rep1/` and `analysis/scan/rep2/` and
   recomputes all nine binding free energies, all six ΔΔG values, both replica ΔΔG values
   and both wild-type windows, reproducing every tabulated value exactly. The six ΔG values
   are also **re-derivable from the deposited decompositions**: run
   `python3 analysis/scan/verify_ddg_from_decomp.py`, which sums the `DELTAS:` section of each
   `allmode/decomp_<MUT>.dat` file per frame and reproduces the tabulated ΔG to within
   1.06 kcal/mol (RMS 0.75, Pearson r = 0.999820, ranking identical). The file layout is:
   `Complex:` (672 rows/frame) → `Receptor:` (671) → `Ligand:` (1, TDC of the ligand, no
   free-energy offset) → `DELTAS:` (672, per-residue binding contribution, ligand row carries
   `Internal = 0.0` because the free-ligand energy is already subtracted).
5. **Figures**: `scripts/make_figures.py`, `scripts/make_fig1_v2.py`.
6. **Manuscript DOCX**: `scripts/md2docx.py manuscript/manuscript.md`.

## Provenance status of the §4.5 energy table

| Quantity | Status |
|---|---|
| Six mutant ΔG (M141A … V29A) | **artifact-backed** — `analysis/scan/rep1/mmpbsa_<MUT>.dat` (gmx_MMPBSA output of the 20 ns re-simulation of each mutant); independently reproducible from `analysis/scan/allmode/decomp_<MUT>.dat` (`DELTAS:` section), RMS 0.75 kcal/mol vs the pipeline log |
| Two independently seeded replica ΔG (M141A, R194A) | **artifact-backed** — `analysis/scan/rep2/mmpbsa_<MUT>_rep2.dat`, with `gmx_MMPBSA_<MUT>_rep2.log` recording the command line, the trajectory (`md_<MUT>_rep2_img.xtc`) and the 100 processed frames |
| WT ΔG −38.06 ± 2.14 (0–24.8 ns window) — the scan reference | **artifact-backed** — `analysis/wt/mmpbsa_wt_100frames.dat` and the recovered output text `analysis/wt/WT_MMGBSA_OUTPUT_0to24.8ns.txt` |
| WT ΔG −32.40 ± 1.73 (30–50 ns window) — convergence / window-sensitivity check | **artifact-backed** — `analysis/wt/mmpbsa_wt_matched_30to50ns.dat` (gmx_MMPBSA, 100 complex frames); input trajectory and verbatim regeneration recipe retained as an independent cross-check |
| Mutant starting coordinates (all six) | **artifact-backed** — `analysis/scan/rep1/complex_<MUT>.gro`; `verify_mutant_topologies.py` confirms complex = receptor + 82-atom ligand and WT − receptor = substitution difference (7 / 7 / 14 / 9 / 1 / 6) for every mutant |
| Solvated, equilibrated mutant boxes | **not deposited** — >14 MB each; the pipeline log records the fresh minimisation, NVT and NPT equilibration |

Every number in the §4.5 table and in Fig. 3 is therefore recomputed from a retained output by
`analysis/scan/verify_all_dG_outputs.py`; none depends on a pipeline log.

**Provenance of the recovered outputs (2026-10-24).** The mutant, replica and 30–50 ns wild-type
outputs above were recovered from a local 5.0 GB tar archive of the remote working tree
(`zss_md_remote_20261023.tar`, 1022 members, packed 2026-10-23 12:04) that had not been examined
when the earlier "log-only" verdicts were written. Their identity is established by the
gmx_MMPBSA headers (run time, structure file, 100 complex frames) and by exact agreement with the
archived pipeline log to both quoted digits (mean and SD). The earlier verdicts for these three
items are retracted; the retained-artifact status above supersedes them.

The WT value remains window-dependent (−38.06 at 0–24.8 ns vs −32.40 at 30–50 ns, a 5.66 kcal/mol
spread), which is disclosed in the manuscript as a limitation of single-trajectory MM-GBSA on 100
frames. Because the reference enters every ΔΔG as an additive constant, re-referencing the scan to
the 30–50 ns window shifts all six values by the same −5.66 kcal/mol and leaves the ranking and
every conclusion unchanged.

## Provenance note (WT 30–50 ns MM-GBSA)

The 30–50 ns wild-type value (ΔG = −32.40 ± 1.73 kcal/mol) was computed over the continued WT
trajectory's **30–50 ns window** (input `wt_30to50ns_200ps.xtc`, 100 frames; structure file
`/root/wt_rebuild/md_ref.tpr`, run 2026-10-20 07:57:57). Its output is retained here as
`analysis/wt/mmpbsa_wt_matched_30to50ns.dat`. The verbatim original command line, the input hashes,
the ligand-topology rebuild step, and a control run that reproduces the deposited 0–24.8 ns result
(−38.06 ± 2.14) are committed at `analysis/wt/REGENERATE_WT_30to50ns.md` as an independent
cross-check. The already-deposited 0–24.8 ns WT output (`mmpbsa_wt_100frames.dat`,
ΔG = −38.06 ± 2.14) underlies §3.3 and supplies the scan reference.

## Caveats (shared with the manuscript)

All energetics are **computational predictions** (single-trajectory MM-GBSA without an entropy term; GB approximation; known favourable bias). No affinity, efficacy, direction-of-modulation, causal, or clinical claim is made anywhere. Single 24.8 ns trajectory, no replicates for the primary pose; the alanine scan is exploratory and directional only.

## Software versions

AutoDock Vina 1.2.7; GROMACS 2024.5 (GPU/CUDA); AmberTools (acpype, antechamber, tleap); gmx_MMPBSA 1.6.5; MDTraj; NumPy; matplotlib.

## License

MIT (see LICENSE).

## Version history

- **v1.0.11** (2026-10-29): corrected the ΔΔG re-referencing sign in this README — re-referencing the alanine scan to the 30–50 ns wild-type window shifts every ΔΔG by **−5.66** kcal/mol (not +5.66); the manuscript title now carries the "(membrane-absent model)" caveat (the interface model contains no lipid bilayer); residual "hotspot" wording in §4.5 and Fig. 3 was softened to "residues" where it conflicted with the §4.5 retraction that no residue-level hotspot conclusion is defensible; and the six tleap-built mutant starting coordinates (`analysis/scan/rep1/complex_*.gro`) are now tracked and SHA-256 listed so the manifest is complete.
- **v1.0.10** (2026-10-29): Round-4 independent expert-review revisions (Eaton 2012 wording, §4.5 residue-level hotspot retraction, JMGM formatting, Graphical Abstract).
