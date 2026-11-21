# Confirm review: PR #135 at e293617 (S1–S4 and nits applied)

**Reviewer:** confirm pass on a fresh clone. This confirm wrote none of `theory/CROSS_FIELD_MAP_2026-11-21.md`, `theory/cross_field_checks/chow_map.py`, `theory/cross_field_checks/chow_map.out`, `tools/test_cross_field_map.py`, the `litmap/PRIOR_ART.md` row, the first independent review, or the S1–S4 fix commits. Same bot family, not a blind second executor; the verdict is from this fresh re-read, an independent re-derivation of the finite-K formula, a numerical check, and a rerun of the committed scripts, not from memory of the edits.
**Date:** Saturday 21 November 2026, started about 9:07 AM ET, finished about 9:12 AM ET (America/New_York).
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/135 (branch `cross-field-map-2026-11-21`, confirm-start head `e2936173fea346e552b72f5f01b898067b5a42ab`, base `main` `32b46bd2e8df2e66318399960c84d384e317be22`).
**Clone:** fresh `/workspace/conf135` (not the first-review clone `/workspace/rev135` and not an author workdir). At confirm start: local PR ref and then branch `cross-field-map-2026-11-21` at `e293617`, merge-base equal to `origin/main` `32b46bd`. Commits on the branch at start: note `57d2dca`, merge of `origin/main` `370f3a1`, first review `d8ee77b`, S1 `34540e6`, S2 `f6c97bb`, S3 `0161da2`, S4+nits `e293617`. Clean tree at confirm start. Nothing from this PR merged at the start of this confirm. `/workspace/looper` and `/workspace/gtao-evo` were not touched. Compute at nice 19.

**Verdict: READY**

The note is still a derivation, a prior-art verdict, and a data inventory. It is not a prereg, not a lock, and not a field result. The four should-fixes and the wording nits from the first review are applied correctly. `CORE.md` and `THEORY.md` are each byte-identical to current `origin/main` (SHA-256 `CORE.md` `1d48bb351d7d2d25622abe1fa8f06d5603b7121904d17033ff2004057fe3b555`; `THEORY.md` `19a1e326b69b435a8334577386bc27ace0f19d20783ac811f7518fd134be1524`). The law-of-adaptive-organization hypothesis sentence is unchanged in those two files and is quoted correctly in the note. The cross-substrate bet is graded **at most 1, unverified** (not 1–2). The finite-K transient formula re-derives and checks numerically. Checkers PASS. Residuals below do not block a merge of this unlocked note.

At confirm start the PR was open, head `e293617`, base `32b46bd`, seven commits, six files, +366 / −0 relative to `origin/main`.

---

## What was checked

- Fresh clone at the stated start head; `git merge-base HEAD origin/main` equals `32b46bd`. `git diff --stat origin/main...HEAD` at start: six files (`litmap/PRIOR_ART.md`, `reviews/cross_field_2026-11-21/REVIEW.md`, `theory/CROSS_FIELD_MAP_2026-11-21.md`, `theory/cross_field_checks/chow_map.out`, `theory/cross_field_checks/chow_map.py`, `tools/test_cross_field_map.py`). Working tree clean at start. `/workspace/looper` and `/workspace/gtao-evo` not opened.
- First review at `reviews/cross_field_2026-11-21/REVIEW.md` compared to the should-fix list (S1, S2, S3, S4, nits). Fixes checked against the pre-fix tree (`370f3a1` / note `57d2dca`) and against `e293617`.
- Independent re-derivation of the finite-K one-sided transient (below) and an independent geometric-program numeric check, not only a rerun of `chow_map.py`.
- `CORE.md` and `THEORY.md` are each identical to `origin/main`. `README.md`, `STATUS.md`, and `OPEN_WORK.md` are also identical to `origin/main`. The hypothesis sentence is the same string in `CORE.md` line 24 and `THEORY.md` line 41: "The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment." The note quotes that sentence accurately at line 3.
- The six-file diff versus current `origin/main` does not touch `CORE.md`, `THEORY.md`, `CLAIM_MAP_v2.md`, `STATUS.md`, or any locked results, prereg, or deviations file.
- Cited DOIs queried on `https://api.crossref.org/works/{doi}` this session (Chow 1974 retried after an initial 429). All resolved as cited.
- `nice -n 19 python3 theory/cross_field_checks/chow_map.py` PASS, output byte-identical to committed `chow_map.out`. `pytest tools/test_cross_field_map.py` 1 passed. `python3 tools/check_consistency.py` PASS. `python3 tools/check_open_work.py` PASS.

---

## S1 — fixed; T20(A) is K* vs log R, scale range held fixed

Pre-fix, §0 said "T20 part A (count grows with log range, passed in-model)," which is the misstatement fixed on `main` in PR #134.

HEAD states T20 part A as: K* grows roughly linearly in log stakes R with scale range held fixed, official (A) gates 12/12 in-model; T20 overall not supported because (B) failed. That matches the official record used in `theory/CACHE_HIERARCHY_PRIOR_ART_2026-11-21.md` and in `reviews/cache_prior_art_2026-11-21/REVIEW.md` S1.

---

## S2 — fixed; formula re-derived; numeric check passes

§2.3 now states that C_{k+1}/C_k = D_{k+1}/D_k = q = 1/(θγ) is exact for all finite K and S, even when θγ ≥ 1. §2.5 gives the exact finite-K solution, one-sided decay from the small-s (k = 1) edge when θγ < 1 (x_K closest to x*), backward decay from the large-s (k = K) edge when θγ > 1, the uniform law x_k = (ln S)/K at θγ = 1, and the x_1 ≥ 0 feasibility bound. `chow_map.py` Part 1 now labels S = exp(K · ln r_s) as sitting on the fixed point with no boundary mismatch, and Part 3 is a direct GP solve with mismatched S, including θγ = 1 and θγ > 1.

Independent re-derivation (this confirm). From the two first-order conditions D_k = γ λ C_k and λ C_k = θ D_{k+1}, the adjacent ratios C_{k+1}/C_k = D_{k+1}/D_k = 1/(θγ) = q hold at every adjacent pair, with no appeal to a large-K limit. Writing x_k = ln(s_k/s_{k-1}) and y_k = ln(t_{k+1}/t_k) gives y_k = ln q + θ x_k and x_{k+1} = ln q + γ y_k, hence x_{k+1} − x* = g (x_k − x*) with g = θγ and

ln r_s = x* = −(1+γ) ln(θγ) / (1 − θγ),  ln r_t = y* = −(1+θ) ln(θγ) / (1 − θγ).

The recurrence plus Σ_{k=1}^K x_k = ln S then gives x_k − x* = g^{k−1} (x_1 − x*) and

K x* + (x_1 − x*) (1 − g^K)/(1 − g) = ln S  (g ≠ 1),

so

x_1 − x* = (1 − g)/(1 − g^K) · (ln S − K x*),

and therefore

x_k − x* = (θγ)^{k−1} · (1 − θγ)/(1 − (θγ)^K) · (ln S − K x*),

which is the formula in §2.5. The g → 1 limit is 1/K by L'Hôpital, so x_k = (ln S)/K identically. The sign of (1−g)/(1−g^K) is positive for g ≠ 1, so when ln S > K x* the deviations decay from k = 1 if g < 1 and grow toward k = K if g > 1. The bound x_1 ≥ 0 is equivalent to ln S ≥ K x* − x* · [1 − (θγ)^K]/(1 − θγ), as written.

Independent numeric check (own GP solve, nice 19): algebraic identities hold to machine precision (sum of x_k, recurrence, x_1 < 0 when the bound is violated, g → 1 limit). Direct convex solves at K = 6 for (θ, γ) ∈ {(0.5, 0.5), (0.7, 0.8), (1.0, 1.0), (1.2, 1.2), (0.3, 1.0)} match the exact x_k and exact C_{k+1}/C_k = D_{k+1}/D_k = q to worst error 3.27×10^{-5}, with the predicted one-sided directions. Official `chow_map.py` rerun at nice 19 is byte-identical to committed `chow_map.out` (Part 1 mid-level relative error ≤ 4.65×10^{-4} in the well-conditioned cases; Part 3 worst mismatched-S GP error 3.09×10^{-5}; RESULT: PASS).

---

## S3 — fixed; cross-substrate bet is at most 1, unverified

Pre-fix, both the note §3 and the `litmap/PRIOR_ART.md` row graded the cross-substrate bet as `1–2`. Under the litmap rubric, 2 requires a new formula or test. HEAD grades the map itself **novelty 0** and the cross-substrate bet **at most 1 (same formula/idea, new domains), unverified**. The note states explicitly that grade 2 does not apply: the formula is Chow 1974 (0), the cross-substrate template is prior art (0), and no test is locked. The `PRIOR_ART.md` cell matches: "0 for the map; at most 1 for the cross-substrate bet, unverified." Nothing in this PR inflates that grade.

Chow 1974 Eqs. (36)–(41) are credited in the note §3 (Eq. 36 for cost share = delay share, Eq. 39 for the 1/(θγ) cost ratio, Eq. 41 for the (θγ) recurrence), alongside Welch 1978, with the public bitsavers copy `ibmrd1803B.pdf` noted and the "Full text not read (paywalled)" wording gone. The compact `PRIOR_ART.md` cell credits Eq. 36 and Eq. 39; Eq. 41 is in the note (residual 2 below). Verified DOIs for West, Brown & Enquist 1997 (`10.1126/science.276.5309.122`), Lee, Flack & Krakauer 2024 (`10.1098/rspb.2024.1606`), and Benna & Fusi 2016 (`10.1038/nn.4401`) are in the note §3; the first two are also in the litmap row.

---

## S4 and nits — applied

§5 row 2 no longer lists Breslau et al. 1999 as a measured θ for m(s) = s^{−θ}. It states Zipf-like rank popularity α ∈ [0.64, 0.83] < 1, hit ratio ∼ (s/N)^{1−α}, and finite-catalog miss rate 1 − (s/N)^{1−α}, and notes that a scale-free miss curve s^{−θ} with θ > 0 would require α > 1 and θ = α − 1.

Nits: §2.2 now calls D_k the delay contribution and D_k/T its share of delay. The §2.3 "number of levels" row now says ≈ ln(S/s_1)/ln r_s once s_1 is pinned, or once K is optimized against per-level upkeep h. §0 now distinguishes Chow and Roundy (via optimization) from Benna & Fusi (cascade design) and Jaques (empirically). The three DOIs named in the first review's nit list are present in §3.

---

## No overclaim; no test locked; novelty not inflated

The file is still not a prereg and not a lock. The bottom line is unchanged: 0 fields have all three pieces measured and compiled today; 1 (caches/storage) can reach it with public data; the bar was 3; nothing was locked. The cache field is still described as an anchor, not independent support, because engineers optimize with Chow-type models. The cross-substrate bet remains at most novelty 1, unverified. No official row is re-scored. `CORE.md`, `THEORY.md`, and the law sentence were not edited by this PR.

---

## Checkers (this clone, nice 19)

- `nice -n 19 python3 theory/cross_field_checks/chow_map.py` — PASS; output identical to `theory/cross_field_checks/chow_map.out`
- `nice -n 19 python3 -m pytest tools/test_cross_field_map.py` — 1 passed
- `python3 tools/check_consistency.py` — PASS (0 FAIL; 23 frozen-record INFO hits; soft length WARNs on THEORY.md and README.md already present on `main`)
- `python3 tools/check_open_work.py` — PASS (union missing from OPEN_WORK.md: 0)

---

## Crossref (this session)

All of the following resolved: Chow 1974, 10.1147/rd.183.0194, *IBM J. Res. Dev.* 18:194–203, "On Optimization of Storage Hierarchies"; Chow 1976, 10.1109/tc.1976.5009230, *IEEE Trans. Comput.*, 1976; Welch 1978, 10.1109/tc.1978.1675120, 1978; Lera & Sornette 2019, 10.1371/journal.pone.0214911, *PLOS ONE*; Zhou, Sornette, Hill & Dunbar 2005, 10.1098/rspb.2004.2970; West, Brown & Enquist 1997, 10.1126/science.276.5309.122, *Science* 276; Lee, Flack & Krakauer 2024, 10.1098/rspb.2024.1606, *Proc. R. Soc. B*; Benna & Fusi 2016, 10.1038/nn.4401, *Nat. Neurosci.*; Alpern, Carter & Feig 1990, 10.1109/FSCS.1990.89581, FOCS; Hartstein et al. 2006, 10.1145/1128022.1128064; Breslau et al. 1999, 10.1109/infcom.1999.749260; Anderson & Schooler 1991, 10.1111/j.1467-9280.1991.tb00174.x; Roundy 1985, 10.1287/mnsc.31.11.1416; Hamilton et al. 2007, 10.1098/rspb.2007.0564; Gray & Graefe 1997, 10.1145/271074.271094; Appuswamy et al. 2019, 10.1145/3318163.

---

## Residuals (do not block)

1. **§2.1 still mentions Breslau et al. 1999 in the same parenthetical as the definition of m(s) = s^{−θ}.** The wording there is only "measure Zipf-like request popularity on the web," which is accurate. The S4 qualification the first review asked for is in the inventory table. Not a gap in the required fix.
2. **The compact `litmap/PRIOR_ART.md` cell credits Chow 1974 Eqs. 36 and 39 but not Eq. 41.** The recurrence is credited in the note §3, which is where the first review's equation-level credit is carried. Not a gap in the required fix.
3. **`reviews/README.md` does not yet index this review folder.** The first review did not require that row. Not a blocker for this unlocked note.
4. **Chow 1974 full text was not re-opened in this confirm.** Bibliographic details were re-checked on Crossref. Equation-level credit was checked against the first review's inspection of the public bitsavers copy, not re-read here.

This confirm does not merge.
