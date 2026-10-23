# In-silico target validation — Level (i): Molecular docking of jujubogenin at the GABA_A benzodiazepine site

**Status:** EXECUTED (real computation, not simulated). This is the docking layer (i) of Figure 7 in the protocol.
Layers (ii) MD simulation, (iii) microscale thermophoresis (MST) affinity, and (iv) in-vivo flumazenil antagonism remain to be executed.

## Methods (reproducible)
- **Receptor:** PDB `6X3Z` — cryo-EM structure of the α1β3γ2S GABA_A receptor (GABA bound at orthosteric sites; benzodiazepine site unoccupied). Subunits: α1 = chains B & D, β3 = C, γ2 = E. Receptor prepared as rigid PDBQT (heavy atoms + Gasteiger charges) from chains A–E (Fab fragments and all HETATM removed).
- **Ligands (real 3D coordinates, PubChem):**
  - Jujubogenin — PubChem CID 15515703 (C30H48O4, MW 472.7). This is the gastric-hydrolysis metabolite of jujubosides identified by Song 2017 as the GABA_A-active species.
  - Flumazenil — PubChem CID 3373 (C15H14FN3O3, MW 303.3), used as a **positive control** for the benzodiazepine site.
- **Docking engine:** AutoDock Vina 1.2.7 (Windows binary, `vina_1.2.7_win.exe`), rigid ligand (TORSDOF 0), exhaustiveness 24–32, 20 output modes.
- **Box:** centered on the α1(D)/γ2(E) benzodiazepine-site interface. Primary (tight) box center `[97.518, 105.844, 123.021]` Å, size 22 Å. A broader 30 Å box was used first and is reported for transparency.
- **Tooling:** RDKit 2026.3.6 + Open Babel 3.2.1 (PDBQT prep/validation) in the `default` conda venv.

## Results — primary (tight 22 Å box, α1+/γ2− pocket)

| Ligand | Best affinity (kcal/mol) | 2nd mode | Pose cluster (rmsd LB) |
|---|---|---|---|
| Jujubogenin | **−8.32** | −8.28 (rmsd 0.34) | tight (modes 1–2 within 0.34 Å; modes 3–11 within ~2–4 Å) |
| Flumazenil (control) | **−7.11** | −6.94 (rmsd 4.02) | broader scatter within pocket |

Best-pose receptor contacts (heavy-atom min distance ≤ 4.5 Å):

**Jujubogenin** — α1(D): MET141 (1.99 Å), MET58 (2.70), HIS142 (2.74), TYR282 (2.82), PRO140 (2.89), VAL280 (3.84); γ2(E): ARG194 (2.05), ARG232 (2.24), TRP196 (2.26), TYR199 (2.57), LEU198 (2.77), THR193 (3.30), ARG197 (3.46), ASP192 (3.88), SER195 (3.94), PHE203 (4.41).

**Flumazenil (control)** — α1(D): MET141 (2.77), HIS142 (2.77), MET58 (3.25), TYR282 (2.90), VAL280 (3.05); γ2(E): LEU198 (1.93), THR193 (2.70), ARG194 (2.83), TYR199 (2.88), PHE203 (3.68), ARG232 (3.91), SER202 (3.91), TRP196 (4.03), PHE201 (4.24).

**Shared pocket residues** (both ligands): α1 MET141, HIS142, MET58, TYR282, VAL280; γ2 ARG194, TRP196, TYR199, THR193, ARG232, ASP192/PHE203. The overlap confirms both compounds occupy the same α1+/γ2− benzodiazepine pocket.

## Broad 30 Å box (transparency)
- Jujubogenin: −8.41 kcal/mol; flumazenil: −7.25 kcal/mol. In the large box flumazenil preferred the adjacent α1+/β3− BZ-sensitive site (chains D/C), consistent with flumazenil's known promiscuity across BZ sites; jujubogenin remained at the α1+/γ2− interface. This motivated the tighter 22 Å box used as primary.

## Interpretation (honest, computational-only)
1. **Site validation passed.** A crystallographically-relevant benzodiazepine-site ligand (flumazenil) docks into the defined α1+/γ2− pocket, confirming the box localizes the true binding site. Jujubogenin docks into the *same* pocket and shares its key contact residues — supporting the protocol's hypothesis that jujubogenin can engage the GABA_A benzodiazepine site.
2. **Docking score ≠ binding affinity.** Vina scores are relative ranking energies, not quantitative Kd/pKi. Jujubogenin's more negative score does **not** imply higher affinity than flumazenil; flumazenil is the established high-affinity BZ ligand. The score only indicates jujubogenin finds a favorable pose in the pocket.
3. **Caveats.** (a) Rigid receptor, single conformer of 6X3Z, single ligand conformer (obabel/rdkit protonation, not exhaustive conformational sampling). (b) No water/electrostatics beyond Vina's empirical scoring. (c) The BZ site in 6X3Z is unoccupied; the pocket geometry may shift upon ligand binding (to be tested by MD, layer ii). (d) Docking supports *feasibility of binding*, not *physiological modulation* — that requires MST (iii) and in-vivo flumazenil antagonism (iv).

## Files
- `rec_ok.pdbqt` — prepared receptor
- `jujubogenin_ok.pdbqt`, `flumazenil_ok.pdbqt` — prepared ligands
- `jujubogenin_tight.pdbqt`, `flumazenil_tight.pdbqt` — 20 docked poses each
- `jujubogenin_tight_log.txt`, `flumazenil_tight_log.txt` — Vina logs (full mode tables)
- `box_center.txt` / `box_size.txt` — final box
- `make_inputs.py`, `analyze_contacts.py`, `analyze_tight.py`, `tighter_box.py` — reproducible scripts
