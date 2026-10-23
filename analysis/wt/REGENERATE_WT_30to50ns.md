# Regenerating the 30–50 ns wild-type MM-GBSA reference

**Status (2026-10-23): the output file is still missing.** The value it should contain,
ΔG<sub>WT</sub> = −32.40 ± 1.73 kcal/mol, is recorded in the archived pipeline log
(`analysis/scan/mut_ddg_results.txt`, line 3: "WT reference ΔG = -32.40 ± 1.73 kcal/mol
(recomputed, matched 30-50ns window)", timestamped Tue Oct 20 04:46:54 CST 2026), but the
primary gmx_MMPBSA `.dat` for that run was never pulled back from the compute host.
This document is the exact recipe to reproduce it, so that the number becomes
artifact-backed rather than log-documented.

Everything needed is either archived here or archived in the author's project directory
(`data/wt_100ns/`, `docking/md_autodl/`). No new science is required — only one MM-GBSA
job on a Linux host.

---

## 1. Original protocol (recovered verbatim from `gmx_MMPBSA_wt.log`)

The 0–24.8 ns WT run was executed as:

```
gmx_MMPBSA -i mm.in -cs ../md.tpr -ct ../prod_sample_img.xtc -ci ../index.ndx -cg 0 1 \
            -cp ../topol.top -lm ../JUB.acpype/JUB_bcc_gaff2.mol2 -o mmpbsa_r3.dat -nogui
```

* working directory `/root/zss_md/_mmpbsa_r3`; inputs in `/root/zss_md/`
* `mm.in` (identical to the archived `data/wt_100ns/mm.in.wt_original`):

```
&general
startframe=1, endframe=100, interval=1, verbose=2, keep_files=0,
/
&gb
igb=5, saltcon=0.150,
/
```

* index groups: `-cg 0 1` → group 0 = `[ Receptor ]`, group 1 = `[ Ligand ]`
  (the archived `data/wt_100ns/index_wt.ndx` contains exactly these two groups)
* receptor mask `:1-671`, ligand mask `:672`, ligand residue name `UB1` (82 atoms)
* toolchain recorded in the log: GROMACS **2024.5** (`/opt/gmx/bin/gmx`),
  conda env `md` (Python 3.10.22) with **gmx_MMPBSA 1.6.5**, **cpptraj**, **tleap**,
  **parmchk2**, **sander** (AmberTools), ParmEd 4.3.1, Linux x86-64
* output: ΔTOTAL = **−38.06 ± 2.14** kcal/mol → archived as
  `analysis/md/mmpbsa_r3.dat` and `analysis/wt/mmpbsa_wt_100frames.dat`

## 2. Inputs for the 30–50 ns window (all archived, SHA-256 verified)

| File | Role | SHA-256 |
|---|---|---|
| `data/wt_100ns/wt_30to50ns_200ps.xtc` | trajectory, 101 frames (30.0–50.0 ns, 200 ps) | `55c044618ccf1669410d3b4905fa006ceb978323a73d7646971c7e436cdff95b` |
| `data/wt_100ns/md_WT_ref60ns_214802.tpr` | system tpr used as `-s md_ref.tpr` when the subset was cut (see `log_subset30.txt`) | `e22e52d2f076ae6b70a7e95202ec2ad4641e05b7c8e326e9179215762e9304fd` |
| `data/wt_100ns/md_WT_rebuilt_214802.tpr` | alternative tpr, same 214802-atom system | `9f5b027a9d2e8975d6e1bad944102150d3ff55aa031731d16cc6d7ca8cbf4eed` |
| `data/wt_100ns/topol_WT_rebuilt.top` | system topology | `81f57d001b683da34551f271f009b5d4469179f95e3356e04c19bed4946b1e1c` |
| `docking/md_autodl/zss_md_results/topol.top` | original topology (as used by the 0–24.8 ns run) | verify on host |
| `data/wt_100ns/index_wt.ndx` | index with `[ Receptor ]` / `[ Ligand ]` | `74a1bd57ca3d02a07733a58ab61e9ca3f2e3d3870e3519ed001df4630573591e` |
| `data/wt_100ns/mm.in.wt_original` | protocol namelist (above) | `0b302e4cc58930303489e19e2143bab83fad016f4e363d3a1c2fa8e6e382c527` |

The subset was cut with (see `log_subset30.txt`):

```
gmx trjconv -s md_ref.tpr -f wt_100ns_img2.xtc -o wt_30to50ns_200ps.xtc -b 30000 -e 50000 -dt 200
```

so frame 0 = 30.0 ns and frame 100 = 50.0 ns (101 frames). With `endframe=100` the
calculation uses frames 1–100, i.e. 100 frames, matching the pipeline log's "100 frames".

**Pick the tpr/top pair that matches the trajectory** (both candidates are the same
214802-atom system; confirm with `gmx trjconv ... -dump 0` that atom count, ordering and
the UB1 residue line up before running).

## 3. Ligand topology (`JUB_bcc_gaff2.mol2`) — not archived, must be rebuilt

The original ligand file (`/root/zss_md/JUB.acpype/JUB_bcc_gaff2.mol2`, GAFF2 with
AM1-BCC charges, residue name UB1) was not pulled back. Rebuild it from the archived
docked pose:

```bash
acpype -i docking/md_autodl/ligand_pose.mol2 -c bcc -a gaff2 -o JUB
# ensure the residue name is UB1 (82 atoms) as in the simulated system
```

**Verify the rebuild before trusting any number:** the GROMACS topology already embeds the
charges and atom types that were actually used in the simulation. Dump them and compare
against the rebuilt mol2:

```bash
gmx dump -s md_WT_ref60ns_214802.tpr | grep -A90 'ub1\|UB1'   # atom names, types, charges
```

Accept only if atom count = 82, atom types are the GAFF2 set (c3/hc/oh/ho/…), and the
partial charges match the acpype output to ~1e-3 e. If they do not, stop: a divergent
ligand topology invalidates the comparison with the archived 0–24.8 ns value.

## 4. The run

```bash
mkdir wt_30to50 && cd wt_30to50
cp <inputs as in §2> .
gmx_MMPBSA -i mm.in.wt_original -cs md_WT_ref60ns_214802.tpr \
           -ct wt_30to50ns_200ps.xtc -ci index_wt.ndx -cg 0 1 \
           -cp topol_WT_rebuilt.top -lm JUB.acpype/JUB_bcc_gaff2.mol2 \
           -o mmpbsa_wt_30to50ns.dat -nogui
```

Expected result (from the pipeline log): ΔTOTAL ≈ **−32.40 ± 1.73 kcal/mol**.

## 5. Mandatory control — validate the toolchain first

Do **not** trust the 30–50 ns number until the identical protocol reproduces the archived
0–24.8 ns result. The control input is archived:

```bash
# 100 frames at 248 ps over 0–24.8 ns (same spacing as the original prod_sample_img.xtc)
gmx trjconv -s md.tpr -f docking/md_autodl/zss_md_results/prod100.xtc \
            -o ctrl_0to24p8_100fr.xtc -dt 248
gmx_MMPBSA -i mm.in.wt_original -cs md.tpr -ct ctrl_0to24p8_100fr.xtc \
           -ci index.ndx -cg 0 1 -cp topol.top -lm JUB.acpype/JUB_bcc_gaff2.mol2 \
           -o mmpbsa_ctrl_0to24p8.dat -nogui
```

Acceptance criteria (compare against `analysis/wt/mmpbsa_wt_100frames.dat`):

| quantity | archived | tolerance |
|---|---|---|
| ΔTOTAL mean | −38.06 | ±0.5 kcal/mol |
| ΔTOTAL SD | 2.14 | ±0.3 kcal/mol |
| ΔCOMPLEX / ΔEREC / ΔELIG signs and rough magnitudes | see file | consistent |

If the control fails, the local toolchain or the rebuilt ligand topology has diverged from
the original run; the 30–50 ns result must then be discarded rather than reported.

## 6. After a successful run

1. Commit `mmpbsa_wt_30to50ns.dat` (and the control output) to `analysis/wt/`.
2. Add both to `MANIFEST.md` with SHA-256.
3. Update the manuscript §4.5 transparency note and the Data availability statement to
   name the file; remove the "pending regeneration" wording.
4. Re-tag the repository and regenerate the submission DOCX.
5. Deposit the >1.5 GB raw trajectories (`wt_100ns_img.xtc`, `prod100.xtc`) on Zenodo and
   record the DOI in the Data availability statement.

## 7. What this does *not* fix

The six mutant ΔG values and the two replica ΔΔG values in §4.5 are documented only in the
pipeline log; their MM-GBSA outputs were likewise never archived, and their MD trajectories
are not retained, so they cannot be recomputed without repeating 8 × 20 ns of MD. The
archived per-residue decompositions (`analysis/scan/`, `crossmap_*.csv`) support the
per-residue claims but do not reconstruct the totals (verified 2026-10-23: no linear
combination of the Complex/Receptor/Ligand decomposition sections reproduces the logged
ΔG for any of the six mutants). §4.5 must therefore continue to state that the mutant
summary values are transcribed from the archived pipeline log.
