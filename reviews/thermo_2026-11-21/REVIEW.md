# Independent hostile review: PR #122 (T27 thermodynamic / selection bridge)

**Reviewer:** independent (wrote none of the PR, BRIDGE.md, FLOOR.md, SELECTION.md, PREREG.md, predictions, runner, library, official run, RESULTS, OPEN_WORK / STATUS edits, or math_checks).
**Date:** Saturday 21 November 2026, started 12:14 AM ET, finished 12:25 AM ET (America/New_York).
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/122
**Clone:** fresh `/workspace/gtao-rev122/repo` at head `3517e465e94e2b791f965f12b36910bfcd724d89`, base `4398bbdc434b766d4b761aa86d8b8836b0ef8c4c` (merge-base equals base). Clean tree at review start. Nothing pushed or merged. `/workspace/looper` was not touched. Compute at nice 19. Author workdir `/workspace/gtao-thermo/core/bridge_2026-11-21/` was read only as corroboration of timestamps; every packaged file there is byte-identical to this head.

**Verdict: READY-WITH-FIXES**

The official gates recompute exactly from the locked predictions and stored outputs. The prereg and predictions were SHA-256 locked at 12:05:31 AM EST, before any official world was evaluated (official start 12:05:33 AM EST). Official seeds 2026112100–02 do not collide with prior Model S generator sets. P1 passes 3/3, P2 passes 3/3 (empirical β-excess 0.922–1.065 against d/2 = 1), P3 fails 0/3. The official verdict is FAIL and must stand; no rescue is registered, and none should be. The Sella–Hirsh mapping, the equipartition formula, the d/20 consistency note, and the CT4+Landauer corollary are correctly stated and not overclaimed. The “already in the repository” list checks out. All nine DOIs resolve on Crossref and match the stored bibliographic records. CORE.md and the hypothesis sentence are unchanged. Checkers pass; `pytest tools/` is 126 passed (the header still says 125). None of the issues below flip a gate or the FAILED verdict. They should be fixed before merge, without touching the locked prereg, the predictions file, or the official numbers.

---

## What was checked

- Fresh clone at the stated head/base; diff `4398bbd..3517e46` (one commit, 18 files). Package `core/bridge_2026-11-21/` plus the OPEN_WORK.md and STATUS.md diffs.
- SHA-256 of PREREG.md and predictions.json against LOCK.txt, PREREG.sha256, PREDICTIONS.sha256, run_t27.json, and RESULTS.md. Workdir mtimes and birth times at `/workspace/gtao-thermo` used only as corroboration of lock/start order.
- Independent regeneration of the three official worlds from the locked generator; recomputation of coarse J tables, connectivity, polished minima, Hessians, whitened lattices, and exact Boltzmann diagnostics (no official number moved). Independent rescoring of P1, P2, and P3 from stored occupation summaries.
- Independent re-run of committed `run_t27.py` at nice 19 (124.6 s): `run_t27.json` matches the official file exactly except the wall-clock `seconds` field. Official artifacts were restored afterwards; the review clone is otherwise clean of that rerun.
- Seed non-collision of 2026112100..2026112115 against S5 rng 1000–1119, convexity_search 0–119, convexity_wide 5000–5119, and named seeds 20261120 / 2026112020, plus a broader repo scan for those literals.
- Math: Sella & Hirsh 2005 (re-read against the PNAS text), Moran detailed balance, equipartition on a quadratic, discrete-lattice caveats, P2 tautology, FRAMEWORK §9 band and the d/20 ratio, CT4+Landauer corollary, two-temperature section.
- “Already in the repository” pointers grepped in THEORY.md, CORE.md, `theory/SCALE_ENDS.md`, and `measurement/FRAMEWORK.md`.
- All nine DOIs re-queried on the Crossref API this review.
- OPEN_WORK IDs vs base `4398bbd`; `python3 tools/check_open_work.py`; `python3 tools/check_consistency.py`; `python3 -m pytest tools/ -q`.
- Wording: “all physics,” “law proved,” rescue, CORE claims, hypothesis sentence.

---

## Integrity

- PREREG.md SHA-256 `25955df4ffb825254100568c9b9d1e751b9d5e0e533146a5d438414c8d5ba994`. Matches LOCK.txt, PREREG.sha256, run_t27.json, RESULTS.md, and a re-hash of the file on disk. Bytes 10047, as recorded.
- predictions.json SHA-256 `6715777ca45d02ad443a3e5003f19849331a9e60dba900aa6f6c68c93e7adfe3`. Matches LOCK.txt, PREDICTIONS.sha256, run_t27.json, RESULTS.md, and a re-hash of the file on disk. Bytes 2246, as recorded.
- Workdir file order, byte-identical to this head (America/New_York):
  - `run_t27.py` mtime 12:04:40 AM EST
  - `predictions.json` birth/mtime 12:04:49 AM EST (made read-only at lock)
  - `PREREG.md` birth/mtime 12:05:22 AM EST (made read-only at lock)
  - `LOCK.txt`, PREREG.sha256, PREDICTIONS.sha256 12:05:31 AM EST
  - `run_t27.log` birth 12:05:33 AM EST (official start; the runner printed `LOCK ok` first)
  - `run_t27.json` / log finish 12:07:41 AM EST (127.2 s at nice 19)
- The lock is genuinely before any official world. Pre-lock pilots in `/tmp/t27_pilot.py`, `t27_pilot2.py`, `t27_pilot3.py`, `t27_mix.py`, and `t27_mix2.py` used only the already-published S5 rng seed 1000, or 1000–1019. No official candidate seed was evaluated before lock. Predictions were written before the final PREREG bytes, and both were locked before start. Criteria in predictions.json match PREREG.md §5.
- The PREREG header says “Friday 20 November 2026, late evening ET.” The file was written and locked on Saturday 21 November at 12:05 AM EST. The lock timestamp itself is correct. See S4.
- LOCK.txt records the branch as beside `7275c4b`. That was accurate for the branch at lock time. `main` had already become `4398bbd` (PR #121 merged 12:04:05 AM EST). The single commit was later rebased onto that base; the package contents are what this review scored.
- `bridge_lib.py` and `run_t27.py` were not hash-locked. `bridge_lib.py` in the author workdir has mtime 12:06:26 AM EST, during the official run. The official log’s first warning is the smoking gun: `bridge_lib.py:180: RuntimeWarning: overflow encountered in scalar power` / `gN = gamma ** N_pop`. The committed `moran_fixation` is a log-stable rewrite (docstring: “gamma**N never overflows”). Because the official process had already imported the module at 12:05:33, the stored official numbers were produced by the pre-patch in-memory function. The committed function agrees with the overflowing `gamma ** N` form to machine precision on a wide ratio grid, including the overflow regime (where both go to the correct 0 or 1−γ limit). An independent re-run of the committed runner reproduces official `run_t27.json` exactly except wall-clock `seconds`. This is a documentation and lock-hygiene issue, not a change of criterion and not a change of any official number. See S2–S3. No DEVIATIONS file was written.

Official rng seeds 2026112100, 2026112101, 2026112102 (candidates through 2026112115) do not collide with the locked exclusion sets. `seed_collides` is implemented as written. A broader scan did not find those literals used as Model S world-generator seeds elsewhere.

---

## Official gates (recomputed from stored data)

Worlds, coarse J\*, unique interior K=2 argmin, graph connectivity (1562/1562), polished minima, Hessians (SPD, smaller eigenvalue well above 10^{-4}), high-β K=2 Boltzmann mass (≥ 0.978 > 0.95), and fine-lattice interior minima all recompute exactly. Mixing SANITY holds on every official cell (TV ≤ 0.20).

| Gate | Criterion | Independent result | Verdict |
|---|---|---|---|
| P1 | unique mode of pooled coarse occupation = unique coarse argmin, all three official worlds, β ∈ {8, 10, 12} | 3/3 worlds, 9/9 cells. Modes 157, 146, 180 equal the argmin. TVs 0.0089, 0.0014, 0.0389; 0.0160, 0.0195, 0.0029; 0.0422, 0.0110, 0.0195 | **PASS** |
| P2 | \|β(J̄−J\*) − d/2\| / (d/2) ≤ 0.20 on the whitened K=2 lattice, d=2, all three worlds, all three high β | 3/3 worlds, 9/9 cells. Empirical β-excess **0.922–1.065** (max relative error 7.8%). Exact Boltzmann diagnostic 1.004–1.011 | **PASS** |
| P3 | at β=0.5, coarse grid: mean J > J\*; at least two K with mass ≥ 0.10; low-β excess ≥ 2× mean high-β empirical coarse excess | **0/3**. Clauses 1 and 3 hold on every world (means 104.905, 104.879, 104.827 against J\* 102.080, 102.296, 102.445; excess ratios 168.50, 104.88, 59.38). Clause 2 fails on every world: masses on K=0,1,2,3 are 0.000, 0.001, 0.085, 0.913; 0.000, 0.001, 0.066, 0.933; 0.000, 0.000, 0.066, 0.934. One K ≥ 0.10 in each case | **FAIL** |
| Overall | PASS iff three official-valid worlds and P1∧P2∧P3 on every one | Three official-valid worlds (first three candidates; none rejected). P3 fails | **FAIL** |

Every RESULTS.md figure checked against `run_t27.json` agrees (rounding included: ratios reported as 168, 105, 59; TVs to four decimals; P2 table 1.049/1.028/1.065, 0.968/1.019/0.955, 0.999/0.922/0.991). Exact Boltzmann on the same coarse grids shows the same P3 pattern: K=2 mass 0.079, 0.076, 0.071, all under the 0.10 floor, with the rest on K=3. This is not a mixing miss and not a scoring bug.

No gate was changed after seeing the data. The FAILED verdict stands. No rescue is registered, and none should be. Scoring official P2 on exact Boltzmann weights, dropping a failing world, or replacing the two-K clause after the fact would be exactly the rescues the prereg forbids.

### Lesson (not a rescue): the P3 two-K floor was ill-posed at lock time

The locked operationalization of “designs spread” was “at least two layer counts K with occupation mass ≥ 0.10” at β=0.5 on a K=0..3 grid of 21 log-rates (1 + 21 + 210 + 1,330 designs) with a unit layer-cost term. That combination was already going to fail, and this was knowable at lock time without touching an official seed.

- Combinatorics plus the unit layer cost give a rough K=3 vs K=2 factor (1330/210)·e^{−β} ≈ 3.84 at β=0.5, versus 1.41 at β=1.5 and 0.002 at β=8. Entropy on the larger slice wins at the locked low β.
- The only design world used before lock was S5 rng seed 1000. Exact Boltzmann on that locked grid at β=0.5 already has only one K at or above 0.10 (K=3 mass 0.908, K=2 mass 0.090). At β=1.5 — the value actually piloted in `/tmp/t27_mix2.py` — the two-K clause would have passed (K=2 mass 0.166). The pre-lock pilots never printed K-masses at the locked β=0.5.
- Official exact Boltzmann at β=0.5 is the same failure (K=2 mass 0.071–0.079). At β=1.5 the same official grids would have met the two-K floor (K=2 mass 0.143–0.155).

The mean still sits above J\*, as clause 1 required and as RESULTS.md says. A different spread statistic would be a new prereg, not a rescue of P3. The official 0/3 stands. The lesson is that this particular clause was a bad operationalization of “spread,” visible from the locked grid, the locked β, and the pilot world, before the official run.

---

## Math

- **Sella & Hirsh 2005** is correctly stated. In the weak-mutation, monomorphic, origination–fixation regime, with symmetric mutation, the stationary weight is f^ν with ν = N−1 for haploid Moran, ν = 2(N−1) for haploid Wright–Fisher, and ν = 2N−1 for diploid Wright–Fisher with multiplicative fitness (their Table 1 and eq. 5). SELECTION.md uses the Moran case π_i/π_j = (r_i/r_j)^{N−1} and notes the diploid WF form f^{2N−1} as their leading-order / large-N weight. Detailed balance plus equal edge clocks (no degree bias) is the right condition for π ∝ r^{N−1}. The linear map m = −α J, r = exp(m), is clearly labelled an assumption; under it, β = α(N−1) and π ∝ exp(−β J). This is standard pop-gen applied to J, not a new theorem. Iwasa 1988 and the Shahshahani 1979 credit are apt; the infinite-population geometry is not used as a derivation of π.
- **Equipartition.** E[J]−J\* = d/(2β) is exact for a quadratic J = J\* + ½(θ−θ\*)ᵀH(θ−θ\*) on R^d under a Boltzmann measure (2β(J−J\*) ~ χ²_d). It is not exact on a truncated discrete lattice, and it is not a claim about the coarse mixed-K grid. T27 applies it on a whitened product lattice of half-width 3.5 with 51 points per axis, with J\* the minimum on that lattice. The exact-Boltzmann diagnostic 1.004–1.011 shows that discretization, truncation, and residual non-quadraticity of Model S are small here. That is the right way to apply the formula on a discrete grid, and it is not overstated as a theorem on the grid.
- **P2 is near-tautological given exact Boltzmann.** The quantitative content of equipartition is algebra once the measure is Boltzmann and the well is quadratic. The lattice was designed, on the pilot, so that exact β-excess would sit “within a few percent of 1.” Official P2 is correctly scored on Moran occupation, not on those exact weights (the prereg forbids the swap). Empirical 0.922–1.065 against a 20% bar therefore tests whether the simulated dynamics recovered a near-algebraic moment, not a new physical fact. The more direct dynamics check is the mixing TV (0.09–0.13 on the fine lattice, inside the 0.20 validity bar). P2 is a legitimate sampler-recovery gate and a weak test of the lag formula itself. That does not make the pass a cheat; it does mean P1 and the lag-as-prediction reading in SELECTION.md should not be described as if P2 had independently established equipartition.
- **FRAMEWORK §9 band and d/20.** The qualification protocol in FRAMEWORK §9 (and THEORY §3) has ε = 10/(σ N_e), a fractional gap in J, with the factor of 10 a conservative choice, not Lynch’s. Under the linear map, σ = α J at an operating point, β = α(N−1) ≈ σ N_e / J\*, so typical fractional excess ≈ d/(2σ N_e), and the ratio to the band is d/20. The algebra is correct. The package does not change the locked factor of 10, and it distinguishes a one-dimensional rival-excluding band from a d-dimensional scatter. N vs N−1 vs N_e is treated as an approximation, honestly.
- **Stakes / kT corollary.** CT4 is the first-nat threshold κ < −(D∘IB)′(0⁺). With the accounting convention κ ≥ κ_floor = kT·ν (nats; erasure-type updates) and with w Δℓ_1 defined as the stakes per update, ρ = w Δℓ_1 / (ν kT) and ρ ≤ 1 ⇒ K\* = 0 is the same threshold with κ replaced by its floor. Units are consistent once Δℓ_1 is per-update, as FLOOR.md says. It is correctly labelled a corollary, not a new theorem, and it is not used as a new reason atoms have no model (E1+E2 remain the load-bearing argument). When β_phys ≫ 1 the floor does no design work. Not overstated. “Real systems sit at the floor” is explicitly not claimed.

---

## Already in the repository, and the two temperatures

The “already in the repository” list is accurate. None of the following is presented as new: floors on the prices in J (THEORY, “one currency” paragraph; CORE.md definition, which names Landauer; Still et al. is in that THEORY paragraph); CT4 / first bit must pay; Bialek, Nemenman & Tishby 2001 and the causal-state conjecture in THEORY §9; SCALE_ENDS E1, E2, S1–S4, SE3, SE7 and the Kelly-type E_gen > β_phys kT inequality; FRAMEWORK §3.11 (β_phys; cell value INCONCLUSIVE); operational “strongly selected,” σ, N_e, drift barrier, and ε = 10/(σ N_e) in THEORY §3 and FRAMEWORK §9; ruin-constraint temperature z = B/(σ τ^H) in THEORY (iv), CT18, CT18-H, CT25; C3, F1 and DECISIVE as PROXY-FAIL and out of the structural core; Drăgulescu & Yakovenko as analogy only (THEORY (iv) and the 12 Nov 2026 X post). What the package claims as new is the application of the stationary law to J, the d/(2β) lag, the consistency note on the existing band, the explicit ρ ratio, and the two-temperature distinction. That split is fair.

The two-temperature section is honest. z is the world’s stress on a design (feasibility); 1/β is the noise of the selection search (spread around the cheapest feasible design). No kelvin identification is claimed for either, beyond the Landauer floor on the prices in J. A large-deviation link is listed as missing math, not forced. The two quantities are allowed to vary independently. One notation should-fix: σ in z = B/(σ τ^H) is the shock scale of CT18, while σ in the qualification band is the cost-to-fitness map of THEORY §3. THEORY already uses both meanings; the bridge note uses them in adjacent paragraphs without a flag. See S5.

---

## DOIs (Crossref, this review, 21 November 2026)

All nine DOIs in `crossref_dois.json` resolved and match the stored title, container, issued date, volume, issue, pages, and authors:

| DOI | Work |
|---|---|
| 10.1147/rd.53.0183 | Landauer 1961, IBM J. Res. Dev. 5(3):183–191 |
| 10.1103/PhysRevLett.109.120604 | Still, Sivak, Bell & Crooks 2012, PRL 109, 120604, “Thermodynamics of Prediction” |
| 10.1103/PhysRevLett.124.050601 | Still 2020, PRL 124, 050601, “Thermodynamic Cost and Benefit of Memory” |
| 10.1162/089976601753195969 | Bialek, Nemenman & Tishby 2001, Neural Computation 13(11):2409–2463 |
| 10.1073/pnas.0501865102 | Sella & Hirsh 2005, PNAS 102(27):9541–9546 |
| 10.1016/s0022-5193(88)80243-1 | Iwasa 1988, J. Theor. Biol. 135(3):265–281 |
| 10.1090/memo/0211 | Shahshahani 1979, Mem. AMS 17(211) |
| 10.1038/nrg.2016.104 | Lynch et al. 2016, Nat. Rev. Genet. 17(11):704–714 |
| 10.1007/s100510070114 | Drăgulescu & Yakovenko 2000, Eur. Phys. J. B 17(4):723–729 (Crossref author “Dragulescu”) |

Roles in the notes are apt. Still et al. 2012 is correctly scoped to their isothermal, no-feedback, Markov setting.

---

## Overclaims, CORE, OPEN_WORK

No “all physics” claim; BRIDGE.md denies it in so many words. Nothing is “proved about nature.” Official labels are in-model, numerical, FAIL. The hypothesis remains a hypothesis. CORE.md is byte-identical to base `4398bbd`. The hypothesis sentence, “The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment,” is unchanged.

OPEN_WORK IDs on base `4398bbd` are all still present (59 → 61). Added: W13, T27. None removed. T26 (already on main as a hypothesis pointer) is updated to record the T27 official FAIL and still labelled “Hypothesis, not a result,” not a new term in J, and not a change to CORE.md. T27 records the lock hashes, the 3/3–3/3–0/3 split, the K=3 failure mode, and “no rescue.” W13 correctly marks the review as owed. STATUS.md only notes that PR #121 merged as `4398bbd` and that open work lives in OPEN_WORK.md, which is the standing rule. The OPEN_WORK header still says “125 tests”; that tally is now stale. See S1.

---

## Checkers and tests

- `python3 tools/check_open_work.py`: PASS (union of not-DONE items.json / QUEUE.md missing from OPEN_WORK.md = 0).
- `python3 tools/check_consistency.py`: PASS (0 FAIL; advisory length WARNs on THEORY.md and README.md, pre-existing).
- `python3 -m pytest tools/ -q`: **126 passed** in 106.5 s, including `tools/test_bridge_checks.py` (which runs `math_checks.py` to “ALL OK”: Landauer units, Moran detailed balance, quadratic equipartition, qualification-band algebra, official-seed non-collision, lock hashes, lattice degree).

---

## Should-fixes (do not touch the locked prereg, predictions, or official numbers)

1. **OPEN_WORK test tally.** The header still says “125 tests.” `pytest tools/` on this head collects and passes 126, because `tools/test_bridge_checks.py` was added. Update the tally.
2. **Document the mid-run `moran_fixation` rewrite.** Official log, 12:05–12:07 AM EST: overflow at `bridge_lib.py:180` (`gN = gamma ** N_pop`). The committed function is a log-stable rewrite, saved at 12:06:26 AM EST during the run, and was not the in-memory function that produced the official file. It is numerically equivalent, and a re-run of the committed runner reproduces official `run_t27.json` exactly except `seconds`. Put that in a dated DEVIATIONS file. It is not a criterion change and it does not reopen a gate.
3. **Hash-lock the runner and library.** LOCK.txt hashes only PREREG.md and predictions.json. Future tests should also pin `run_t27.py` and `bridge_lib.py` (or their equivalents) at lock time. Here, record the committed hashes in the deviations note: `run_t27.py` `26039b3c81862f36e01ac516d17aa91ab6fd50e4b36cebfd0aafeaa0ccbdb19a`, `bridge_lib.py` `4e779b3dd4754dfa29a4ef74836a8986837f31a92c55601ae32579911e4b8fd2`.
4. **PREREG header date.** The header says “Friday 20 November 2026, late evening ET.” Lock time is Saturday 21 November 2026, 12:05:31 AM EST. Do not edit PREREG.md (that would break the lock hashes). Note the actual stamp in RESULTS or DEVIATIONS.
5. **Two meanings of σ.** In BRIDGE.md / SELECTION.md, flag that σ in z = B/(σ τ^H) is the shock scale of CT18, while σ in ε = 10/(σ N_e) is the cost-to-fitness map of THEORY §3 / FRAMEWORK §9. No identification is implied, but the same note uses both without a label.

---

## Blockers

None. The official FAIL stands, the lock is real, the math is correctly stated, CORE is untouched, and the mid-run library edit does not change a number.
