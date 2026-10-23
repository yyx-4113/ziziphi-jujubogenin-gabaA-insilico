# ziziphi-jujubogenin-gabaA-insilico

**Reproducibility package for:** "Jujubogenin does not preferentially engage the GABA_A benzodiazepine site: an in silico study of a candidate allosteric cavity at the α1/γ2 interface" (single-author, purely computational study).

**Author:** Yongxin Yang — Department of Anesthesiology, The Second Affiliated Hospital of Fujian University of Traditional Chinese Medicine, Fuzhou, Fujian 350003, China. ORCID 0009-0004-9698-6552.

## What this repository contains

This is a **computational-only** study. No animals, humans, tissues, or wet-lab measurements were used. The repository provides the full analysis code, input structures, and all derived products needed to reproduce every reported number. Raw all-atom MD trajectories are >1.5 GB and are archived separately (Zenodo; DOI to be issued on acceptance); the deposited code + derived products are sufficient to reproduce all values without the raw trajectories.

```
analysis/
  docking/   docking logs (juju_BZ, flum_BZ, jujubogenin_tight, flumazenil_tight), docking_results.md, box_center.txt
  md/        MD metrics (rmsd_final.csv/json), MM-GBSA (mmpbsa_r3.dat), interaction energies (interaction_energy_summary.json, contact_residue_energy.json), post-equilibration structure (npt.gro)
  scan/      alanine-scan ΔΔG tables (mut_ddg_results.txt, mut_ddg_replica_results.txt), post_summary.txt, diag_summary.json, cross-map matrices (crossmap_*.csv)
  wt/        0–24.8 ns wild-type MM-GBSA output (mmpbsa_wt_100frames.dat); see wt/README.md for the 30–50 ns window status
figures/     Fig. 1–3 (PNG + SVG) and their generation scripts
scripts/     md2docx.py (manuscript → DOCX), verify_rg.py (protein radius of gyration), figure-generation scripts
manuscript/  manuscript_ZSS_insilico_v3.0.md (source), manuscript.md (submission copy), manuscript.docx (rendered)
```

## How to reproduce

1. **Docking** (AutoDock Vina 1.2.7): see `analysis/docking/` logs. The BZ-corrected box is centred on [81.46, 119.93, 120.91] (20 Å); the exploratory mis-centred box is centred on [97.518, 105.844, 123.021] (22 Å).
2. **MD** (GROMACS 2024.5, amber99sb-ildn, GAFF2/AM1-BCC ligand): `analysis/md/` holds the derived metrics; `verify_rg.py` recomputes the protein-alone radius of gyration from `npt.gro` (3.46 nm).
3. **MM-GBSA** (gmx_MMPBSA 1.6.5, igb=5, saltcon 0.150 M, 100 frames, no entropy term) and **energy-group** interaction energies: `analysis/md/`.
4. **Alanine scan** (six 20 ns mutant re-simulations): `analysis/scan/`.
5. **Figures**: `scripts/make_figures.py`, `scripts/make_fig1_v2.py`.
6. **Manuscript DOCX**: `scripts/md2docx.py manuscript/manuscript.md`.

## Important provenance note (WT 30–50 ns MM-GBSA)

The wild-type MM-GBSA reference used for the alanine-scan ΔΔG values (ΔG = −32.40 ± 1.73 kcal/mol) was computed over the continued WT trajectory's **30–50 ns window** (input `wt_30to50ns_200ps.xtc`, 100 frames). Its dedicated output (`mmpbsa_wt_30to50ns.dat`) is being regenerated on the compute host and will be committed to this repository **before submission**; see `analysis/wt/README.md`. The already-deposited 0–24.8 ns WT output (`mmpbsa_wt_100frames.dat`, ΔG = −38.06 ± 2.14) underlies §3.3.

## Caveats (shared with the manuscript)

All energetics are **computational predictions** (single-trajectory MM-GBSA without an entropy term; GB approximation; known favourable bias). No affinity, efficacy, direction-of-modulation, causal, or clinical claim is made anywhere. Single 24.8 ns trajectory, no replicates for the primary pose; the alanine scan is exploratory and directional only.

## Software versions

AutoDock Vina 1.2.7; GROMACS 2024.5 (GPU/CUDA); AmberTools (acpype, antechamber, tleap); gmx_MMPBSA 1.6.5; MDTraj; NumPy; matplotlib.

## License

MIT (see LICENSE).
