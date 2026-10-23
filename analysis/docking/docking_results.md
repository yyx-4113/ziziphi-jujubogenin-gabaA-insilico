# Molecular docking of jujubogenin at the human α1β2γ2 GABA_A receptor

**Status:** EXECUTED (real computation). Docking is the first computational layer of the
study; molecular dynamics and in-silico alanine scanning were subsequently performed and are
reported in `../md/` and `../scan/`. The decisive functional tests (electrophysiology,
affinity measurement, in-vivo sleep end-points) are explicitly **outside the scope** of this
study and are not claimed here.

**Revision note (2026-10-24).** This file previously recorded an earlier docking pass whose
conclusion, that jujubogenin and flumazenil occupy the same benzodiazepine pocket, has been
**retracted** in the manuscript. The retraction's cause was a search box centred 21.46 A
from the benzodiazepine site (see "Documented failure mode" below). The file has been
rewritten so that every number below is traceable to one of the four deposited Vina logs,
and the exploratory box is no longer described as the benzodiazepine site. Run
`verify_pose_geometry.py` in this directory to reproduce the Fig. 1 geometry claims.

## Receptor

- **Structure:** PDB `6X3Z`, human GABA_A receptor α1β2γ2 in complex with GABA; cryo-EM,
  3.23 A, EMD-22037. Deposited coordinates are in `structures/6X3Z.pdb`.
- **Subunit assignment, verified from the deposited coordinates** (not from the RCSB
  annotation, whose chain mapping is unreliable for this entry). Chains were identified by
  the subunit-signature residues of the benzodiazepine site:

  | chains | signature residues found | subunit |
  |---|---|---|
  | B, D | HIS102 and SER205 | α1 (338 residues, numbering 10–347) |
  | A, C | neither | β2 (334 residues, numbering 7–340) |
  | E | TYR58 and PHE77 | γ2 (333 residues, numbering 25–357) |

  Chains F/G/H/I of the deposit are Fab fragments. Independent confirmation: in the
  flumazenil co-crystal `6X3U`, the co-crystallised ligand contacts HIS102/SER205 on chain D
  and TYR58/PHE77 on chain E, so chain D is necessarily α1 and chain E γ2.
- **Prepared receptor:** `structures/rec_ok.pdbqt`, rigid, heavy atoms with Gasteiger
  charges, all five receptor chains retained (13,653 atoms; Fab and all HETATM removed).
  Chain labels are preserved from the deposit, so chain D = α1 and chain E = γ2.

## Ligands

- **Jujubogenin** — PubChem CID 15515703 (C30H48O4, MW 472.7), the gastric-hydrolysis
  metabolite of jujubosides identified by Song 2017 as the GABA_A-relevant species.
- **Flumazenil** — PubChem CID 3373 (C15H14FN3O3, MW 303.3), positive control for the
  benzodiazepine site.

## Engine and boxes

AutoDock Vina 1.2.7; rigid ligand (TORSDOF 0); exhaustiveness 32; 20 output modes;
grid spacing 0.375 A. Two search boxes were used, and the distinction between them is the
whole point of the analysis:

| box | centre (A) | size | purpose |
|---|---|---|---|
| **BZ box** | 81.46, 119.93, 120.91 | 20 A | crystal-validated benzodiazepine site |
| **exploratory cavity box** | 97.518, 105.844, 123.021 | 22 A | unbiased search of the α1/γ2 interface |

The BZ box centre was placed on the Cα centroid of the 13 residues that contact flumazenil
in the 6X3U co-crystal (chain D: 100, 102, 159, 160, 203, 205, 206, 207, 210; chain E: 58,
77, 79, 142); the grid centre and that Cα centroid differ by 0.27 A. The exploratory box
centre lies **21.46 A** from the BZ centroid.

## Results (from the four deposited logs)

| log | ligand | box | best affinity (kcal/mol) | second mode |
|---|---|---|---|---|
| `flum_BZ_log.txt` | flumazenil | BZ 20 A | **−7.086** | −6.895 |
| `juju_BZ_log.txt` | jujubogenin | BZ 20 A | **−4.403** | −3.938 |
| `jujubogenin_tight_log.txt` | jujubogenin | cavity 22 A | **−8.324** | −8.284 (rmsd 0.34 A) |
| `flumazenil_tight_log.txt` | flumazenil | cavity 22 A | **−7.11** | −6.943 |

**Pose geometry** (reproduced by `verify_pose_geometry.py`; pose centroid = unweighted mean
of all atoms of the best-scoring pose, measured from the BZ box centre):

| pose | distance to BZ centroid | Fig. 1 value |
|---|---|---|
| flumazenil, BZ box | 7.49 A | 7.5 A |
| jujubogenin, BZ box | 11.44 A | 11.4 A |
| flumazenil, cavity box | 22.90 A | 22.9 A |
| jujubogenin, cavity box | 23.12 A | 23.1 A |

## Documented failure mode

An earlier docking pass treated the exploratory box as the benzodiazepine site, reported
jujubogenin −8.32 kcal/mol and flumazenil −7.11 kcal/mol "in the benzodiazepine pocket", and
concluded from the shared contact residues that both ligands occupy the same site. That
conclusion is **wrong and is retracted** in the manuscript. The box was centred 21.46 A
from the benzodiazepine site, so it samples the membrane-proximal α1/γ2 cavity instead; the
two ligands never competed for the same volume. Re-docking both ligands into the properly
centred BZ box gives flumazenil −7.086 kcal/mol against jujubogenin −4.403 kcal/mol, i.e.
jujubogenin does **not** preferentially occupy the benzodiazepine site under this protocol.

## Interpretation

1. **Protocol validation passed.** Flumazenil redocks into the crystal-defined
   benzodiazepine site at −7.086 kcal/mol, contacting α1 HIS102/SER205/VAL203 and γ2
   TYR58/PHE77, a subset of the 6X3U contact set.
2. **Jujubogenin does not prefer that site.** In the identical box it scores −4.403 kcal/mol.
3. **A distinct cavity is identified.** In the exploratory box jujubogenin scores
   −8.324 kcal/mol at a membrane-proximal α1/γ2 cavity whose centroid lies 23.1 A from the
   benzodiazepine centroid, with no contact residue shared with the classical
   benzodiazepine set. This pose was carried into MD.
4. **Score comparison is intra-ligand only.** The −8.324 versus −4.403 comparison ranks two
   poses of the *same* ligand in *different* search volumes; it is not an affinity ratio,
   and a Vina score is not a Kd or pKi. Confirming site preference requires a
   cavity-targeted re-dock, which the manuscript lists as remaining work.
5. **Caveats.** Rigid receptor, single conformer, single ligand conformer, no explicit water
   or entropy; the benzodiazepine site of 6X3Z is unoccupied, so its geometry may shift on
   binding. Docking supports feasibility of a pose, not physiological modulation.

## Files in this directory

| file | content |
|---|---|
| `flum_BZ_log.txt`, `juju_BZ_log.txt` | Vina logs, benzodiazepine box (20 A) |
| `jujubogenin_tight_log.txt`, `flumazenil_tight_log.txt` | Vina logs, exploratory cavity box (22 A) |
| `flum_BZ.pdbqt`, `juju_BZ.pdbqt`, `flumazenil_tight.pdbqt`, `jujubogenin_tight.pdbqt` | 20 poses each, best pose first |
| `box_center.txt` | exploratory cavity box centre |
| `structures/6X3Z.pdb`, `structures/6X3U.pdb` | deposited receptor structures |
| `structures/rec_ok.pdbqt` | prepared docking receptor |
| `verify_pose_geometry.py` | reproduces the Fig. 1 geometry table above |
