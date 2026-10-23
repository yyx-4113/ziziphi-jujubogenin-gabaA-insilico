# ziziphi-jujubogenin-gabaA-insilico

**Reproducibility package for:** "Jujubogenin does not preferentially engage the GABA_A benzodiazepine site: an in silico study of a candidate allosteric cavity at the α1/γ2 interface" (single-author, purely computational study).

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
             verify_ddg_from_decomp.py (reproduces the six ΔG values from those files),
             verify_bz_separation.py (reproduces the §3.1 contact-set / BZ-set separation
                                     geometry from structures/6X3Z.pdb: 11.0 Å closest Cα–Cα,
                                     all 25 contacts beyond 12 Å of the BZ-site centroid)
  wt/        0–24.8 ns wild-type MM-GBSA output (mmpbsa_wt_100frames.dat), the recovered output text
             (WT_MMGBSA_OUTPUT_0to24.8ns.txt), and the 30–50 ns regeneration recipe; see wt/README.md
figures/     Fig. 1–3 (PNG + SVG) and their generation scripts
scripts/     md2docx.py (manuscript → DOCX), verify_rg.py (protein radius of gyration), figure-generation scripts
manuscript/  manuscript_ZSS_insilico_v3.0.md (source), manuscript.md (submission copy), manuscript.docx (rendered)
```

## How to reproduce

1. **Docking** (AutoDock Vina 1.2.7): see `analysis/docking/` logs. The BZ-corrected box is centred on [81.46, 119.93, 120.91] (20 Å); the exploratory mis-centred box is centred on [97.518, 105.844, 123.021] (22 Å).
2. **MD** (GROMACS 2024.5, amber99sb-ildn, GAFF2/AM1-BCC ligand): `analysis/md/` holds the derived metrics; `verify_rg.py` recomputes the protein-alone radius of gyration from `npt.gro` (3.46 nm).
3. **MM-GBSA** (gmx_MMPBSA 1.6.5, igb=5, saltcon 0.150 M, 100 frames, no entropy term) and **energy-group** interaction energies: `analysis/md/`.
4. **Alanine scan** (six 20 ns mutant re-simulations): `analysis/scan/`. The six ΔG values are
   **re-derivable from the deposited decompositions**: run
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
| Six mutant ΔG (D141A … E29A) | **artifact-backed** — reproducible from `analysis/scan/allmode/decomp_<MUT>.dat` (`DELTAS:` section), RMS 0.75 kcal/mol vs the pipeline log |
| WT reference ΔG −32.40 ± 1.73 (30–50 ns window) | **pipeline log only** — the dedicated MM-GBSA output was never pulled back from the compute host. Regeneration recipe: `analysis/wt/REGENERATE_WT_30to50ns.md` |
| WT ΔG −38.06 ± 2.14 (0–24.8 ns window) | **artifact-backed** — `analysis/wt/mmpbsa_wt_100frames.dat` and the recovered output text `analysis/wt/WT_MMGBSA_OUTPUT_0to24.8ns.txt` |
| Two replica ΔΔG (+21.78, +7.85) | **pipeline log only** — no replica decomposition was archived and the replica trajectories were not retained |

Because the WT reference enters every ΔΔG as an additive constant, the ΔΔG **ranking and signs
are invariant** to the missing WT artifact: against the artifact-backed −38.06 the ΔΔG become
+12.92 / +24.46 / +34.97 / +32.78 / +22.63 / +21.72 with the ordering unchanged. The WT value is
window-dependent (−38.06 at 0–24.8 ns vs −32.40 at 30–50 ns, a 5.66 kcal/mol spread), which is
disclosed in the manuscript as a limitation of single-trajectory MM-GBSA on 100 frames.

## Important provenance note (WT 30–50 ns MM-GBSA)

The wild-type MM-GBSA reference used for the alanine-scan ΔΔG values (ΔG = −32.40 ± 1.73 kcal/mol) was computed over the continued WT trajectory's **30–50 ns window** (input `wt_30to50ns_200ps.xtc`, 100 frames). Its dedicated output (`mmpbsa_wt_30to50ns.dat`) is not among the retained artifacts and the original compute host is no longer reachable; the input trajectory is retained and the verbatim regeneration recipe with its mandatory control run is committed at `analysis/wt/REGENERATE_WT_30to50ns.md`, so the value is re-derivable on any Linux host but is currently documented only in the archived pipeline log. See `analysis/wt/README.md`. The already-deposited 0–24.8 ns WT output (`mmpbsa_wt_100frames.dat`, ΔG = −38.06 ± 2.14) underlies §3.3.

## Caveats (shared with the manuscript)

All energetics are **computational predictions** (single-trajectory MM-GBSA without an entropy term; GB approximation; known favourable bias). No affinity, efficacy, direction-of-modulation, causal, or clinical claim is made anywhere. Single 24.8 ns trajectory, no replicates for the primary pose; the alanine scan is exploratory and directional only.

## Software versions

AutoDock Vina 1.2.7; GROMACS 2024.5 (GPU/CUDA); AmberTools (acpype, antechamber, tleap); gmx_MMPBSA 1.6.5; MDTraj; NumPy; matplotlib.

## License

MIT (see LICENSE).
