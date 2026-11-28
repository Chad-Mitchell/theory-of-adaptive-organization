# Preregistration: internal-model keystone for rhythms, plus fractal and cymatics checks

**Locked:** Friday 20 November 2026, 6:16 PM ET (America/New_York), in `/workspace/gtao-core` beside `main` at `a1a98aa`. Written *before* any experimental run of the extended library, the IMP-N60 predictions on new designs, the fractal sweep, or the cymatics sweep. Existing already-computed files that this prereg may *read* (not re-fit) are named below; they were produced under earlier preregs or notes and are not results of this test.

**Hypothesis under test (parent diagnosis; may be wrong).** N60's increment formula fails for rhythms because the layer library is only first-order stores (each layer one real time constant, an exponential smoother), while a rhythm is a complex pole pair. Approximating an oscillation with real stores is a basis mismatch, so ε_K is non-convex and no count of real stores recovers argmin J. The missing piece is the internal model principle (Francis & Wonham 1976, "The internal model principle of control theory," *Automatica* 12:457–465, doi 10.1016/0005-1098(76)90006-6, verified on Crossref 20 Nov 2026; earlier statement Francis & Wonham 1975, *Appl. Math. Optim.* 2:170–194 / the Crossref record 10.1007/bf01448180). A system that must track a signal has to contain a model of that signal's own dynamics — an oscillator to track a rhythm (as circadian clocks do via entrainment). Restated keystone: a layer matches a mode in *kind* as well as time scale; one layer per mode whose stakes pay, with a rhythm tracked by a resonant (second-order) layer.

**Status labels used later:** `in-model`, `numerical`, `PROVED` only if actually proved. This file is a prereg, not a result.

---

## 0. What is already on disk (readable, not a result of this test)

- `rhythm_rule.json`: 21 designed rhythm worlds, first-order-only E_K and E_∞, R-grid comparisons (189). World ids and poles are the fixed world set for Part A.
- `rhythm_counterexample.py` / `.json`: the worked example (wide-search seed 2), included in those 21 as `seed2_two_light`.
- `s5_rerun.json`: 120 Model S (OU-sum) worlds, seeds 0..119, first-order E_K and N60/argmin on `R_GRID = logspace(-1, 7, 161)`. Used for the Model S *regression of the closed-form rule against already-computed argmin*, not re-optimized except for the small extended-library subset in §5.
- Merged solver: `theory/layers_checks/stores.py` (guarded inversion, v2.67 / PR #116). Not modified.
- Local pre-#116 `core/keystone_checks/stores.py` is not used.

No file named `RHYTHM_RESULTS.md`, `resonant_layers.py`, or any `*DEVIATIONS*` for this test existed at lock time.

---

## 1. Extended layer library

A design is a finite collection of modules from the library Λ below. The merged `stores.py` is not modified; the library lives in a new module `core/keystone_checks/resonant_layers.py`.

**First-order store** (the existing Model S / N60 module). One real pole −b with b > 0. One state. Transfer function of the form g·b/(b + s), same family as `stores.py`. **Cost c = 1.**

**Resonant layer.** One real second-order block with parameters β > 0 and Ω ≠ 0. Poles −β ± iΩ. Two states. Transfer function (p s + q) / (s² + 2β s + (β² + Ω²)), with the two linear gains (p, q) optimized in closed form for fixed (β, Ω), the same way g is optimized for fixed b. A resonant layer is *one module of degree 2*, not two independent first-order stores: the poles are constrained to be a conjugate pair. **Cost c = 2.**

**Cost justification.** The reduced N60 objective is J = C + R (E / E_∞) with R = w E_∞ / h and h the upkeep per *state dimension* (the memory term κ I_mem pays per stored sufficient statistic). A first-order store holds one statistic; a resonant layer holds two (the quadrature pair). This is "counted by degree" as in CT21 and the keystone sentence. A cost of 1 per *module* regardless of degree is rejected in this prereg: it would cheapen a rhythm relative to an OU mode of equal degree and would break the Model S regression.

**Total degree / cost.** C = n_first + 2 n_res. Argmin is over composition (n_first, n_res) *and* the continuous parameters, with C ranging from 0 (act blind, E_0 = Var(s)) upward. The old "K" of N60 is this C when the library is first-order only.

**MSE.** Exact in the linear-Gaussian model: either the Lyapunov covariance of the world-plus-filter state (extension of the reviewer realization in `rhythm_rule.py`) or an equivalent closed-form Gramian; gains by the #116 guarded (Jacobi-scaled, truncated) inversion. No `minimum.accumulate`. E_∞ is the Yovits–Jackson integral on the joint spectrum (existing, already confirmed on the worked example). A design with E < E_∞ − 10^{-9} is a bug, not a result.

---

## 2. Predicted rule (IMP-N60)

The rule must predict C* and the included mode set from the world's poles, variances, observation-noise density N, and stakes R *alone*. It must not compute, or look at, an optimized ε_C curve over the library.

Parse the world into modes: an OU mode is a real pole −a with variance σ_m²; a rhythm is a conjugate pair −α ± iω with variance σ_m² (the sum of the two pole residues' real parts, as in `osc_world`). Let E_∞ be the joint causal MMSE (Yovits–Jackson on the sum spectrum). For each mode m let E_∞^{(m)} be the causal MMSE of *that mode alone* in the same white noise N (OU: the Kalman formula P = N(√(a² + 2 a σ_m²/N) − a); rhythm: Yovits–Jackson on that mode's spectrum, equivalently the 2×2 Kalman–Riccati error). Isolated causal value:

    V_m = (σ_m² − E_∞^{(m)}) / E_∞

Cost c_m = 1 if m is OU, c_m = 2 if m is a rhythm. **Include mode m's matched layer iff R V_m > c_m** (strict; ties take the lower cost / fewer modes, i.e. leave it out).

**Predicted design S\***: the set of included modes, each tracked by a *matched* layer of the same kind (first-order store for OU, resonant layer for a rhythm). **Predicted cost C\* = Σ_{m∈S\*} c_m.** Predicted module counts follow. Modes with R V_m ≤ c_m are left untracked (the K* = 0 case is included: if no mode pays, C* = 0).

This is the generalization of N60 stated as: per mode m, include its matched layer if R times that mode's isolated causal error reduction, measured in units of joint E_∞, exceeds its degree-cost.

**What the rule does not do.** It does not optimize filter parameters. It does not evaluate E for subsets of modes in the joint world (that would be a 2^n argmin on computed errors, closer to a tautology). Isolated V_m can be a poor approximation when modes overlap strongly; that is a predicted weakness, not a post-hoc excuse, and is tested by including both well-separated and close frequency worlds in the fixed set.

**Tautology check (required).** (i) The prediction code path does not call the library optimizer and does not read optimized E_C. Predictions for all Part A (world, R) pairs are written to `imp_n60_predictions.json` (with a SHA-256) *before* the extended-library optimizations are run, and are not edited afterwards. (ii) IMP-N60 is not an identity on an arbitrary ε sequence: it does not take an ε sequence as input. The earlier hull increment, by contrast, equals argmin J for any sequence; that identity is not this rule.

---

## 3. Pass / kill criteria

Ties in J: two designs are co-minima if |J_a − J_b| ≤ 10^{-9} max(1, |J_a|). A predicted C* matches if it equals the leftmost (lowest-C) minimizer, or any co-minimizer's C.

**SANITY (kill the library / optimizer if this fails).** For each of the eight one-oscillator worlds, one optimized resonant layer (n_res=1, n_first=0) must satisfy ε = E/E_∞ − 1 < 10^{-3}. The matched-pole design (layer poles fixed at the world's poles, gains only) is also reported; it is not a kill criterion by itself, but if it is far above E_∞ while the optimized layer reaches it, that is worth a diagnosis (Kalman poles ≠ process poles).

**PRIMARY (Part A).** On the 21 rhythm worlds × 9 R values = 189 comparisons, IMP-N60's predicted C* equals the extended-library argmin C* in **≥ 95%** of comparisons (≥ 180/189). The extended-library argmin is the lowest-J design among the compositions in §6 (including C=0 and the already-computed first-order-only designs from `rhythm_rule.json`).

**MUST (worked example).** For `seed2_two_light` at R = 3, predicted C* equals the extended-library argmin C*. The old first-order-only argmin K=3 is *not* the target; the target is the new library's argmin. This is a kill for the "R=3 must give the right K" requirement even if the 95% gate is met.

**REGRESSION (Model S).** On all 120 S5 worlds and the S5 R-grid (161 points; 19,320 comparisons), IMP-N60 (all c_m=1) is computed from poles, v, N, R only and compared to the already-stored argmin of K + R(1+ε_K) on K=0..J (from `s5_rerun.json`, not re-optimized). Pass: match in **≥ 95%** of all 19,320, *including* the K*=0 hole (IMP-N60 is required to predict C*=0 when no mode pays; the hole is a success if predicted, a miss if not). Also report the match rate against N60-from-0 and against N60-as-written (the latter starts at 1 and cannot predict 0). A 12-world extended-library subset (§5) checks that adding resonant modules does not improve E enough, at the rhythm R-grid, to change argmin relative to first-order-only; a change is a reported miss for this subset, not folded into the 19,320.

**TAUTOLOGY.** Fail the "predictive" claim if predictions were computed from optimized ε_C, or if they were altered after the library sweep. The hull identity is not reused.

**CYMATICS and FRACTAL** have their own criteria in §8–§9; they do not kill PRIMARY by themselves.

**If PRIMARY, MUST, or SANITY fails:** diagnose causally in `RHYTHM_RESULTS.md` (basis mismatch not the cause? cost wrong? isolated V_m too crude for overlapping modes? optimizer miss?). Do *not* patch IMP-N60 after seeing the data. Process deviations (budget cuts, a seed typo, an optimizer bugfix that does not change the rule) go in a dated `DEVIATIONS_YYYY-MM-DD.md` *before* the affected results are treated as scored, when that is still possible; otherwise the deviation is disclosed and the affected cells are labelled unsecured. Changing the inclusion rule or the cost after seeing argmin is not a deviation; it is a new, unregistered rule.

---

## 4. World sets and seeds

**R-grid for rhythms, cymatics stakes, and the 12-world Model S subset:** R ∈ {0.5, 1, 2, 3, 5, 10, 20, 50, 100}, the same grid as `rhythm_rule.py`.

**Part A — 21 rhythm worlds**, exactly `rhythm_rule.py:world_list()`, already stored in `rhythm_rule.json`. The two-oscillator worked example is world `seed2_two_light` (not a 22nd world). Ids, in file order of `world_list()`:

1. `seed2_two_light` (wide-search seed 2; ω ≈ 0.05512, 0.82460; ζ ≈ 0.10153, 0.01824; variances 0.361872, 0.331825; N=0.04014640614993535)
2–9. `1osc_z{0.02,0.08,0.25,1.0}_N{0.04,0.2}` (ω=1, variance 1)
10–17. `2osc_{sep15,close2}_{light_light,light_medium,medium_medium,heavy_heavy}` (sep15: ω=0.05,0.8; close2: ω=0.5,1.0; N=0.04; variances 0.5,0.5; ζ pairs (0.02,0.02), (0.02,0.25), (0.25,0.25), (1,1))
18–21. `3osc_{light_light_light,mixed,medium_medium_medium,heavy_heavy_heavy}` (ω=0.05,0.3,1.5; N=0.04; variances 1/3 each; ζ (0.02,0.02,0.02), (0.02,0.25,1.0), (0.25,0.25,0.25), (1,1,1))

**Part B — Model S regression:** seeds 0..119 of `s5_rerun.py:world()` (rng `default_rng(1000+seed)`, J ∈ {3,4}, separations ×3..×100, v and N as in that function). Closed-form IMP-N60 vs stored argmin: all 120. Extended-library check: the 12 seeds **0, 1, 2, 3, 4, 5, 50, 51, 52, 53, 54, 55** (six from the start of the list and six from the middle; J will fall as the generator decides — not hand-picked by convexity or gap).

**BASE_SEED = 20261120** (same calendar seed as `rhythm_rule.py`). Optimizer RNGs: for world index i (0-based in the Part A list, or the Model S seed), composition key d (a stable integer encoding of (n_res, n_first)), seed = BASE_SEED + 1000*i + 17*d. Fractal and cymatics seeds in §8–§9. IMP-N60 itself uses no RNG.

---

## 5. Optimizer

Reviewer multi-start, extended to resonant parameters: informed initializations with Ω near world frequencies and β near world damping (and scaled copies), plus random starts; Nelder–Mead; L-BFGS-B polish; differential evolution when the parameter count is ≤ 6. 2% separation of *real* store rates (as in #116); resonant layers kept at distinct |Ω| by a 2% floor when n_res ≥ 2. Guarded inversion. Lyapunov MSE is a check on SANITY, on the worked example, and on any increasing-E or below-E_∞ flag, not a term in the objective.

Compute cap: about 2.5 hours wall, `nice 19`. If the cap binds, the order of work is: (1) write predictions and hash, (2) SANITY, (3) Part A compositions in §6, (4) MUST world first among Part A, (5) cymatics (a) from those fits plus the §8 sweep, (6) fractal, (7) 12-world Model S extended check, (8) the 19,320 closed-form regression (cheap; do it with the predictions). Unfinished cells are reported as unfinished, not as passes.

---

## 6. Extended-library compositions scored for argmin (Part A)

For a world with n rhythms (and no OU modes, which is every Part A world):

- C = 0 (blind).
- First-order only: n_first = 1..2n+2, E taken from `rhythm_rule.json` (already computed; not re-fit unless a stored E is flagged increasing or below E_∞ — then re-fit that cell and disclose).
- Resonant only: n_res = 1..n, and n_res = n+1 (one extra resonant, a over-complete internal model).
- Mixed, budgeted: (n_res, n_first) ∈ {(1,1), (1,2)} for every n; also (2,1) when n ≥ 2; also (2,2) and (3,1) when n = 3.

That is enough to beat or lose to first-order K=3 on the worked example and to test whether leftover real stores still pay once matched resonants are available. Designs not in this list are out of the scored argmin; if after the run we wish we had included another composition, that is a new test, not a silent addition.

---

## 7. Analytic hope (not a pass criterion)

If a matched resonant layer for a single rhythm nearly attains E_∞^{(m)}, and if well-separated modes nearly add, then ε_C along the *matched-internal-model path* (add modes in decreasing V_m, paying c_m at each step) has decrements V_{(1)} ≥ V_{(2)} ≥ … after sorting, hence is convex in cumulative cost. The known non-convexity would then be a basis artefact: a first real store on a lightly damped rhythm buys little (it cannot oscillate), a later store completes a crude two-pole approximation, so adjacent decrements are not monotone. This paragraph is a target for an argument in the results note. It is **not** proved in this prereg and will not be labelled PROVED unless a proof is actually given.

---

## 8. Cymatics check (in-model)

Named for the Chladni picture only as an analogy: a driven plate takes the shape of the driving mode; here, the optimized design is predicted to take the shape of the world's spectrum, and to change that shape in jumps.

**(a) Frequency locking.** On every Part A world with n_res = n (one resonant layer per rhythm) at the optimized parameters, pair each layer's |Ω| to a distinct world frequency ω by the assignment that minimizes the sum of relative errors. **Prediction:** for light-damped worlds (every ζ ≤ 0.08), the median relative locking error min_π median_k |Ω_k − ω_{π(k)}| / ω_{π(k)} is **< 0.05**. Report the full error table. For heavier damping, report the same numbers with no hard fail (spectra are not sharply peaked). Also report locking of β to α, as a descriptive, not a fail criterion. Status: in-model, numerical.

**(b) Discrete jumps under a continuous sweep.** Two sweeps, both starting from `2osc_sep15_light_light` (ω = 0.05 and 0.8, ζ = 0.02, 0.02, variances 0.5, 0.5, N = 0.04), which is in the 21-world set:

- *Stakes sweep:* R from 0.25 to 200, 41 points log-spaced (np.logspace(np.log10(0.25), np.log10(200), 41)), world frozen. Seed = BASE_SEED + 80000 + point_index.
- *Frequency sweep:* the faster rhythm's ω_2 from 0.1 to 8.0, 31 points log-spaced, R fixed at 3, other world parameters frozen. Seed = BASE_SEED + 90000 + point_index.

At each point, take the argmin C* over the compositions in §6 (re-optimized at that point; first-order-only is re-fit here because the world or the comparison is new). **Prediction:** C* and the composition (n_res, n_first), and also which modes are tracked when that is identifiable from locking, are *piecewise constant* in the swept parameter, with isolated jumps (a layer added, removed, or reassigned). A smooth drift of *continuous* parameters inside a fixed composition is allowed and expected (Ω may track ω). A smoothly changing C*, or a composition that chatters at every grid step without a crossing of J, is a fail of (b).

**Relation to CT41 (inaction / redesign band).** CT41 (PROVED in-model, `theory/DYNAMICS.md`) scores a *non-move* after a measured input change against a lump-sum redesign cost k with band Δ_R(k) from CL19. This check is in-model and has no field k. The mapping we will report, and not stretch: at zero redesign cost, the optimal composition jumps exactly where two designs' J curves cross; between crossings the same composition is optimal (an inaction region in the swept coordinate). If a lumpy redesign cost k were charged to change composition, the jump would be delayed until the J-gap exceeds k (hysteresis; Dixit 1989 as already cited under CL19/CT41). We report the zero-k crossing locations and, at those neighbourhoods, the J-gap as a function of the swept parameter, in the same units as C. We do *not* treat this as a field test of CT41, and we do not choose k after seeing the gaps. Status: in-model, numerical.

---

## 9. Holographic / fractal check (in-model)

**Prior art (verified 20 Nov 2026).** Vidal 2007, "Entanglement Renormalization," *Phys. Rev. Lett.* 99, 220405, doi 10.1103/physrevlett.99.220405 (Crossref). Swingle 2012, "Entanglement renormalization and holography," *Phys. Rev. D* 86, 065007, doi 10.1103/physrevd.86.065007 (Crossref). Mehta & Schwab 2014, "An exact mapping between the Variational Renormalization Group and Deep Learning," arXiv:1410.3831 (verified on the arXiv; **no Crossref DOI**, not a journal article). The physical picture: a stack of layers, each summarizing the layer below at a coarser scale (MERA / renormalization). In a scale-free world the number of layers should grow like the log of the range of scales, at roughly equal value per layer.

**Worlds.** Sum of OU modes (Model S), geometric rates, power-law variances, using the existing `stores.scalefree_world` construction: τ log-spaced in [τ_min, τ_min Γ], v ∝ τ^{α−1}, total variance 1, spectrum ~ f^{−α} inside the band. Fixed:

- τ_min = 1
- α ∈ {0.5, 1.0, 1.5}
- span Γ ∈ {10, 10², 10³, 10⁴}
- per_decade = 1, hence geometric spacing ρ = 10 and J = 1 + log10(Γ) ∈ {2, 3, 4, 5}
- N = 0.05
- R ∈ {1, 3, 10, 30, 100, 300}

One extra spacing check, not folded into the primary count: α = 1, per_decade = 2 (ρ = √10), Γ ∈ {10, 10², 10³}, so J ∈ {3, 5, 7}, same N and R. Optimizer seed = BASE_SEED + 10000 + 100*Γ_index + 10*α_index + K, with Γ_index, α_index 0-based in the lists above (the extra arm uses +20000). Library: first-order stores only (this is Model S). Solver: merged `stores.py` + reviewer multi-start as in `s5_rerun.py`. K = 0..J (E_J should meet E_∞).

**Predictions.**

1. At high stakes, K* grows as log(Γ)/log(ρ). Concretely, at R = 100 and at R = 300, and also at the smallest R on the grid for which N60-from-0 (equivalently IMP-N60, if they agree) includes every mode, **K* = J = 1 + log10(Γ)** for all 12 primary (Γ, α) worlds. Misses are reported per cell. The extra per_decade=2 arm should give K* = J = 1 + 2 log10(Γ) at the same high-R points.
2. Roughly equal value per layer, especially at α = 1: the coefficient of variation of the J adjacent decrements (ε_{k−1} − ε_k) for k = 1..J is **< 0.5** at each primary world. (For α ≠ 1 the spectrum is tilted; CV may be larger; report, and hard-fail only α = 1.)
3. N60-from-0 matches argmin J whenever ε is convex on K=0..J (expected here, as Model S). Convexity itself remains unproved; this arm does not claim a proof.

**Test of N60.** This *is* the test of whether N60 reproduces the renormalization/MERA counting on scale-free Model S worlds. Status: in-model, numerical.

---

## 10. Outputs (after the run)

- `core/keystone_checks/imp_n60_predictions.json` and its SHA-256, written before library optimizations.
- `core/keystone_checks/RHYTHM_RESULTS.md` — verdict vs this prereg, numbers, diagnoses, labels (`in-model` / `numerical` / `PROVED` only if proved).
- `core/keystone_checks/rhythm_im_run.json` (or split files) with designs, E, locking errors, sweep traces, fractal curves.
- Updates to `core/KEYSTONE_NOTE.md` and `OPEN_WORK.md` (T18 / W9) with honest labels. No push, no merge.

A SHA-256 and timestamp of *this* file, as locked, are recorded in the results (and printed at lock time). The file is not edited after lock except to correct a typo that does not change a criterion, which would itself be a dated deviation.
