# Hostile review of C1 (rnd/stepback/C1.md and rnd/stepback/c1/)

*26 Nov 2026, America/New_York. Independent hostile review. Local note only: nothing committed or pushed, no email sent, THEORY.md and CORE.md untouched, C1.md not edited. Repo context was read from a fresh clone of `forge-rnd-record-cost-2` at `a57f1f7` (CORE.md, the T63 entries in `theory/PHYSICS_CHAIN_2026-11-23.md`) and from STEPBACK.md (row C1, §5, and the wording note C9-5). Every number below is **OBSERVED** output of the scripts in this folder unless it is labelled otherwise. The review reuses `c1_vacua.Vacuum` only after checking it independently (item 1).*

## Overall: **PASS-WITH-FIXES**

The numerics are right. The entropies, vacua, k-grid, greedy rule and criteria code all reproduce, and the scored outcomes in the §2 table stand as written: SP is an open miss 4/4, V3/V4 pass H1-2D and ISO, and V1/V2 miss both. Three readings built on those numbers do not hold as worded (H1–H3 below), and the C1′ score is too high (M5). None of the fixes changes a scored pass or miss.

## What was checked and holds

1. **Correlation-matrix entropies (Q1).** `rv_verify.py` / `rv_verify.out`:
   - Exact many-body diagonalisation on a 4×4 torus (N = 8, sparse Fock-space Hamiltonian, explicit fermion-sign reduced density matrix) against the correlation-matrix formula used by `S_bits`. S(T) and S(T + 2 sites) agree to 10 digits for π-flux m = 0.5, NN m = 0.5 and π-flux m = 0 (antiperiodic).
   - C1's k-space vacua against an independent real-space diagonalisation (64×64 sites, antiperiodic) on four regions (T, T + ring, a far pair, a diagonal strip). Gapped V2 and V4 agree to ≤ 3×10⁻⁸ bits. Critical V3 agrees to ≤ 2×10⁻⁴ and V1 to ≤ 2.4×10⁻², which is the finite-size error of the 64-site check, not of C1's K = 256 grid (see item 3).
2. **π-flux gauge and masses (Q2).** The y-bond sign (−1)^x gives flux π in every plaquette. A second, independent gauge (x-bond sign (−1)^y) gives identical entropies to all printed digits. The staggered mass gaps both families at min|E| = 0.500 = m, as expected for a sublattice-odd mass on a bipartite lattice. Filling is exactly 0.5 in all four vacua.
3. **k-grid (Q2).** The twisted grid (offsets 0.31, 0.67) converges. Along the published greedy sequences, gains at K = 256 and K = 1024 differ by at most 6.9×10⁻⁴ relative (V1, median 1.5×10⁻⁴) and 1.0×10⁻⁵ (V3) (`rv_kconv.out`). The stored gains are recomputed exactly. V1 at K = 256 has a residual |Im P| ≤ 7.7×10⁻⁴: the twist breaks the k ↔ −k pairing. It falls with K (1.9×10⁻⁴ at K = 1024) and does not move any criterion.
4. **Greedy well defined (Q3).** Exact ties are common: 27 (V1), 42 (V2) and 15 (V3) of the first 120 steps have more than one candidate within 10⁻¹⁰ of the best, mostly symmetry orbits. Reversing the tie rule (lexicographically last instead of first) gives the same first-120 set in V1 and a symmetric image with identical criteria in V2 and V3 (κ_min, |S|, fill, iso, ρ_in and ρ_out all identical) (`rv_analyze.out`). Widening the window to Chebyshev 6 gives the identical order in V1 and V3, which extends C1's own window check from V4. The prefix rule and κ_min = min(g[:120]) are implemented as §1 states.
5. **Criteria reproduced (Q4).** An independent re-implementation of fill, ISO, ρ_in and ρ_out (`rv_analyze.py`, ConvexHull instead of Delaunay) reproduces every §2 table entry.
6. **Species identity (Q7).** I(T^⊗n : S^⊗n) = n·I(T:S) for independent copies, so the greedy order is unchanged and record(κ, n) = record(κ/n, 1): **ELEMENTARY**, correct. C1's check is a code identity, as the note says. A genuine check (greedy on the block-diagonal n = 2 correlation matrix, 40 steps, V3) gives the identical order with max |g₂ − 2g₁| = 1.2×10⁻¹³ (`rv_species_aniso.out`).
7. **DOIs (Q9).** All 11 DOIs in C1.md §4 resolve on Crossref with matching authors, year and venue (`rv_crossref.txt`). So do 16 more listed under M4.

## High

**H1. V1/V2 are not "checkerboard" or "sublattice-selective", and their edges are not ragged.** The §2 caveat (b), the §5 label "ragged (sublattice-selective)" and open item 3 describe a record that is "sharp on one sublattice and empty on the other". The records do not look like that (`rv_map.out`):
- The V1 and V2 records at κ_min are solid, sharp-edged **X shapes** with four arms along the diagonals and empty wedges along the axes.
- The odd-(x+y) fraction of S is 0.483 (V1) and 0.496 (V2), so both sublattices are filled equally.
- Fill is 0.48/0.66 because the shape is **non-convex**: the convex hull includes the empty axis wedges.
- The parity zeros cannot be the cause. V3 has the same zeros (|C(0,r)| ≤ 9×10⁻¹⁹ at even x+y; `rv_verify.out`), yet V3's record is compact (fill 0.97).

The cause is the flat, nested Fermi surface. Single-site I(T:site) along the diagonals exceeds that along the axes by 18× at r = 6 and 109× at r = 24 in V1, and by 76× to 7×10⁶ in V2 (`rv_decay2.out`), so the cost buys diagonal arms.

**Fix:** relabel V1/V2 as "sharp-edged, non-convex (X-shaped, diagonal arms)". The scored H1-2D open miss stands, because §1 fixed fill ≥ 80% as part of "sharp", but the reading "ragged / fuzzy / checkerboard" is withdrawn. Retarget open item 3 from a parity-aware fill to a convexity-independent sharpness measure, for example edge width along rays. Remove "half filling zeroes C at even x+y" as a reason in the §1 expectation (see L2).

**H2. Lemma C1-FOC is stated as a two-sided bracket; only the addition side holds for the final record. The "stationarity at the margin" bridge sentence is false as worded.**
- The literal statement is true: the last site added had gain ≥ κ *when it was added*, and the best next site has gain < κ.
- But "the single-site marginal at the cut brackets κ" and "Lemma C1-FOC is the discrete counterpart … stationarity at the margin" read as statements about the final record. In all four vacua, the record at κ_min contains a boundary site whose **removal** costs only 0.974κ (V1, site (1,5)), 0.974κ (V2), 0.911κ (V3) and 0.940κ (V4) (`rv_pairs.out`). Deleting it raises J = I − κ|S|.
- So the greedy record is not a local optimum of the cost even against single-site moves. Later additions make earlier sites partly redundant.
- On the addition side: no pair among the top-40 single candidates beats 2κ (best 1.73–1.96κ), so the addition inequality held in the moves tested.

**Fix:** restate C1-FOC as "greedy stopping guarantees max_q ΔI(q | S) < κ only; deletion marginals of boundary sites can be < κ (observed 4/4)". Change the Jacobson paragraph to "no single-site addition improves the cost". Drop "stationarity". The bridge label stays HYP and becomes narrower. If a stationary record is wanted, use greedy plus a deletion/swap pass (local search) and say so.

**H3. The isotropy hypothesis as worded ("set by the vacuum's low-energy (Lorentz-like) symmetry") is not supported by this design, because the shape test cannot separate it from alternatives.**
- **Control (post hoc, unscored).** NN hopping at μ = −2 (filling 0.185) is non-relativistic and has no Dirac cones. Its single-site mutual-information contours are anisotropic: diagonal/axis ratio 2.26–2.47 at r = 6–24, stable with r, which is about 1.3× in radius given the r⁻³ decay. Yet its greedy record at |S| = 128 passes ISO (iso 0.115, diag/axes 1.12) and fill (1.00) as cleanly as V3 (`rv_analyze.out`, `rv_decay2.out`, `rv_map.out`).
- So at |S| ≈ 120, the greedy record under-reports a roughly 30% correlation anisotropy as roughly 12%, and a non-Lorentz vacuum passes.
- **What survives, and is not a sublattice artifact.** V3/V4 correlations really are isotropic beyond the lattice scale. Wedge-averaged single-site I(T:site), diagonal/axis, is 1.00, 0.98, 1.00 and 0.97 at r = 8, 12, 16 and 24 in V3, and 1.02, 0.88, 1.00 and 0.87 in V4. It is 0.6 at r = 6, a lattice effect. The sublattice zeros are the same as in V1 (H1).

**Fix:** reword the HYP to "the record's shape follows the anisotropy of the vacuum's correlations, and at reachable sizes the greedy record compresses it". Withdraw "Lorentz-like" as the identified input. In this sample, "Dirac vs not" is confounded with "nested square Fermi surface vs not". The STEPBACK reading ("anisotropy → isotropy/Lorentz named as the input") needs a vacuum that is isotropic but not Lorentz-like to tell the two apart, and that vacuum also passes.

## Medium

**M1. Criterion drift in H1-2D's radial weight (no effect on scores).** §1 says "radial weight about the plaquette centre, as in G4-1". G4-1 scheme A used the **indicator of T∪S** (rnd/forces-gravity/NOTE.md H1; `g4_1_horizon.py`: `w[U]=1`). `c1_analyze.py` uses the **greedy gains on S only**, labelled "proxy". With the G4-1 weight, r99 − r90 is 2.09 / 0.61 / 0.48 / 0.48 (V1–V4), so the r-part passes everywhere. V1/V2 still miss H1-2D on fill, V3/V4 still pass, and the scores are unchanged. **Fix:** disclose the drift in §2 and report both values. Caveat (c) then becomes "the r-test is non-binding under either weight".

**M2. ISO resolution is coarse at these sizes.** Ideal digital shapes scored with the same metric (`rv_analyze.out`):
- a digital disc scores iso 0.124 (n = 40), 0.120 (80) and 0.062 (120);
- a **1.25:1 ellipse scores 0.129 at n = 80 and passes**;
- a diamond scores 0.176 at n = 80 and passes;
- an axis-aligned square fails at every size (0.34–0.45);
- a 2:1 ellipse fails (0.59–0.83).

So an ISO pass means "not square or 2:1", not "isotropic within 20%". The V3/V4 values at n = 40 (0.124) equal the digital-disc floor. **Fix:** state the floor next to the table, and in any later shape test compare against the digital-disc baseline at the same n.

**M3. The SP open miss stands, but the reading under-reports what the layer numbers show (post hoc, unscored).**
- In all 16 vacuum × target cases, ρ_out < 1 < ρ_in: 0.37–0.74 and 1.28–3.25.
- For a non-submodular set function, that inequality pair, not an equality, is the form a discrete shadow price can take: removing the inner layer is not worth it, and adding the outer layer is not worth it.
- §1 asked for equality within 20%, which is a fair pre-stated test, and it is an open miss 4/4.

**Fix:** add one sentence. The layer-level inequalities ρ_out < 1 < ρ_in hold in 16/16 cases (OBSERVED post hoc, unscored), while the price band they leave is wide (0.4–3.3κ), so no per-site boundary price is pinned. Do not rescore.

**M4. Missed prior art.** All entries below were verified on Crossref this session (`rv_crossref.txt`).
- **Greedy mutual-information subset selection with per-element cost is standard.** Guestrin, Krause & Singh 2005, "Near-optimal sensor placements in Gaussian processes", ICML '05 265–272, 10.1145/1102351.1102385. Its guarantees rest on submodularity (Nemhauser, Wolsey & Fisher 1978, Math. Program. 14:265, 10.1007/BF01588971). Mutual information is not submodular in general, which is the same complementarity C1 measures (ρ_in > 1) and the reason H2 happens. C1 should cite both and frame C1-FOC as the known greedy stopping property.
- **Spatial distribution of entanglement.** Chen & Vidal 2014, "Entanglement contour", J. Stat. Mech. P10011, 10.1088/1742-5468/2014/10/P10011 (contour for free fermions, the closest to a "per-site share"). Coser, De Nobili & Tonni 2017, J. Phys. A 50:314001, 10.1088/1751-8121/aa7902. Tonni, Rodríguez-Laguna & Sierra 2018, J. Stat. Mech. 043105, 10.1088/1742-5468/aab67d. Botero & Reznik 2004, PRA 70:052329, 10.1103/PhysRevA.70.052329. Kudler-Flam, MacCormack & Ryu 2019, J. Phys. A 52:325401, 10.1088/1751-8121/ab2dae. Wen 2018, PRD 98:106004, 10.1103/PhysRevD.98.106004. Klein Kvorning, Herviou & Bardarson 2022, SciPost Phys. 13:080, 10.21468/SciPostPhys.13.4.080 (local information per site and scale).
- **2D free-fermion entanglement, Fermi surface vs Dirac.** Li, Ding, Yu, Roscilde & Haas 2006, PRB 74:073103, 10.1103/PhysRevB.74.073103. Barthel, Chung & Schollwöck 2006, PRA 74:022329, 10.1103/PhysRevA.74.022329. Swingle 2010, PRL 105:050502, 10.1103/PhysRevLett.105.050502. Mutual information for free fermions: Bernigau, Kastoryano & Eisert 2015, J. Stat. Mech. P02008, 10.1088/1742-5468/2015/02/P02008. Reviews: Casini & Huerta 2009, J. Phys. A 42:504007, 10.1088/1751-8113/42/50/504007; Peschel & Eisler 2009, J. Phys. A 42:504003, 10.1088/1751-8113/42/50/504003. π-flux origin: Affleck & Marston 1988, PRB 37:3774, 10.1103/PhysRevB.37.3774.
- **Not found.** A limited search found no paper on greedy, per-site-priced region selection for I(T:S) around a fixed tracker in lattice vacua. C1's "novelty: low" stands, and the FOC part has no novelty.

**M5. C1′ (ellipse test) is well posed only after fixes, and its score is too high.**
- **The continuum half is already answered, in seconds.** Anisotropic π-flux with t_y = 0.5 predicts aspect v_x/v_y = 2. The equal-mutual-information contour aspect of single sites is 1.68, 1.80, 1.90, 1.97 and 1.95 at r_y = 4, 6, 8, 12 and 16, and 1.00 at every radius for t_y = 1 (`rv_species_aniso.out`; the r_y = 24 entry is beyond the computed range and is discarded). A hit on "the record tracks the light-cone metric" is therefore mostly settled by correlations alone, plus the continuum's coordinate rescaling (known).
- **What C1′ would actually measure** is the greedy record's compactness bias. Per H3, at |S| ≈ 120 the greedy record compresses a 1.3× anisotropy to about 1.12×.
- **Required before running:** a pre-fixed aspect estimator (for example the second-moment tensor of T∪S, or ray extents); a tolerance; the target |S| or radius; a t_y = 1 control; and the correlation-only contour aspect as the baseline the record is compared with.
- **Rescore:** p ≈ 0.35 that the record reaches within 15% of v_x/v_y at reachable sizes; V_hit ≈ 2 (the contour part is known); p_miss ≈ 0.55; V_miss ≈ 1.5 (it quantifies the greedy compression already seen in H3). Cost ≈ 3 h. EIV ≈ 1.5, so **≈ 0.5/h**, with a range of 0.4–0.6, down from 0.75. A cheaper first step is the correlation-only contour test above, which is already done.

## Low

- **L1.** The run note "V1 has exact zero modes on the twisted grid (min|E| = 0 at K = 128)" is false. min|E| = 3.1×10⁻⁵, 7.7×10⁻⁶, 1.9×10⁻⁶ and 4.8×10⁻⁷ at K = 64, 128, 256 and 512. The twist avoids every exact zero, the occupation is unambiguous, and S(T) converges (2.90402359 → 2.90402980, K = 256 → 512). Open item 5 can be closed. (The real-space antiperiodic 64×64 check does have 128 exact zero modes, but that is a property of that check, not of C1's grid.)
- **L2.** The §1 expectation gives "half filling zeroes C(x, y) at even x + y" as a reason V1 fails ISO. The same zeros hold in V3 (H1), so they are not a reason. The square Fermi surface is.
- **L3.** No script in `c1/` produces `c1_checks.out` (the window check and the species check), so those lines cannot be reproduced from the folder. Add the script.
- **L4.** "§1 written 09:56, before any C1 code" is self-attested and not hash-locked. The file mtimes (`c1_vacua.py` 09:57) are consistent with it. §1 does call itself exploratory, so this is disclosure only.
- **L5.** Wording. C1.md uses the reserved word (the one kept for the CORE.md:7 sentence only) in "area-…" phrases: the §3 Jacobson paragraph, the §4 table roles and the §5 last line. STEPBACK C9-5 already asks for "area scaling" in anything carried toward the repo. Paper titles cited verbatim can keep their own wording.
- **L6.** In V2 at κ_min, the sector radii (4.27 / 4.03 / 4.14 on the axes) show symmetry broken by a partial orbit at the prefix cut. This is harmless, but it means iso carries about ±0.03 of tie noise in V2.
- **L7.** Caveat (a) is right that lattice effects are large, but it is not specific. See Q5 below for which conclusions survive.

## Q5: do lattice effects at radius 7–8 undermine every conclusion?

No. Taking each conclusion in turn:
- **SP open miss.** Robust. It is structural non-additivity, present at every target from |S| = 40 to 160.
- **V1/V2 anisotropy.** Robust and growing with r. The diagonal/axis mutual-information ratio rises from 18 to 109 between r = 6 and 24 in V1.
- **V3/V4 isotropy of correlations.** Supported independently at r = 8–24.
- **"ISO pass means isotropic, and Lorentz is the input."** Not supported at this size (H3, M2).
- **V1/V2 "ragged".** A concavity effect of the fill measure, not a lattice-noise effect (H1).

## Corrected labels (to replace C1.md §5 where they differ; append, do not rewrite)

- **ELEMENTARY:**
  - C1-SP, record(κ, n) = record(κ/n, 1). Confirmed, including a genuine block-diagonal n = 2 run.
  - C1-FOC, **addition side only**: max_q ΔI(q | S) < κ at the stopping point. It is the known greedy stopping property (M4). The deletion side fails 4/4 (OBSERVED, H2).
- **OBSERVED (scored per §1, unchanged):** SP is an open miss 4/4. V3/V4 pass H1-2D and ISO. V1/V2 are open misses on H1-2D (fill) and ISO.
- **OBSERVED (descriptive, corrected):**
  - V1/V2 records are sharp-edged, non-convex X shapes with diagonal arms (diag/axes 1.70 / 1.60), not checkerboards.
  - V3/V4 single-site mutual information is isotropic within 3% (V3) and 13% (V4) for r = 8–24.
  - The window check passes on V1, V3 and V4.
  - The tie rule does not affect any criterion.
- **OBSERVED (post hoc, unscored):**
  - ρ_out < 1 < ρ_in in 16/16 cases.
  - The greedy record is not deletion-stable (4/4).
  - The non-relativistic NN μ = −2 control passes ISO and fill.
  - In the anisotropic π-flux, single-site contour aspect approaches v_x/v_y (1.68 → 1.97).
- **HYP (narrowed):**
  - The record's shape follows the vacuum's correlation anisotropy, and greedy records at |S| ~ 10² compress it. "Lorentz-like symmetry is the input" is withdrawn as not separable by this design.
  - Anything beyond "no single-site addition improves the cost" as an analogy to Jacobson 2016.
- **CHOSEN:** unchanged, plus a disclosure: the H1-2D radial weight is the greedy gains, not the G4-1 indicator (M1).
- **Rank effect:** C1′ ≈ 0.5/h (M5), which moves it below C12b-A ≈ 0.67. C1 as a route needs no further units.

## Files (this folder, all local)

`rv_verify.py/.out` (ED, real-space, gauge, zero modes) · `rv_kconv.py/.out` · `rv_greedy.py`, `rv_greedy_mu.py`, `rv_*.json`, `rv_*.log` (tie, window and μ = −2 reruns) · `rv_analyze.py/.out` (independent criteria, baselines) · `rv_map.py/.out` · `rv_decay.py/.out`, `rv_decay2.py/.out` · `rv_pairs.py/.out` · `rv_species_aniso.py/.out` · `rv_crossref.py`, `rv_crossref.txt`.
