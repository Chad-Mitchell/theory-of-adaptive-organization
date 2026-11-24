# Independent hostile review: GTAO tracking duel (`duel-2026-11-23/`)

*Reviewer: an independent agent. I did not write the duel. Review date: Monday 23 November 2026, America/New_York. Inputs: `PREREG.md` (sha256 f4b8f59f…), `DUEL_MEMO.md`, and `checks/`. These were checked against a fresh clone of GTAO `main` d592662 (`CORE.md:52,70,78,80`) and against `WALLS_REVIEW.md` §4–§5. Work was done in `/workspace/revduel` with TMPDIR set there and nice 19; the scratch was deleted afterwards. `THEORY.md` is untouched (sha256 5fa1abba…). Nothing was posted and no PR was opened. The memo was fixed in place with 18 `[REVIEWER EDIT 2026-11-23]` marks. Checks are in `duel_review_checks/` and hashed in `SHA256SUMS`. Labels: PROVED (in-model) / KNOWN / CONJECTURE / SPECULATION.*

> "The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment." (`CORE.md:7`)

## 0. Bottom line

- **The outcome stands.** Step (ii) does not survive in the reviewer's sense. The criterion cells are D, R-Hol: FC1 is LOSE and FC2 is TIE. That holds in the memo's run, in my byte-identical rerun, and after I restored the preregistered classical offset.
- **"Continuity, not quantum" stands.**
- **Two secondary readings were overstated, and both are now corrected in the memo.**
  1. The strict no-bath "clean WIN" under R-Hardy is a feasibility result against a frozen record. Once the preregistered offset is restored, it becomes MIXED.
  2. "a3 never had lower stake" holds only because the offset was not implemented.
- **One deviation was not logged:** the offset was fixed at 0 in code although PREREG §4 says "optimized". A second was post hoc: the S2 strict skip. I ran S2 strict per the PREREG's literal definition.
- **The sphere follow-up, as proposed, cannot produce a quantum WIN.** Against the classical band-limited rotor it is capped at TIE (§6, PROVED (in-model), elementary). Müller–Masanes 2013 already shows that single-system symmetry gives a ball in every dimension, and that interaction between two systems is what picks out quantum theory. The fair next test is a composite or interaction task.

## 1. Preregistration integrity

| Check | Result |
|---|---|
| `sha256sum PREREG.md` = `f4b8f59f97db0d98a48a149149db4cf67cd4d92eaf75f3a5101fd61618453c85` = `PREREG.sha256` | **PASS** |
| PREREG predates results | **PASS (filesystem evidence only).** PREREG.md was created and modified at 20:45:00.92 EST and PREREG.sha256 at 20:45:00.93. The first script was created at 20:46:54 (`duel_core.py`). The first output was written at 20:50:57 (`duel_mc.out`). The grid finished at 20:59:18 and the memo at 21:09:35. There is no git commit and no external timestamp. |
| Header-time deviation ("~9:15 PM") | **PASS as disclosed (memo §8.1), but it matters more than the memo says.** Taken literally, 9:15 PM is after every result, so only file times show the prereg came first. Recommendation: commit or otherwise externally timestamp each prereg before any computation. |
| `checks/SHA256SUMS` | **PASS** (16/16 OK). |
| Prior duel computation before the prereg? | None found (`/workspace/duel` deleted; walls checks contain no duel grid). P1 and P2 follow analytically from Fejér–Riesz, which the prereg itself anticipates ("to be shown"). So "predictions borne out" is weak evidence for those two, because they are identities, not tests. |

## 2. Rerun from a fresh copy

Every script was rerun at nice 19 from a fresh copy (`grid`, `decide`, `lemmas`, `mc`, `pinfo`, `freesize`). **All outputs are byte-identical** to `checks/`: `grid_results.json` d6f8bf9d…, `decisions.out` 8a1205…, and the lemma, MC, p-info and free-size outputs (`rerun_hashes.txt`, `rerun_decisions.out`). The counts quoted in memo §0 and §4 match `decisions.out` exactly. The aggregate labels follow PREREG §6 as coded (≥90% WIN with no LOSE gives WIN; ≥50% LOSE gives LOSE; ≥90% TIE gives TIE; anything else is MIXED). The 6 FC2 R-Hol LOSE cells are a3 at λ = 0.1, T = 0.25, N ∈ {48, 64} (`rev_checks.out` R2).

Note: `duel_decide.py` gives c1 and the orbitope **b's own** stake and feasibility. Their tie with b is therefore imported from L1, not computed independently. That is legitimate, because L1 is correct (§4), but the grid does not test it.

## 3. Deviations and post-hoc choices

1. **S2 strict skip (memo §8.3): post hoc, now run.** PREREG §6 defines strict as "a3 excluded", and that can be computed in S2. Results with the memo's a-values (`rev_checks.out` R4):
   - R-Hol FC1: LOSE (519 L / 113 T).
   - R-Hol FC2: TIE (614 T / 18 L).
   - R-Hardy FC1: MIXED (572 W / 2 T / 58 L).
   - R-Hardy FC2: MIXED (608 W / 6 T / 18 L).
   - Every LOSE is at τ = 1/8.
2. **Unlogged: offset not optimized.** PREREG §4 says "Estimator θ̂ = 2πk/N + offset, offset optimized". `duel_core.a_char1`/`a_tail_fourier` use offset 0. I re-optimized a constant offset (256 points on the circle) and a finer rate grid (49 factors, including the frozen record), using exact bin arithmetic with noise convolution (`patch_a.py`). It agrees with the memo's Fourier tails to 6e−5 (`validate_patch.out`). Results (`decisions_patched.out`):

| Row | Memo | Offset restored |
|---|---|---|
| D R-Hol FC1 main (criterion) | LOSE 475 L / 85 T | **LOSE** 488 L / 84 T |
| D R-Hol FC2 main (criterion) | TIE 554 T / 6 L | **TIE** 543 T / 29 L |
| D R-Hardy FC1 main / strict | MIXED / WIN 560 | MIXED 526 W / 1 T / 45 L / **MIXED** 530 W / 1 T / 41 L |
| D R-Hardy FC2 main / strict | MIXED / WIN | MIXED / **MIXED** 548 W / 4 T / 20 L |
| S1 R-Hardy FC1 / FC2 strict | WIN / WIN | **MIXED** 676 W / 2 T / 70 L / **MIXED** 712 W / 7 T / 29 L |
| S2 R-Hol FC2 main | TIE 575 T / 57 L | **MIXED** 524 T / 148 L |
| All others | — | labels unchanged |

   - Every change is at T = 0.25 (D, S1) or τ = 1/8 (S2).
   - Mechanism: a frozen N-state record aimed at the middle of a quarter turn (offset π/4) keeps |e| < π/4 + π/N, so it meets the ruin cap for N ≥ 4 with no bath and K = N.
   - At N = 4–5 with tight ε, b is infeasible where that frozen record is feasible, which produces a few LOSEs at λ = 0.
   - This is a known-horizon trick, but it is preregistered freedom.
   - b was **not** given the matching freedom (its rate is fixed at the world's rate, PREREG §4). The patched counts are therefore an upper bound on the classical side's gain.
3. **P3 mechanism.** Once the offset is restored, classical records have lower stake than b in 39 cells (`rev_checks.out`; at small N, mostly S2 τ = 1/8). The prediction's mechanism does show up at the shortest horizons. The memo's "partial miss" was an artifact of the missing offset.
4. Memo deviations 2 and 4–6 are accurate as stated.

## 4. Per-claim assessment

| # | Claim | Assessment |
|---|---|---|
| C1 | Quantum record on one generator spans ≤ 2N−1 real dims | **PASS.** ρ_jk(t) = ρ_jk e^{−i(j−k)ωt}. The span is the diagonal (1) plus a rotating 2-plane per band d = 1..N−1, giving 1 + 2(N−1). Measured ranks were 3/5/9/15. Wording fixed: the *phases* are Toeplitz, not ρ. PROVED (in-model). |
| C2 | Canonical-phase readout laws = nonnegative trig polys of degree ≤ N−1 | **PASS.** p(φ) = (1/2π)Σρ_jk e^{i(k−j)φ} is nonnegative of degree ≤ N−1. Conversely, Fejér–Riesz gives p = \|q\|² with q a pure state, and mixtures keep the class. Any covariant phase POVM (seed b_jk PSD with unit diagonal) stays in the same class, and the optimal readout for a covariant task can be taken covariant (Holevo), so nothing is lost by restricting to canonical. KNOWN ingredients (Fejér 1916), PROVED (in-model) assembly. |
| C3 | Equivalence with the restricted rotor c1 and the Carathéodory orbitope | **PASS with nuance.** c1: law = preparation density, the same set. Orbitope: the law of a pure state at φ₀ is a shifted kernel k(φ−φ₀), and mixtures convolve, which reaches every nonneg trig poly. Stake and ruin are identical. The nuance: c1 is classical only *ontologically*. Operationally its state space is non-simplex (a linear image of the quantum state space, dual to the orbitope). So "a classical continuous tracker ties" should read "a non-simplex theory with a classical hidden-point model ties". Edited in memo §0.4. |
| C4 | L2: I ≤ ln N without Holevo (max ≤ N·mean) | **PASS.** Cauchy–Schwarz on \|Σc_k e^{ikφ}\|². For c1 the supremum is strictly below ln N, since a trig poly cannot be flat at the cap on an arc. The cap is therefore an inequality, not an equality, which is fine for R-Hol. |
| C5 | L5 at R-Hardy excludes classical continuous | **PASS for simplex records. Reason corrected for c1:** with exact readout, N_max(c1) = 1 (a nonzero nonnegative trig poly has finitely many zeros). Edited. |
| C6 | L6 orbitope has exactly N perfectly distinguishable states, K = 2N−1 | **PASS.** Shifted Fejér kernels give a partition of unity with δ_ij at the nodes (rerun 4e−31). The upper bound holds because each effect needs n−1 double zeros, at most 2(N−1). |
| C7 | Finite continuous-time Markov record: limsup ruin ≥ ½ | **PASS with qualifier.** Holds for a time-homogeneous record. Irreducible chains mix, so the record becomes independent of θ₀ and P(\|e\|>π/2) → ½ exactly for any estimate law. Reducible chains: a frozen class label cannot follow the rotation, and the period-average is ½. A time-dependent rule imports a clock (a2). Edited. |
| C8 | Coherence bound: decay ≥ 2π tan(π/N) per revolution | **PASS.** Re-derived: for the uniform unicyclic chain λ₁ = r(e^{2πi/N}−1); setting \|Im\| = 2π gives r* = 2π/sin(2π/N) and −Re = 2π tan(π/N), with equality. Any generator obeys \|Im λ\|/(−Re λ) ≤ cot(π/N). Attribution checked in arXiv:2605.15884 (Kolchinsky, Ohga, Ito; read): Table 1 credits the affinity-free sector bound to Dmitriev–Dynkin 1946 (stated for stochastic matrices; the generator form follows) and the tanh(F/2n)cot(π/n) bound to Ohga–Ito–Kolchinsky 2023 (PRL 131:077101, "Thermodynamic bound on the asymmetry of cross-correlations"), which strengthens Barato–Seifert's 2017 conjecture. The memo's wording is consistent. KNOWN. |
| C9 | Woods et al. 2022 as "KNOWN in substance" | **PASS with caveat.** PRX Quantum 3:010319 (read via arXiv:1806.00491) shows ticking quantum clocks reach about quadratically better precision than classical ones of the same dimension. The duel's b is a one-shot stopwatch, not a ticking clock, and its advantage is only against *simplex* records. "In substance" is fair; "same result" would not be. |
| C10 | Classical continuous tracker fairly priced or strawmanned? | **Not strawmanned. If anything it was favored under FC1**, where c1 may restrict its state space by law while quantum pays for all N². A quantum theory restricted by the same kind of law to the visited section is FC2, which gives a TIE. FC2 is the symmetric comparison, and FC1's LOSE mostly restates that full quantum theory is bigger than the task needs. The N-state classical side, by contrast, **was under-optimized** (offset, coarse rate grid; §3). |
| C11 | Do the FC1/FC2/R-Hol/R-Hardy choices bias the result? | **Yes, in predictable ways, all disclosed except the offset.** FC1 is biased against b, FC2 is symmetric, and R-Hardy excludes c1 by premise. R-Hol caps a quantity that b attains (χ = ln N) but c1 cannot quite reach. The main price, λ per nat of *dimension*, comes from walls memo §6, not CORE. GTAO's own memory coordinate is mutual information (`CORE.md:52`), and under that pricing (P-info) b LOSES in 144/144 cells. The most CORE-faithful pricing is therefore the least favorable to quantum. Heat is unpriced (`CORE.md:70`). Pricing it would penalize a3 only, which can move R-Hardy main toward the strict variant but cannot touch the criterion cells. |
| C12 | Step (ii) criterion not met; R-Hardy recorded as conditional; "continuity, not quantum" | **PASS. Stands.** |
| C13 | Strict R-Hardy "clean WIN" | **FAIL as worded.** It is feasibility-only against a frozen record without offset. With the preregistered offset it is MIXED. Edited. |
| C14 | "a3 never had lower stake than b" (P3 partial miss) | **FAIL as general claim.** It is an artifact of the missing offset (39 cells). Edited. |
| C15 | S2 strict "not run" justified | **FAIL as procedure** (post hoc). It was computable, I ran it, and it does not affect the criterion. |
| C16 | 22 DOIs resolve on Crossref | **PASS.** All 22 were rechecked on Crossref, and titles, authors and venues match (`crossref_memo.out`, `crossref_retry.out`). The two added in this review also resolve: Hardy 2004, 10.1016/j.shpsb.2003.12.001; Montina 2008, 10.1103/PhysRevA.77.022104. arXiv:2605.15884 exists (HTTP 200, read). |
| C17 | Repo grep "no prior GTAO treatment" | **PASS.** Only an unrelated Fejér identity appears, in `tests/SPF_NOISE_PROXY`. |
| C18 | Wording rules | **PASS.** No "solved", no kill or final-judgment language, no claim to derive QM, labels present. "Loses" is used only as the decision-rule term. |

## 5. Does the outcome stand?

**Yes.** The preregistered criterion is quantum WIN in D, R-Hol, FC1 or FC2. It is not met in the original run (LOSE, TIE), in my rerun (identical), or with the offset restored (LOSE 488/84, TIE 543/29). The R-Hardy rows are recorded, as PREREG §6 requires, as "survives only conditional on a premise that excludes classical continuous by definition", and since the orbitope ties or beats b, also as "the cost selects continuity but not quantum theory specifically". The corrected secondary reading is narrower: an autonomous, closed, finite-dimensional record that must stay ruin-free *beyond short known horizons* needs a non-simplex continuously reversible state space. That is KNOWN in substance (Hardy 2001 Axiom 5; quantum-clock literature). The ruin-cap wording is GTAO's own. Over a quarter turn, a frozen discrete record with an offset is enough.

## 6. The sphere follow-up: worth running? How to make it fair

**What memo L7 checks is right.** A spin coherent state's SU(2) orbit spans all N² dimensions, and Σ_{ℓ≤N−1}(2ℓ+1) = N².

**But as proposed it is capped at TIE (PROVED (in-model), elementary; `sphere_check.out`):**
- Every covariant readout law of a spin-(N−1)/2 record is nonnegative and band-limited to ℓ ≤ N−1, with max ≤ N·mean. Rerun: band-fit residual about 1e−15; max/mean ≤ N for random states and random axially symmetric seeds.
- A classical restricted sphere rotor whose preparations are all such densities has the same K = N². Its law set contains the quantum one, strictly so for N ≥ 3. Witness: ρ = I − 2|m=0⟩⟨m=0| for spin 1 has eigenvalue −1, yet its Husimi function is cos²θ, which is nonnegative, band-limited and at the cap.
- For N = 2 the two sets coincide (the Bloch ball; KNOWN as the Kochen–Specker single-qubit hidden-variable model).
- So on stake and ruin quantum can at best tie, and the idle-parameter headwind disappears only to show this deeper fact. KNOWN in general: a single system with one readout family always has a classical model, and quantum and classical separate only with incompatible measurements or composites.

**What Müller–Masanes 2013 already shows (NJP 15:053040, read via arXiv:1206.0630).**
- Postulates:
  1. Direction information can be sent and recovered with a rotatable device in d dimensions.
  2. Minimality: the system carries no more than direction information.
  3. Local tomography for pairs.
  4. A continuous reversible, non-product interaction between two "direction bits".
- From postulates 1–2 alone, the single-system state space is a d-dimensional ball for **every** d.
- Only adding 3–4 forces d = 3 and two-qubit quantum theory, including unitary dynamics.
- So the literature already contains the result that single-system rotation tracking does not single out quantum theory, and that interaction does. That is exactly where a GTAO duel would have to go.

**Recommendation.** Do not run the single-system sphere duel as specified, because its best possible outcome is fixed in advance. Run a redesigned duel only if it is fair in the following sense, preregistered before any computation:
1. **The task needs either interaction or later-chosen readouts.** Option (a): two records track two coupled rotors and must exchange information through a continuous reversible joint evolution (MM2013 postulate 4). Option (b): the question asked of the record (which axis, or which incompatible observable) is chosen only after preparation, so one record must serve a tomographically complete family.
2. **Symmetric comparators.** Either every side may adopt an epistemic "law", or none may. Price everyone on the same coordinate: operational dimension, ontic dimension, or mutual information (`CORE.md:52`). Report all three. Prior art on ontic cost: Hardy 2004 (ontological excess baggage), Montina 2008 (ontic-state complexity).
3. **Composite pricing stated in advance.** Under local tomography, K_AB = K_A·K_B, which is the quantum product rule. The competing GPTs for the composite must be named in advance, including minimal and maximal tensor products.
4. **A proof that a WIN is possible.** Show in the prereg that no admissible competitor's achievable law set contains quantum's for the task. If one does, the duel is capped at TIE before it starts, as here.
5. **Give b the same freedoms as its competitors:** rate, offset, readout seed.

Treated this way, the follow-up is essentially "is local tomography (Hardy Axiom 4 / MM2013 postulate 3) a cost minimum?" That is step (iii) of the walls door, and it is the honest next question: CONJECTURE that it could be informative, SPECULATION that it favors quantum.

## 7. Revised plain words for Chad (audio)

We ran a fair contest. A dial turns steadily, and three kinds of memory try to keep track of it without ever being badly wrong: a quantum one, a simple one with a fixed number of slots, and a smooth classical one with a built-in blur. Over long stretches, the slot memory can't keep up, and both the quantum memory and the smooth one stay steady. So the rule against going broke really does call for smooth, reversible change. That part of your hunch holds up. But quantum didn't win. The smooth blurred dial does exactly as well while storing fewer numbers, and so does a made-up third kind of theory. That's because following one dial only uses a thin slice of what a quantum memory can hold. The review also found that over very short stretches, a simple frozen memory aimed at the middle of the turn sometimes beats quantum. We also learned that tracking a ball turning in every direction won't settle it: a blurred classical ball can copy anything the quantum one reads out. The real test is two memories that have to interact with each other, or a question that's chosen only after the memory is set. That's where quantum and classical genuinely come apart.

## 8. Files (`duel_review_checks/`, hashed in `SHA256SUMS`)

- `rev_checks.py` → `rev_checks.out`: R1 strict feasibility; R2 the 6 FC2 losses; R3 stake comparison; R4 S2 strict per PREREG; R5 a first offset probe, superseded by `patch_a`.
- `patch_a.py` → `patch_a.out`, `grid_patched.json.gz`; `duel_decide.py` (memo's, unchanged) on the patched grid → `decisions_patched.out`. `validate_patch2.py` → `validate_patch.out`.
- `sphere_check.py` → `sphere_check.out`.
- `crossref.py` with `dois.txt`/`extra.txt` → `crossref_memo.out`, `crossref_retry.out` (rate-limit retry), `crossref_extra.out`.
- `rerun_decisions.out`, `rerun_hashes.txt`: the fresh-copy rerun.
- Paths in the scripts point to the deleted scratch (`../fresh/checks/grid_results.json`, the memo's grid, hash d6f8bf9d…). To reproduce, point them at `duel-2026-11-23/checks/grid_results.json`.
