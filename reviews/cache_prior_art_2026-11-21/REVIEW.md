# Independent hostile review: PR #134 (cache-hierarchy prior art; no lock)

**Reviewer:** independent (wrote none of the PR, `theory/CACHE_HIERARCHY_PRIOR_ART_2026-11-21.md`, or the `litmap/PRIOR_ART.md` row). Same bot family, not a blind second executor.
**Date:** Saturday 21 November 2026, started 8:45 AM ET, finished 8:55 AM ET (America/New_York).
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/134
**Clone:** fresh `/workspace/rev134/repo` at head `a07903c9e0b3d4306dea74ff64537f406c601f2a` (branch `cache-prior-art-2026-11-21` / local `pr134`), merge-base and `origin/main` `a65b64e`. Clean tree at review start. Nothing merged. `/workspace/looper` and `/workspace/gtao-evo` were not touched. Compute at nice 19.

**Verdict: READY-WITH-FIXES**

The note is a prior-art verdict, not a prereg, not a lock, and not a scored result. That decision is right: with power-law hit and technology functions, the cache-hierarchy design problem is already Chow's 1974 geometric program, so a held-out pass would support the storage-hierarchy literature (already checked against simulation by Jacob et al. 1996) and would fail R3 of unmerged PR #133 §2 by construction. All eight cited DOIs resolve on Crossref this session; the quoted sentences from Chow 1974/1976, Welch 1978, Jacob et al. 1996, and Hartstein et al. 2006 match the OpenAlex abstracts; bibliographic details (titles, venues, volumes, pages, years, author lists) match Crossref. `CORE.md` and `THEORY.md` are untouched. The law-of-adaptive-organization hypothesis sentence is unchanged and is quoted correctly. `python3 tools/check_consistency.py` at nice 19: **PASS** (0 FAIL; frozen-record INFO hits and soft length WARNs already on main).

Two should-fixes belong in this PR before merge. Neither moves a theorem, a lock, or a field verdict, and neither overturns the "do not lock" conclusion.

- **S1.** T20 part A is misstated as "K* grows linearly in the log of the scale range (passed 12/12)." The official T20(A) gate, which did pass 6/6 + 6/6, is that K* grows roughly linearly in **log R** with the world's scale range **held fixed** (primary worlds: four decades; R = w E_∞ / h, grid 1 to 10^8). The phrase "log of the scale range" is the holographic *motivation* in the T20 prereg, not the gate that passed, and T20 overall was **not supported** because prediction (B) failed. Chow's abstracts state a different law: K* ∝ log(systems capacity) (1974) or log(required hierarchy capacity / cache capacity) (1976). Mapping T20(A) onto Chow as the same result is not fair. The no-lock conclusion can rest on Chow already having solved this domain's program, not on identity with T20(A).
- **S2.** The CT34 row over-credits Przybylski, Horowitz & Hennessy 1989. Their abstract shows an interaction (a first-level cache changes the second-level size vs cycle-time optimum). CT34 is a composition theorem: the team's optimized cost enters the parent as F(x) + J*_T(θ(x)), and is a constant upkeep only when θ does not depend on x. The abstract does not state that theorem. The row is not part of the official novelty-0 grade, which is correct; it still should not be presented as the same form.

Nits: the Jacob et al. comment is 1997 and is a citation correction, not further support for the closed form or the spending proportions; the Mattson stack-distance / one-trace claim is the paper's well-known contribution but is not in the OpenAlex abstract the note says was the source; the "no hit" grep overstates what a search for the string "miss rate" shows; "in any currency" is CT24's homogeneity, not a claim in the Welch or Jacob abstracts.

---

## What was checked

- Fresh clone at the stated head/base; diff `a65b64e..a07903c` (one commit, 2 files, +37 / −0): new `theory/CACHE_HIERARCHY_PRIOR_ART_2026-11-21.md` and one new row in `litmap/PRIOR_ART.md`. No other path is touched. `CORE.md` and `THEORY.md` are byte-identical to `origin/main`.
- Every DOI on `https://api.crossref.org/works/{doi}` this session (all eight: Chow 1974, Chow 1976, Welch 1978, Jacob et al. 1996, the Jacob comment, Przybylski et al. 1989, Mattson et al. 1970, Hartstein et al. 2006). Abstracts reconstructed from OpenAlex inverted indexes this session. Full papers were not read, matching the note's own limit; one secondary check (Semantic Scholar TLDR for Mattson) is flagged as such below.
- Each table mapping against the canonical statements: T20(A) in `core/keystone_checks/holographic_2026-11-20/PREREG.md` §5.1 and `RESULTS.md` §1 and the official-gates table; T7b in `theory/THEOREMS.md`; CT24 and CT34 in `THEORY.md` (front-matter "Scale-free cost shares" and Appendix B.9 / B.10).
- Novelty-0 against the legend in `litmap/PRIOR_ART.md` ("0: stated before, in the same form") and against the existing "Nested levels" row (T7b already graded 1–2, with Roundy 1985 and others).
- The "not already in the repository" grep, the claimed-reachable public data hosts, the citation of R3 in unmerged PR #133 §2 (read from `pr133` / `799d44e`, not on this branch), and the hypothesis sentence.
- `python3 tools/check_consistency.py` (nice 19): PASS, 0 FAIL.

---

## 1. DOIs and abstracts

All eight DOIs return Crossref `status: ok`. Titles, containers, volumes, pages, years, and author lists match the note's short cites, with the comment-year and Mattson-abstract caveats below. Crossref has no abstracts; OpenAlex does.

| Cite in the note | Crossref this session | Abstract vs claimed result |
|---|---|---|
| **Chow 1974**, *IBM J. Res. Dev.* 18:194, doi 10.1147/rd.183.0194 | C. K. Chow, "On Optimization of Storage Hierarchies," *IBM Journal of Research and Development* 18(3):194–203, May 1974. | Both quoted sentences are verbatim in the OpenAlex abstract, including "directly proportional to the logarithm of the systems capacity" and constant cost / access-time / capacity ratios of adjacent levels. The abstract also calls the optimization "a geometric programming problem," which supports the note's "Chow's geometric program." |
| **Chow 1976**, *IEEE Trans. Comput.* C-25:157, doi 10.1109/tc.1976.5009230 | C. K. Chow, "Determination of Cache's Capacity and its Matching Storage Hierarchy," *IEEE Transactions on Computers* C-25(2):157–164, February 1976. | The quoted "linearly with the logarithm of the ratio of the required hierarchy capacity and the cache capacity" is verbatim. |
| **Welch 1978**, *IEEE Trans. Comput.* C-27:408, doi 10.1109/tc.1978.1675120 | Author listed only as **Welch** (affiliation: Sperry Research Center); "Memory Hierarchy Configuration Analysis," *IEEE Transactions on Computers* C-27(5):408–413, May 1978. No given name in Crossref or OpenAlex; the note's "Welch 1978" is as the databases have it. | The quoted cost-share = delay-share sentence is verbatim. The abstract also states the setting: given memory sizes and access probabilities, minimize average access time under a cost constraint, with a power-function speed–cost assumption. |
| **Jacob, Chen, Silverman & Mudge 1996**, *IEEE Trans. Comput.* 45:1180, doi 10.1109/12.543711 | B.L. Jacob, P.M. Chen, S.R. Silverman, T.N. Mudge, "An analytical model for designing memory hierarchies," *IEEE Transactions on Computers* 45(10):1180–1194, 1996. | Closed-form optimal size of each level, "money spent on an n level hierarchy is spent in a fixed proportion until another level is added," and "in all but one case … within 5% of optimal" are all in the abstract. Fair. |
| **Comment**, 46:1151, doi 10.1109/12.628401 | Same four authors (order Jacob, Chen, Mudge, Silverman), "A comment on 'An analytical model for designing memory hierarchies'," *IEEE Transactions on Computers* **46**(10):1151, **1997** (not 1996). | The abstract is a citation correction: their 1996 description "did not accurately reflect" MacDonald & Sigworth 1975. It does not support the closed-form or the spending-proportion results. **Nit:** attach the year 1997 and say what the comment is. |
| **Przybylski, Horowitz & Hennessy 1989**, ISCA, doi 10.1145/74925.74939 | S. Przybylski, M. Horowitz, J. Hennessy, "Characteristics of performance-optimal multi-level cache hierarchies," *Proceedings of the 16th annual international symposium on Computer architecture — ISCA '89*, pp. 114–121, 1989. The cited DOI resolves. (OpenAlex also lists a non-resolving identifier `10.1145/isca.1989.714545` for the same work; that does not undermine the cited DOI.) | The paraphrase — first-level cache changes the optimal second-level design, size up, cycle time less important — matches the abstract (L1 filtering reduces L2 hits, "decreasing the importance of the cycle-time of the second-level cache relative to its size," and "increases the optimal cache size"). Fair as a paraphrase; see §2 for the CT34 mapping. |
| **Mattson, Gecsei, Slutz & Traiger 1970**, *IBM Syst. J.* 9:78, doi 10.1147/sj.92.0078 | R.L. Mattson, J. Gecsei, D. R. Slutz, I. L. Traiger, "Evaluation techniques for storage hierarchies," *IBM Systems Journal* 9(2):78–117, 1970. | The OpenAlex abstract only introduces storage hierarchies across technologies. It does **not** mention stack-distance curves or evaluating all sizes from one trace. That is the paper's well-known contribution; Semantic Scholar's TLDR this session ("determining, in one pass of an address trace, performance measures for a large class of … multilevel storage systems") supports it. **Nit:** the note says abstracts were the source and the full papers were not read; this particular claim exceeds the abstract. Qualify the source. |
| **Hartstein, Srinivasan, Puzak & Emma 2006**, Computing Frontiers, doi 10.1145/1128022.1128064 | A. Hartstein, V. Srinivasan, T. R. Puzak, P. G. Emma, "Cache miss behavior" (subtitle "is it √2?"), *Proceedings of the 3rd conference on Computing frontiers*, pp. 313–320, 3 May 2006. | "Falls as a power law … exponent −0.3 to −0.7" and "directly related to the time dependence of cache references" are in the abstract (the note slightly condenses "lies between −0.3 to −0.7" and "the exponent in the power law is directly related to…"). Fair. |

No DOI is invented or broken. No title, venue, or page range is wrong.

---

## 2. Mappings to T20(A), T7b, CT24, CT34

Canonical statements used: T20 prereg lines 7–9 and 143–149, and Results §1 plus the official-gates table (Family S (A) 6/6, Family M (A) 6/6); `theory/THEOREMS.md` T7b; `THEORY.md` CT24 (front matter and B.9) and CT34 (B.10).

**T20 part A — not a fair mapping as written. This is S1.**

The note's left-hand cell says: "K* grows linearly in the log of the scale range (T20 part A, passed 12/12 in-model)."

That is not T20(A). The official prediction (A) is: "The argmin layer count K* grows roughly linearly in log R as R runs from 1 to 10^8" (`PREREG.md`), with R = w E_∞ / h, and with the world's scale range held fixed at four decades for every primary world. The 12/12 figure is correct (6/6 Family S + 6/6 Family M on the official gates). The phrase "the number of layers should grow with the log of the scale range" appears in the T20 prereg as the *holographic picture* being analogized, not as gate (A). T20 overall was not supported: prediction (B) (log-spaced rates aligned to the world's scale bands) failed in every primary world.

Chow's independent variable is capacity, or a capacity ratio, not R. Under a power-law technology one can argue that capacity, cost, and access time (hence miss penalty) are tied, so log(capacity ratio) and log(access-time range) are proportional. That analogy has to be stated as an analogy. It is not what the 12/12 pass tested, and it does not make T20(A) "stated before, in the same form" as Chow 1974.

The §2 lead-in, "every part of the prediction GTAO would make in this domain was derived … from the same kind of cost model," and §3.1, "arrived at GTAO's layer-count, spacing and cost-share results," over-identify T20(A) with Chow for the same reason. The R3 paragraph can stand: fitting Chow's / Jacob's program on cache miss-rate curves and calling it a test of J is not distinctive, whether or not T20(A) is the same equation as Chow's.

**T7b — fair, with the domain label already in the row.**

T7b (`THEOREMS.md`) is: items with natural intervals spread log-uniformly over a log-span L, served by K shared clocks, have equal optimal log-widths (geometrically spaced intervals), because ψ(Δ) = 2 sinh(Δ/2) − Δ is strictly convex. It is already marked "Roundy-type, known in substance," and the existing "Nested levels" PRIOR_ART row already credits Roundy 1985, Shankar & Howard 2013, and others, at novelty 1–2. Chow 1974's constant cost, access-time, and capacity ratios, under power-law hit-ratio and technology-cost functions, is the same form in this domain (constant ratios under scale-free / power-law inputs). The objects differ (clock intervals vs storage-level sizes, times, and costs). The note's "Both inputs are power laws, exactly the scale-free case" is a fair reading of the Chow 1974 abstract. This is prior art for the *cache-domain* spacing claim, not a downgrade of T7b's general grade. Fair.

**CT24 — fair for fixed cost shares in this domain; slightly tight on "in any currency."**

CT24 (`THEORY.md` B.9): if J(x; p) = Σ p_i φ_i(x) and the feasible set does not depend on p, then at the optimum the share of term i equals the elasticity of J* in p_i, and the shares sum to 1. Currency-freeness is homogeneity of degree 1. A binding ruin constraint is a stated counterexample. The one-tracker split (α−1):1 is a special case.

Jacob's abstract does state fixed spending proportions ("money spent on an n level hierarchy is spent in a fixed proportion until another level is added"). That is the same form, in this domain, as "fixed cost shares at the optimum." Welch's abstract is a more specific first-order property: each unit's *cost* share equals its *delay* share, under a power-function speed–cost assumption, for given sizes and access probabilities. That is a cousin, not CT24's share = price-elasticity theorem, and it slightly understates Welch to flatten it into "fixed cost shares." Neither abstract states currency-freeness, or CT24's ruin caveat, or the (α−1):1 split. **Nit:** keep the Jacob/Welch credit for fixed (and, for Welch, balanced) shares in this domain; do not attribute "in any currency" to those papers.

**CT34 — over-credited. This is S2.**

CT34 (`THEORY.md` B.10): J(x, y) = F(x) + G(y; θ(x)); exactness is min_{x,y} J = min_x [F(x) + J*_T(θ(x))]; J*_T is a constant upkeep "if θ does not depend on x (and, generically, only if)." There is a second-order bound for weak coupling, and a shared driver is a stated counterexample.

The note's left-hand gloss, "A layer's design is set by what the layer above passes down (CT34 linking)," is already looser than the theorem. Przybylski's abstract supports only the interaction: what L1 passes down (a filtered reference stream) changes L2's optimal design point. That is in the direction of CT34's θ(x), and it is worth recording as related engineering fact. It is not CT34's composition or upkeep result, and it is not "same form." The note correctly omits CT34 from the "should cite … before any public novelty claim" list and from the novelty-0 row; the table still presents the two as matched. Qualify the row. Do not treat Przybylski as prior art for CT34 itself.

---

## 3. Novelty-0 grading

The legend: **0** = stated before, in the same form; **1** = same idea, different domain; **2** = new formula or test; **3** = nothing close found.

The new row grades "Layer count and spacing in memory hierarchies (T20 part A, T7b, CT24 in caches)" as **0**, with "None in this domain: J with power-law hit and technology functions is Chow's geometric program." The note body says "novelty 0–1 (stated before, same domain or same form)."

- **0 is the right grade** for geometric spacing and for a log-capacity (or log capacity-ratio) level-count law *in caches*: same domain, same form as Chow 1974/1976. Jacob's fixed spending proportions likewise sit at 0 in this domain for the "fixed cost shares" consequence. The "adds" cell is honest.
- **0 is not the right grade for T20 part A as such**, because T20(A) is K* vs log R, not vs log capacity, and that is S1. The component label should not list "T20 part A" as already stated by Chow without the axis caveat. After that correction, leave the row at 0 for the cache-domain program (spacing + Chow's level-count law + fixed shares). Do not rewrite the existing T7b general row (already 1–2).
- The body's "0–1" is a gloss over "same domain or same form." Once T20(A) is taken out of the identity claim, the table's 0 is the grade that matches the legend. Harmonize the wording so 0 and 0–1 are not left in unexplained tension.
- §3.1 is right that this is an independent derivation / consistency check, not a test, and that it cuts against novelty rather than for it. §3.3–3.4 (ruin cap, prefetching, pooling; R3 fails by construction in a domain whose local optimizer is already written down) are appropriately modest and are not scored here as new claims.

---

## 4. Other file checks

**Grep claim.** Author-name and "stack distance" searches confirm these papers are not credited elsewhere. "Welch" elsewhere is the spectrum estimator (grid preregs and results), as the note says. The parenthetical is too broad: a search for "miss rate" hits unrelated text (`reviews/night2/SELF/RESULTS.md`, and "MISS rates" in a pass-rule audit). Tighten to: these authors/papers are not credited; the only "Welch" hits outside this note are the spectrum estimator.

**Public data, "reachable today."** Confirmed this session: Cantin & Hill, "Cache Performance for SPEC CPU2000 Benchmarks" (Version 3.0, May 2003), is up at `https://research.cs.wisc.edu/multifacet/misc/spec2000cache-data/`. `https://www.7-cpu.com/` returns 200. The note names the host, not that exact path; the claim is true. Distinctiveness, not data, is the blocker, as stated. The mid-2000s "memory wall" flattening remark is general knowledge, not a DOI claim, and was not independently re-derived.

**R3 (PR #133 §2).** The cited rule is in an unmerged sibling (`revealed-prices-2026-11-21`, head `799d44e`, not on this branch). The note already locates itself "beside `main` `a65b64e` and PR #133." The use of R3 is faithful: if GTAO and Chow/Jacob, fitted the same way, give the same held-out K* and size ratios, a pass supports the rival. Fair. The Jacob comment's existence is a reminder that even inside this literature, closed-form predecessors (MacDonald & Sigworth 1975) were easy to under-describe; that is a nit, not a required addition.

**Law sentence, CORE, consistency.** Hypothesis sentence unchanged in `CORE.md` line 24 and `THEORY.md` line 41, and quoted correctly in the note. `CORE.md` / `THEORY.md` diffs against `origin/main` are empty. `check_consistency.py`: PASS, 0 FAIL.

**What the PR does not do, correctly:** it does not lock a test, write a prereg, compile scored data, or apply the recommended citations into `THEORY.md` / `THEOREMS.md` (it only adds the PRIOR_ART row and says those results "should cite" the papers "before any public novelty claim"). That is the right scope.

---

## 5. Fixes

Clear-cut fixes to apply on this branch, as separate commits, without merging:

**S1.** In the note's table and in §§2–3, state T20 part A as K* vs log R with scale range held fixed (12/12 is the official (A) gates only; T20 overall was not supported). State Chow's law as K* vs log capacity (or capacity ratio). If an analogy under power-law technology is offered, label it as an analogy, not as the 12/12 result. Adjust the PRIOR_ART component label so "T20 part A" is not listed as already stated by Chow without that caveat. Do not change the novelty-0 grade of the cache-domain program, and do not lock a test.

**S2.** Qualify the CT34 / Przybylski row: related interaction, not CT34's composition or upkeep theorem; not prior art for CT34 itself; not part of the novelty-0 grade.

**Nits.** (i) Jacob comment: year 1997, and describe it as a citation correction regarding MacDonald & Sigworth 1975, not as support for the 1996 results. (ii) Mattson: stack-distance / one-trace is the well-known contribution and is supported by a Semantic Scholar TLDR this session; it is not in the OpenAlex abstract. (iii) Tighten the grep sentence. (iv) On the CT24 row, do not attribute "in any currency" to Welch or Jacob.

---

## What stands

The prior-art verdict stands, once S1 and S2 are applied: do not lock a cache-hierarchy test of GTAO; credit Chow 1974/1976, Welch 1978, and Jacob et al. 1996 before any public novelty claim about layer count, spacing, or fixed cost shares in this domain; treat the agreement as an independent derivation, novelty 0 in this domain, not as evidence that goes beyond the storage-hierarchy theory. The hypothesis sentence is untouched. No scored data were compiled in this PR.

This review does not merge.
