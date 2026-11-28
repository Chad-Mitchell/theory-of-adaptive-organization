# Confirm review: PR #137 at caaee48 (S1–S3 applied)

**Reviewer:** confirm pass on a fresh clone. This confirm wrote none of `theory/FREEZE_PROCESS_2026-11-21.md`, `theory/freeze_process_checks/freeze_process.py`, `theory/freeze_process_checks/freeze_process.out`, the first independent review, or the S1–S3 fix commits. Same bot family, not a blind second executor; the verdict is from this fresh re-read, an independent re-derivation of the Euler–Lagrange recurrence and the γ_E relic asymptotic, a numerical check of those against the DP and an independent ODE/integral, and a rerun of the committed script, not from memory of the edits.
**Date:** Saturday 21 November 2026, started about 10:21 AM ET, finished about 10:26 AM ET (America/New_York).
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/137 (branch `freeze-process-2026-11-21`, confirm-start head `caaee4858179c9841fe173ba5c644e9d26daf00d`, base at confirm start `main` `cd84095`; current `origin/main` is `5f252e6672e009bac12af481401613b67f471c14`).
**Clone:** fresh `/workspace/conf137` (not the first-review clone `/workspace/rev137` and not an author workdir). At confirm start: PR ref checked out at `caaee48`, merge-base with `origin/main` was `cd84095` (branch behind by PR #136). Commits on the branch at start: note `8d15ada`, first review `3c104d0`, S1 `de73bc5`, S2 `c3c12d8`, S3 `caaee48`. Clean tree at confirm start. Nothing from this PR merged at the start of this confirm. `/workspace/looper` and `/workspace/gtao-evo` were not touched. Compute at nice 19.

During this confirm, `origin/main` `5f252e6` was merged into the branch (`661bb4e`, clean, field2 files only). Confirm nits are `131189331c45621477d679de4cc254bc0be3826a`.

**Verdict: READY**

The note is still a derivation. It is not a prereg, not a lock, and not a field result. The three should-fixes from the first review (S1–S3) are applied correctly. The Euler–Lagrange recurrence and the relic asymptotic re-derive and check numerically, including at interior DP reads and at Hor = 20,000. Proton/crystal claims remain strictly `ANALOGY`. `CORE.md` and `THEORY.md` are each byte-identical to current `origin/main` (SHA-256 `CORE.md` `1d48bb351d7d2d25622abe1fa8f06d5603b7121904d17033ff2004057fe3b555`; `THEORY.md` `19a1e326b69b435a8334577386bc27ace0f19d20783ac811f7518fd134be1524`). The law-of-adaptive-organization hypothesis sentence is unchanged. Novelty grades in §§2, 3.1, and 4 are KNOWN / 0 or 0–1 as required; §5 and §7 are honest given Kibble–Zurek, annealing, and Néel/Brown prior art (no further numeric downgrade; one wording nit on §5, applied). Checkers PASS. Residuals below do not block a merge of this unlocked note.

At confirm start the PR was open, head `caaee48`, base `cd84095`, five commits, four files, +735 / −0 relative to then-`origin/main`.

---

## What was checked

- Fresh clone at the stated start head; `git merge-base HEAD origin/main` at start was `cd84095`. `git diff --stat origin/main...HEAD` at start: four files (`reviews/freeze_2026-11-21/REVIEW.md`, `theory/FREEZE_PROCESS_2026-11-21.md`, `theory/freeze_process_checks/freeze_process.out`, `theory/freeze_process_checks/freeze_process.py`). Working tree clean at start. `/workspace/looper` and `/workspace/gtao-evo` not opened.
- First review at `reviews/freeze_2026-11-21/REVIEW.md` compared to the should-fix list (S1, S2, S3). Fixes checked against the pre-fix tree (`8d15ada` / review `3c104d0`) and against `caaee48`.
- Independent re-derivation of the Euler–Lagrange condition and of the relic asymptotic (below), with an independent numerical check, not only a rerun of `freeze_process.py`.
- `CORE.md` and `THEORY.md` are each identical to current `origin/main` `5f252e6`, both before and after the merge of main. `README.md`, `STATUS.md`, `OPEN_WORK.md`, and `measurement/CLAIM_MAP_v2.md` are also identical to `origin/main`. The hypothesis sentence is the same string in `CORE.md` line 24 and `THEORY.md` line 41: "The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment." The note states that it does not edit that sentence and does not quote it.
- The four-file diff versus current `origin/main` does not touch `CORE.md`, `THEORY.md`, `measurement/CLAIM_MAP_v2.md`, `STATUS.md`, or any locked results, prereg, or deviations file (confirm nits touch only the derivation note).
- `nice -n 19 python3 theory/freeze_process_checks/freeze_process.py` PASS; output byte-identical to committed `freeze_process.out` (numpy 2.5.5, scipy 1.18.1, Python 3.13.5). `python3 tools/check_consistency.py` PASS. `python3 tools/check_open_work.py` PASS. Re-checked after the merge of main and after the nit edit.

---

## S1 — fixed; Euler–Lagrange and tail asymptotics hold

Pre-fix, §4 fitted `q_last ~ 0.6 c/(W τ_c Hor)` and said "exactly two more reads after onset." Both fail outside the original five-row table.

HEAD states the exact Euler–Lagrange conditions `u(t_k) − u(t_{k−1}) = q(t_k)(t_{k+1} − t_k)` (interior) and `u(t_N) − u(t_{N−1}) = q(t_N)(Hor − t_N)` (last read), the tail `q_last ≈ τ_c q(t_{N−1})/(Hor − t_N)`, Hor → ∞ saturation of N (N = 403 on Hor ∈ [1500, 10⁶] at τ_c = 20, c = 0.005), `t_N ~ τ_c ln(Hor/τ_c)`, and `q_last · Hor ∝ 1/ln(Hor/τ_c)`. "Exactly two" is now O(1) (2 in the first five rows, 3 at Hor = 5000 and 20,000). The official script checks last-read EL (max rel err 0.010), read-count saturation between Hor = 1500 and 5000, and the O(1) post-onset bound.

Independent re-derivation (this confirm). Differentiating `cN + W Σ_k ∫_{t_k}^{t_{k+1}} (u(t) − u(t_k)) dt` with `t_0 = 0`, `t_{N+1} = Hor` in `t_k` gives, by Leibniz, a contribution `u(t_k) − u(t_{k−1})` from the preceding segment and `−q(t_k)(t_{k+1} − t_k)` from the following segment, which is the stated recurrence.

Independent numeric check (own DP driver, same grid rule, nice 19), including the official six runs and Hor = 20,000: interior EL max relative error 0.042, median 10^{-6}–10^{-5}; last-read EL relative error ≤ 0.010, matching the official check. At τ_c = 20, c = 0.005: N = 403 at Hor = 1500, 5000, and 20,000; 3 reads after onset at Hor = 5000 and 20,000; `t_N = 414.61` at Hor = 20,000, consistent with the logarithmic drift. The remaining-horizon tail cost at Hor = 20,000 is 3.88×10^{-4} < c = 0.005 and is already well below c, so the N = 403 saturation claimed through Hor = 10⁶ is supported by the tail argument (`W τ_c² q(t_{N−1})` shrinks as 1/ln(Hor/τ_c)) without a full O(n²) DP at 10⁶. Official `freeze_process.py` rerun at nice 19 is byte-identical to committed `freeze_process.out` (ALL CHECKS PASS).

---

## S2 — fixed; relic formula and reheating qualification hold

HEAD gives the exact asymptotic `x_∞ − x*(0) = −[ln(τ_c/(ζ τ_1)) + γ_E]/(α ζ) + O(e^{−S_∞})` with `S_∞ = τ_c/(ζ τ_1)`, the `pζ = 1` boundary (no frozen relic, lag → p/α), the §6.4 reheating qualification (resume near `τ_a(q) ~ τ_h` is above `q_fo` only for `τ_h < τ_c`; slow heating unfreezes below `q_eff` and dips `f` toward `f*(q)` before climbing), Jung et al. 1990 and Chakrabarti & Acharyya 1999 in §6.4, and the §7 wording that `W·H/(2c)` is the dimensionless lifetime-stake-to-two-reads ratio while `W/c` is the price ratio.

Independent re-derivation (this confirm). With `q(t) = q_0 e^{−t/τ_c}`, `x*(t) = x*(0) − t/(α τ_c)`, and `τ_a = τ_1 e^{ζ t/τ_c}`, the change of variable `u = e^{−ζ t/τ_c}` turns the linear ODE into

`x_∞ − x*(0) = (1/(α ζ)) ∫_0^1 S_∞ e^{−S_∞ u} ln u du`

plus a transient `O(e^{−S_∞})`. The integral equals `−(ln S_∞ + γ_E) + O(e^{−S_∞} ln S_∞)`, which is the stated formula. At `pζ = 1`, `S(t) → ∞` so there is no frozen relic, and the lag of the linear ODE with `x* ~ −(p/α) ln t` and `τ_a ~ t` converges to p/α.

Independent numeric check (own DOP853 ODE and an independent quadrature of the exact integral, not a call to the official `relic_exp`): at ζ ∈ {0.5, 1, 2} and τ_c ∈ {100, 1000}, ODE, exact integral, and γ_E asymptotic agree to ~10^{-12}. At p = ζ = 1, the lag at t = 10^5 is 0.499995 against p/α = 0.5. Official S6 at τ_c = 1000 matches the same closed form to the printed 10^{-8} tolerance (and in fact to the printed 6 decimals).

---

## S3 — fixed; §§2, 3.1, 4 are KNOWN / 0 or 0–1

Pre-fix, §§2, 3.1, and 4 were labelled `UNCONFIRMED novelty`, and the targeted search for §4 was left OPEN.

HEAD grades §2 **novelty 0** (elementary corollary of Theorem 8 and Cho & Garcia-Molina 2003), §3.1 **novelty 0** (elementary fixed-cost algebra; stated in the §8 table at `caaee48`, and also in the §3.1 body after the confirm nit), and §4 **KNOWN in substance (novelty 0–1)**, with the checking / AoI / EOQ / inattention citations (Barlow et al. 1963, Keller 1974, Viscolani 1991, Rabi et al. 2012, Sun et al. 2020, Hollier & Mak 1983, Reis 2006, Abel et al. 2007/2013, Alvarez et al. 2011) in §§4, 8, and References. §9 item 3 records that the targeted search was completed in review. Jung et al. 1990 and Chakrabarti & Acharyya 1999 are in §6.4 as S2 required. No live `UNCONFIRMED novelty` grade remains (the preamble now only mentions the old label as having been downgraded).

---

## §5 relic scaling and §7 freeze temperature: grades are honest

No further numeric downgrade is required.

- **§5 / §8 relic row.** The integral freeze-out condition is already credited as KNOWN (cosmology). The power-law-in-quench-time form is already labelled ANALOGY to Kibble–Zurek (and annealing is cited). ζ is disclosed as assumed, not derived. That is the honest grade given the prior art the first review named. The one inflated sentence at confirm start, "The ramp-time dependence is the only possibly new part," overstated the novelty of a form already present in Kibble–Zurek and annealing. The confirm nit replaces it with the ANALOGY and confines the untested GTAO-specific piece to the exponents (α, ζ) and the explicit γ_E prefactor in this ODE. The table grade is unchanged.
- **§7 / §8 T_f row.** The form is already labelled KNOWN (Néel/Brown blocking, Dodson closure, Kramers). Putting the price ratio inside the logarithm, and the ~10% shift under a 1000× price change, is the standard weak log-dependence of a blocking or closure temperature. That is honest; it is not a new temperature formula.

Proton, nucleus, and crystal claims remain strictly **ANALOGY** in §§0, 8, with E1 (nothing selects a proton's response) stated in plain words. Nothing in this PR promotes them to a design prediction.

---

## No lock, no scored test, hypothesis unchanged

The file is still not a prereg and not a lock. The three predictions (abrupt vs gradual shutdown, relic vs ramp time, nearly price-free T_f) remain OPEN and not qualified. No official row is re-scored. `CORE.md`, `THEORY.md`, and the law sentence were not edited by this PR.

---

## Checkers (this clone, nice 19)

- `nice -n 19 python3 theory/freeze_process_checks/freeze_process.py` — PASS; output identical to `theory/freeze_process_checks/freeze_process.out`
- `python3 tools/check_consistency.py` — PASS (0 FAIL; 23 frozen-record INFO hits; soft length WARNs on THEORY.md and README.md already present on `main`)
- `python3 tools/check_open_work.py` — PASS (union missing from OPEN_WORK.md: 0)

---

## Residuals (do not block)

1. **The official script still checks Euler–Lagrange only at the last read**, not at interior reads. Independent interior checks pass (max rel err 0.042, consistent with grid discretization). Not a gap in the required S1 fix.
2. **The official script does not rerun Hor = 20,000 or 10⁶.** The note's Hor = 20,000 claims (N = 403, 3 post-onset reads) were verified here; the 10⁶ saturation claim is supported by the tail-cost argument rather than a full DP at that horizon.
3. **`reviews/README.md` does not yet index this review folder.** The first review did not require that row. Not a blocker for this unlocked note.

This confirm does not merge.
