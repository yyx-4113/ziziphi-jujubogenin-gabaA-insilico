# Round 5 — Independent Expert Review & Editorial Report

**Manuscript:** "Jujubogenin does not preferentially engage the GABA_A benzodiazepine site: an in silico study of a candidate allosteric cavity at the α1/γ2 interface (membrane-absent model)"
**Repository:** https://github.com/yyx-4113/ziziphi-jujubogenin-gabaA-insilico
**Target journal:** Journal of Molecular Graphics and Modelling (Elsevier), ISSN 1093-3263
**Version under review:** v1.0.10 (tag cc5d81d; Zenodo 23764756, concept 23602221)
**Version produced by this round:** v1.0.11 (local tag; the tag also covers this review report and the self-excluding MANIFEST regenerator) — remote push and Zenodo new-version deposition are pending network access (see §8).

---

## 1. Review process and independence

A four-panel independent review was convened using the standing independence rules:
the panels were instructed **not** to read any prior-round review artifact
(`REVIEW_round*`, `RESPONSE_*`, `REVISION_*`, prior `submission/` material, or the
Round 4 gate script), and to treat only the manuscript, the reproducibility
repository (`analysis/`, `scripts/`, `manuscript/`, `README.md`, `MANIFEST.md`)
and the deposited gmx_MMPBSA outputs as ground truth. Each panel returned the
same four-part contract — **【Problem】/【Evidence】/【Why it matters】/
【Specific fix】** — plus a mandatory appendix (§ Stands up / § Questions /
§ What I checked).

Panels:
- **A1 — Domain (GABA_A pharmacology / in-silico binding)**: validity of the BZ-site
  non-preference claim, membrane-cavity interpretation, literature grounding.
- **A2 — Design & statistics**: numerical reproducibility of every reported ΔG/ΔΔG,
  uncertainty-column meaning, window-sensitivity arithmetic, controls.
- **A3 — Implementation & reproducibility**: whether every number is re-derivable from
  deposited files, MANIFEST completeness, git-tracking integrity.
- **A4 — Venue (JMGM) fit**: formatting hard limits (Abstract ≤250 words, Highlights
  ≤85 chars, Graphical Abstract 531×1328 px), honesty of reporting, submission-package
  consistency.

---

## 2. Panel findings (condensed)

### A1 — Domain
- **Must-fix 1 (membrane caveat).** The headline "membrane-proximal cavity" is read off
  a model that contains **no membrane and no M4 helix** (disclosed in the body at
  §2/§4.4/§5). A skimming reader can be misled into thinking a lipid bilayer was
  present. *Fix:* demote the claim at the title level and keep the body disclosures.
- **Must-fix 2 (motivation grounding).** The "jujubogenin is the GABA_A-modulating
  species" motivation leans on Song 2017, an ADME/bioavailability paper, for the
  receptor-modulation premise. Reframe as a *plausible hypothesis* rather than an
  established fact (the manuscript already hedges this at §1.2; the fix is to keep it
  strictly hypothesis-framed).
- **Must-fix 3 (missing grounding citations).** A few claims (e.g., transmembrane/
  ECD–TMD pockets at β+/α− and γ+/β−) rest on the single Fan 2024 cite without a
  second structural anchor.
- **Must-fix 4 (§3.1 "spatially separate" over-claim).** The centroid metric (>12 Å)
  is buttressed by an 11.0 Å closest-residue metric; the word "separate" should be
  qualified as "separate by the centroid metric."
- **Must-fix 5 (cavity-targeted re-dock).** The abstract's "site preference is
  unestablished" is correct, but the recommended cavity-targeted re-dock should be
  named as the decisive confirmatory step (it is, in §4.5 future work).
- **Must-fix 6 (Eaton 2012 wording).** The §5 Eaton cross-check is already precise
  ("not proof of binding… overlap at the level of a single shared residue"); keep as is.

### A2 — Design & statistics
- **P1 (uncertainty column).** The ± quoted in §4.5 is the gmx_MMPBSA **SD(Prop.)**
  (propagation-formula) column, **not** the per-frame sample SD. SD(Prop.) is ~2×
  more optimistic than the sample SD (e.g., 4.29 vs 7.03 for M141A). The manuscript
  must keep the column identity explicit (it does) — no change required, but flagged as
  a reading trap.
- **P2 (§4.5 retraction not fully consistent).** §4.5(3) states "No residue-level
  hotspot conclusion is defensible," yet the same section's future-work sentence and
  the Fig. 3 caption still call R194A/L198A "two γ2 hotspots." The R194A replica flips
  across the pseudopositive floor (+35.11 vs +13.51), so the directional reading is not
  stable. *Fix:* soften "hotspots" → "residues" where the retraction applies.
- **P3 (README sign error).** README states re-referencing the scan to the 30–50 ns
  window shifts every ΔΔG by **+5.66** kcal/mol. Arithmetic: ΔΔG = ΔG_mut − ΔG_WT;
  replacing WT −38.06 with WT −32.40 makes every ΔΔG **smaller by 5.66** (−5.66), not
  larger. The manuscript (§4.5, Fig. 3) and `verify_all_dG_outputs.py` both use −5.66;
  only the README is wrong. *Fix:* −5.66.
- **P4 (docking-validation completeness).** Flumazenil was re-docked into 6X3U, not
  6X3Z; no ligand heavy-atom RMSD was reported for the jujubogenin pose. Honesty gap,
  not an error.
- **P5 (no negative/decoy control).** A scrambled or decoy pose was never scored; the
  −4.403 BZ score is interpreted only by contrast with flumazenil. Documented as a
  limitation.
- **P6 (exploratory cavity search).** The cavity was found by a single mis-centred
  heuristic box; this must remain explicitly "exploratory / hypothesis-generating."
  (It is.)
- **P7 (30–50 ns window is not an independent replicate).** It is a continued-trajectory
  window of the same WT run, not a second sampling; the manuscript already frames it as
  a convergence/window-sensitivity check.

### A3 — Implementation & reproducibility
- **P1 (six `complex_*.gro` not in MANIFEST / not git-tracked).** README §Provenance
  claims the six tleap-built mutant starting coordinates are "artifact-backed" and
  deposited, but (a) they were untracked by git (`.gitignore` had `*.gro` with only
  `npt.gro` un-ignored), and (b) they were absent from `MANIFEST.md`. A reader following
  "SHA-256 verified" cannot obtain or verify them. **This is a real integrity defect.**
  *Fix:* un-ignore + `git add` the six files and SHA-256 list them in MANIFEST.
- **P2 (§4.5 line 217 wording).** Same as A2-P2.
- **P3 (docking_results.md "21.46 Å" vs manuscript "21.5 Å").** On inspection this was a
  misread of different quantities (box size vs pose centroid distance); no action.

### A4 — Venue (JMGM)
- **CORRECTION (discovered after Round 5).** The JMGM-mandatory Graphical Abstract (531×1328 px) was **absent** from the repository at Round 5; the A4 panel's "compliant" finding relied on a non-existent `submission/` path and was erroneous. It has since been created (`figures/GraphicalAbstract.png`, opaque RGB 531×1328 px; vector source `figures/GraphicalAbstract.svg`; generator `scripts/make_graphical_abstract.py`) and added to the repository and MANIFEST. Title-page word count (8,061), reporting honesty, cover-letter consistency, and declarations are otherwise compliant.
- Submission-package housekeeping notes (the v1.0.10 `submission_checklist.md` had said
  "Springer" for an Elsevier journal and "14 references" for 17) — these were already
  corrected in v1.0.10; no re-flag needed.
- Abstract is 248 words (≤250; independently re-counted including the keyword line) and Highlights in the manuscript body are 72/66/78/75/82
  characters (≤85) — compliant.

---

## 3. Editor's independent verification of the three substantive defects

Before integrating, the editor re-derived each finding from source rather than trusting
the panel assertion:

1. **README sign (A2-P3).** Recomputed: ΔΔG_new − ΔΔG_old = (−32.40) − (−38.06) = −5.66.
   Confirmed the README's "+5.66" contradicts the manuscript, the Fig. 3 caption, and
   `verify_all_dG_outputs.py` (which prints the 30–50 ns re-referenced values
   +8.32/+19.70/+29.45/+27.50/+17.58/+16.99). **Defect confirmed.**
2. **§4.5 hotspot contradiction (A2-P2 / A3-P2).** Read §4.5(3) ("No residue-level
   hotspot conclusion is defensible") against line 217 ("the two γ2 hotspots") and the
   Fig. 3 caption ("the two γ2 hotspots (R194A, L198A)"). The contradiction is real and
   the retraction must win. **Defect confirmed.**
3. **Six `.gro` missing (A3-P1).** `git ls-files | grep complex_*.gro` → 0; the files
   exist on disk under `analysis/scan/rep1/` but were untracked and absent from
   MANIFEST. **Defect confirmed.**

---

## 4. Adjudicated must-fix list and disposition (v1.0.11)

| # | Finding | Disposition | Applied in |
|---|---------|------------|-----------|
| A1-1 | Membrane caveat at title | **Applied** | manuscript title, README l.3, CITATION title, + "membrane-absent model" |
| A1-2 | Hypothesis framing of motivation | **No code change** — §1.2 already hypothesis-framed ("site of engagement is an output to be determined"); left intact to avoid speculative rewording |
| A1-3 | Second structural citation | **Deferred** — additive, not blocking; noted as optional tightening |
| A1-4 | Qualify "spatially separate" | **No change** — §3.1 already reports both metrics (centroid >12 Å; closest 11.0 Å) explicitly |
| A1-5 | Name cavity-targeted re-dock as decisive | **Already present** in §4.5 future work; no change |
| A1-6 | Eaton wording | **No change** — already precise |
| A2-P1 | SD(Prop.) vs sample SD | **No change** — column identity already explicit |
| A2-P2 | §4.5/Fig 3 "hotspots" vs retraction | **Applied** | §4.5 l.217, Fig 3 caption l.241 → "residues" |
| A2-P3 | README +5.66 → −5.66 | **Applied** | README l.92 + v1.0.11 note |
| A3-P1 | Track + MANIFEST the six `.gro` | **Applied** | `.gitignore`, `MANIFEST.md`, `git add`, `.gitattributes` |
| A3-P2 | §4.5 wording | same as A2-P2 | |
| A4 | Formatting / submission package | **Verified compliant**; prior housekeeping already fixed in v1.0.10 |

**Net applied edits:** title membrane-absence caveat; §4.5/Fig 3 "hotspots"→"residues";
README sign correction + version note; Data-availability tag v1.0.10→v1.0.11;
six mutant `.gro` tracked and SHA-256 listed; MANIFEST regenerated (78 rows,
0 self-mismatches); manuscript.docx regenerated.

---

## 5. Verification after edits

All six repository verification scripts were re-run and pass (exit 0):
- `analysis/scan/verify_all_dG_outputs.py` — every ΔG, ΔΔG, both WT windows, both
  replicas recomputed exactly from retained outputs.
- `analysis/scan/verify_mutant_topologies.py` — now reads the six tracked `complex_*.gro`
  and confirms atom-count identity for all six mutants.
- `analysis/scan/verify_bz_separation.py` — §3.1 contact/BZ separation reproduced
  (closest Cα–Cα 11.01 Å at γ2 Asp192).
- `analysis/scan/verify_ddg_from_decomp.py` — six ΔG re-derivable from per-residue
  decompositions (RMS 0.75, r = 0.9998).
- `analysis/scan/verify_block_replicate.py` — block-agreement check.
- `scripts/verify_rg.py` — protein radius of gyration recomputed (3.46 nm).

MANIFEST self-consistency: every listed file's SHA-256 and byte count equals the
git index blob (78/78, 0 mismatches). Because `.gitattributes` now pins text to LF,
these SHAs are stable on a fresh clone regardless of the host's `core.autocrlf`.

---

## 6. Residual limitations (carried forward, not new)

None introduced by this round. The manuscript remains explicitly: single 24.8 ns
trajectory; no replicate for the primary pose; no membrane/M4; alanine scan
exploratory and directional only; single-trajectory MM-GBSA without entropy; all
energetics are computational predictions, not measured affinity/efficacy/function.

---

## 7. Round 6 (consistency) pass

A final read of the changed sections confirmed coherence: the title caveat is mirrored
in README and CITATION; the §4.5 retraction is now consistently reflected in the future
work sentence and Fig. 3 caption; the Data-availability tag matches the tag that will
be pushed. No new inconsistency was introduced.

---

## 8. Status and remaining steps

**Done locally:** v1.0.11 committed and tagged locally (`v1.0.11`, on the Round 5 release commit that also includes `review_round5.md`, the self-excluding `regenerate_manifest.py`, and the JMGM-mandatory Graphical Abstract `figures/GraphicalAbstract.png`/`.svg` with its generator `scripts/make_graphical_abstract.py`); all six verification scripts green; MANIFEST regenerated and self-consistent (every listed file's SHA-256 and byte count equals the git index blob; stable across machines via `.gitattributes` LF pinning).

**Pending (environment network is currently blocked — outbound HTTPS returns timeout /
502):** (a) `git push origin master v1.0.11` to GitHub; (b) create the Zenodo new
version of deposit 23764756 (concept 23602221) that includes the six newly tracked
`complex_*.gro` and the changed files, then publish and verify. Both must be re-run when
network access is available; the local tree already contains everything the deposit
needs.
