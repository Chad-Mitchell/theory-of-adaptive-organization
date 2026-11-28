# Confirm review: PR #134 at d924a30 (S1, S2 and nits applied)

**Reviewer:** confirm pass on a fresh clone. This confirm wrote none of `theory/CACHE_HIERARCHY_PRIOR_ART_2026-11-21.md`, the `litmap/PRIOR_ART.md` row, the first independent review, or the S1 / S2 / nits fix commits. Same bot family, not a blind second executor; the verdict is from this fresh re-read and re-check, not from memory of the edits.
**Date:** Saturday 21 November 2026, started about 8:53 AM ET, finished about 8:56 AM ET (America/New_York).
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/134
**Clone:** fresh `/workspace/conf134` (not the first-review clone `/workspace/rev134` and not an author workdir). At confirm start: branch `cache-prior-art-2026-11-21` at head `d924a30f3027b5e63e1c27aa15d44f23391f5879`, merge-base and then-`origin/main` `a65b64e4f6863900c8d789f51e590dad67dd8a41`. Commits on the branch at start: note `a07903c`, first review `daa1179`, S1 `615c149`, S2 `332baa9`, nits `d924a30`. During this confirm, PR #133 merged to `main` as `cda9c41ce625b07e10755c8b41b54deb927460e8`. `origin/main` was merged into this branch with no conflicts (no overlapping paths; merge commit `1b1b62af93cd1f6d09b2133c46890d1043c4c48f`). Checkers were re-run after that merge. Clean tree at confirm start and after the merge. Nothing from this PR merged at the start of this confirm. `/workspace/looper` and `/workspace/gtao-evo` were not touched. Compute at nice 19.

**Verdict: READY**

The note is still a prior-art verdict, not a prereg, not a lock, and not a scored result. The two should-fixes and the four nits from the first review are applied correctly. After the merge of PR #133, `CORE.md`, `THEORY.md`, and `README.md` are each byte-identical to current `origin/main` (SHA-256 `CORE.md` `1d48bb351d7d2d25622abe1fa8f06d5603b7121904d17033ff2004057fe3b555`; `THEORY.md` `19a1e326b69b435a8334577386bc27ace0f19d20783ac811f7518fd134be1524`; `README.md` `594328b57839642536f02ef96021350bfaed97952ba6e339ae556941a6a87651`). The law-of-adaptive-organization hypothesis sentence is unchanged in those three files and is quoted correctly in the note. All eight cited DOIs re-resolve on Crossref this session, including the Jacob comment as 1997, 46:1151. Checkers PASS. No new overclaim. Residuals below do not block a merge of this unlocked prior-art note.

At confirm start the PR was open, head `d924a30`, base `a65b64e`, five commits, four files, +165 / −0. After merging current `main`, the PR still touches only those four files relative to `cda9c41`.

---

## What was checked

- Fresh clone at the stated start head; `git merge-base` then equaled `origin/main` `a65b64e`. `git diff --stat origin/main...HEAD` at start: five commits, four files (`litmap/PRIOR_ART.md`, `reviews/README.md`, `reviews/cache_prior_art_2026-11-21/REVIEW.md`, `theory/CACHE_HIERARCHY_PRIOR_ART_2026-11-21.md`). Working tree clean at start. `/workspace/looper` and `/workspace/gtao-evo` not opened.
- First review at `reviews/cache_prior_art_2026-11-21/REVIEW.md` compared to the should-fix list (S1, S2, nits i–iv). Fixes checked against the pre-fix tree (`a07903c`) and against `d924a30`.
- T20(A) re-read at `core/keystone_checks/holographic_2026-11-20/PREREG.md` §5.1 and lines 7–9, and at `RESULTS.md` official-gates table and §1. CT34 re-read at `THEORY.md` B.10 (the CT34 paragraph).
- After PR #133 landed, `origin/main` `cda9c41` was merged into this branch (clean). `CORE.md`, `THEORY.md`, `README.md`, `STATUS.md`, and `OPEN_WORK.md` are each identical to current `origin/main`. The hypothesis sentence is the same string in `CORE.md` line 24, `THEORY.md` line 41, and `README.md` line 9: "The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment."
- The four-file diff versus current `origin/main` does not touch `CORE.md`, `THEORY.md`, `CLAIM_MAP_v2.md`, `STATUS.md`, `FRAMEWORK.md`, or any locked results, prereg, or deviations file.
- All eight DOIs queried on `https://api.crossref.org/works/{doi}` this session.
- R3 in the now-merged `theory/REVEALED_PRICES_2026-11-21.md` §2 re-read: a pass that does not differ from a named rival, fitted the same way, supports the rival as much as the law. The note's use remains faithful.
- `python3 tools/check_open_work.py` PASS. `python3 tools/check_consistency.py` PASS (0 FAIL; 23 frozen-record INFO hits; soft length WARNs on THEORY.md and README.md already present on `main`). Both were re-run after the merge of `main`.

---

## S1 — fixed; T20(A) is K* vs log R, span fixed, not Chow's log-capacity axis

Pre-fix, the first table row and §3.1 treated T20 part A as "K* grows linearly in the log of the scale range (passed 12/12)" and as already stated by Chow.

HEAD states T20 part A as: K* grows roughly linearly in log R, with the world's scale range held fixed (official (A) gates 12/12 in-model; R = w E_∞ / h). It records that the holographic motivation in the T20 prereg — layers growing with the log of the scale range — is a different claim, and that T20 overall was not supported because prediction (B) failed. Chow 1974/1976 are stated as log-linear in *capacity* (or a capacity ratio), not in the stakes R that T20(A) varied. Any coincidence under an identification of capacity ratio with a scale range, or under power-law technology tying capacity to access time, is labeled an analogy, not an identity, and "not what the 12/12 pass tested."

That matches the official record. `PREREG.md` line 9 and §5.1: K* grows roughly linearly in log R as R runs from 1 to 10^8. Primary worlds hold the scale range fixed (Γ = 10^4, four decades). `RESULTS.md`: Family S (A) 6/6 and Family M (A) 6/6, overall **NOT SUPPORTED** because (B) failed in both families.

§2's lead-in no longer says every part of the GTAO prediction in this domain was already derived. §3.1 no longer says the field "arrived at GTAO's layer-count" results; it credits geometric spacing, a log-capacity level count, and fixed cost shares, and says this is not a statement that T20 part A (K* vs log R) was already in Chow. §3.2 says T20 part A should not be listed as already stated by Chow without the axis caveat. The body wording "novelty 0–1" is gone; the cache-domain results are graded **novelty 0** (stated before, in the same form, in this domain), which is what the first review asked to harmonize.

The PRIOR_ART component label no longer lists "T20 part A, T7b, CT24 in caches" as the already-stated bundle. It now reads: Chow's log-capacity level count and geometric ratios, compared with T7b and CT24 in caches; T20 part A is K* vs log stakes, a different axis — see the note. The novelty-0 grade of the cache-domain program is unchanged. No test was locked.

---

## S2 — fixed; Przybylski is an interaction, not CT34

The CT34 table row is qualified. It still records Przybylski, Horowitz & Hennessy 1989 as related, not the same result: the abstract shows an interaction (L1 filtering changes L2's optimal size vs cycle-time tradeoff). It states CT34 as the composition theorem: the team's optimized cost enters the parent exactly as F(x) + J*_T(θ(x)), and is a constant upkeep only when θ does not depend on x (`THEORY.md` B.10). The abstract is said not to state that composition or the upkeep condition. The row is not treated as prior art for CT34 itself, and is not part of the novelty-0 grade.

That is what B.10 says: J(x, y) = F(x) + G(y; θ(x)); exactness is min_{x,y} J = min_x [F(x) + J*_T(θ(x))]; J*_T is a constant upkeep if θ does not depend on x (and, generically, only if).

---

## Nits — applied

1. **Jacob comment.** Year is 1997, *IEEE Trans. Comput.* 46:1151, doi 10.1109/12.628401, described as a citation correction regarding MacDonald & Sigworth 1975, not additional support for the closed-form or the spending-proportion results. Crossref this session: type journal-article, issued 1997, title "A comment on 'An analytical model for designing memory hierarchies'", container *IEEE Transactions on Computers* 46:1151, authors Jacob, Chen, Mudge, Silverman. Matches. The 1996 paper itself (doi 10.1109/12.543711) is 45:1180–1194, as cited.
2. **Mattson.** Stack-distance / one-trace evaluation is now called the paper's well-known contribution, supported this session by a Semantic Scholar TLDR, and is explicitly not in the OpenAlex abstract (which only introduces storage hierarchies across technologies; full paper not read).
3. **Grep.** The claim is now limited to bibliographic hits for Chow, Przybylski, Mattson, Hartstein, or "stack distance," with the only outside "Welch" hits being the spectrum estimator in the grid tests. A search for the string "miss rate" is stated to hit unrelated text (a Looper self-result and a pass-rule audit) and is not evidence about these papers.
4. **Currency.** The CT24 row now says currency-freeness ("in any currency") is CT24's homogeneity, not a claim in the Welch or Jacob abstracts.

The other six DOIs also resolve as cited: Chow 1974, 10.1147/rd.183.0194, *IBM J. Res. Dev.* 18:194–203; Chow 1976, 10.1109/tc.1976.5009230, *IEEE Trans. Comput.* C-25:157–164; Welch 1978, 10.1109/tc.1978.1675120, C-27:408–413 (Crossref and OpenAlex list the author only as Welch, no given name); Przybylski, Horowitz & Hennessy 1989, 10.1145/74925.74939; Mattson, Gecsei, Slutz & Traiger 1970, 10.1147/sj.92.0078, *IBM Syst. J.* 9:78–117; Hartstein, Srinivasan, Puzak & Emma 2006, 10.1145/1128022.1128064.

---

## No overclaim; no test locked

The file is still a prior-art verdict in one domain, not a new law and not a lock. The no-lock conclusion still rests on R3: in this domain, J with power-law hit and technology functions is Chow's geometric program, so a held-out pass would support the storage-hierarchy theory, not GTAO. That conclusion no longer depends on identifying T20(A) with Chow. Novelty 0 is scoped to the cache-domain results (geometric spacing, log-capacity or log capacity-ratio level count, fixed cost shares). T20 part A is carved out. No official row is re-scored. `CORE.md` and the law sentence were not edited by this PR.

---

## Checkers (this clone, after merging current main)

- `python3 tools/check_open_work.py` — PASS (union missing from OPEN_WORK.md: 0)
- `python3 tools/check_consistency.py` — PASS (0 FAIL)

---

## Residuals (do not block)

1. **The compact `litmap/PRIOR_ART.md` cell still lists Przybylski, Mattson, and Hartstein in the same prior-art cell as Chow, Welch, and Jacob, without a parenthetical on Przybylski.** The component label no longer claims CT34, and the note's table carries the required qualification. That is the S2 fix the first review asked for. Not a gap in the required fix.
2. **The note still locates itself "beside `main` `a65b64e` and PR #133."** That was accurate when the note was written. During this confirm, PR #133 merged as `cda9c41`. The locator is historical. R3 in the merged `theory/REVEALED_PRICES_2026-11-21.md` §2 is the same rule the note relies on.
3. **Full papers were not opened in the note, the first review, or this confirm.** Bibliographic details were re-checked on Crossref. The Mattson stack-distance source caveat is present in the text; the Semantic Scholar TLDR was not re-fetched here.

---

## Recommendation

Merge is appropriate. The two should-fixes and the four nits are applied, the eight DOIs resolve as cited, CORE and the law sentence are untouched by this PR, and no test is locked. This is not a scored result, and it does not start a cache-hierarchy test of GTAO.
