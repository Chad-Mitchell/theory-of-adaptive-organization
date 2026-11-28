# Independent hostile review: PR #135 (cross-field map; no lock)

**Reviewer:** independent (wrote none of PR #135, `theory/CROSS_FIELD_MAP_2026-11-21.md`, `theory/cross_field_checks/chow_map.py`, `theory/cross_field_checks/chow_map.out`, `tools/test_cross_field_map.py`, or the `litmap/PRIOR_ART.md` row). Same bot family, not a blind second executor.
**Date:** Saturday 21 November 2026, 9:03 AM EST (America/New_York).
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/135 (branch `cross-field-map-2026-11-21`, pre-merge head `57d2dca`, retargeted base from `cache-prior-art-2026-11-21` to `main` `32b46bd`, and merged `origin/main` resolving `litmap/PRIOR_ART.md` conflict at `370f3a1`).
**Clone:** fresh `/workspace/rev135` (nothing merged; `/workspace/looper` and `/workspace/gtao-evo` untouched; compute at nice 19).

**Verdict: READY-WITH-FIXES**

The note derives the two-exponent Chow (1974) map for reuse worlds, explicitly credits prior art, inventories published data across six fields, and correctly concludes that **0 fields** have all three pieces measured and compiled today, so **nothing is locked**. Core algebra (posynomial convexity, Welch identity $D_k = \gamma \lambda C_k$, total $T:\lambda C = \gamma$, fixed-point ratios $\ln r_s$, $\ln r_t$, $q = 1/(\theta\gamma)$, contraction factor $\theta\gamma$) is verified by independent re-derivation and numerical rerun at nice 19 (`chow_map.py`, `tools/test_cross_field_map.py`). All 13 DOIs cited in the note and `litmap/PRIOR_ART.md` (plus the 3 additional DOIs for WBE 1997, Lee, Flack & Krakauer 2024, and Benna & Fusi 2016) resolve on Crossref. `CORE.md` and `THEORY.md` are untouched, the hypothesis sentence is unchanged, and `tools/check_consistency.py` and `tools/check_open_work.py` pass.

Four should-fixes belong in this PR before merge. None invalidates the "0 fields ready, nothing locked" bottom line.

- **S1 (Stale T20(A) statement from pre-#134 branch).** `theory/CROSS_FIELD_MAP_2026-11-21.md` §0 states `T20 part A (count grows with log range, passed in-model)`. That repeats the exact misstatement fixed on `main` in PR #134 (`reviews/cache_prior_art_2026-11-21/REVIEW.md` S1): the official T20(A) 12/12 pass varied **stakes** $\log R$ with the world's scale range held fixed, "log of the scale range" was the holographic motivation, and T20 overall was not supported because prediction (B) failed.
- **S2 (Boundary-transient and exact-ratio math in §§2.3 & 2.5, plus `chow_map.py` Part 1).**
  1. §2.3 lists `adjacent cost ratio C_{k+1}/C_k (= delay ratio) = q = 1/(θγ)` under "Value at the fixed point." In fact, $C_{k+1}/C_k = D_{k+1}/D_k = 1/(\theta\gamma)$ holds **exactly at every adjacent pair $(k, k+1)$ for any finite $K$ and any boundary $S$** (including $\theta\gamma \ge 1$), directly from the two first-order conditions $D_k = \gamma \lambda C_k$ and $\lambda C_k = \theta D_{k+1}$.
  2. §2.5 item 1 states: *"Deviations from the universal ratio decay as $(\theta\gamma)^k$ from each edge."* That is inaccurate. Because $x_{k+1} - x^* = \theta\gamma (x_k - x^*)$ and $\sum_{k=1}^K x_k = \ln S$, the exact finite-$K$ solution is
     $$x_k - x^* = (\theta\gamma)^{k-1}\,\frac{1 - \theta\gamma}{1 - (\theta\gamma)^K}\,(\ln S - K x^*).$$
     For $\theta\gamma < 1$, deviations decay **from the small-$s$ ($k=1$) edge only** (with $x_K$ closest to $x^*$). For $\theta\gamma > 1$, the forward map repels and deviations decay **backward from the large-$s$ ($k=K$) edge** toward $k=1$. For $\theta\gamma = 1$, there is no repelling fixed point: $\ln q = 0$ gives $x_k = (\ln S)/K$ identically for all $k$ (set by $S$ and $K$). Also note that when $K$ is too large for $S$ ($\ln S < K x^* - \frac{1-(\theta\gamma)^K}{1-\theta\gamma} x^*$), the unconstrained GP gives $x_1 < 0$ ($s_1 < s_0 = 1$).
  3. In `theory/cross_field_checks/chow_map.py` Part 1 (line 63), `S = float(np.exp(lrs*K))` sets $\ln S = K x^*$, putting all $K$ levels directly on the fixed point with zero boundary transient (contrary to the comment `# choose S so the interior can approach the fixed point`). Add a Part 3 direct-GP check with a mismatched $S \ne \exp(K x^*)$ (and $\theta\gamma = 1, >1$) so the full convex optimizer also verifies exact $C_{k+1}/C_k = q$ and one-sided $(\theta\gamma)^{k-1}$ decay.
- **S3 (Prior-art credit and novelty grade inflation).**
  1. Both `litmap/PRIOR_ART.md` and `theory/CROSS_FIELD_MAP_2026-11-21.md` §3 grade the cross-substrate bet as `1–2` ("0 for the map; 1–2 at most for the cross-substrate bet, unverified"). Under `litmap/PRIOR_ART.md`'s own rubric (`1: same idea, different domain`; `2: new formula or test`), `2` is inflated: the formula is Chow 1974 (novelty 0), the cross-substrate universality-from-optimization template is Lera & Sornette 2019 / WBE 1997 / Lee, Flack & Krakauer 2024 (novelty 0), and **no test is written or locked**. The honest grade is **0 for the map; at most 1 for the cross-substrate bet (same formula, new domains, unverified)**.
  2. Inspection of Chow 1974's full text (publicly mirrored at `ibmrd1803B.pdf`) shows Chow 1974 already derived not only geometric spacing and log-capacity level count, but also **cost share = delay share** (Eq. 36, four years before Welch 1978), the adjacent cost/delay ratio $1/(\alpha\beta) = 1/(\theta\gamma)$ (Eq. 39), and the $(\theta\gamma)$ recurrence (Eq. 41). Credit Chow 1974 alongside Welch 1978 in §3 and note the public bitsavers copy (do not state "Full text not read (paywalled)").
- **S4 (Inventory table §5 factual qualification on Breslau et al. 1999).**
  Row 2 lists `Measured: Breslau et al. 1999 (doi 10.1109/infcom.1999.749260), Zipf-like popularity` under `World exponent θ`. Breslau et al. (1999) measured Zipf-like request-popularity exponents $\alpha \in [0.64, 0.83] < 1$ across six Web proxy traces, not the miss-curve exponent $\theta$ in $m(s) = s^{-\theta}$. For independent Zipf-like requests with $\alpha < 1$, the asymptotic hit ratio scales as $(s/N)^{1-\alpha}$, giving miss rate $1 - (s/N)^{1-\alpha}$ (finite-catalog dependent, not $s^{-\theta}$ with $\theta > 0$, which requires $\alpha > 1$ with $\theta = \alpha - 1$). Qualify row 2 so Breslau et al. 1999 is not misread as a measured $\theta > 0$ for $m(s) = s^{-\theta}$.

**Nits:**
- §§2.2 (lines 29, 31): $D_k = m(s_{k-1}) t_k$ is level $k$'s delay contribution (unnormalized), whereas $D_k / T$ is its share of delay.
- §2.3 table (`number of levels | ≈ ln(S/s_1)/ln r_s`): in §2.1 $K$ is fixed; $K \approx \ln(S/s_1)/\ln r_s$ holds once $s_1$ is pinned or $K$ is optimized against fixed per-level upkeep $h$ (omitted in §2.1).
- §0 line 7: Benna & Fusi (2016) fixed their cascade timescale ratio $n^2$ by hand rather than optimizing a speed–cost power law, and Jaques (1990) reported empirical time-span strata rather than solving an optimization model.
- §3: add DOIs for West, Brown & Enquist 1997 (`10.1126/science.276.5309.122`), Lee, Flack & Krakauer 2024 (`10.1098/rspb.2024.1606`), and Benna & Fusi 2016 (`10.1038/nn.4401`).

---

## 1. Derivation and `chow_map.py` check

Independent re-derivation of `theory/CROSS_FIELD_MAP_2026-11-21.md` §2:
- **Convex GP form:** With $u_k = \ln s_k$ ($u_0 = 0$, $u_K = \ln S$) and $v_k = \ln t_k$, $J = \sum_{k=1}^K e^{-\theta u_{k-1} + v_k} + \lambda a \sum_{k=1}^K e^{-\gamma v_k + u_k}$ is a posynomial with $2K$ exponent vectors spanning $\mathbb{R}^{2K-1}$, hence strictly convex and coercive in $(u, v)$ with a unique global minimum.
- **FOCs and Welch identity:** $\partial J / \partial v_k = 0 \implies D_k = \gamma \lambda C_k$ for all $k=1,\dots,K$. Summing gives $T = \gamma \lambda C$ ($T : \lambda C = \gamma$, loss share $\gamma/(1+\gamma)$) and $D_k/T = C_k/C$ at every level. $\partial J / \partial u_k = 0 \implies \lambda C_k = \theta D_{k+1}$ for $k=1,\dots,K-1$. Combining both gives $C_{k+1}/C_k = D_{k+1}/D_k = 1/(\theta\gamma) = q$ identically at every adjacent pair $(k, k+1)$, independent of $K$ and $S$.
- **Closed forms:** Setting $x_k = u_k - u_{k-1}$ and $y_k = v_{k+1} - v_k$ yields $y_k = \ln q + \theta x_k$ and $x_{k+1} = \ln q + \gamma y_k$, giving $x_{k+1} - x^* = \theta\gamma (x_k - x^*)$ with
  $$\ln r_s = x^* = -\frac{(1+\gamma)\ln(\theta\gamma)}{1-\theta\gamma}, \qquad \ln r_t = y^* = -\frac{(1+\theta)\ln(\theta\gamma)}{1-\theta\gamma}.$$
  At $\theta = \gamma = 0.5$: $\ln r_s = \ln r_t = 4 \ln 2 = \ln 16$ ($r_s = r_t = 16$), $q = 4$, $1/\log_{10}(16) \approx 0.8305$. Exact.
- **Script rerun (pre-fix, nice 19):** `theory/cross_field_checks/chow_map.py` and `pytest tools/test_cross_field_map.py` both pass (`WORST mid-level relative error (well-conditioned cases) 4.65e-04`, exact `(theta*gamma)^7` recurrence contraction, `RESULT: PASS`; matches committed `chow_map.out`). The diagnostic `q = 6.25 > 4` case in Part 1 has BFGS stopping tolerance noise at level 1 because $D_1/J \sim q^{-8} \approx 4.3 \times 10^{-7}$.

---

## 2. Prior art and Crossref DOI verification

All cited DOIs resolved on Crossref API this session (`2026-11-21`):
- `10.1147/rd.183.0194`: Chow (1974), *IBM J. Res. Dev.* 18:194–203. Full text inspected via public mirror (`ibmrd1803B.pdf`): Eqs. (36)–(39) contain cost-share = delay-share and cost ratio $1/(\alpha\beta)$; Eq. (41) gives the $\alpha\beta$ recurrence; Eqs. (45)–(60) give the geometric spacing and log-capacity count (including the exact $\alpha=\beta=0.5 \implies 4\text{–}7$ levels for $10^6\text{–}10^8$ example).
- `10.1109/tc.1976.5009230`: Chow (1976), *IEEE Trans. Comput.* C-25:157–164.
- `10.1109/tc.1978.1675120`: Welch (1978), *IEEE Trans. Comput.* C-27:408–413.
- `10.1371/journal.pone.0214911`: Lera & Sornette (2019), *PLOS ONE* 14:e0214911. Full text read: derives discrete hierarchies by maximizing production minus coordination cost, producing universal scaling ratios $3\text{–}4$ across human and animal hierarchies and $3\text{–}20$ span-of-control in Fortune 500 firms.
- `10.1098/rspb.2004.2970`: Zhou, Sornette, Hill & Dunbar (2005), *Proc. R. Soc. B* 272:439–444.
- `10.1126/science.276.5309.122`: West, Brown & Enquist (1997), *Science* 276:122–126.
- `10.1098/rspb.2024.1606`: Lee, Flack & Krakauer (2024), *Proc. R. Soc. B* 291:20241606 (verified in `litmap/LITMAP.md`).
- `10.1038/nn.4401`: Benna & Fusi (2016), *Nat. Neurosci.* 19:1697–1706 (arXiv:1507.07580 checked: cascade timescale ratio $n^2$ is a chosen discretization parameter).
- `10.1109/FSCS.1990.89581`: Alpern, Carter & Feig (1990), FOCS, pp. 600–608.

---

## 3. Inventory table factual spot-checks

All inventory DOIs resolved on Crossref and abstracts checked via OpenAlex / PDF:
- **Hartstein et al. 2006** (`10.1145/1128022.1128064`): abstract reports cache miss rate varies as an inverse power law with exponent `-0.3` to `-0.7`. Matches `θ ≈ 0.3–0.7`.
- **Gray & Graefe 1997** (`10.1145/271074.271094`) and **Appuswamy et al. 2019** (`10.1145/3318163`): verified.
- **Breslau et al. 1999** (`10.1109/infcom.1999.749260`): PDF checked; measured Zipf-like popularity exponents across six Web proxy traces are $\alpha \in [0.64, 0.83] < 1$, which yields hit ratio $\sim (s/N)^{1-\alpha}$ rather than a scale-free miss curve $s^{-\theta}$ ($\theta > 0$). Requires qualification (S4).
- **Anderson & Schooler 1991** (`10.1111/j.1467-9280.1991.tb00174.x`): verified; measures behavioral need probability vs recency/frequency/spacing, accurately noted as behavioral rather than synaptic.
- **Roundy 1985** (`10.1287/mnsc.31.11.1416`): verified; proves power-of-two integer-ratio policies are within 2% of optimal, accurately described as a policy theorem rather than field data.
- **Hamilton et al. 2007** (`10.1098/rspb.2007.0564`): verified; branching ratio close to 4 across 339 hunter-gatherer societies.

---

## 4. Consistency and core checks

- `CORE.md` and `THEORY.md`: unchanged relative to `origin/main` (`32b46bd`).
- Hypothesis sentence: verbatim unchanged (`CORE.md:24`, `THEORY.md:41`, quoted accurately in `theory/CROSS_FIELD_MAP_2026-11-21.md:3`).
- `python3 tools/check_consistency.py`: **PASS** (0 FAIL).
- `python3 tools/check_open_work.py`: **PASS** (0 missing).
- `pytest tools/test_cross_field_map.py`: **1 passed**.

---

## 5. Fixes to apply on this branch (separate commits, no merge)

- **S1:** Update `theory/CROSS_FIELD_MAP_2026-11-21.md` §0 to state T20 part A as $K^*$ vs $\log R$ with scale range held fixed (12/12 official (A) gates; T20 overall not supported), matching `main`.
- **S2:** In `theory/CROSS_FIELD_MAP_2026-11-21.md` §§2.3 & 2.5, state that $C_{k+1}/C_k = D_{k+1}/D_k = q$ is exact for all finite $K$ and $S$, correct the boundary-transient statement to one-sided $(\theta\gamma)^{k-1}$ decay from the small-$s$ edge for $\theta\gamma < 1$ (backward from $k=K$ for $\theta\gamma > 1$, uniform $(\ln S)/K$ at $\theta\gamma = 1$, plus the $x_1 \ge 0$ feasibility bound), and add a mismatched-$S$ finite-$K$ GP verification in `chow_map.py` (with updated `chow_map.out`).
- **S3:** Downgrade the cross-substrate bet novelty grade in `litmap/PRIOR_ART.md` and `theory/CROSS_FIELD_MAP_2026-11-21.md` §3 from `1–2` to **at most 1 (same formula, new domains, unverified)**, credit Chow 1974 Eqs. (36)–(41) for cost-share = delay-share and the $\theta\gamma$ recurrence alongside Welch 1978, and add the verified DOIs for WBE 1997, Lee et al. 2024, and Benna & Fusi 2016.
- **S4 + Nits:** Qualify Breslau et al. 1999 ($\alpha \in [0.64, 0.83] < 1$, finite-catalog hit ratio rather than $s^{-\theta}$ with $\theta > 0$) in §5 row 2, and apply the wording nits in §§0, 2.2, and 2.3.

This review does not merge.
