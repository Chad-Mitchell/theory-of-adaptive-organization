# Independent hostile review: PR #133 (revealed-prices fair-test standard, proposed amendment, and status refresh)

**Reviewer:** independent, hostile pass (wrote none of `theory/REVEALED_PRICES_2026-11-21.md` or the PR's `CORE.md`, `STATUS.md`, and `OPEN_WORK.md` edits; same bot family as the author executor, disclosed).
**Date:** Saturday 21 November 2026, ~8:45 AM ET (America/New_York).
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/133
**Clone:** fresh `/workspace/rev133` on branch `revealed-prices-2026-11-21`, reviewed head `799d44ec23571bd73caaf7f25fdf9b4f16b559d1` (`799d44e`, after commits `25809f9` and `799d44e`), merge-base `a65b64e` (PR #132 merged on `origin/main`). `/workspace/looper` and `/workspace/gtao-evo` were not touched. Nothing merged.

**Verdict: READY-WITH-FIXES** (4 blockers, 5 should-fixes; all are textual, algebraic, drafting, or status-refresh fixes in unlocked docs; no locked test or computation needs rerunning; §8 remains a proposal awaiting Chad's decision C7).

---

## Summary

The core insight of `theory/REVEALED_PRICES_2026-11-21.md` is sound in the slack-ruin expected-cost regime: `argmin J` is invariant to multiplying `J` by a positive scalar, so fitness-unit absolute prices are not needed to locate the optimum, and overidentified revealed prices fitted on a holdout-disjoint split (`R1`–`R4`) are a valid empirical test when `R2` (reachable-set exclusion) and `R3` (rival separation) are verified before opening the scored data. The §9 dataset audit is honest (zero candidates qualified; nothing locked or run) and accurately reflects the checked records.

However, the reviewed head `799d44e` cannot merge as written because of four blockers:
1. **B1:** §3.2 miscounts independent price ratios for `t ≥ 2` technologies (`sum of ratios + 1` omits the `t − 1` cross-technology scale ratios; the true count in a single currency is `sum of ratios + t`), and §3.2/§5 conflate CT34's single-currency cooperative partial minimization with multi-currency/multi-agent layers (which would add `K − 1` unknown exchange rates if currencies genuinely differed).
2. **B2:** §1 item 1 omits CT24's binding-ruin qualification (`THEORY.md` line 101; `scope_checks.py` §1b): when the ruin constraint binds and `(B, y)` are observed in currency units, `argmin J` is **not** scale-invariant because `J/B`, `y/B`, and `w/B` enter the feasible set.
3. **B3:** §8 item 1 contradicts §3.1 on the counting rule (`n_score > p` vs `n_fit ≥ p, n_score ≥ 1`), omits nuisance parameters, rank/R2/R3 checks, and CT34 premise checks; and §8 item 4 creates an asymmetric falsifiability loophole by allowing an unqualified ordinal selection-gradient test to count for **support** while barring its failure from **killing** (contrary to `THEORY.md` line 51 `"not evidence either way"`).
4. **B4:** `STATUS.md` line 3 falsely states *"None of #117–#132 bumped CLAIM_MAP"* (PR #117 bumped `CLAIM_MAP_v2.md` to v2.67 before PR #116 bumped it to v2.68), and `STATUS.md` line 8 / `REVEALED_PRICES` §1 line 19 overstate that *every* field path stalled on fitness-unit prices (`GRID-CROSS` stalled on `d1` data; *E. coli* P1/P3 failed R3 discrimination as well as `σ, T_red`; `VIS-1F` failed on both `(h, w)` and L3).

The hypothesis sentence (`"The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment."`) is unchanged across `THEORY.md` (line 41), `CORE.md` (line 24), and `REVEALED_PRICES_2026-11-21.md` (lines 3, 106). Kills still require absolute §3 qualification.

---

## What was checked

- Fresh clone `/workspace/rev133` at `799d44e` (`git diff --stat a65b64e..799d44e`: 4 files changed, +140 / −3). `THEORY.md`, `measurement/FRAMEWORK.md`, `measurement/CLAIM_MAP_v2.md`, and locked test artifacts are untouched.
- Math and model checks against `THEORY.md` (`a65b64e` lines 11, 36, 41, 43, 48, 51, 53, 101, 111, 153, 159, 472), `theory/GENERAL_THEOREM.md` §6 (`S1`), `theory/meq_checks/scope_checks.py` (§§1b, 2), `measurement/FRAMEWORK.md` §9, and `CORE.md` §2–§3.
- Prior art check on revealed preference, inverse optimization/IRL, structural estimation, Sargan/Hansen, drift barrier, and hierarchical decomposition / Bellman value functions.
- All 20 DOIs in `theory/REVEALED_PRICES_2026-11-21.md` (15 in §6, 5 in §9) verified via Crossref (`https://api.crossref.org/works/{doi}`) and DataCite (`https://api.datacite.org/dois/{doi}`) this session; non-DOI citations (`'t Hooft 1993` via arXiv `gr-qc/9310026`, `Ng & Russell 2000` ICML 2000 pp. 663–670, `Dantzig & Wolfe 1960` and `Geoffrion 1970` in `THEORY.md` / `litmap/verify/VERIFIED_DOIS.txt`) verified.
- Dataset spot-checks in §9 against opened primary/registry records:
  - Dunlap, Papaj & Dornhaus 2017 (`PMC5413896`, `10.1098/rsfs.2016.0149`; figshare `10.6084/m9.figshare.4769539`): 4 persistence (`q = 0.99, 0.86, 0.73, 0.60`) × 3 error-cost ratios (`ε = 0.28, 1, 2`) in sucrose solutions, rising sampling with change rate, suboptimal tracking. Matches §9.
  - Sung et al. 2012 (`PMC3494944`, `10.1073/pnas.1216223109`): confirms `N_e` estimated as `π_s / (k u)` (`k = 4` or `2`), inducing correlation with `u`. Matches §9.
  - *Tetrahymena* (`10.5061/dryad.z612jm6k7`), Wolves (`10.5061/dryad.2j125`), and Hall, Humphries & Kramer 2007 (`10.1139/Z07-030` abstract): verified via DataCite/Dryad v2 API and Crossref.
- `STATUS.md`, `CORE.md`, and `OPEN_WORK.md` checked against `git log` on `main` (`a1a98aa..a65b64e`) and `measurement/CLAIM_MAP_v2.md` (v2.68, tally 318).
- Repo checks on `799d44e`: `python3 tools/check_open_work.py` PASS; `python3 tools/check_consistency.py` PASS (0 FAIL; 23 frozen-record INFO hits; 2 pre-existing soft length WARNs); `pytest tools/ -q` (at nice 19, `~/.elan/bin` on `PATH`): **146 passed in 2:57**.

---

## Blockers (must fix before merge)

1. **B1 — Algebraic bug in §3.2 (`t` distinct technologies) and currency/agent conflation with CT34 (§3.2, §5).**
   - §3.2 line 55 claims: *"with t distinct technologies it is the sum of their ratios plus one."* For `t` technologies in one currency with `r_1, ..., r_t` primitive prices (`r_j − 1` internal ratios each) plus 1 top stake `w_top`, there are `Σ r_j + 1` absolute prices and `Σ r_j = Σ(r_j − 1) + t` independent ratios: **sum of within-technology ratios plus `t`**, not `+ 1` (`t − 1` cross-technology scale ratios were dropped). For two read technologies (`r_1 = r_2 = 1`, `0` internal ratios each), `+ 1` yields `p = 1`, contradicting §3.4 (`p = 2`).
   - §5 lines 79–81 claims each layer has *"its own units"* and calls *"the child's optimized cost, expressed in the parent's units, is the exchange rate between neighbours."* If cross-layer exchange rates `e_k` were unknown, `p` would gain `K − 1` free parameters and grow with `K`, contradicting §3.2. `THEORY.md` line 472 (CT34) is defined in a **single common currency** (`J = F(x) + G(y; θ(x))`), so §3.2's bound must state the single-currency (or known-conversion) premise explicitly.

2. **B2 — Scale invariance in §1 item 1 fails when the ruin constraint binds (`THEORY.md` line 101 / CT24).**
   - §1 line 23 claims `argmin_𝒟 c·J(𝒟) = argmin_𝒟 J(𝒟)` unconditionally and states *"(The ruin constraint is also in ratios: the reserve B and income y are measured in the same currency as J.)"*
   - Per `THEORY.md` line 101 (CT24) and `theory/meq_checks/scope_checks.py` §1b, when the ruin constraint binds, the feasible set `{𝒟 : P(ruin) ≤ ε}` depends on `J/B`, `y/B`, and `w/B` (via `σ² ∝ w²`). If `B` and `y` are observed in currency units while `J`'s prices are fitted only up to an unknown scale `c`, rescaling `J` by `c` alters the feasible set and `argmin J` is **not** scale-invariant. §1 and §3.1 must restrict pure price-ratio identification to the ruin-absent or ruin-slack regime (or count `w/B` as an extra free scale parameter in `p` when ruin binds and `B, y` are fixed observables).

3. **B3 — §8 proposed amendment: counting-rule contradiction in item 1 and asymmetric falsifiability in item 4.**
   - *Item 1:* Line 108 writes `"(more scored observables than free price ratios after CT34 linking, counted before data)"` (`n_score > p`). This contradicts §3.1 (`n_fit ≥ p` and `n_score ≥ 1`, overidentifying df `n_fit + n_score − p ≥ 1`, e.g. `m = 2` in §3.4 where `n_fit = 1 = p` and `n_score = 1 = p`), omits non-price nuisance parameters in `p`, omits full-rank / R2 / R3 requirements, and assumes `"after CT34 linking"` without requiring pre-test verification of CT34's premises. Item 2's `"Item 3 likewise"` is also imprecise regarding `FRAMEWORK` §9 item 3's `"re-measure once"` clause (non-price inputs can be re-measured once before comparison if a validity gate fails; fitted prices on the fit set cannot).
   - *Item 4:* Line 111 proposes admitting an ordinal selection-gradient test (§4, without §3 qualification `σ, N_e, ε`) *"for **support and for counting against**, not for a kill"*. Under `THEORY.md` line 51 and `FRAMEWORK.md` §9 item 1, an unqualified class is *"not evidence either way."* Allowing an unqualified gradient test to earn support for the hypothesis while refusing to let a well-powered failure kill creates an asymmetric confirmation standard. Under C7, §8 item 4 must be revised so that either (A) ordinal selection-gradient tests without §3 qualification test only the PF17 corollary and **cannot** earn `CORE.md` §3 support (nor kill), or (B) if Chad admits a power-checked gradient test for the main hypothesis, its preregistered failure must carry symmetric refutation weight.

4. **B4 — Factual errors in `STATUS.md` refresh vs `git log` on `main`, and overstatement on field blockers.**
   - `STATUS.md` line 3 claims: *"None of #117–#132 bumped CLAIM_MAP."* False: PR #117 (`b12af70`) bumped `CLAIM_MAP_v2.md` to **v2.67** (note at line 77; tally 312), before PR #116 (`a1a98aa`) bumped it to v2.68. It is **#118–#132** that did not bump the `CLAIM_MAP` version (#124 and #127 edited *E. coli* prospect notes without bumping v2.68 or the 318 tally).
   - `STATUS.md` line 8 (*"Every field path stalled on independently measured, fitness-unit prices"*) and `REVEALED_PRICES` §1 line 19 (*"Every field attempt from 18 to 21 November (E. coli, the grids, VIS-1F, the shortlist) stopped at the same gate: prices measured independently of the design, in fitness units"*) overstate the merged record: `GRID-CROSS` (PR #128) was blocked by missing pre-control imbalance data (`d1`), *E. coli* P1/P3 (PR #127) failed R3 discrimination (`τ_v = 1.160 s` in `[1.093, 1.171]` s) alongside missing `σ` and `T_red`, and `VIS-1F` (PR #130) was dropped on **both** `(h, w)` and L3 (`VIS1F_DROP_2026-11-21.md` line 5).

---

## Should-fixes

1. **S1 — §3.4 unknown-stakes count error (line 65).** *"with items read at different stakes but one technology p stays 1 if the stakes are measured, 2 if not"* is false when `m > 2` items each have an unknown stake `w_i` (`p` can be up to `m`, not `2`). `p = 2` holds only if there are at most two distinct unmeasured stake levels (e.g., two stake groups, or `m = 2`).
2. **S2 — §3.1 order vs rank condition.** Clarify that `n_fit ≥ p` is only the order condition; identification also requires full rank (the fit set must vary exogenous conditions/features independently rather than repeating uninformative conditions).
3. **S3 — §5 misreading of CT34 and §6 prior-art overclaim on §3.2.**
   - §5 lines 79–81 attributes *"each layer is an agent solving the same problem with its own currency"* and *"the child's optimized cost, expressed in the parent's units, is the exchange rate"* to CT34. Neither is in `THEORY.md` line 472 (CT34 is single-currency cooperative partial minimization; separate-interest agents belong to CX2/CT31; and `J*_T(θ(x))` enters as a constant upkeep `h` only when `θ` is independent of `x`).
   - §6 line 94 claims *"the CT34-based count (§3.2)"* as *"this repository's"*. Using Bellman optimality / partial minimization (`J*_T(θ(x))`) so downstream value functions do not add free parameters per stage is standard in dynamic programming and structural estimation (Rust 1987; Bellman 1957); only the mapping onto `J` and CT34's shared-driver/weak-coupling exclusions is repository-specific.
4. **S4 — Wrong line citation (§0 line 8) and minor citation/dataset nits (§6, §9).**
   - `REVEALED_PRICES` §0 line 8 cites `THEORY line 43 ("only dimensionless ratios matter")`; that quote is on **line 36**.
   - §6 line 89 writes `Ng & Russell 2000, ICML proceedings (no DOI; credited by title, not Crossref-checked)` without actually giving the title (*"Algorithms for Inverse Reinforcement Learning"*, ICML 2000, pp. 663–670).
   - §9 Hall, Humphries & Kramer 2007 (`10.1139/Z07-030`): the abstract specifies that renewal frequency and magnitude were experimentally manipulated on *artificial* food patches (and sampling did not track them); clarify that artificial-patch renewal rate was manipulated while natural world spectrum was not measured and no public data was found.
5. **S5 — Minor precision in `STATUS.md` line 3.** `history/2026-11-21_NIGHT.md` lists PRs #121–#131 (PR #132 created that record).

---

## DOI / Citation verification log (all checked this session)

- **Crossref (17 DOIs, all 200 OK matching authors/year/journal/title):** `10.2307/2548836` (Samuelson 1938), `10.2307/2549561` (Samuelson 1948), `10.2307/2525382` (Afriat 1967), `10.2307/1912771` (Varian 1982), `10.1287/opre.49.5.771.10607` (Ahuja & Orlin 2001), `10.1115/1.3653115` (Kalman 1964), `10.2307/1911259` (Rust 1987), `10.2307/1907619` (Sargan 1958), `10.2307/1912775` (Hansen 1982), `10.1038/246096a0` (Ohta 1973), `10.1073/pnas.1216223109` (Sung et al. 2012), `10.1038/nrg.2016.104` (Lynch et al. 2016), `10.1073/pnas.0501865102` (Sella & Hirsh 2005), `10.1126/science.276.5309.122` (West, Brown & Enquist 1997), `10.1063/1.531249` (Susskind 1995), `10.1098/rsfs.2016.0149` (Dunlap, Papaj & Dornhaus 2017), `10.1139/Z07-030` (Hall, Humphries & Kramer 2007).
- **DataCite / Dryad (3 DOIs, all resolved):** `10.6084/m9.figshare.4769539` (Dunlap et al. 2017 supplement), `10.5061/dryad.z612jm6k7` (Jacob et al. 2024 *Tetrahymena*), `10.5061/dryad.2j125` (Schlägel et al. 2018 wolves).
- **Non-DOI:** `'t Hooft 1993` (`arXiv:gr-qc/9310026v2` verified), `Ng & Russell 2000` (*"Algorithms for Inverse Reinforcement Learning"*, ICML 2000, pp. 663–670 verified), `Dantzig & Wolfe 1960` (`10.1287/opre.8.1.101`) and `Geoffrion 1970` (`10.1287/opre.18.3.375`) already verified in `litmap/verify/VERIFIED_DOIS.txt`.

---

This review does not merge the PR.
