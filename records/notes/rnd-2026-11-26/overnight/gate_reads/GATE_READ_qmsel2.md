# Gate read: qm-selection-2 prereg (theory/qm-selection-2-2026-11-26)

Reader: Forge executor (separate from the author agent). Read 2026-11-26, 05:45–05:55 ET.
Object: lock commit `641c695`, branch tip `4d161b0` (mitchell-moving fork). Fresh clone: `/workspace/gate-qmsel2/repo`.
Scope of this read: the locked files only. The search was **not** run. The only code executed was the five
SO(3) control bodies of the selftest, through a harness that imports the locked script and calls the same
code path (`/workspace/gate-qmsel2/harness/so3_controls.py`, output `so3_controls.out`). No SU(3), Sp(2) or
G₂ orbit, capacity or face was computed. No repo commit or push.

## Decision: FAIL (amend under a NEW lock; this lock stays as committed)

The lock itself is clean (hashes match, pushed before any run, no run exists). The prereg fails the gate on
method: three parts of the hit path are under-tested in a direction that can produce a **false HIT**
(non-exposed faces, bit faces, capacity witness), one predeclared scope list is incomplete, and one change
made after a control output is not disclosed in §0. Each needs a change to `search_rank2.py` or `PREREG.md`,
which means a new lock (new directory or new commit with a new `PREREG.sha256`), never an edit to `641c695`.

## 1. Hashes and order (PASS)

| file | sha256 at 4d161b0 | PREREG.sha256 |
|---|---|---|
| PREREG.md | 4cd2f0ea4ca4402e…91fd2529b4abd | match |
| search_rank2.py | 14841f66ccd8f49e…fc98da5134a1 | match |

- None of the six files in the directory changed between `641c695` and `4d161b0` (`git diff` empty).
- Lock commit time 04:40:10 ET. `641c695` is not an ancestor of the earlier pushed tips (4c693b6, d4c0d19,
  b365edc); it reached GitHub in the push `dd46a0d..4d161b0` at 10:44:41Z = **05:44:41 ET** (activity API),
  matching WORKLOG 05:44. So the GitHub anchor for "lock before run" is 05:44:41 ET.
- No `search_rank2.out` or `RESULTS.md` exists in any clone or scratch folder on the box. The lock predates any run.
- `check_lock` in `--run` refuses to start on a hash mismatch (read, not exercised).

## 2. Controls (observed, reproduced)

Harness rerun at 05:53 ET (numpy 2.5.5, scipy 1.18.1, python 3.13.5, 48 s): all five controls and both
bit-face checks reproduce `selftest.out` **bit-identically** (same α to every printed digit):
B3 TARGET (α 0.49999998, cap 2, bit face 3-ball); Z3 MISS on cost (cap_UB 2); C1 hSFP fail (gap 0.3525);
Z2 hSFP fail (gap 1.5, cap_UB 3, cap_LB 3, bit face dim 2, not a ball); B3×B3 MISS on cost.
So the code is deterministic on this box at these versions.

## 3. FIX36 §10 items

| # | item | status |
|---|---|---|
| 1 | blind protocol, pushed lock, separate gate reader | met (this read; GATE_READ.md to be committed before any run) |
| 2 | Weyl-chamber families | met: 3° full circle + numerically located Weyl-singular directions |
| 3 | full enumeration incl. U(2) dims 9–15 | met for the named groups (counts checked independently: Sp(1)^k sums in dims 9–15 give 10/34/35, Sp(1)⁴ 11 declared not covered); scope list incomplete for neighbours (A8) |
| 4 | G₀ for every body | met numerically; no per-body closure check (A6) |
| 5 | exact capacity | upper bound valid (see §5); lower bound is numerical (A3) |
| 6 | predeclared SU(3) flag tie | met (TIE counts as a hit, §2 G1; expectation 50%, §5) |
| 7 | rule for Jordan bodies | met: non-complex Jordan bodies are scored by the same rule |
| 8 | non-exposed faces, P6 bit-face clause, P4+P2⇒P3 | **not met**: P4+P2⇒P3 noted; non-exposed faces not actually reached (A1); bit-face clause tested on one pair (A2) |

## 4. Hit rule (well-posed; fair, with two gaps)

- Well-posed: HIT iff SFP pass, hSFP pass, bit-face pass and d < N_LB²−1; TIE iff N_LB = N_UB = N and
  d = N²−1 with the same passes; TARGET iff the full signature (d, N, dim G₀, pure-state dim) equals
  complex QM_N with N_LB = N_UB; else MISS/OPEN. Each outcome is a function of printed numbers.
- SU(3) flag tie: predeclared, counted as a hit, separated from complex QM₃ by pure-state dim (6 vs 4).
  Fair. Note that a TIE rests on N_LB = 3, so it inherits gap A3.
- Non-complex Jordan bodies (real QM_N, balls, quaternionic QM₃) are scored by the same rule as any body:
  fair, and real QM₅ and the balls are expected to fail on hSFP or cost (§5), which is honest.
- Gap: the hit direction depends on three tests that report "pass (no failure found)". A pass there is the
  absence of a found failure, so under-testing moves bodies toward HIT. A1–A3 below close this.

## 5. Capacity bounds

- **Upper bound (valid, proved-in-model).** α = LP minimum of e(c) over effects nonnegative on a finite
  sample of the orbit (plus cutting planes at true orbit points), e(x₀) = 1. Fewer constraints than the
  true effect cone, so α ≤ λ and N_UB = ⌊1/α + 1e-6⌋ ≥ N. Centroid is exact (projection onto the G-fixed
  subspace). Observed α are all just below the exact values (e.g. Z2 0.3333333203 vs 1/3), the safe side.
  Solver tolerance could only push α above λ by ~1e-7, inside the 1e-6 slack. Non-blocking: raise slack to 1e-4 (N5).
- **Lower bound (can wrongly decide a hit: yes).** N_LB comes from a witness set of states with an effect
  family, validated by local minimization from the 12 lowest grid points at tolerance 1e-6. A witness that is
  negative somewhere between grid points passes. A strict HIT (d < N_LB²−1) and a TIE both use N_LB, so a
  wrong N_LB can turn a MISS into a HIT. Amendment A3.

## 6. Family coverage and enumeration

- Rank-2 list (sums of real irreducibles with a zero weight, dim ≤ 15): SU(3) 8; Sp(2) 5, 10, 14, 5⊕10;
  G₂ 7, 14. Complete for these groups (5⊕14 = 19, 7⊕7 reduces to one copy since dim Z = 1, 8⊕8 = 16).
- Directions: 3° grid on the full circle (about 10 points per 30° chamber for SU(3)) plus singular
  directions found by a 0.25° scan and bounded minimization. SU(3) singular angles land exactly on
  30° + 60°k; G₂ 14 on a 30° lattice; Sp(2) 10 and 5⊕10 on 45° lattices. Sp(2) 14 spacing is irregular
  (65.56, 131.46, 179.65, …), which is expected if the random Cartan basis is not orthonormal in the
  Killing metric, but it is not checked against |W| = 8. Non-blocking (N2).
- Products: rank-2 bodies on a 15° sub-grid plus all singular members × Sp(1)^k (k ≤ 3), plus 5⊗3. The
  singular offsets in products differ from the singles (e.g. Sp(2) 10: 1.4185 vs 0.5322) because the
  enumeration draws a new random Cartan basis; fine, but it makes the enumeration depend on the RNG
  stream and on numpy's linear-algebra output (A7).
- Not covered but not declared: see A8.

## 7. G₀ per body (expectations; the run must print and confirm)

Hypothesis, from the representation theory, to be compared with the run's printed dim_G0:
generic SU(3) 8, Sp(2) 10/14/5⊕10, G₂ 14 bodies: G₀ = G (dim 8, 10, 10, 14). Sp(2) 5: orbit is S⁴ in
R⁵, a ball, so G₀ = SO(5) (dim 10; same as Sp(2)'s image). G₂ 7: orbit S⁶, ball B7, G₀ = SO(7) (dim 21,
larger than G₂). Singular SU(3) direction (CP²): G₀ = PU(3) (dim 8). Sp(1)^k sums: product of SO(3)
images unless a summand is a ball of larger symmetry; products: product of factor groups.
The script computes G₀ from the tangency null space at max(60, 4d²) samples; closure is checked only in
the selftest. A spurious extra generator could change rank G₀ and flip SFP (A6).

## 8. Non-exposed faces (depth 2): not tested

§4 says depth 2 is reached by "lexicographic exposure" with the functional ℓ₁ + 0.01ℓ₂. A fixed positive
combination exposes an exposed face of the body, not the face of the ℓ₁-face exposed by ℓ₂; a true
depth-2 face is the maximizer of ℓ₂ **over the ℓ₁-face** (a two-stage optimization), and a non-exposed
face is in general not exposed by any single functional. The PREREG's argument that the minimal exposed
face is invariant does not show that an hSFP failure on a non-exposed face is seen. So depth 2 is untested
in fact, and the test can only miss failures (false-HIT direction). Amendment A1.

## 9. Seeds (PASS)

SEED = 20261127; body i uses default_rng(SEED + i) in `--list` order; controls use SEED+1000+i and
SEED+2000+i, outside 0..926, so no overlap. Result independent of worker count (per-body RNG). Fixed before
any outcome. Gap: the enumeration order itself is not checked at run time (A7).

## 10. §0 disclosure

The five listed bugs are consistent with `selftest.out`. One further change is **not** disclosed: an
earlier selftest output on this box (`/tmp/selftest1.out`, 03:24:54 ET, before the locked script's
03:57 version) labels the B3 control `"jordan_type": "ball B3 (spin factor)"`, `"outcome": "TIE (P6
bit-face clause holds)"`; the locked script labels it `complex QM` / `TARGET`. The change (complex QM_2 added
to the Jordan table, which is correct: the Bloch ball is complex QM₂) altered a control's scored outcome
after the author saw it. It touches only the TARGET label and does not use new-group output, so it does not
taint the lock, but §0 says all fixes are listed. Amendment A9 (disclose it). The 24-min selftest time
under load is disclosed.

## 11. Can a post-hoc relabel turn a miss into a hit?

§6 forbids it ("Relabels … never move a miss to a hit"). Remaining routes, closed by the amendments:
(a) an OPEN body (timeout, undecided face) later re-run and called a hit of this prereg (A10);
(b) moving a body between TARGET and TIE/HIT through the Jordan table (frozen by the hash; A9 discloses the
one earlier change); (c) re-running with other numpy/scipy versions or another enumeration order (A7).

## 12. Amendments required for a NEW lock

- **A1 Non-exposed faces.** Implement true lexicographic exposure: for each S-invariant ℓ₁, compute the
  ℓ₁-face's pure states, then maximize ℓ₂ over that face (two stages), and test hSFP there; or declare
  depth 2 untested and make "pass" read "pass at depth 1" with any HIT/TIE reported as conditional on depth ≥ 2.
- **A2 Bit-face clause over all bit faces.** Test the minimal face (not the minimal exposed face) of
  (p+q)/2 for every witness pair and for one representative of every Weyl-inequivalent pair of
  distinguishable T-fixed pure states. HIT/TIE only if all are 3-balls; any non-ball ⇒ MISS; any undecided ⇒ OPEN.
- **A3 Independent N_LB check.** Before scoring HIT or TIE, re-validate the witness on a fresh orbit
  sample (≥ 10⁵ points, separate seed SEED+10⁶+i) with ≥ 100 local-minimization starts; minimum ≥ −1e-6
  or the body is OPEN. Print the minimum found.
- **A4 hSFP false-MISS guards.** Check the number of T-fixed points found against |W|/|W_v| and mark the
  body OPEN on mismatch; re-confirm any failure certificate with 5× more starts; use a threshold no tighter
  than 1e-6·rad for every eps (currently 1e-8·rad at eps = 0.01, near BFGS gtol 1e-10/200 iterations).
- **A5 TARGET guard.** Report TARGET only when the signature matches and the body is the known CP^{N−1}
  orbit (SU(3) singular direction, B3); any other body matching the tuple is printed as "TARGET-signature,
  check by hand" and not scored as a miss or hit until checked.
- **A6 Per-body G₀ closure.** Check that the computed g0 basis closes under the bracket (residual
  < 1e-8) and is antisymmetric; otherwise OPEN. Print dim G₀ and rank G₀ (already printed).
- **A7 Reproducibility.** `--run` must regenerate the enumeration and compare names (in order) with the
  committed `list.out`; abort on mismatch. Record numpy/scipy/python versions in PREREG and abort if they differ.
- **A8 Scope disclosure.** Add to "Not covered", and to the G5 next step: rank-3 groups in range —
  SU(4)≅Spin(6) adjoint (d = 15, dim Z = 3; contains complex QM₄ and the N = 4 flag analogue of the
  predicted tie), Sp(3) on 14 (dim Z = 2; quaternionic QM₃ and generic directions with d = 14 < 15, where
  capacity 4 would be a strict hit), Spin(7) on 8 (ball) — and the SO(n) balls B9–B15 outside the products listed.
- **A9 §0 completeness.** Add the B3 relabel (ball/TIE → complex QM/TARGET, between 03:24 and 03:57 ET)
  as a sixth pre-lock change.
- **A10 OPEN bodies.** State that any OPEN body resolved after this run is a new, unregistered result,
  not a hit or miss of this prereg.

## 13. Non-blocking notes

- N1 3° grid: narrow windows are declared; keep.
- N2 Print the located singular angles with their residual σ and check their count against |W|.
- N3 Bit face uses wit[0], wit[1] only (subsumed by A2).
- N4 tfixed_points uses 300 starts (subsumed by A4).
- N5 UB slack 1e-6 is adequate (α observed on the safe side); 1e-4 costs nothing.
- N6 3600 s budget set for an unloaded machine; the run command says so. Record wall time per body.

## 14. Labels

Observed: hashes, timing, control outputs, the 03:24 earlier selftest. Proved-in-model: UB validity,
hSFP failure certificates (given SFP), enumeration completeness for the named groups. Hypothesis: the G₀
expectations in §7 and the rank-3 content in A8 (to be checked by a later prereg).
