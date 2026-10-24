# Jujubogenin does not preferentially engage the GABA<sub>A</sub> benzodiazepine site: an in silico study of a candidate allosteric cavity at the α1/γ2 interface

**Author:** Yongxin Yang

**Affiliation:** Department of Anesthesiology, The Second Affiliated Hospital of Fujian University of Traditional Chinese Medicine, Fuzhou, Fujian 350003, China

**ORCID:** 0009-0004-9698-6552

**Correspondence:** 960856791@qq.com

**Article type:** Original research, computational pharmacology (in silico)

---

## Abstract

**Background.** Postoperative sleep disturbance (PSD) is common after anaesthesia and surgery and is associated with delirium-like behaviour and impaired recovery. *Ziziphi Spinosae Semen* (ZSS, 酸枣仁) is used for insomnia, but its saponins are poorly absorbed and activity resides in metabolites rather than the parent glycosides: jujuboside A has an oral bioavailability of 1.32%, hydrolysis is predominantly gastric, and jujuboside B and jujubogenin, not the parent molecules, are the species reported to modulate GABA<sub>A</sub> receptors (Song et al., 2017; Jiang et al., 2007). Which metabolite engages which site, and whether a docked pose is dynamically stable, has not been addressed computationally for the perioperative setting; engagement of the benzodiazepine (BZ) site has been assumed rather than tested.

**Objective.** To determine *in silico* which site of the GABA<sub>A</sub> receptor jujubogenin engages, using a docking protocol validated against a crystal standard, and whether the resulting pose is stable under explicit-solvent molecular dynamics.

**Methods.** Jujubogenin (PubChem CID 15515703) and flumazenil (CID 3373) were docked with AutoDock Vina 1.2.7 at the α1/γ2 interface of the human α1β2γ2 GABA<sub>A</sub> receptor (PDB 6X3Z; chains D = α1, E = γ2). The protocol was validated against the flumazenil co-crystal (PDB 6X3U): the initial search box proved to be centred 21.5 Å from the crystallographic BZ site, and all docking was repeated with a box centred on that site. The best jujubogenin pose was carried into all-atom molecular dynamics (GROMACS 2024.5; amber99sb-ildn protein, GAFF2 ligand with AM1-BCC charges, TIP3P water, 0.15 M NaCl; dodecahedral box, 1.2 nm clearance; 214,802 atoms) on an RTX 4090 and analysed over **24.8 ns (497 frames)** with explicit **PBC imaging** before every metric. Binding free energy was estimated by MM-GBSA and cross-checked against energy-group interaction energies.

**Results.** Under the identical, crystal-validated protocol, flumazenil redocked into the BZ site (−7.086 kcal/mol; contacts α1 HIS102/SER205/VAL203 and γ2 TYR58/PHE77, a subset of the crystal contact set). Jujubogenin scored only **−4.403 kcal/mol at the BZ site** and did not reproduce the classical BZ contact pattern; an exploratory search outside the BZ box identified a distinct interfacial cavity pose (**−8.324 kcal/mol**) whose 25 simulation contact residues share **no** residue with the classical BZ set and whose centroid lies 23.1 Å from the BZ-site centroid (the two poses come from different search boxes; see §2.2). In that cavity pose jujubogenin remained stably bound throughout 24.8 ns: ligand heavy-atom RMSD **0.42 ± 0.10 Å (maximum 0.66 Å)**, backbone RMSD **2.36 ± 0.32 Å**, pocket-residue RMSD **1.72 ± 0.21 Å**, ligand–pocket centroid distance steady at **2.086 ± 0.060 nm**; no dissociation was observed. MM-GBSA gave **ΔG = −38.06 ± 2.14 kcal/mol** (ΔVDWAALS −47.11, ΔEEL −10.37, ΔEGB +24.74, ΔESURF −5.31; no entropy term); a second, differently implemented energy-group interaction energy (−52.86 ± 4.93 kcal/mol, 64.9% from γ2) agrees in its gas-phase components, although the two totals differ by ~15 kcal/mol because the energy-group estimate omits solvation and entropy.

**Conclusions.** Jujubogenin is not predicted to preferentially occupy the GABA<sub>A</sub> benzodiazepine site. An exploratory search identifies a distinct, membrane-proximal cavity at the α1/γ2 interface (a candidate allosteric site) as a stable binding pose over 24.8 ns, but the relative preference between sites is not established by docking and requires a cavity-targeted re-dock for confirmation. All energetics are **computational predictions**: no affinity, efficacy, direction of modulation, causal, or clinical claim is made, and the functional consequence of binding at this cavity is untested.

**Keywords:** *Ziziphi Spinosae Semen*; jujubogenin; GABA<sub>A</sub> receptor; benzodiazepine site; allosteric site; molecular docking; molecular dynamics; MM-GBSA; postoperative sleep disturbance

**Highlights**

- Under a crystal-validated docking protocol, jujubogenin does **not** preferentially occupy the GABA<sub>A</sub> benzodiazepine site.
- An exploratory search identifies a membrane-proximal cavity at the α1/γ2 interface (25 contact residues, none shared with the benzodiazepine set) that remains stably bound over 24.8 ns of molecular dynamics.
- The cavity pose and the BZ-site pose derive from different search boxes, so the relative preference between sites is not established and requires a cavity-targeted re-dock.
- Two computational energetics approaches, differing in their treatment of topology and solvation, give favourable but enthalpic, unconverged estimates; no affinity, efficacy, or functional claim is made.
- Two easily repeated and easily missed failure modes, namely a mis-centred docking search box and trajectories analysed without periodic-boundary imaging, are documented as methodological cautionary cases.

---

## 1. Introduction

### 1.1 Postoperative sleep disturbance

Sleep architecture is disrupted after anaesthesia and surgery, with reduced NREM and REM sleep, increased fragmentation, and altered delta power in the first postoperative days (Jia et al., 2020; Wang et al., 2026). These disturbances co-occur with delirium-like behaviour and are a plausible contributor to delayed recovery. A microbiota-focused study has reported associations between the gut microbiome and PSD (Yang et al., 2026), but that work was correlational: it did not assess intestinal barrier integrity, did not perform microbiota depletion or transplantation, and did not localise a molecular target.

### 1.2 Where *Ziziphi Spinosae Semen* activation actually occurs

ZSS is used for insomnia. Its sedative constituents include jujubosides, but the pharmacokinetics redirect the mechanistic question (Jiang et al., 2007). Jujuboside A has an oral bioavailability of approximately 1.32%, and hydrolysis is predominantly gastric rather than microbiota-dependent (Song et al., 2017). The species reported to modulate GABA<sub>A</sub> receptors are jujuboside B and the aglycone **jujubogenin**, not the parent glycoside (Song et al., 2017). Any receptor-level claim must therefore be made about the metabolite, and the site of engagement is an output to be determined, not an assumption imported from the parent molecule.

### 1.3 Objectives

1. To validate the docking protocol against a crystal structure of the benzodiazepine site before any site assignment is drawn.
2. To determine which site of the α1/γ2 interface jujubogenin engages, and to report that assignment with its evidence.
3. To test whether the resulting pose is dynamically stable in explicit solvent, and to estimate binding energetics with two computational approaches that differ in their treatment of topology and solvation.
4. To state explicitly which mechanistic claims this design can and cannot support.

---

## 2. Methods

All work is computational. **No animals, no human subjects, no tissues, and no wet-laboratory measurements were involved in this study.**

### 2.1 Receptor and ligand preparation

The human α1β2γ2 GABA<sub>A</sub> receptor structure (PDB 6X3Z, in complex with GABA; Kim et al., 2020) was used. Because the benzodiazepine site is formed at an α/γ interface, the α1 subunit (chain D; modelled residues 10–347) and the γ2 subunit (chain E; modelled residues 25–357) were extracted to build the dimeric interface model used here; the two β2 subunits, the GABA molecules bound at the β+/α− interfaces, and the crystallization Fab were excluded. The modelled segment spans the extracellular domain and the membrane-proximal part of the transmembrane domain, but contains no membrane, no M4 helix, no intracellular loop, and not the full pentamer. Missing atoms were tolerated during topology generation (`pdb2gmx -missing`). The ligand, jujubogenin (CID 15515703), was prepared from its docked pose; flumazenil (CID 3373) served as the protocol-validation ligand.

### 2.2 Molecular docking with crystal-standard validation

AutoDock Vina 1.2.7 (Eberhardt et al., 2021; Trott et al., 2010) was used. **The search box was validated before any biological interpretation was drawn.** The reference BZ site was defined from the flumazenil co-crystal structure (PDB 6X3U; human α1β2γ2 + GABA + flumazenil, ligand residue FYP; Kim et al., 2020): protein residues within 4 Å of the bound flumazenil were α1 SER159, PHE100, HIS102, TYR160, VAL203, SER205, SER206, THR207, TYR210 and γ2 TYR58, ALA79, PHE77, THR142: the classical benzodiazepine-site residue set (Sigel and Buhr, 1997). Its centroid, mapped into the 6X3Z frame, is [81.46, 119.93, 120.91].

Our first search box was centred at [97.518, 105.844, 123.021], i.e. **21.5 Å from the crystallographic BZ-site centroid**, so that both ligands were sampled in the wrong region of the interface (their best poses lay 23.1 and 22.9 Å from the site, for jujubogenin and flumazenil respectively). A wider 30 Å box (centre 102.257/111.077/121.082) reproduced the same misplacement (−8.405 and −7.254 kcal/mol), showing the error was systematic rather than a sampling artefact. **All docking reported here was therefore repeated** with a 20 Å box centred on [81.46, 119.93, 120.91] at exhaustiveness 32. Validation is two-sided: flumazenil must recover the BZ site under this protocol (it does), and only then is jujubogenin's behaviour at that site interpretable.

A limitation of the docking search must be stated explicitly. The 20 Å box centred on the BZ site reaches at most 17.3 Å (a box corner) from the BZ centroid and therefore does **not** cover the interfacial cavity, which lies 23.1 Å away. Consequently the cavity pose (Vina −8.324) was obtained only from the exploratory mis-centred search and was **not** re-sampled under a BZ-corrected box; the −8.324 (cavity) and −4.403 (BZ-site) scores therefore come from two different search volumes and are **not** a direct test of site preference. The cavity pose is carried forward as a hypothesis-generating candidate identified by exploratory docking and validated for *stability* by the MD simulation below; a cavity-targeted re-dock (box defined from the MD-refined pose) is required to confirm the pose is recoverable under a correctly placed search and is listed among the still-needed computations in §4.5.

Vina scores are reported as **ranking energies**, not as quantitative affinities.

### 2.3 Molecular dynamics system

| Parameter | Value |
|---|---|
| Engine | GROMACS 2024.5 (Abraham et al., 2015; GPU build, CUDA) |
| Protein force field | amber99sb-ildn (Lindorff-Larsen et al., 2010) |
| Ligand parameters | GAFF2 (Wang et al., 2004), AM1-BCC charges (acpype / AmberTools) |
| Water | TIP3P |
| Ions | 0.15 M NaCl |
| Box | Dodecahedron, 1.2 nm clearance |
| Protein | α1 (338 residues) + γ2 (333 residues); ligand UB1, 82 atoms |
| Water / ions | 67,802 water molecules; 198 Na⁺, 209 Cl⁻ (the 11-ion Cl⁻ excess exactly neutralises the protein's formal charge of +11 at pH 7 with neutral histidines) |
| Total atoms | 214,802 |
| Hardware | NVIDIA RTX 4090 |

Equilibration followed energy minimisation (steepest descent) → NVT (100 ps) → NPT (100 ps). Production settings: 2 fs timestep, 300 K (v-rescale), Parrinello–Rahman pressure coupling, LINCS constraints, PME electrostatics, trajectory written every 50 ps.

**Intended versus achieved length.** Production was configured for 100 ns. The run was terminated early by the host platform sending SIGTERM at **step 12,420,100 (24.84 ns)**; GROMACS shut down cleanly and wrote a complete, uncorrupted 24.8 ns trajectory, which is what is analysed here. A continuation run towards 100 ns was subsequently started and had reached at least 50 ns at the time of writing. That continuation supplies no primary metric: the 24.8 ns trajectory remains the basis of §3.1–3.3. It is used only twice, and only as a convergence and reference check, namely for the 30–50 ns window comparison in §3.3 and for the wild-type reference in the alanine scan in §4.5.

### 2.4 Trajectory analysis

Analysis used MDTraj (McGibbon et al., 2015). **Two steps proved decisive and are stated so the work is reproducible:**

1. **Periodic-boundary imaging.** GROMACS writes coordinates wrapped into the box; mdtraj does not reassemble molecules by default. All trajectories were passed through `image_molecules()` before any metric was computed. Omitting this inflated the apparent backbone RMSD roughly 16-fold (3.75 nm versus the correct 0.236 nm) and produced, in early MM-PBSA attempts, unphysical energies (5.4 × 10⁸ kcal/mol) that were discarded.
2. **Backbone superposition.** Frames were superposed on protein backbone atoms before RMSD calculation, so reported values reflect internal motion rather than global tumbling.

Metrics: ligand heavy-atom RMSD, protein backbone RMSD, RMSD of residues within 6 Å of the ligand (the binding-site pocket, 24 residues), ligand-to-pocket centroid distance, and per-residue Cα RMSF. Two distinct residue sets are reported and should not be conflated. The contact set is the 25 residues within 4 Å of the ligand at any point in the trajectory (a union over all 497 frames); this set supplies the contact map and the per-residue energy decomposition. The binding-site pocket is the 24 residues of the 6 Å shell used for the pocket-RMSD and centroid-distance metrics; because that shell is a single fixed list rather than a trajectory union, the two sets are defined on different bases and are not nested, which is why the tighter-cutoff set is the larger of the two. Both counts are reported as computed. A radius-of-gyration series was also computed on all atoms of the system (protein plus solvent); because such a value is dominated by the solvent box it is retained in the metrics file but is not used here as evidence about the receptor, and the receptor's compactness is instead checked on the protein atoms alone (see §3.2).

### 2.5 Binding energetics: two independent approaches

**MM-GBSA.** gmx_MMPBSA 1.6.5 (Valdés-Tresanco et al., 2021) was run on the PBC-imaged trajectory: 100 frames (one every 250 ps), generalized Born igb=5, saltcon 0.150 M, 298.15 K, ligand parameters taken from the GAFF2/AM1-BCC mol2 file. **No conformational entropy term (−TΔS) was computed**; the value is therefore an enthalpic MM-GBSA estimate, which is known to be systematically biased towards favourable (negative) values, and is used here only as relative, qualitative evidence. All ± values reported for these estimates are standard deviations over the 100 frames.

**Energy-group interaction energy.** As a second cross-check that differs in implementation, the production trajectory was re-run with `energygrps` (protein–ligand, α1–ligand, γ2–ligand) and `nstenergy=1`, and short-range Coulomb plus Lennard-Jones terms were extracted over the same 100 frames. This shares no topology-rebuilding or solvation step with the MM-GBSA pipeline, although both approaches start from the same trajectory and the same GAFF2/AM1-BCC ligand charges, so they are independent in their treatment of topology and solvation rather than in their input data.

---

## 3. Results

### 3.1 Docking: flumazenil recovers the benzodiazepine site; jujubogenin does not

| Ligand | Search box | Best Vina score (kcal/mol) | Pose centroid to BZ-site centroid | Assignment |
|---|---|---|---|---|
| Flumazenil | Crystal-validated BZ centre | **−7.086** | 7.5 Å | BZ site; contacts α1 HIS102/SER205/VAL203, γ2 TYR58/PHE77 |
| Jujubogenin | Crystal-validated BZ centre | **−4.403** | 11.4 Å | no stable BZ-site pose (peripheral, weak) |
| Flumazenil | Mis-centred interface box (22 Å) | −7.110 | 22.9 Å | interfacial cavity (the wrong site) |
| Jujubogenin | Mis-centred interface box (22 Å) | **−8.324** | 23.1 Å | interfacial cavity; **this pose was carried into MD** |

Flumazenil's redocking contacts are a subset of the 6X3U crystal contact set, so the protocol (receptor preparation, protonation, scoring, box) recovers the BZ site within the limits of the method (the 7.5 Å centroid offset and the subset of crystal contacts reproduced are given in the table above). Jujubogenin under the identical protocol scores −4.403 kcal/mol, 3.9 kcal/mol less favourable than the −8.324 kcal/mol its exploratory cavity pose scored in the different, mis-centred box, a cross-box comparison that ranks nothing directly (§2.2); its best BZ-box pose sits at the periphery of the search box (11.4 Å from the BZ centroid) without reproducing the classical contact pattern. Figure 1 shows the two poses, the two site centroids, and the 23.1 Å separation between them.

**Site assignment from the simulation.** The 25 residues within 4 Å of jujubogenin during the 24.8 ns trajectory were α1 MET58, PRO140, MET141, HIS142, LEU143, GLU144, VAL280, ALA281, TYR282 and γ2 ASP192, THR193, ARG194, SER195, TRP196, ARG197, LEU198, TYR199, PHE201, SER202, PHE203, VAL204, SER230, ARG232, TYR356, LEU357. This set shares **no** residue with the classical BZ set (α1 PHE100, HIS102, SER159, TYR160, VAL203, SER205, SER206, THR207, TYR210; γ2 TYR58, ALA79, PHE77, THR142), and the two groups are also spatially separate: every one of the 25 residues lies more than 12 Å from the centroid of the BZ site (the mean Cα position of those 13 residues; closest approach 14.8 Å, γ2 Asp192), and the closest residue-to-residue approach between the two sets is 11.0 Å Cα–Cα (γ2 Asp192 to γ2 Tyr58). The cavity is on the membrane-proximal side of the α1/γ2 interface: its contacts span the C-terminal extracellular region (α1 Met58, Pro140–Glu144; γ2 Asp192–Arg232) and extend to the top of the modelled transmembrane segments (α1 Val280–Tyr282; γ2 Tyr356–Leu357).

The earlier reading, that jujubogenin and flumazenil "share the benzodiazepine pocket", was an artefact of the mis-centred search box, which forced both ligands into the same wrong cavity. It is retracted here.

Because the cavity pose and the BZ-site pose were obtained from different search boxes (see §2.2), their Vina scores rank the two sites only within their respective boxes and do not by themselves establish which site jujubogenin prefers; the MD stability of the cavity pose is reported here as a separate, stability-only observation.

### 3.2 Molecular dynamics: the cavity pose is stable and does not dissociate

Over 24.8 ns (497 frames; Fig. 2):

| Metric | Value |
|---|---|
| Ligand (jujubogenin) heavy-atom RMSD | **0.042 ± 0.010 nm (0.42 ± 0.10 Å)**, max 0.066 nm |
| Protein backbone RMSD | **0.236 ± 0.032 nm (2.36 ± 0.32 Å)**, max 0.340 nm |
| Binding-site pocket residues (24 residues) RMSD | **0.172 ± 0.021 nm (1.72 ± 0.21 Å)** |
| Ligand ↔ pocket centroid distance | 2.086 ± 0.060 nm (range 1.91–2.28 nm) |
| Cα RMSF | median 0.103 nm, p90 0.173 nm |

The receptor is stable (backbone RMSD 2.36 ± 0.32 Å with no drift, and a protein-alone radius of gyration of 3.46 nm on the retained post-equilibration structure, consistent with an intact two-subunit fragment), the binding pocket is comparatively rigid (1.72 ± 0.21 Å), and jujubogenin stays within 0.42 ± 0.10 Å of its docked pose with a ligand–pocket centroid distance that never approaches dissociation; rare dissociation on longer timescales cannot be excluded from a single 24.8 ns trajectory.

### 3.3 Binding energetics (computed)

**MM-GBSA (100 frames, no entropy term):**

| Component | Δ (kcal/mol) |
|---|---|
| ΔVDWAALS | −47.11 ± 2.11 |
| ΔEEL | −10.37 ± 0.28 |
| ΔEGB (polar solvation) | +24.74 ± 0.25 |
| ΔESURF (non-polar solvation) | −5.31 ± 0.02 |
| ΔGGAS | −57.48 ± 2.12 |
| ΔGSOLV | +19.43 ± 0.25 |
| **ΔTOTAL** | **−38.06 ± 2.14** |

**Energy-group interaction energy (same 100 frames):** −52.86 ± 4.93 kcal/mol total (Coulomb −9.42 ± 2.79; Lennard-Jones −43.43 ± 3.56), decomposed as γ2 −34.28 kcal/mol (64.9%) and α1 −18.58 kcal/mol (35.1%); minimum ligand–subunit distances 0.189 nm (α1) and 0.210 nm (γ2). The 25 contact residues contribute −51.78 kcal/mol in sum (α1 −18.13, γ2 −33.65), with the largest single contributions from α1 MET141 (−7.18), γ2 ARG194 (−5.48), γ2 LEU198 and SER202 (−4.76 each), γ2 TYR199 (−3.56) and α1 HIS142 (−3.57).

The two approaches are independent in their treatment of topology and solvation: MM-GBSA rebuilds AMBER topologies and adds solvation, whereas the energy-group rerun touches neither, although both start from the same trajectory and the same ligand charges; their van der Waals (−47.11 versus −43.43) and electrostatic (−10.37 versus −9.42) **gas-phase** components agree closely, so the favourable estimate for this cavity is not an artefact of either pipeline. The two **totals**, however, differ by ~15 kcal/mol because the energy-group estimate omits solvation and entropy; both remain **computed predictions** of the gas-phase/enthalpic type and neither measures affinity. The MM-GBSA ΔG is also **not converged**: the continued trajectory's 30–50 ns window yields −32.40 ± 1.73 kcal/mol, a ~6 kcal/mol shift from the 0–24.8 ns value, so the absolute MM-GBSA number should be read as indicative only (the 30–50 ns wild-type estimate is backed by its own retained gmx_MMPBSA output, `analysis/wt/mmpbsa_wt_matched_30to50ns.dat`, and the committed regeneration recipe with its control run remains deposited as an independent cross-check; it is reported here as a convergence check only and is not used as the reference for the §4.5 alanine scan, which uses the deposited 0–24.8 ns value).

---

## 4. Discussion

### 4.1 What this study adds

Three things. First, the site of engagement is treated as an output rather than an assumption: under a protocol validated against a crystal standard, jujubogenin does **not** preferentially occupy the benzodiazepine site, and a specific alternative, a membrane-proximal cavity at the α1/γ2 interface, is identified with its contact-residue evidence. Second, that cavity pose is stable over 24.8 ns and does not dissociate, with two independent computational approaches agreeing that binding there is favourable. Third, the work records two failure modes that are easy to repeat and easy to miss, namely a search box centred 21.5 Å from the intended site and trajectories analysed without periodic-boundary imaging, together with the external-standard checks that exposed them.

### 4.2 What a candidate allosteric site at this interface would mean

GABA<sub>A</sub> receptors carry several structurally distinct modulatory sites: the orthosteric GABA sites at β+/α− extracellular interfaces, the benzodiazepine site at the α+/γ− interface, and transmembrane sites for neurosteroids, general anaesthetics and picrotoxin. A ligand bound at the membrane-proximal α1/γ2 interface would sit at the ECD–TMD junction, where the coupling loops that are thought to transduce binding into gating are located; modulation from there, if any, would be allosteric rather than benzodiazepine-site-like. This is the hypothesis the present data motivate. It is explicitly **not** a functional finding: nothing here shows that jujubogenin changes receptor function, in either direction, at this or any site.

A transmembrane or ECD–TMD-junction pocket at this interface is not a speculative invention. In this receptor class, transmembrane modulatory sites are well established: etomidate binds the β+/α− intersubunit cavity (Eaton et al., 2012), and the broader principle that pLGIC transmembrane pockets can host neurosteroids and general anaesthetics is long settled. More directly, Fan et al. (2024) showed that β-estradiol occupies a pocket at the ECD–TMD interface of the human ρ1 GABA_A receptor and disrupts the allosteric transition that couples GABA binding to pore opening, the same interface class the present candidate cavity occupies. To the best of our knowledge, no ligand has yet been resolved at the α+/γ− transmembrane face in published GABA_A structures (we did not perform a systematic survey), so the present cavity sits at a plausible but still less-precedented location. This receptor-class context is what makes the cavity hypothesis worth testing; it remains a hypothesis, because the present study provides no functional evidence for it.

### 4.3 What this study explicitly does not establish

1. **No benzodiazepine-site engagement.** Jujubogenin is not predicted to preferentially occupy the BZ site. A weak, non-preferential interaction at that site cannot be excluded from docking alone; the claim is "no preferential engagement", not "no interaction whatsoever".
2. **No affinity.** Vina scores are ranking energies. The MM-GBSA ΔG is a computed prediction without a conformational entropy term and with a known favourable bias. No K<sub>d</sub>, K<sub>i</sub>, IC<sub>50</sub>, or measured ΔG is reported.
3. **No efficacy or direction of modulation.** Whether jujubogenin acts as an agonist, antagonist, positive modulator, negative modulator, or neutral binder (at the cavity or anywhere else) is unknown. Flumazenil-reversal logic does not apply, because the engaged site is not the benzodiazepine site.
4. **No causal claim.** No mutagenesis, electrophysiology, or in vivo experiment was performed.
5. **No pharmacological or clinical claim.** No sleep, behavioural, barrier, inflammatory, or microbiota endpoint was measured. Nothing here supports a treatment recommendation.
6. **Not a microbiota study.** Because hydrolysis is predominantly gastric, neither this work nor a microbiota-depletion design addresses the hydrolysis step; microbiota contributions remain an open, separately testable question and, on present evidence, are more likely permissive than required.

### 4.4 Model-specific limitations

- **Reduced receptor model.** Only the α1–γ2 interface was simulated (extracellular domain plus the upper transmembrane segments, in water): no membrane, no M4 or intracellular segments, no β2 subunits, no bound GABA, and not the full pentamer. Interfacial geometry, and therefore the shape of the cavity, is approximated.
- **Sampling.** 24.8 ns from a single trajectory, no replicates, no enhanced sampling. This addresses pose stability, not thermodynamics, and cannot exclude rare dissociation.
- **Single pose.** One docked cavity pose was propagated; alternative poses, and any BZ-site pose, were not compared dynamically.
- **Energetics.** MM-GBSA without −TΔS; GB approximation; systematic negative bias; usable only as relative evidence. The energy-group value is a gas-phase molecular-mechanics interaction energy and is not a binding free energy either.
- **Docking.** Vina scores rank poses; the −8.324 versus −4.403 comparison ranks poses for the same ligand only and is not an affinity ratio.

### 4.5 How the hypothesis should be tested

The hypothesis is falsifiable. Because this study is entirely in silico, the first tier of tests is computational and requires no laboratory work; the decisive functional tests are experimental and lie outside this study's scope. The first computational step, in-silico alanine scanning of the cavity hotspots, has now been performed and is reported here as an **exploratory within-computation scan**; the remaining computational and experimental steps follow. The scan is hypothesis-generating, not confirmatory (see the diagnostics below).

**Within-computation validation performed: in-silico alanine scanning and per-residue decomposition.** Six single-point alanine mutants were constructed in silico at the cavity: the four planned hotspot residues (α1 MET141; γ2 ARG194, LEU198, SER202) plus two non-contact controls deliberately placed outside the ligand shell (α1 MET81, 5.16 nm from the ligand centroid; γ2 VAL29, 4.95 nm), to discriminate true contact loss from sampling artefacts. A transparency note on mutant construction: for 5 of the 6 in-silico mutants the topology-build step (tleap) returned a non-zero exit code (exit = 1); the substitution was nevertheless verified quantitatively, because the receptor atom count of each built topology equals the wild-type count (10,907 atoms) minus exactly the atom difference of the intended substitution (10,900 for the two MET→ALA mutants, 10,893 for ARG→ALA, 10,898 for LEU→ALA, 10,906 for SER→ALA and 10,901 for VAL→ALA), and each mutation sits at the intended position; the exit code is therefore recorded as a build warning rather than a failed substitution, and the resulting topologies were used for the re-simulation. That atom-count identity is re-checked from the deposited files, not from the pipeline log, by `verify_mutant_topologies.py`, which reads each `rep1/complex_<mutant>.gro` and confirms two independent equalities for all six mutants: the complex atom count equals receptor plus ligand (82 atoms for jujubogenin), and the wild-type count minus the built receptor count equals the substitution difference quoted above; the two MET→ALA mutants are additionally confirmed to carry the same receptor count. The scan results are shown in Fig. 3. For each mutant the alanine-substituted complex was re-simulated for 20 ns under the protocol of §2.3 (the pipeline log records fresh minimisation, NVT and NPT equilibration for the five newly built mutants; the coordinates built by tleap for each mutant are deposited as `rep1/complex_<mutant>.gro`, while the solvated and equilibrated boxes, at more than 14 MB each, are not), MM-GBSA binding free energy was recomputed, and the change relative to the wild-type reference (ΔG<sub>WT</sub> = −38.06 ± 2.14 kcal/mol, the 0–24.8 ns value that is also the binding-energy result of §3.3 and whose MM-GBSA output `mmpbsa_wt_100frames.dat` is deposited in the reproducibility repository) was taken as ΔΔG, defined as ΔΔG = ΔG<sub>mutant</sub> − ΔG<sub>WT</sub> so that a positive value means the substitution is destabilising. Each of the nine binding free energies entering this comparison (six first replicas, two independently seeded second replicas and the wild-type reference) is backed by a retained gmx_MMPBSA output file, so every number in the table below is re-derivable from the deposits. An asymmetry in this comparison must be stated: the wild-type reference is drawn from the 24.8 ns primary trajectory, whereas each mutant ΔG is computed from an independent 20 ns re-simulation, so the two are not matched in sampling length (24.8 versus 20 ns) and the resulting ΔΔG inherits that asymmetry on top of the single-replica noise quantified below. A second wild-type estimate exists from the continued trajectory's 30–50 ns window (ΔG<sub>WT</sub> = −32.40 ± 1.73 kcal/mol), a 5.66 kcal/mol window dependence that is reported here as a limitation rather than hidden; because the wild-type reference enters ΔΔG only as an additive constant, re-referencing the scan to that window would shift all six values by the same +5.66 kcal/mol (to +13.98, +25.36, +35.11, +33.16, +23.24 and +22.65 respectively), leaving the ranking and every conclusion below unchanged, so the choice of window does not affect the directional reading. That 30–50 ns estimate is backed by a retained output of its own, `analysis/wt/mmpbsa_wt_matched_30to50ns.dat` (gmx_MMPBSA, 100 complex frames); its input trajectory `wt_30to50ns_200ps.xtc` (100 frames at 200 ps, built from the continued run) and the verbatim protocol that produced it (`analysis/wt/REGENERATE_WT_30to50ns.md`, with a control run that reproduces the deposited 0–24.8 ns value) are retained alongside it. Both windows are reported so the reader can see the sensitivity; the scan's ΔΔG values use the 0–24.8 ns reference.

| Mutant | Residue (chain) | In contact shell? | ΔG (kcal/mol) | ΔΔG (kcal/mol) |
|---|---|---|---|---|
| D141A | α1 MET141 | yes (planned hotspot) | −24.08 ± 4.29 | +13.98 ± 4.79 |
| D81A | α1 MET81 | no (5.16 nm) | −12.70 ± 3.46 | +25.36 ± 4.07 |
| E194A | γ2 ARG194 | yes (planned hotspot) | −2.95 ± 2.61 | +35.11 ± 3.38 |
| E198A | γ2 LEU198 | yes (planned hotspot) | −4.90 ± 9.78 | +33.16 ± 10.01 |
| E202A | γ2 SER202 | yes (planned hotspot) | −14.82 ± 0.95 | +23.24 ± 2.34 |
| E29A | γ2 VAL29 | no (4.95 nm) | −15.41 ± 1.73 | +22.65 ± 2.75 |

ΔΔG uncertainties are propagated from the mutant and wild-type propagated standard deviations (the gmx_MMPBSA SD(Prop.) column; the per-frame sample standard deviations printed beside it in the same outputs are larger, 4.04 to 12.00 kcal/mol) as √(SD<sub>mutant</sub>² + SD<sub>WT</sub>²); they describe within-run sampling only and are far smaller than the replica spread reported below.

A second, independently seeded replica of each of the two scans (20 ns, regenerated velocities; outputs `mmpbsa_D141A_rep2.dat` and `mmpbsa_E194A_rep2.dat` in `analysis/scan/rep2/`, with the corresponding gmx_MMPBSA logs recording the command line and the 100 processed frames) gave ΔΔG of +27.44 ± 5.44 (D141A) and +13.51 ± 6.26 (E194A) kcal/mol, differing from the first-replica estimates by 13.5 and 21.6 kcal/mol respectively. This spread, far larger than the standard deviation *within* a single run (0.95 to 9.78 kcal/mol across the six mutants, and below the spread in every case), demonstrates that the point estimates are not reliable and must be read only as a **directional ranking**, never as quantitative binding energies.

Three diagnostic conclusions follow, and each is stated only as strongly as the data allow. **(1) No distal pocket perturbation.** The per-residue binding contribution, ΔG<sub>res</sub>(i) = Complex(i) − Receptor(i), was computed across all 671 interfacial residues for every mutant. The non-mutated residues showed near-identical energy profiles across all six backgrounds (maximum absolute deviation of up to **1.00 kcal/mol**, at residue α1 140, small relative to the +14 to +35 kcal/mol ΔΔG values), with no evidence of allosteric spread or global backbone collapse. This supports the reading that the computed ΔΔG reflects a *local* perturbation at the mutated residue rather than a pocket-wide structural failure, a genuine strength of the within-computation design. **(2) Per-residue decomposition cannot localise the lost contact.** At the mutated position itself, ΔG<sub>res</sub> changed by < 1 kcal/mol in every case. The cause is the standard MM-GBSA cancellation: an alanine substitution alters the residue's self-energy in both the complex and the isolated receptor by nearly the same amount, so the difference (the binding contribution) cancels toward zero (for D81A and E29A the complex and receptor electrostatic terms were identical to three significant figures, giving ΔG<sub>res</sub> = 0 exactly). The large ΔΔG values (up to +35 kcal/mol) are therefore *not* explained by any specific lost residue–ligand contact and are more plausibly attributed to single-replica global sampling/approximation error; they are reported as directional only. **(3) Non-contact ΔΔG is pseudopositive.** D81A and E29A lie well outside the ligand contact distance, so their large positive ΔΔG (+25.36 and +22.65 kcal/mol) cannot arise from lost contact and are identified as sampling artefacts, setting a pseudopositive floor of roughly +23 to +25 kcal/mol for this design. Against that floor only γ2 ARG194 (+35.11) and γ2 LEU198 (+33.16) rise clearly above it; γ2 SER202 (+23.24) is marginal, sitting above the lower control but below the upper one, and α1 MET141 (+13.98) falls below both controls and is only 2.9 of its own propagated standard deviations. The scan therefore supports a directional signal at the two γ2 hotspots and does not support one at α1 MET141; this is a consistency check, not a quantitative attribution.

A completeness limitation must be stated. The per-residue decomposition also flags two γ2 residues outside the present scan set as strong contributors, γ2 ARG232 and γ2 ARG197 (mean Complex TOTAL −170.3 and −166.7 kcal/mol respectively across the six mutant backgrounds, against a map-wide range of +19 to −256 kcal/mol). Two caveats belong with those numbers: the residue-level Complex TOTAL is dominated by intra-residue and solvation terms that largely cancel in the binding contribution, so it ranks contacts rather than quantifying lost binding, and the largest single value in the whole map (−255.6 kcal/mol) sits at α1 residue 347, the C-terminal arginine, which is not a cavity contact at all. These two residues are therefore the first candidates for an extended scan and define the current scan set's completeness limit. All values here are computational predictions from single-trajectory MM-GBSA without an entropy term; none is a measured binding free energy. (The raw scan outputs, per-residue decomposition tables, and cross-map diagnostics are deposited in `analysis/scan/` of the reproducibility repository. The six mutant ΔG values in the table above are re-derivable from those deposits: each `decomp_<mutant>.dat` file carries a per-frame, per-residue decomposition (the `DELTAS:` section, 672 rows × 100 frames), and summing the TOTAL column within each frame and averaging over the 100 frames reproduces the tabulated value to within 1.06 kcal/mol (RMS 0.75, Pearson r = 0.9998); the recomputation is scripted as `analysis/scan/verify_ddg_from_decomp.py`. Every one of the nine binding free energies behind this table and Fig. 3 is recomputed from the deposited outputs by `analysis/scan/verify_all_dG_outputs.py`, which reproduces each tabulated value exactly: the six first-replica values by `analysis/scan/rep1/mmpbsa_<mutant>.dat`, the two independently seeded replica values by `analysis/scan/rep2/mmpbsa_D141A_rep2.dat` and `mmpbsa_E194A_rep2.dat`, and the wild-type reference used in this table (ΔG = −38.06 ± 2.14 kcal/mol, 0–24.8 ns window) by the deposited `mmpbsa_wt_100frames.dat`. The alternative 30–50 ns window value (−32.40 ± 1.73 kcal/mol, a 5.66 kcal/mol window dependence) is likewise backed by a deposited output, `analysis/wt/mmpbsa_wt_matched_30to50ns.dat`, and would shift all six ΔΔG values by the same +5.66 kcal/mol without changing their ranking. All values are accordingly reported as directional rather than quantitative.)

**Computational and experimental steps still required.** The remaining two computational tests are unchanged in design. A membrane-embedded full-pentamer simulation (α1β2γ2 with all four transmembrane segments in lipid) would test whether the cavity survives in a physiological geometry, which the present two-chain aqueous model cannot address. Replicate trajectories and the 100 ns extension now in progress would test whether the pose is robust to sampling rather than a single-trajectory observation, and longer sampling would support a proper entropy estimate. The directional signal at the two γ2 hotspots from the scan above should be extended rather than taken as quantitative: an expanded scan that includes γ2 ARG232 and ARG197, and that reports ΔΔG as a mean ± range across replicas, would convert the present directional ranking into a more defensible specificity claim. Beyond computation, the decisive tests are experimental and lie outside this study's scope: contact-residue mutagenesis with an electrophysiological readout (GABA concentration–response on α1β2γ2 wild-type and mutants, looking for a shift in EC<sub>50</sub> rather than benzodiazepine-like behaviour, with flumazenil co-administration as a *discriminator* in which failure to reverse is consistent with, not proof of, non-BZ-site action), and direct affinity measurement (microscale thermophoresis or surface plasmon resonance against an α1/γ2 interface construct). In the perioperative setting, a PSD model with sleep architecture as the primary endpoint could test jujubogenin and jujuboside B, with the site question settled by the mutagenesis and discriminator experiments just described. The present work is designed to make those experimental tests cheaper to run and easier to interpret, not to substitute for them.

### 4.6 Relation to prior in silico models of jujubogenin action

Two earlier computational studies frame the present result, and each is stated so as not to overstate agreement.

**Chen et al. (2008) predicted an orthosteric GABA-site mode.** Using a homology-model-built GABA_A receptor, Chen, Chen, Wu & Tsai (2008) reported that jujubogenin forms two hydrogen bonds with β2 Thr226 and β2 Tyr229 at the orthosteric GABA site. That prediction was made on a modelled receptor and was not validated against a crystal structure. The present study used the crystal-guided α1β2γ2 structure (PDB 6X3Z) and asked a different question: does jujubogenin preferentially occupy the benzodiazepine site, and if not, where. It did **not** test the orthosteric β2 site. The two studies are therefore orthogonal. Both are consistent with jujubogenin being a plausible GABA_A ligand, but at different sites, and the present work neither confirms nor refutes the Chen et al. (2008) orthosteric assignment.

**One point of convergence with experiment is encouraging but not confirmatory.** γ2 Ser195, which the present MD identifies as a cavity-contact residue (§3.1), is the same position that Eaton et al. (2012) used as a substituted-cysteine (loop F) probe of the α1/γ2 interface: modification of γ2(S195C) potentiated GABA-gated but not etomidate-gated current, indicating that this interface region transmits agonist-specific conformational change. That the candidate cavity contacts a residue already known to report on α1/γ2 interfacial motion is a useful cross-check. It is not proof of binding, because the experimental probe sits in the extracellular domain whereas the present cavity model spans the ECD–TMD junction, and the overlap is at the level of a single shared residue.

---

## 5. Conclusion

Jujubogenin, the aglycone metabolite of *Ziziphi Spinosae Semen* saponins, is not predicted to preferentially occupy the GABA<sub>A</sub> benzodiazepine site. Under a protocol validated by redocking flumazenil into the crystallographically defined site, an exploratory search identifies a distinct, membrane-proximal cavity at the α1/γ2 interface (25 contact residues, none shared with the classical benzodiazepine set, 23.1 Å from that site) where jujubogenin remains stably bound for 24.8 ns (ligand heavy-atom RMSD 0.42 ± 0.10 Å), although the relative preference between sites is not established by docking and requires a cavity-targeted re-dock for confirmation. Two independent computational approaches yield favourable (computed) binding estimates for this cavity (MM-GBSA ΔG −38.06 ± 2.14 kcal/mol; energy-group interaction energy −52.86 ± 4.93 kcal/mol), but both are enthalpic predictions without an entropy term and are not converged. This is a **computational, hypothesis-generating** result that localises a candidate allosteric site for a ZSS metabolite; it motivates, and does not substitute for, a cavity-targeted re-dock, affinity measurement, contact-residue mutagenesis, electrophysiological tests of allosteric modulation, and in vivo testing.

---

## Figure legends

**Figure 1.** Docked poses at the α1/γ2 interface of the human α1β2γ2 GABA<sub>A</sub> receptor (PDB 6X3Z; Cα traces of chain D = α1, chain E = γ2). **(a)** Overview: flumazenil (red; best Vina pose from the crystal-validated 20 Å box, −7.086 kcal/mol) occupies the benzodiazepine (BZ) site, whose centroid is defined by the 13 crystallographic contact residues; jujubogenin (orange; −8.324 kcal/mol) occupies a distinct membrane-proximal cavity identified in the exploratory search. The two site centroids are 23.1 Å apart. The two poses were obtained from different search boxes (§2.2), so the scores rank sites only within their respective search volumes. **(b)** Zoom on the BZ site: flumazenil best pose with the five redocking contact residues labelled (pose centroid 7.5 Å from the BZ-site centroid). **(c)** Zoom on the candidate cavity: jujubogenin docked pose with the four alanine-scan hotspot residues labelled (γ2 SER202 lies 5.0 Å from the docked pose and becomes a 4 Å contact during MD). Rendered directly from docking coordinates; no surface or cartoon representation is implied.

**Figure 2.** Stability of the jujubogenin cavity pose over the 24.8 ns explicit-solvent trajectory (PBC-imaged, backbone-superposed). Top: ligand heavy-atom RMSD (mean 0.042 ± 0.010 nm). Middle: protein backbone RMSD (mean 0.236 ± 0.032 nm). Bottom: ligand–pocket centroid distance (mean 2.086 ± 0.060 nm). Dashed lines show trajectory means. No dissociation occurs within this single trajectory; rare dissociation on longer timescales cannot be excluded.

**Figure 3.** In-silico alanine scan of the cavity hotspots (§4.5). Bars show ΔΔG relative to the wild-type reference (WT ΔG = −38.06 ± 2.14 kcal/mol, the 0–24.8 ns window whose MM-GBSA output is deposited; the 30–50 ns window, whose output is deposited as well, would shift every bar by the same +5.66 kcal/mol); error bars are standard deviations propagated from the mutant and wild-type estimates (single 20 ns replica). Blue bars: planned contact-shell hotspots; red bars: non-contact controls (α1 MET81, γ2 VAL29), whose pseudopositive ΔΔG defines the shaded sampling-artefact floor; only the two γ2 hotspots (E194A, E198A) rise clearly above that floor. Diamonds: independently seeded replicas of D141A (+27.44 ± 5.44 kcal/mol) and E194A (+13.51 ± 6.26 kcal/mol), both backed by retained outputs in `analysis/scan/rep2/`; the 13.5 and 21.6 kcal/mol differences from the first-replica estimates show that the scan is directional only.

---

## Declarations

**Ethics.** Not applicable. This study used no animals, human participants, tissues, or identifiable data; it is entirely computational. No ethics approval was required or sought, and no approval number is asserted.

**Data availability.** The full reproducibility package is deposited in the author's public repository at https://github.com/yyx-4113/ziziphi-jujubogenin-gabaA-insilico (tag v1.0.5), which contains the analysis code, input structures, and all derived products required to reproduce every reported value. The repository is organized as: `analysis/docking/` (the four Vina logs `juju_BZ_log.txt`, `flum_BZ_log.txt`, `jujubogenin_tight_log.txt`, `flumazenil_tight_log.txt`; the best poses `flum_BZ.pdbqt`, `juju_BZ.pdbqt`, `flumazenil_tight.pdbqt`, `jujubogenin_tight.pdbqt`; the prepared receptor and the source structures under `structures/`; `box_center.txt`; `docking_results.md`; and `verify_pose_geometry.py`, which reproduces the Fig. 1 pose-geometry values); `analysis/md/` (MD metrics `rmsd_final.csv` and `rmsd_final.json`, MM-GBSA `mmpbsa_r3.dat`, interaction energies `interaction_energy_summary.json` and `contact_residue_energy.json`, post-equilibration structure `npt.gro`, the source of the protein-alone radius of gyration in §3.2); `analysis/scan/` (alanine-scan ΔΔG tables `mut_ddg_results.txt` and `mut_ddg_replica_results.txt`; the gmx_MMPBSA output files of all six first replicas `rep1/mmpbsa_<mutant>.dat` and of both independently seeded second replicas `rep2/mmpbsa_<mutant>_rep2.dat`, with `rep2/gmx_MMPBSA_<mutant>_rep2.log` recording the command line and the 100 processed frames; `verify_all_dG_outputs.py`, which recomputes every binding free energy and every ΔΔG in §4.5 and Fig. 3 from those outputs; the tleap-built starting coordinates of all six mutants `rep1/complex_<mutant>.gro` and `verify_mutant_topologies.py`, which re-checks the atom-count identity behind the §4.5 build-warning note from those coordinates and from `mut_ddg_results.txt`; the per-residue decomposition files `allmode/decomp_<mutant>.dat` from which the six mutant ΔG values are re-derivable (each carries a `DELTAS:` decomposition of 672 rows × 100 frames whose per-frame TOTAL sums, averaged over the 100 frames, reproduce the tabulated values to within 1.06 kcal/mol; scripted as `analysis/scan/verify_ddg_from_decomp.py`), per-residue decomposition matrices `crossmap_complex_total.csv` and `crossmap_dG_res.csv`, `diag_summary.json`; and `verify_bz_separation.py`, which reproduces the §3.1 contact-set/BZ-set separation geometry from the deposited 6X3Z coordinates (closest Cα–Cα approach 11.0 Å between γ2 Asp192 and γ2 Tyr58; all 25 contact residues beyond 12 Å of the BZ-site centroid)); `analysis/wt/` (the 0–24.8 ns-window wild-type MM-GBSA output `mmpbsa_wt_100frames.dat`, which underlies §3.3 and supplies the deposited wild-type reference for the §4.5 scan; and, for the 30–50 ns-window value reported in §3.3 and §4.5 as a convergence and window-sensitivity check, its own output `mmpbsa_wt_matched_30to50ns.dat` (100 complex frames), the retained input trajectory `wt_30to50ns_200ps.xtc` and the verbatim regeneration recipe `REGENERATE_WT_30to50ns.md` with its control run); `figures/` (Fig. 1–3 source and renders); `scripts/` (`md2docx.py`, `verify_rg.py`, figure-generation scripts); and the manuscript source. Raw all-atom molecular-dynamics trajectories exceed 1.5 GB and exceed the repository's per-file size limit, so they are not deposited; the deposited analysis pipeline and derived products are sufficient to reproduce every number in this manuscript without them. A frozen copy of the repository, including every derived product and verification script named above, is archived at Zenodo (<https://doi.org/10.5281/zenodo.23602221>).

**Software.** AutoDock Vina 1.2.7; GROMACS 2024.5; AmberTools (acpype, antechamber, tleap); gmx_MMPBSA 1.6.5; mdtraj; NumPy; matplotlib.

**Funding.** None.

**Conflicts of interest.** None declared.

**Author contribution.** Yongxin Yang performed all docking, simulation, analysis, and writing.

---

## References

1. Song, P., Zhang, Y., Ma, G., Zhang, Y., Zhou, A., & Xie, J. (2017). Gastrointestinal absorption and metabolic dynamics of jujuboside A, a saponin derived from the seed of *Ziziphus jujuba*. *Journal of Agricultural and Food Chemistry*, *65*(38), 8331–8339. https://doi.org/10.1021/acs.jafc.7b02748

2. Jiang, J.-G., Huang, X.-J., Chen, J., & Lin, Q.-S. (2007). Comparison of the sedative and hypnotic effects of flavonoids, saponins, and polysaccharides extracted from Semen *Ziziphus jujube*. *Natural Product Research*, *21*(4), 310–320. https://doi.org/10.1080/14786410701192827

3. Jia, X., Zhang, L., Zhang, W., Zhou, Y., Song, Y., Liu, C., Yang, N., Sun, J., Sun, Z., Li, Z., Shi, C., Han, Y., Yuan, Y., Shi, J., Liu, Y., & Guo, X. (2020). Melatonin ameliorates the sleep disorder induced by surgery under sevoflurane anaesthesia in aged mice. *Basic & Clinical Pharmacology & Toxicology*, *128*(2), 256–267. https://doi.org/10.1111/bcpt.13498

4. Wang, J., Zhou, F., Zhang, X., Jia, S., Liu, H., Fei, X., Yin, L., Zhang, Z., Liu, Y., Fang, Y., Dong, H., Lu, Z., & Zhong, H. (2026). DMH glutamatergic and GABAergic neurons differentially regulate post-anesthesia sleep disturbance through CB1R signaling. *Anaesthesiology and Perioperative Science*, *4*(1), 39. https://doi.org/10.1007/s44254-026-00185-y

5. Kim, J. J., Gharpure, A., Teng, J., Zhuang, Y., Howard, R. J., Zhu, S., Noviello, C. M., Walsh, R. M., Lindahl, E., & Hibbs, R. E. (2020). Shared structural mechanisms of general anaesthetics and benzodiazepines. *Nature*, *585*(7824), 303–308. https://doi.org/10.1038/s41586-020-2654-5

6. Sigel, E., & Buhr, A. (1997). The benzodiazepine binding site of GABA<sub>A</sub> receptors. *Trends in Pharmacological Sciences*, *18*(11), 425–429. https://doi.org/10.1016/S0165-6147(97)01118-8

7. Yang, R.-Z., Lin, S., Huang, L.-T., Weng, J., Liu, Q.-M., Chen, H.-S., Ruan, N., & Zeng, K. (2026). Effect of targeted probiotics on anesthesia-induced sleep disturbances via modulating the gut microbiome and metabolites. *Food Science & Nutrition*, *14*(1), e71447. https://doi.org/10.1002/fsn3.71447

8. Trott, O., & Olson, A. J. (2010). AutoDock Vina: improving the speed and accuracy of docking with a new scoring function, efficient optimization, and multithreading. *Journal of Computational Chemistry*, *31*(2), 455–461. https://doi.org/10.1002/jcc.21334

9. Eberhardt, J., Santos-Martins, D., Tillack, A. F., & Forli, S. (2021). AutoDock Vina 1.2.0: new docking methods, expanded force field, and Python bindings. *Journal of Chemical Information and Modeling*, *61*(8), 3891–3898. https://doi.org/10.1021/acs.jcim.1c00203

10. Abraham, M. J., Murtola, T., Schulz, R., Páll, S., Smith, J. C., Hess, B., & Lindahl, E. (2015). GROMACS: high performance molecular simulations through multi-level parallelism. *SoftwareX*, *1–2*, 19–25. https://doi.org/10.1016/j.softx.2015.06.001

11. Lindorff-Larsen, K., Piana, S., Palmo, K., Maragakis, P., Klepeis, J. L., Dror, R. O., & Shaw, D. E. (2010). Improved side-chain torsion potentials for the Amber ff99SB protein force field. *Proteins*, *78*(8), 1950–1958. https://doi.org/10.1002/prot.22711

12. Wang, J., Wolf, R. M., Caldwell, J. W., Kollman, P. A., & Case, D. A. (2004). Development and testing of a general Amber force field. *Journal of Computational Chemistry*, *25*(9), 1157–1174. https://doi.org/10.1002/jcc.20035

13. Valdés-Tresanco, M. S., Valdés-Tresanco, M. E., Valiente, P. A., & Moreno, E. (2021). gmx_MMPBSA: a new tool to perform end-state free energy calculations with GROMACS. *Journal of Chemical Theory and Computation*, *17*(10), 6281–6291. https://doi.org/10.1021/acs.jctc.1c00645

14. McGibbon, R. T., Beauchamp, K. A., Harrigan, M. P., Klein, C., Swails, J. M., Hernández, C. X., ... & Pande, V. S. (2015). MDTraj: a modern open library for the analysis of molecular dynamics trajectories. *Biophysical Journal*, *109*(8), 1528–1532. https://doi.org/10.1016/j.bpj.2015.08.015

15. Chen, C. Y.-C., Chen, Y.-F., Wu, C.-H., & Tsai, H.-Y. (2008). What is the effective component in suanzaoren decoction for curing insomnia? Discovery by virtual screening and molecular dynamic simulation. *Journal of Biomolecular Structure and Dynamics*, *26*(1), 57–64. https://doi.org/10.1080/07391102.2008.10507223

16. Eaton, M. M., Lim, Y. B., Bracamontes, J., Steinbach, J. H., & Akk, G. (2012). Agonist-specific conformational changes in the α1/γ2 subunit interface of the GABA_A receptor. *Molecular Pharmacology*, *82*(2), 255–263. https://doi.org/10.1124/mol.112.077875

17. Fan, C., Cowgill, J., Howard, R. J., & Lindahl, E. (2024). Divergent mechanisms of steroid inhibition in the human ρ1 GABA_A receptor. *Nature Communications*, *15*(1), 7795. https://doi.org/10.1038/s41467-024-51904-7
