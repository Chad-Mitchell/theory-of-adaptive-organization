# Confirm review: PR #136 at 2f4b2ff (S1–S4 applied)

**Reviewer:** confirm pass on a fresh clone. This confirm wrote none of `theory/FIELD2_FEASIBILITY_2026-11-21.md`, the first independent review, or the S1–S4 fix commits. Same bot family, not a blind second executor; the verdict is from this fresh re-read and independent recomputation, not from memory of the edits.
**Date:** Saturday 21 November 2026, started about 10:14 AM ET, finished about 10:17 AM ET (America/New_York).
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/136 (branch `field2-feasibility-2026-11-21`, confirm-start head `2f4b2ff4e3dffb3acae23c97a677ff9010e386ca`, base `main` `cd84095`).
**Clone:** fresh `/workspace/conf136` (not the first-review clone `/workspace/rev136` and not an author workdir). At confirm start: PR ref checked out as local `pr136` at `2f4b2ff`, merge-base equal to `origin/main` `cd84095`. Commits on the branch at start: note `c4f798a`, first review `bb7afd6`, S1 `9b9fb5d`, S2 `952c737`, S3 `1ac9e39`, S4 `2f4b2ff`. Clean tree at confirm start. Nothing from this PR merged at the start of this confirm. `/workspace/looper` and `/workspace/gtao-evo` were not touched. Compute at nice 19.

**Verdict: READY**

The note is still a Pass 0 scouting memo, not a prereg, not a lock, and not a scored test. The four should-fixes from the first review (S1–S4) are applied correctly. Independently recomputed figures match the note: Appuswamy three-point γ = 0.4905 on Table 6 prices, Gray & Graefe γ = 0.3410, OhioLINK α_rank ≈ 0.91 from 7.2%/80% under the note's finite-catalog formula, and library γ is stated as conditional on an assumed open-stack retrieval time. `CORE.md` and `THEORY.md` are each byte-identical to current `origin/main` (SHA-256 `CORE.md` `1d48bb351d7d2d25622abe1fa8f06d5603b7121904d17033ff2004057fe3b555`; `THEORY.md` `19a1e326b69b435a8334577386bc27ace0f19d20783ac811f7518fd134be1524`). The law-of-adaptive-organization hypothesis sentence is unchanged in those two files and is quoted correctly in the note. Checkers PASS. Residuals below do not block a merge of this unlocked note.

At confirm start the PR was open, head `2f4b2ff`, base `cd84095`, six commits, two files, +260 / −0 relative to `origin/main`.

---

## What was checked

- Fresh clone at the stated start head; `git merge-base HEAD origin/main` equals `cd84095`. `git diff --stat origin/main...HEAD` at start: two files (`reviews/field2_2026-11-21/REVIEW.md`, `theory/FIELD2_FEASIBILITY_2026-11-21.md`). Working tree clean at start. `/workspace/looper` and `/workspace/gtao-evo` not opened.
- First review at `reviews/field2_2026-11-21/REVIEW.md` compared to the should-fix list (S1, S2, S3, S4). Fixes checked against the pre-fix tree (`c4f798a`) and against `2f4b2ff`.
- Independent recomputation (nice 19, own OLS and the note's H(s)=(s/N)^{1-α} inversion), not a copy of the first review's numbers.
- `CORE.md` and `THEORY.md` are each identical to `origin/main`. `README.md`, `STATUS.md`, `OPEN_WORK.md`, and `CLAIM_MAP_v2.md` are also identical to `origin/main`. The hypothesis sentence is the same string in `CORE.md` line 24 and `THEORY.md` line 41: "The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment." The note quotes that sentence accurately at line 3.
- The two-file diff versus current `origin/main` does not touch `CORE.md`, `THEORY.md`, `CLAIM_MAP_v2.md`, `STATUS.md`, or any locked results, prereg, or deviations file.
- `nice -n 19 python3 tools/check_consistency.py`: **PASS** (0 FAIL).
- `nice -n 19 python3 tools/check_open_work.py`: **PASS** (0 missing).

---

## S1 — fixed; Appuswamy three-point γ uses Table 6 and is 0.4905

Pre-fix, the compiled table and the DRAM–HDD pairwise fit used Table 6's $50 / $0.025/GB, but the three-point DRAM–SATA–HDD OLS silently used Table 1's $49 / $0.0245/GB, giving γ = 0.4925 (R² = 0.9982) and 50/100 µs sensitivities 0.4844 / 0.4728.

HEAD reports γ = **0.4905** (R² = 0.9984) using Table 6 HDD cost $0.025/GB, with sensitivities 0.4826 (R² = 0.9717) at 50 µs and 0.4711 (R² = 0.9426) at 100 µs, and notes that Table 1's $49 shifts the three-point fit only to 0.4925. Independent OLS on (ln t, ln c) with DRAM $5.00/GB at 100 ns, SATA $415/800 GB at t = 1/67,000 s, and HDD $0.025/GB at 5 ms reproduces γ = 0.49054, R² = 0.99838; 50 µs: 0.48261 / 0.97170; 100 µs: 0.47111 / 0.94263; Table 1 $0.0245/GB: 0.49245. The pairwise DRAM–HDD fit remains 0.48969 (note 0.4897). The cache band γ ∈ [0.34, 0.49] and the §1.2 Chow ratios at γ = 0.490 are unchanged and recompute to the stated ranges (r_t floor 16.0 is 15.94 rounded; q upper 6.81 is from 0.4897 rather than 0.490, as the first review already noted).

---

## S2 — fixed; OhioLINK implied α_rank is ≈ 0.91

Pre-fix, the library row and the honesty gate said 7.2% drive >80% of loans, implied α_rank ≈ 0.56, and placed the 11.4% non-circulating share in Table 3 p. 796.

HEAD states that 7.2% of manifestations account for 80% of loans (p. 801 and Table 6 p. 802), which under H(s)=(s/N)^{1-α} implies α_rank ≈ 0.91 < 1, and that the paper reports no fitted Zipf slope (Fig. 3 is lin-log). The 11.4% non-circulating share is now Table 6 p. 802; Table 3 p. 796 correctly carries the ARL 7.45M / 0.144/yr and depository 4.18M / 0.025/yr figures. Independent inversion 0.072^{1-α} = 0.80 gives α_rank = 0.9152, which rounds to 0.91. The value is still < 1, so the scale-free gate still fails and the Pass 1 recommendation stands. The honesty-gate figure is likewise 0.91.

---

## S3 — fixed; library γ is conditional on an assumed t_open

Pre-fix, the library γ cell was labeled "Measured, independent," Payne was quoted as "≤ 24 h," the 0.322 / 0.28–0.35 figures were given without saying that 10 min (and the 5–15 min band) is assumed, Courant's circulation element was not disclosed, and the verdict said "γ & ladder ready."

HEAD labels the cell "Published costs, latency partly assumed," quotes Payne as "typically within 24 h," states 0.322 at an *assumed* 10 min open-stack retrieval vs. 24 h depository, states that the 0.28–0.35 band is 5–15 min on the inflated pair, and says open-stack retrieval time is not measured in Courant or Payne. Courant's $4.26 and $0.86 are disclosed as perpetual annual averages that include circulation, not holding cost alone. The verdict is "ladder ready, γ usable once t_open is pre-specified." The recommendation and the draft prereg outline carry the same qualifications. Independent recomputation: −ln(0.86/4.26)/ln(24 h / 10 min) = 0.32196 (note 0.322); no-inflation 0.28876 (note 0.289); 5 min → 0.2826 and 15 min → 0.3506, matching the 0.28–0.35 band. Library γ is not called a fully measured two-tier exponent.

---

## S4 — fixed; qualification cite, Huddersfield, Gray page, Jackson TAT

- K2 now points to `THEORY.md` §3 (operational σ, N_e, ε=10/(σ N_e), rival, T_red; see also `CORE.md` §2 and `measurement/FRAMEWORK.md` §9). Confirmed against those files: the five-item checklist is `THEORY.md` lines 45–51; `CORE.md` §3 is the hypothesis paragraph; `CORE.md` §2 already points to THEORY §3; the CORE load-bearing table cites "THEORY §3, FRAMEWORK §9."
- Lawrence et al. 2001 p. 542 is now described as documenting costing-system weakness / weak cost-management incentives, not a recorded σ, N_e qualification.
- "Huddersfield" is gone from the honesty gate. The four studies listed are Bulick 1978, OhioLINK 2014, Hashimoto 2024, and Burrell 1980/85.
- Gray & Graefe 1997 Table 8 is cited as MSR-TR-97-33 p. 7, not p. 6.
- Jackson 2004 is $18.35/tx, 15.6 calendar days, not "15.6–16 days."

---

## No lock, no scored test, hypothesis unchanged

The preamble and §3.2 header still state **Pass 0 / not a prereg / nothing locked / no scored test / do NOT lock yet.** There is no preregistration hash, no scored prediction, and no `CLAIM_MAP` row. The note does not claim that library θ > 0 is already measured; the honesty gate and the table both say scale-free θ > 0 is unverified and that published static circulation has α_rank < 1. Nothing in this PR edits the hypothesis sentence.

---

## Residuals (do not block READY)

These are leftover first-review nits, not unapplied should-fixes:

- Hashimoto 2024 is still not labeled a conference abstract in the registry, though it is no longer called a journal article; the CCDF-to-α conversion 1/μ ∈ [0.50, 0.61] recomputes.
- Sandler 2012 remains in the §4 registry unused in the body.
- Bulick 1978 still says "direct fit α_rank ≈ 0.26" without stating the unweighted frequency-class OLS estimator.
- The $3.7×10^3$ ATP/min/PSD figure is still attributed in a clause with Cohen et al. 2013, Heo et al. 2018, and Karbowski 2019, without a single-source pin.
- The §1.2 Chow q upper end 6.81 is the 0.4897 pairwise value; at the rounded γ = 0.490 it is 6.80.

None of these creates a lockable field, withdraws the library-first recommendation, or meets the first review's NOT READY conditions. After S1–S4 the note remains an honest Pass 0 map of where a Field-2 test could be built.
