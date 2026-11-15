# CLAIM_MAP_FINAL: A Theory of Adaptive Organization (GTAO), every claim marked

Sunday 15 Nov 2026, written about 03:00–04:00 AM ET (America/New_York) by a Grok Bot executor for Chad, via Ace. Private. Nothing was posted, sent or made public. This file supersedes `night1/FORMAL/CLAIM_MAP.md` (02:22 ET), which is out of date in several rows.

**What GTAO is, in one line.** A falsifiable causal theory: drift destroys the information an organization holds, re-buying it draws on a finite budget, and selection keeps the cheapest ways of spending that budget, so what an organization tracks, how often, and whether a shared level holds it are caused by its environment's drift structure and its sensing prices. It is not a law, and it is not a theory of everything.

**Bottom line, plainly.**
- **Confirmed on real data, specific to GTAO: nothing.** The one real-data pass tonight (supervisors read outside material about 14–19% more often) is Mintzberg's "monitor" role, which was already published.
- **Killed on real data:** the item-level news-recall slope (P1), vigilance by rank in Enron email, and, earlier, the strong news-exponent match, the τ structure of failure rates, and √N in languages.
- **Proved inside the model:** a set of correct, elementary theorems. Most rest on known foundations: Marschak & Radner 1972, Veldkamp & Wolfers 2007, Van Zandt & Radner 2001, EOQ and inventory pooling, and Topkis.
- **Simulations:** the passes are circular, and four simulated locked predictions failed.
- **Open:** everything distinctive about GTAO in real systems.

---

## 0. How to read this map

**Status: exactly one per row.**
- **PROVED**: proved inside the model 𝓜 (`FORMAL/AXIOMS.md`), with the scope stated after the hostile math review's corrections. This says nothing about real systems.
- **PASSED**: a locked prediction passed on **real data**.
- **KILLED**: a locked kill rule fired, a locked pass criterion failed, a proof or counterexample refuted the claim as stated, or the claim was withdrawn as false. A failed locked prediction *inside a simulation* is also listed as KILLED, and the row says it was in-model.
- **CIRCULAR/NOT EVIDENCE**: a "pass" that could not fail for reasons outside the model, or a valid in-model computation that is not evidence about nature. The qualifier says which.
- **OPEN**: untested, inconclusive, mixed, or a conjecture.
- **PRIOR ART**: the claim, in substance, is already published. The source is credited, and GTAO cannot claim it.

**Columns.** *Claim* · **Status** · *Scope / conditions* · *Evidence and credit* · *Real-data test?*

**Citation verification markers** (the reviewers' own; nothing here is upgraded):
- [FULL]: relevant text read this session.
- [OCR]: Marschak & Radner 1972 scan, read by OCR.
- [ABS]: abstract only.
- [SEC]: known through a named secondary source.
- [BIB]: bibliography verified, content not.
- [UNVERIFIED]: from memory, not relied on.
- [DOI]: DOI resolved in the earlier sweep.
- [cited by math referee]: named by the math referee with no verification level stated, so treat it as unverified.

**Reviews used** (all independent of the authors, and each blind to FIXES/CLAIM_MAP until its own §1–§5 were written):
- `REVIEW/math/REPORT.md` (math);
- `REVIEW/physstat/REPORT.md` and `ANTS1_WRITEUP.md` (physics and statistics);
- `REVIEW/priorart/REPORT.md` (prior art).

The FORMAL adversarial pass (`FIXES.md`) was done by the author executor, so it is **not** independent.

**Abbreviations.**

| Short form | Source |
|---|---|
| M&R | Marschak & Radner 1972 |
| VZR | Van Zandt & Radner 2001 |
| V&W | Veldkamp & Wolfers 2007 |
| AALVZ | Acemoglu, Aghion, Lelarge, Van Reenen & Zilibotti 2007 |
| ADM | Alonso, Dessein & Matouschek 2008 |
| MOVZ | Meagher, Orbay & Van Zandt 2001 |
| DGS | Dessein, Galeotti & Santos 2016 |
| G&M | Geanakoplos & Milgrom 1991 |

---

## A. Sensing classes and the single-tracker lemma (THEOREMS Lemma 1)

| # | Claim | Status | Scope / conditions | Evidence and credit | Real data? |
|---|---|---|---|---|---|
| A1 | Square-root sampling cost for periodic complete reads (R1) and entropy-priced filtering (R2): φ ∝ √(2cWq), a = b = ½ | **PRIOR ART** | Brownian drift, quadratic loss | EOQ (Harris 1913) [classic, not verified this session]. **M&R 1972 ch. 7 §5, eq. 5.13**: optimal recovery frequency ∝ √(value difference / cost) [OCR]. Kalman–Bucy; Duncan 1970 [ABS]; Reis 2006 [FULL]; Keller 1974 [ABS]; Sheridan 1970 [ABS] | n/a |
| A2 | A_θ, separable \|e\|^p and α-stable rows of Lemma 1 | **PROVED** | Standard calculus; R1 with H ≠ ½ uses the hold-last-value estimator, a restriction | s1 checks. Class-A sensing of a *changing* target in cells is already published: Mora & Nemenman 2019 PRL 123:198101 [ABS]; static limit Berg & Purcell 1977 [ABS] | n/a |
| A3 | The (a, b) chart as the classifier of technologies; drift-invariant pricing ⇒ a = b (sufficient only, converse not claimed); averaging gives b = a/2 | **PROVED** | Within P(a, b); the class label "R" is used in T5.6 but never defined (math Issue 2) | Prior-art verdict: PARTIAL, a new organizing device built on known formulas | none |
| A4 | Periodic reading is optimal in R1 | **PROVED** | Deterministic schedules at fixed n (adaptive schedules cannot help because post-read variance is deterministic; state this). **Holds only if the tracker sees nothing between reads.** With continuous observation and costly transmission, event-triggered sampling dominates | Åström & Bernhardsson 2002 [SEC]; math L1(vii) note | n/a |
| A5 | Effort elasticities equal the cost exponents (a, b), so (a, b) is measurable on a lone unit | **PROVED** | In A_θ, "effort" means r^{−θ}, not precision, unless θ = 1 (math L1(viii)) | s1; math m1 | none |

## B. Pooling onset (T1, T2)

| # | Claim | Status | Scope / conditions | Evidence and credit | Real data? |
|---|---|---|---|---|---|
| B1 | T1.1 single crossing: the level is optimal iff N > N\* | **PROVED** | On the reals (N treated as continuous). Edge case: at a = 0, G(0) = −B − h′ (harmless) | math m1 | — |
| B2 | T1.2 exact onset N\* = [ρ^b/((1+ρ)^b − 1)]^{1/(1−a)} | **PROVED** | h = 0, equal prices, a common technology. An exact iff for T1.2 itself | math m1 re-derived. Apparently new as a closed form, elementary [priorart] | none |
| B3 | T1.3 small-share exponent e_g → −(1−b)/(1−a), Π\* = b^{−1/(1−a)} (4 at γ = ½) | **PROVED** | **Asymptotic (ρ → 0), not an exact iff** (math Issue 4). h = 0, or a > b with upkeep | math m1. Apparently new for general (a, b), elementary. Physics referee: a continuous parameter family covering all of (−∞, 0), so **not a universality class** | none (see §H) |
| B4 | The −1 onset (N\* ∝ 1/ρ) when a = b and with large upkeep; amortizing a fixed information cost over N users | **PRIOR ART** | Static or dynamic | **V&W 2007 Prop. 2** [FULL]; Wilson 1975 [ABS]; **VZR 2001** "Arrow effect", Thms 1 and 3 [FULL]; Arrow & Radner 1979 [ABS]. Physics referee: the −1 is a Buckingham-Π homogeneity identity once cost depends on (W, q) only through Wq | P1-type field tests: none |
| B5 | T1.4 exact elasticity formula, negative for all ρ | **PROVED** | h = 0 | math, 40-digit checks | — |
| B6 | T1.5 upkeep dichotomy: e_g → −(1−b)/(1−a) if a > b, → −1 if a ≤ b; ≈ −γ in the intermediate large-ρ regime | **PROVED** | ρ → 0 (and the stated intermediate regime) | math made the proof rigorous with N = N₀y; slopes −1/−2/−4/−0.9988 | — |
| B7 | T1.6 N\* ∝ p_g/p | **PROVED** | **Exact at h = 0** (the original said first order, which understated it) | math. "Cheap central sensing centralizes" is in substance Bloom, Garicano, Sadun & Van Reenen 2014 [FULL]; Garicano 2000 [ABS] | none |
| B8 | T1.7 at h = 0, onset invariant to total volatility and stakes; at h > 0, more total volatility gives levels at smaller N | **PROVED** | In 𝓜 only. **Fails at a = 0** (G stakes-invariant). **Assumes zero processing delay.** With delay, faster environments penalize hierarchy | math. Delay literature points the other way: Aoki 1986 [FULL], Radner 1993 [FULL], MOVZ 2001 [ABS]. Counter-evidence at the level of decision rights: Aghion, Bloom, Lucking, Sadun & Van Reenen 2021 [FULL] | none (F3 row) |
| B9 | T1.8 mixed technologies: e_g → −(1−b_L)/(1−a_L), set by the **level's** class; e_u → +(1−b_m)/(1−a_L) | **PROVED** | **ρ → 0 only**, h = 0 | s9; math | none |
| B10 | T1.8 last sentence: "the opposite signs of T3 survive whenever b_m, b_L < 1" | **KILLED** | False away from small ρ when b_L > b_m | math counterexample C2: level (½, ½) over members (⅔, ⅓) gives e_g = +0.159 at ρ = 100 and +0.301 at 10⁴. The private-drift sign does survive at all ρ | — |
| B11 | T1.9 N\* > 1 | **PROVED** | Only when p_g ≥ p (F17) | s11 | — |
| B12 | T2 broadcast break: onset becomes a ρ threshold; per-link ρ_b = (1+κ′)^{1/b} − 1; per-read ρ_b = 4t/(1−t)² | **PROVED** | κ_b > 0; per-read form for R1, γ = ½ | math re-derived. Mechanism PRIOR ART: Garicano 2000 [ABS], Bolton & Dewatripont 1994 [ABS], Radner 1993 [FULL]; collective-sensing analogue Fancher & Mugler 2017 [ABS]. The closed form is apparently new | none |

## C. Shared versus private drift (T3)

| # | Claim | Status | Scope / conditions | Evidence and credit | Real data? |
|---|---|---|---|---|---|
| C1 | T3 ∂N\*/∂q_g < 0 < ∂N\*/∂q_u at every ρ | **PROVED** | **Common technology only** (else B10), concave in stakes and drift (a < 1, b < 1). Edge case: if p_g < p and the root is < 1, N\* is pinned at 1 and the derivatives are 0 | math m2: 0/3,191 sign violations; s2: 0/17,065. Signed form at every ρ apparently new (elementary IFT) | none |
| C2 | Qualitative "centralize tracking of common shocks, decentralize local ones" | **PRIOR ART** | — | Hayek 1945 [BIB]; **AALVZ 2007** [ABS]; **VZR 2001** [FULL]; V&W 2007 [FULL]; G&M 1991 [FULL, DP text]; Maćkowiak & Wiederholt 2009 via MMW 2023 [FULL survey] | — |
| C3 | THEOREMS/EXTENSIONS citation: ADM 2008 states C2 | **KILLED** | Miscitation | ADM 2008 [FULL] is about strategic cheap talk, coordination versus adaptation. Cite ADM only for that trade-off | — |
| C4 | Cor 3.1 against contingency theory: total volatility neutral (h = 0) or promotes levels (h > 0); opposite signs for shared and private | **OPEN** | Interpretive; zero-delay model | Contingency side: Burns & Stalker; Lawrence & Lorsch [not re-read]. Counter: delay models (B8) | none |

## D. Bundled loss (T4)

| # | Claim | Status | Scope / conditions | Evidence and credit | Real data? |
|---|---|---|---|---|---|
| D1 | T4: under a bundled loss ℓ(e_g + e_u), the **level's technology, not the loss shape**, sets e_g = −(1−b₂)/(1−a₂): −1 for R1/R2, −(1+θ) for A_θ | **PROVED** | Gaussian drift with linear trackers (Gaussian closure), independent phases, small ρ, h = 0. **The proof is a sketch** (math Issue 6): "+o(q_g)" is the wrong bookkeeping, and the re-optimization and envelope steps are asserted. The right statement is lim_{ρ→0} d ln N\*/d ln ρ, which needs two-sided bounds. α-stable drift is open, and phase-locked reads are unchecked | Exact joint optimization without expansion (math m3): −1.018/−1.003/−1.000/−1.000 for p = ½, 1, 2, 4 and −2 for A₁. Also s3, POOLSIM W5, W5_CHECK. Tool: Price 1958 / Bonnet [UNVERIFIED volume and pages]. Contrast with VZR 2001 on loss dependence [FULL]. Apparently new as an application | none |
| D2 | In A_θ and R2, N\* is *exactly* loss-independent (variance reaches a deterministic total) | **PROVED** | Kalman technologies with deterministic variances | Math referee's own observation, checked numerically (m3 identical N\* for \|e\| and e²). Not re-checked by a second party | none |
| D3 | Cor 4.1 (DP1 corrected): lone-member elasticities predict e_g "iff" they equal the technology's quadratic-loss exponents | **PROVED** | Downgraded to **"if, and generically only if"** (math) | — | none |
| D4 | Cor 4.2: separable loss is the right model only when shared and private parts drive different decisions | **OPEN** | A modeling statement, not a theorem | — | none |
| D5 | DP1 original: predict e_g from a lone member's elasticities under its actual loss (e.g. −2 for absolute loss) | **KILLED** | For bundled decisions | T4; W5_CHECK (−1.008 continuous bundled vs −1.997 split) | — |
| D6 | POOLING_REVIEW: absolute loss gives −2, quartic −½ | **KILLED** | For bundled loss (true for split/separable loss only) | s3; W5_CHECK | — |

## E. Vigilance at birth (T5)

V = the level's information effort ÷ a **flat** member's effort. **Caution (math Issue 10):** this compares the level with a member of the *unlevelled* organization, not with the lead's own members, who in 𝓜 do not sample the shared driver at all.

| # | Claim | Status | Scope / conditions | Evidence and credit | Real data? |
|---|---|---|---|---|---|
| E1 | T5.1 V(N\*) = N\*^a (ρ/(1+ρ))^b at equal prices | **PROVED** | Common technology, separable costs | substitution | — |
| E2 | T5.2 as stated: "born more vigilant **iff** a ≥ b" (pointwise) | **KILLED** | — | math C4: a = ⅓ < b = ⅔, ρ = 0.01, h′ = 100 gives V = 1.142 > 1 | — |
| E3 | T5.2 corrected: V(N\*) > 1 **for all** (ρ, h, r) iff a ≥ b; with a < b and h = 0, V → 0 as ρ → 0 | **PROVED** | Uniform statement | math m4; s11 (0/20,000, min 1.0014) | — |
| E4 | T5.3 V(N\*) → b^{−a/(1−a)}ρ^{(b−a)/(1−a)}; constant iff a = b, equal to γ^{−γ/(1−γ)} (**2 at γ = ½**) | **PROVED** | **A ρ → 0 limit at h = 0, and a supremum, not a floor.** "2" needs R1 with Brownian drift (H = ½) or R2: R1 with fBm H = ¾ gives 1.842 (math C3), H = ¼ gives 2.25 | math m2 | see E9–E14 |
| E5 | T5.6 "V ≥ 2 at onset in the read-based class, for every upkeep and price" | **KILLED** | Wrong as stated outside ρ → 0 | math Issue 1: at h = 0, V(N\*) = 1 + (1+ρ)^{−1/2} < 2 for every ρ > 0 (1.995 at ρ = 0.01, 1.707 at ρ = 1, 1.30 at ρ = 10); V < 2 in 10,792 of 20,000 random draws | — |
| E6 | **Replacement for T5.6, the exact formula** (a = b = ½, r = p_g/p, h′ in member-cost units): **V(N\*) = ½·(1 + (1+ρ)^{−1/2})·(1 + √(1 + 4h′(√(1+ρ) − 1)/(rρ)))**. At h′ = 0, V = 1 + (1+ρ)^{−1/2} ∈ (1, 2). V ≥ 2 iff h′/r exceeds a threshold ≈ ρ/2 for small ρ (0.005, 0.050, 0.485, 3.56 at ρ = 0.01, 0.1, 1, 10) | **PROVED** | γ = ½ (R1 with H = ½, or R2), common technology, separable costs, component readability. Note that h′ depends on q_u (math Issue 5) | Math referee m5 (symbolic, and root-finding to 3 × 10⁻¹⁰ over 20,000 draws). Re-checked by this synthesis (`SYNTHESIS/vfloor.py`): max relative error 3 × 10⁻¹³ over 20,000 draws | none |
| E7 | Corollary of E6, used in §3 below: **V(N\*) ≥ 1 + (1+ρ)^{−1/2} for every upkeep and price ratio**, and V(N) ≥ V(N\*) for N ≥ N\* | **PROVED** | As E6 | The second factor of E6 is ≥ 2. Checked numerically by this synthesis: 0 violations in 20,000 draws. Not yet checked by an independent reviewer | none |
| E8 | T5.4 price invariance: V(N\*) does not depend on p_g/p, so it does not depend on per-read broadcast cost either | **PROVED** | **Exact at h = 0** (math). Upkeep breaks it | math m2; s8. Apparently new | **none (never tested)** |
| E9 | T5.5 V grows as N^a beyond onset (√N in R1) | **PRIOR ART** | In substance | M&R 1972 eq. 7.5.13 with value difference ∝ N [OCR]; centralized EOQ orders √N times as often: the square-root law of inventory centralization, Maister 1976 [cited by math referee]; Eppen 1979 [ABS]; Roundy 1985 [ABS] | see E12 |
| E10 | V ∝ ρ^{−θ} in A_θ | **PROVED** | First order, h = 0 | s2 | none |
| E11 | F15 (FIXES): "VIGIL's ≈ 1.15 cannot come from upkeep or prices in class R" | **KILLED** | Holds only as ρ → 0 | math §6: at h = 0, V(N\*) = 1.15 at ρ ≈ 43 (a large shared share, perhaps implausible for VIGIL's setting) | — |
| E12 | Earlier summaries: "about 2× at every rank"; "V > 1 always at birth" (CORE_AUDIT); "V ∝ √(c/c_g) at onset" (ARCH) | **KILLED** | 2 is the small-ρ onset limit; V grows as N^a; V > 1 needs a ≥ b; at onset V is price-invariant | T5.2–T5.5; FIXES R4, R6, R8 | — |

## F. Lattice, ordering, freeze/hold/lookup and the rest (T6–T8, P9–P11, extremes, architecture equation)

| # | Claim | Status | Scope / conditions | Evidence and credit | Real data? |
|---|---|---|---|---|---|
| F1 | T6(a)–(c): J submodular (levels are complements); inclusion; lattice; the largest optimal set is nonincreasing in upkeep h | **PROVED** | Needs the member to track its residual as **one bundle** (H1); concave member costs; submodular level costs | math m4: 0 violations. **Not new as mathematics:** concave∘modular is submodular, plus Topkis (Topkis 1978 [ABS, DOI verified]; Topkis 1998 book and Milgrom & Shannon 1994 [cited by math referee]). Application only. Grouping: Crémer 1980 [ABS] | none |
| F2 | T6(d) stakes accretion | **PROVED** | **Common degree a only.** With level degree a + 0.3, there were 167 accretion failures (math C5) | math m4 | none |
| F3 | T6 lookup counterexample: cheaper lookup or higher stakes with a fallback can **dissolve** a level | **PROVED** | Bounded fallback | s4 §4. Apparently new, minor | none |
| F4 | ARCH §2.3: "bundled reads make J non-submodular" | **KILLED** | — | s4 §7, 0/93,207 | — |
| F5 | ARCH and summaries: "cheaper memory never dissolves a level" | **KILLED** | True for upkeep h; false for lookup u and for stakes with a fallback | F3 | — |
| F6 | P7.1 depth avalanches | **OPEN** | Numerical only | s6. Prior art in kind: Milgrom & Roberts 1990 coherent clusters [ABS] | none |
| F7 | T7(a) ordering: levels fill top-down iff κ < κ\* = (1−a)/(1−b) = 1/\|e_g\|, bottom-up iff κ > κ\* | **PROVED** | **h = 0** for the iff. At h > 0 it is only sufficient (top-down if κ < min(κ\*, 1), bottom-up if κ > max(κ\*, 1)), with an undetermined gap. CLAIM_MAP had dropped the h qualifier | math m4: 0/215 violations; s6, s9. Apparently new, elementary. Neighbours: Garicano 2000 [ABS]; Simon 1962 [BIB]; Willsky 2002 [FULL] | none |
| F8 | T7(b) class dependence: "κ = 0.7 builds top-down with reset sensing and bottom-up with averaging sensing" | **PROVED** | **Zero upkeep only.** At h > 0, κ\* = ½ < 0.7 < 1 falls in the gap where T7(a) is silent | math Issue 9 | none |
| F9 | T7(c) first-order location rule as an "iff" | **KILLED** | As an iff | math: evaluated at R(∅) it is only sufficient (25/113 mismatches; P7.1 is itself a counterexample); at R(L\*) it is a self-consistency condition that can have several solutions. It is not "T6(b)'s rule" | — |
| F10 | T7(c) as a **sufficient** condition (scale kept if n_s^{1−a}q_s^{1−b} > (p_g/p)^{1−a}R^{1−b}/b at R(∅)) | **PROVED** | Small shares, h = 0; extra assumption that members share the level's b, which must be stated | math | none |
| F11 | ARCH §2.3(f) knife edge at κ = 1 | **KILLED** | In general; true only for a = b | T7 | — |
| F12 | T8 cliff: holding effort drops discontinuously to 0 at the lookup edge; hold-versus-lookup break-even; Poisson refresh f\* > 0 iff λ < μW_b/c | **PRIOR ART** | Bounded fallback | Cho & Garcia-Molina 2003 [ABS/SEC]; Gray & Putzolu 1987 "five-minute rule" [BIB/SEC]; EOQ | earlier repo: see K-rows |
| F13 | T8 closed forms: freeze edge q_f = 2c/(WH_l²); lookup edge q_c = (μu − h)²/(2cW); **hold band exists iff μuH_l > 2c + hH_l**; shared store widens the band N² (N^{(1−a)/b} in P(a, b)); edge elasticity 1/b | **PROVED** | R1 quadratic (power class for item 6). Wording: "holding any drifting item pays only if…" refers to the **interior** band, since freezing can still beat lookup | math m4 sympy; s5 (2,000 sets, 0 mismatches). Qualitatively known for shared caches: Wolman et al. 1999 [FULL]. The closed forms are apparently new | none |
| F14 | P9 clock cap 1 − K^{−(1−γ)}; zero with indivisible reads | **PRIOR ART** | Known in kind | Joint replenishment / power-of-two: Roundy 1985 [ABS]; Hölder | — |
| F15 | P10 selection resolution: no level for ρ ≲ ε/b | **PROVED** | Relative resolution ε | math; s7. Idea prior: drift barrier, Sung et al. 2012 [ABS]; Lynch et al. 2016 [DOI]. The ε/b floor is new and trivial | none |
| F16 | P11 readability moves the constant (4 → ≈ 7.3), not the exponent | **OPEN** | Numerical | math m6 Monte Carlo confirms the shared term → T_g | none |
| F17 | E1 depth grows one-for-one with log N when κ < κ\*; bounded fractional saving ≤ bρ | **PROVED** | First order, h = 0 | s10. Log depth in span-limited hierarchies: Williamson 1967 [BIB verified, content SEC]; Beckmann 1977 [BIB verified, content SEC]. Bounded firm size with common components: VZR 2001 [FULL] | none |
| F18 | E2–E3 extremes: N\*(ρ = 1) = (2^b − 1)^{−1/(1−a)}; N\* → 1 as ρ → ∞; N\* ∝ λ^{−b} as the world calms with h > 0 | **PROVED** | First order / numeric | s10 | none |
| F19 | E4 dissolution order: with whole-item lookup, the pooled level dissolves **before** private holding; with component lookup the level becomes a shared store that survives N^{1−a}-fold cheaper lookup | **PROVED** | In 𝓜 | s10 E4 (edges 1.5285, 1.4642, 0.2010). Order apparently new. Qualitative: Bloom et al. 2014 [FULL]; Garicano 2000 [ABS]; Wolman et al. 1999 [FULL] | none |
| F20 | Working conjecture: "private holding dissolves first, then levels" | **KILLED** | Whole-item lookup | F19 | — |
| F21 | E4/E5: cheap lookup moves tracking into a few large shared stores; cheap central sensing centralizes | **PRIOR ART** | Qualitative | Bloom et al. 2014 [FULL]; Garicano 2000 [ABS]; Wolman et al. 1999 [FULL] | — |
| F22 | Architecture equation, first-order rule: keep source m iff q_m Σ_i λ_i B_im² − φ(W_m, q_m) > h; the exact set contains it | **PROVED** | Class R, γ = ½, one read per source, first order in each source's share | ARCH c2 checks. PARTIAL prior: Vayanos 2003 [FULL] (static common factor); Crémer 1980 [ABS]; M&R ch. 6 [OCR] | none |
| F23 | Eigen reading of the architecture equation under rotation-invariant cost | **PRIOR ART** | — | Reverse water-filling, Sims 2003 [PR] | — |
| F24 | Cross-axis coupling: pooled levels resolve faster drift components and keep more temporal layers | **OPEN** | Conjecture | ARCH §2.4 | none |
| F25 | "Organizational structure mirrors the structure of environmental change" (qualitative) | **PRIOR ART** | Qualitative | Kashtan & Alon 2005 [ABS]; Watson et al. 2014 [ABS]; Jones, Arnold & Bürger 2004 [ABS]; Simon 1962 [BIB]; MOVZ 2001 [ABS] | — |
| F26 | Quantitative version: an organization's levels are a cost-thresholded copy of its environment's shared-drift structure, with exponents fixed by its sensing class | **OPEN** | Untested anywhere | ARCH §7 | **none** |

## G. Simulations (nothing in this section is evidence about nature)

| # | Claim / test | Status | Scope / conditions | Evidence | Real data? |
|---|---|---|---|---|---|
| G1 | POOLSIM W1 (−0.971), W2 (−1.007), W6 (−0.469), W7 (+0.014), W8 (−0.503), W9, W3 (ρ threshold): learners recover the onset slopes, and the estimator separates −1, −½ and 0 | **CIRCULAR/NOT EVIDENCE** | Circular. Valid only as a code and estimator check | Physics referee re-run: the slope from the simulator's own expected-cost crossing **with no learners** is −0.994 (W1), −0.997 (W2), −0.976 (W5), −0.482 (W6). Oracle slopes were known before the lock (disclosed) | — |
| G2 | POOLSIM W5 and W5_CHECK: bundled absolute loss gives −1, not −2 | **CIRCULAR/NOT EVIDENCE** | **Not circular**: a genuine in-model computation, independently reimplemented (−0.978 oracle, −1.001 learners; continuous bundled −1.008 vs split −1.997). It motivated T4 (D1) and supports it inside the model only | W5_CHECK.md | — |
| G3 | POOLSIM vigilance V ≈ 2.00 (W1), 9.3 (W2) | **CIRCULAR/NOT EVIDENCE** | Circular in W1/W2/W8 (intervals come from the same √ rule); descriptive in W3/W5 | POOLSIM §2 | — |
| G4 | POOLSIM findability: onset is invisible when decision noise is ≥ about 1% of cost, and noise biases fitted slopes steeper (−1.2 to −2.4) | **CIRCULAR/NOT EVIDENCE** | Valid and informative in-model result, formalized as P10 (F15). **It cuts against field testability** of the distinctive small-ρ regime | POOLSIM §4. Physics referee: "the most important simulation result of the night" | — |
| G5 | SENSING class A (−1.970 vs −2) and A2 (−1.483 vs −1.5) | **CIRCULAR/NOT EVIDENCE** | Circular: "measured" (a, b) have R² = 1.000 and se 0.0000 because they read back the trackers' own cost rule | SENSING/RESULTS.md; physstat §1 #2 | — |
| G6 | SENSING class R learner recovers −1 (locked PASS criterion) | **KILLED** | In-model, locked: a MISS. −0.920 [−0.957, −0.882] excludes −1 (oracle −0.991). Not a wide-band fail, and not a kill of the algebra | SENSING §2, §4 | — |
| G7 | SENSING: the class-independence rival is killed | **OPEN** | The locked rival-kill did not fire because class R missed | SENSING §2 | — |
| G8 | "Members' sensing class predicts the group's onset exponent", presented to Chad as possibly the theory's unique prediction | **KILLED** | Mis-stated: by T1.8 and T4, the **level's** technology sets e_g, and members' b sets only e_u. SENSING could not separate the two because level and members shared one technology | physstat §4, §7.2 | — |
| G9 | SENSING2 EVO_A (evolved averaging policy): locked e_pred −2.118 | **KILLED** | In-model, locked wide-band fail: ê_g = −0.488 [−0.912, −0.064]. **Documented caveats (post-lock, do not overturn the kill):** simulated flat means ≈ 1.5% high in a world where the onset gap is a few thousandths; the locked-policy oracle is −2.000; a mean-corrected descriptive WLS gives −2.328 [−3.566, −1.091], with 4 of 5 cells failing the ceiling screen | SENSING2/RESULTS_2.md | — |
| G10 | SENSING2 complete-check worlds EVO_R, OU_R, JUMP_R, FBM_R | **OPEN** | Officially INCONCLUSIVE: a **locked flat-arm bug** (S1²/N instead of S1²/N²) overstated flat cost by ≈ 51% (FBM 66%), so learners always adopted | Post-lock mean-corrected: OU, JUMP and FBM PASS ≈ −1; EVO_R MISS (−1.189). Post-lock, so not confirmatory | — |
| G11 | SENSING2 QUART_R: T4's risky contrast (lone-member −½ vs technology −1) | **OPEN** | INCONCLUSIVE: the locked design reused the quartic-evolved schedule and did not re-optimize the level under φ₂; nest beat flat at only 1 of 6 ρ | RESULTS_2 §A | — |
| G12 | SENSING2: rival (exponent independent of sensing) killed | **OPEN** | Not killed (needs both EVO worlds to pass) | RESULTS_2 | — |
| G13 | ANTS1 C0, C1, P1-MEAN (0.458–0.498), P3-MEAN, P7 (75/75) | **CIRCULAR/NOT EVIDENCE** | By construction: the MEAN readout is an EWMA, so e\* = the Kalman gain (exponents match K\* to 3 decimals). P7 holds for any filter. The "21 of 21" quoted earlier is this kind of result | ANTS1_WRITEUP | — |
| G14 | ANTS1 P1-MODE, P2, P4(a,b), P5(a,b), P8 | **CIRCULAR/NOT EVIDENCE** | Valid in-model passes, but checks of the authors' own mean-field approximation of their own simulator. Not evidence about real ants. P1-MODE exponents all sit 0.02–0.12 below Kalman, and the band is wide | ANTS1_WRITEUP | — |
| G15 | ANTS1 P3-MODE: an ant-like nonlinear readout pools error as N^{−½} | **KILLED** | In-model, locked: slopes −0.259 to −0.398, 0/5 in band | ANTS1 analysis_output.txt; reproduced by physstat | — |
| G16 | ANTS1 P5(c): lock-in mimic distinguishable from IND by error in jump worlds | **KILLED** | In-model, locked: 36/96 (38%) vs ≥ 80% | same | — |
| G17 | ANTS1 P6 (H77): interior optimal forgetting rate | **KILLED** | In-model, locked: 154/180 (85.6%) vs ≥ 90%. All 26 failures are MEAN readout in fast jump worlds, where forgetting everything (e = 1) is optimal | same | — |
| G18 | ANTS1 methodological result: fade rate does not diagnose independent pooling (followers fade the same with ≈ 4× the error); error scaling does | **CIRCULAR/NOT EVIDENCE** | Valid in-model; useful as a field-design rule | P4(b) 54/54 | — |
| G19 | LAYERS1 P1 (K\* linear in L beats L^{2/3}, 9/12) | **CIRCULAR/NOT EVIDENCE** | Pass, but uninformative: R² differences 0.01–0.02 over 5 points; SCALEFREE says they cannot be told apart | ARCH §3; physstat | — |
| G20 | LAYERS1 P2 span invariance of layer spacing | **KILLED** | In-model, locked: 6/12 vs ≥ 9 | c4_layers1.out | — |
| G21 | LAYERS1 P3 (spacing tightens as w/h rises) | **CIRCULAR/NOT EVIDENCE** | By construction (any accuracy–cost trade-off). The series count was rescaled after the lock | ARCH §3 | — |
| G22 | AI1 (shared agent memory adopted at N > N\*(ρ)), "supported by POOLSIM" | **CIRCULAR/NOT EVIDENCE** | POOLSIM learners minimize the same cost. A non-circular test needs agents *not* given the cost function | EXTENSIONS AI1 | — |

## H. Real-data tests

| # | Claim / test | Status | Scope / conditions | Evidence | Lock notes |
|---|---|---|---|---|---|
| H1 | P1 (theory-v3): within-item, within-respondent forgetting slope in Meeter, Murre & Janssen 2005: a_c ∈ [0.5, 1.2] | **KILLED** | Locked: a_c = 0.3102 < 0.35. **Independent re-fit (physstat): 0.321, 95% CI [0.289, 0.352].** The named competitor C1 (0.24) is **also excluded**, so the data reject both. "Closer to the rival" is not support for the rival | P1_RESULT.md; REVIEW/physstat/rerun | Self-attested lock (fb95b62, 23:46:35); body time "~23:55" post-dates the commit; derivations committed after the lock; runner identity checked only on a 388-row slice |
| H2 | "Forgetting exponent = need exponent" (P3 / MATCH1 strong form, 0.24 vs 0.71) | **KILLED** | Twice: population level (MATCH1) and item level (H1) | — | — |
| H3 | VIGIL (OECD PIAAC, 9 countries) P1 direction: leads read external material more than comparable members (1.14, CI 1.05–1.23; replication 1.19) | **PASSED** | Real data, locked rule passed. **But this is prior art, not GTAO's prediction:** Mintzberg's monitor role [FULL in VIGIL]. Supervisors also read own-task material more (generic). n ≈ 10k, so any non-zero gap is "significant" | VIGIL/RESULTS.md | Lock 01:40:35 → results 01:40:55; PRIOR_ART.md not hashed; RESULTS.md written after the replication output; **raw data now deleted** (cannot be re-run on the box) |
| H4 | VIGIL P2 specificity (advantage specific to shared external drivers) | **OPEN** | The locked "pass" (1.19) came from a misspecified stacked estimator. The correctly specified contrast is **null**: 1.06 (0.98–1.16), replication 1.03 (post hoc, disclosed). Leaning against | same | — |
| H5 | VIGIL P3 √span gradient (theory 0.5) | **OPEN** | Not passed: 0.036 (−0.005 to 0.076); 0.019 in replication; no steeper than for own-task reading. No kill rule fired. Weak instrument (top-coded five-point self-report, no "whose driver") | same | — |
| H6 | VIGIL P4 size ≈ 2 | **OPEN** | Declared non-decisive by its own prereg; observed 1.15–1.19. **The "≈ 2" target was itself wrong as a floor** (E5–E6): at finite ρ the theory predicts V(N\*) ∈ (1, 2) at h = 0. It is also a flat-member comparator issue (math Issue 10) | same | — |
| H7 | VIGIL-2 (Enron email, 98 custodians): external share of received mail rises with rank | **KILLED** | Locked KILL-1 fired: 0.93 (0.82–1.06) per rank level. External volume 1.00 (0.84–1.20); implied subtree elasticity 0.001 (−0.10 to 0.10) vs GTAO band 0.3–0.7. **Adequately powered** (MDE ≈ RR 1.21 per level vs √-law 1.41–2.45). **Weak construct:** received mail is not a sampling choice and is not specific to shared drivers; assistants filter mail; a coarse rank list; no span measure | VIGIL/v2/RESULTS_2.md; physstat re-run | Lock 01:51:23 → **code edited 01:51:29 (6 s after lock)** → dry run → amended lock 01:51:40; the pre-edit file was not retained, so "dry-run-only edit" cannot be verified |
| H8 | Vigilance in firms as a whole (F4: a new central tracker ≈ 2× a unit's effort, growing √N) | **OPEN** | Field direction mixed (H3 prior-art pass, H7 kill); size and growth unsupported on two weak instruments. **The theory has not yet specified an instrument it would accept as a fair kill**; the spec in §3 fixes that | H3–H7 | — |
| H9 | MATCH1 measles freeze-or-hold (Theorem G) | **PASSED** | Earlier locked test, with caveats: town presence ≠ individual exposure; 39 informative lags; **data already read** (an ordinal postdiction per CORE_AUDIT); mechanistic rival (long-lived plasma cells); **not independently reviewed** | repo tests/MATCH1 | Self-attested |
| H10 | Need exponents 0.6–0.8 replicate across news, code, Wikipedia | **CIRCULAR/NOT EVIDENCE** | A real observation, but it is produced by heterogeneous memoryless items (SCALEFREE S1), so it is not evidence for GTAO. Also Anderson & Schooler 1991 [DOI] | repo THEORY §2.4 | — |

## I. Cross-substrate implications (EXTENSIONS §3; each conditional on an unmeasured mapping)

| # | Claim | Status | Scope / conditions | Credit / evidence | Real data? |
|---|---|---|---|---|---|
| I1 | C1 cells: averaging receptors (A₁) give e_g = −2 (vs −1 under R2) | **OPEN** | Class unmeasured in every real substrate. Cells are Berg–Purcell/averaging-limited, so R1 is impossible there (physstat) | Credit: Berg & Purcell 1977 [ABS]; Mora & Nemenman 2019 [ABS]; Kaizu et al. 2014 [ABS]; Govern & ten Wolde 2014 [ABS] | none |
| I2 | C2 averaging pathways build bottom-up cascades when κ > ½ | **OPEN** | As I1 | — | none |
| I3 | C3 shared sensors born far more vigilant (V ∝ 1/ρ in A₁) | **OPEN** | As I1 | — | none |
| I4 | I1 immune freeze/hold/lookup by antigenic drift | **PRIOR ART** | The phase-diagram programme is published. The "cliff" (bimodality) sharpening is new and OPEN | **Mayer, Mora, Rivoire & Walczak 2016 PNAS 113:8630** [ABS]; Kussell & Leibler 2005 [ABS]; Schnaack & Nourmohammad 2021 [ABS]; Rogers 1988 [FULL] | BIO1/COLLAPSE1 mixed (earlier) |
| I5 | I2 conserved epitopes act as levels; I3 herd memory as a shared store | **OPEN** | Conjectured / speculative (I3 is not counted as a prediction) | — | none |
| I6 | A1 ant trail onset N\* ∝ 1/ρ; A3 opposite effects of individual noise and shared patch change | **OPEN** | Upkeep regime, R-type trail | A threshold colony size exists: Beekman, Sumpter & Ratnieks 2001 [ABS, verified] (credit owed); recruitment rises with colony size across species: Beckers et al. 1989 [FULL]. **Counter:** Dornhaus et al. 2006 [FULL], colony size had no significant effect | none |
| I7 | P1 people: an RI (R2) group monitor is born ≈ 2× as vigilant, independent of the monitor's price | **OPEN** | **Wording must change** to "→ 2 as ρ → 0 at h = 0; in (1, 2) at finite ρ" (E6). RI in organizations: DGS 2016 via MMW 2023 [FULL] | — | none |
| I8 | P2 offloading by drift: q_c ∝ u^{1/b}; holding drops discontinuously | **OPEN** | The law is untested. Qualitative offloading is prior art: Sparrow, Liu & Wegner 2011 [ABS, verified]; Risko & Gilbert 2016 [ABS]; Ballard, Hayhoe & Pelz 1995 [ABS] | — | none |
| I9 | F1 firms: a central tracking function appears at N\* ≈ Π\*/ρ, e_g = −1 | **PRIOR ART** | In substance | V&W 2007 [FULL]; VZR 2001 [FULL]; G&M 1991 static manager onset [FULL, DP text] | none |
| I10 | F2 common shocks centralize tracking, idiosyncratic ones decentralize | **PRIOR ART** | = C2 | AALVZ 2007 [ABS]; VZR 2001 [FULL]; Hayek 1945 [BIB]; **not ADM 2008** | none |
| I11 | F3 total volatility promotes central tracking when h > 0 | **OPEN** | Zero-delay model; conflicts with the delay theory and with evidence | Aoki 1986 [FULL]; MOVZ 2001 [ABS]; Aghion et al. 2021 [FULL] (counter-evidence) | none |
| I12 | F5 / AI2: AI cheapens lookup, so middle relay levels dissolve before frontline expertise; tracking concentrates in provider-side stores | **OPEN** | Derived in 𝓜 (F19), conjectured for firms. "Relay levels exist for pooled tracking, not authority" is unsupported (physstat) | Bloom et al. 2014 [FULL] | none |
| I13 | AI3 cheap central sensing centralizes at small N | **PRIOR ART** | In substance | Bloom et al. 2014 [FULL]; Garicano 2000 [ABS] | none |
| I14 | Y1 sublinear city-wide monitoring spend; Y2 geometric service tiers; Y3 depth ∝ log N | **OPEN** | Mappings unmeasured. Y2/Y3 known in kind (Roundy 1985 [ABS]; Jaques 1990 [SEC]; Williamson 1967; Beckmann 1977) | — | Y2: MATCH1 C1 inconclusive |
| I15 | AI4 the theory describes "judgment" in machines | **OPEN** | Speculative; the free-energy version is killed (K1) | — | none |
| I16 | DP1 programme (corrected): measure the **level technology's** exponents (or its price structure) independently, then predict the collective onset exponent | **OPEN** | Apparently new as a programme. Never run on real data | Nearest: Mora & Nemenman 2019 (single-cell exponents, no collective onset) [ABS] | **none** |
| I17 | DP3 software: org-wide wrappers where n_m q_m/Q_res is high at fixed n_m; DP4 accretion after an upkeep drop; DP5 human lookup-cost edge σ_c ∝ u | **OPEN** | Designs only | ARCH §6 | none |

## J. Framing and cross-substrate claims

| # | Claim | Status | Scope / conditions | Credit / evidence |
|---|---|---|---|---|
| J1 | "The same law, with the same constants (Π\* ≈ 4, V ≈ 2, 29%), holds on every substrate" (CORE_AUDIT §2.5e) | **KILLED** | The constants are functions of (a, b) and H, not universal numbers (ARCH §0.2), and V ≈ 2 is now itself corrected (E5) | ARCH; physstat §1 #3 |
| J2 | "The −1 onset is a universality class" | **KILLED** | It is a Buckingham-Π homogeneity identity: any concave cost of Wq gives it | physstat §1 #3 |
| J3 | GTAO is a "law" / a general law of adaptive organization | **OPEN** | **Not supported by novelty or evidence** (priorart §5; physstat §6). Wording rule: call GTAO a falsifiable causal theory. A law could only emerge if one relation held with the same form in ≥ 2 substrates with independently measured classes | — |
| J4 | Cross-substrate, recursive organization (qualitative) | **PRIOR ART** | Qualitative | **Beer's Viable System Model**: recursion "any viable system contains, and is contained in, a viable system", applied from cells to states (Beer 2002 text [FULL]; Beer 1984 JORS [UNVERIFIED details]); Galbraith 1974 [ABS]; Tushman & Nadler 1978 [ABS]; Simon 1962 [BIB] |
| J5 | CORE_AUDIT: "nobody has stated them across substrates" | **KILLED** | Should read "not *quantitatively*" | Beer VSM (J4) |
| J6 | Quantitative cross-substrate claim: the same (a, b) exponent relation in each substrate | **OPEN** | Apparently new; untested | priorart §2 |
| J7 | **Fractal vigilance**: every level's lead watches the drivers its own members share (Chad's t1901 point: shared and private are relative to the level) | **PRIOR ART** | Qualitatively, the claim is Beer's VSM System 4 ("outside and then") at every level of recursion [FULL], plus Mintzberg's monitor role at every managerial level [FULL in VIGIL]. The quantitative version (V(N\*) formula per level, N^a growth) is in E6/E9 and untested on fair data | — |
| J8 | "No one in charge, at every level" | **KILLED** | As stated (killed earlier and narrowed in THEORY §6) | repo THEORY §6 |
| J9 | Narrowed: no one *needs* to be in charge when maintaining shared memory is privately rewarded; otherwise expect enforcement | **OPEN** | Untested; not modeled in 𝓜 (no strategic members) | Olson 1965 / Ostrom 1990 [classic, not fetched] for the commons side |
| J10 | Energy / second law governs adaptive organization above the cell | **KILLED** | Withdrawn by the theory itself (THEORY §2.3: "not literal above the cell"). The physics referee found the energy framing **decorative**: no conserved quantity, entropy production or Landauer-type bound enters any proof, and Axiom 5's "one currency" is an exchange rate within one organization | physstat §1 #4, §2.2 |
| J11 | In cells, R2 is "the thermodynamic floor", which would fix the class and so the exponent | **OPEN** | Asserted, not derived. A_θ and R2 give different exponents (−2 vs −1), so this assignment decides the prediction. Several separate resource limits exist (receptors, time, energy) | Govern & ten Wolde 2014 [ABS]; Mehta & Schwab 2012 [UNVERIFIED] |
| J12 | CORE_AUDIT: "team theory is static" | **KILLED** | False | M&R 1972 ch. 7 "The team in a dynamic environment", incl. periodic recovery with fixed cost and group size ∝ n^{1/(h+1)} [OCR]; Aoki 1986 [FULL]; VZR 2001 [FULL]; Radner 1993 [FULL]; MOVZ 2001 [ABS] |
| J13 | CORE_AUDIT: no dynamic drift → structure theory exists | **KILLED** | — | MOVZ 2001 [ABS]; Aoki 1986 [FULL] |
| J14 | Title "A Theory of Adaptive Organization" is distinctive | **KILLED** | Collides with **Dessein & Santos 2006, "Adaptive Organizations", JPE 114(5):956–985** [FULL] (adaptation to local information vs coordination). It must be cited. **Renaming is Chad's decision**; the repo was not renamed | priorart §3.3 |
| J15 | Core mechanism C (drift destroys held information; re-buying it costs; selection keeps the cheapest allocation; architecture is caused by drift structure and prices) | **OPEN** | It has not passed one discriminating test of its own. In markets its math *is* the economics of information (CORE_AUDIT §2) | CORE_AUDIT §1 |

## K. Earlier repo claims (THEORY.md v1.0 and the public X posts), statuses brought up to date

| # | Claim | Status | Note |
|---|---|---|---|
| K1 | X1 variational free energy = thermodynamic free energy (embodied) | **KILLED** | Withdrawn: definitional or underived. Still et al. 2012 [DOI] does not state it |
| K2 | X2 correction costs rise with temperature like Landauer | **KILLED** | Replaced; τ structure failed |
| K3 | X3 judgment = staying alive under the second law | **OPEN** | Framing, not testable as stated |
| K4 | X4 / N3 / D1 risk ∝ shock × √(time to fix) ÷ buffer; fixed-spread ε_τ = −1; temperature identities | **KILLED** | MATH_ATTACK literal joint kill (populations on any reading; glucose full sample); banks sign-only; the sign follows from dimensional analysis. Credit Black & Cox 1976 [unverified in sweep] |
| K5 | X5 / N5 watching rises then collapses (cliff) | **PRIOR ART** | = F12 (Cho & Garcia-Molina 2003). Cross-domain claim OPEN |
| K6 | X6 / rule 5 copy error grows with hops and drift | **PROVED** | Markov states only; known in kind (Bailis et al. 2012). Field OPEN |
| K7 | X7 stress strengthens up to a ceiling; faster correction raises it | **OPEN** | Ceiling known (bounded antifragility) |
| K8 | X9 higher levels track slower causes (Simon/Kiebel) | **PRIOR ART** | Refined by T7 |
| K9 | N1 √N fade of shared memory (math) | **PRIOR ART** | Kalman averaging. ANTS1: see G13–G18 |
| K10 | N1 application to languages (LANG1, 0.13 vs 0.5) | **KILLED** | Earlier test; the mapping failed |
| K11 | N1(a) Austronesian test | **OPEN** | Not run |
| K12 | N4 geometric layers iff scale-free drift; K\* ∝ (log-span)^{2/3} | **OPEN** | "If" direction known in substance (Roundy; Shankar & Howard). Count inconclusive (MATCH1 C1); LAYERS1 linear fits better and P2 failed (G20) |
| K13 | N6 spectrum → exponent relation (core of THEORY §2) | **OPEN** | Leaning against: every exact exponent tested missed or was inconclusive; MATCH1 D3 redness sign opposite (exploratory) |
| K14 | N7 internal-model bound P ≤ √(2δ)/γ_L | **PROVED** | Self-checked, probably folklore, loose ≈ 10×; not independently reviewed |
| K15 | D2 universality classes of fixing | **OPEN** | Derived, untested |
| K16 | D3 pooling cools, z′ = z√(N/(1+(N−1)ρ)) | **PROVED** | Standard variance algebra |
| K17 | D4 drift reduction substitutes for tracking | **OPEN** | Not modeled in 𝓜 |
| K18 | D7 bet-hedging: "every system pays for a model" | **KILLED** | Kussell & Leibler 2005 [DOI] |
| K19 | D10 immune memory lifetime tracks pathogen drift | **OPEN** | Killed on first read (BIO1 P3a), largely a measurement artifact (COLLAPSE1) |
| K20 | Design rules 1 and 4 | **OPEN** | Near-tautologies, so no test is informative |
| K21 | Design rule 3 (move belief by signal reliability) | **PRIOR ART** | Kalman 1960; Muth 1960 |

---

## 1. Status counts (rows in this file)

150 claim rows, by status:

| Status | Rows | What they are |
|---|---|---|
| PROVED | 40 | In-model theorems with corrected scope (sections A–F) plus K6, K14 and K16. None is evidence about real systems |
| OPEN | 41 | Every cross-substrate implication, the core mechanism, the quantitative cross-substrate claim, inconclusive simulations, and VIGIL specificity, growth and size |
| KILLED | 36 | **5 on real data:** H1 P1 recall slope; H2 forgetting = need; H7 Enron vigilance; K4 τ/temperature structure; K10 √N in languages. **6 locked in-model predictions:** G6, G9, G15, G16, G17, G20. **1 mis-statement superseded by theory:** G8. **24 statements refuted by proof or counterexample, miscited, or withdrawn:** for example E5 V ≥ 2, B10 T1.8 signs, F9 T7(c) iff, C3 ADM citation, J12 "team theory is static", J14 title, J10 energy above the cell |
| PRIOR ART | 19 | The claim is published (credited in the row) |
| CIRCULAR/NOT EVIDENCE | 12 | 11 simulation rows (circular, or valid in-model but not about nature) and one real observation explained by heterogeneity (H10) |
| PASSED | 2 | **H3** (PIAAC direction: a real pass, but Mintzberg's prior art) and **H9** (measles freeze-or-hold: earlier, caveated, a postdiction, not reviewed). **GTAO-specific real-data passes: 0** |

The count is per row of this file. Rows were split where the reviews split a result (for example T5.2 pointwise KILLED and uniform PROVED), so the counts describe the map, not "how much of the theory" is right.

---

## 2. What is genuinely ours (survived all four reviews; each is elementary)

None of these is deep. Each is a short calculation on known models. Each is "apparently new" only after a search of about 45 sources by the prior-art referee. **Before any public novelty claim, the forward-citation sweeps in §3 must be run.**

| # | Result | Exact scope | Real-data test so far |
|---|---|---|---|
| O1 | **The sensing class (a, b) sets the collective onset exponent: e_g = −(1−b)/(1−a), with the level's class doing the setting** (T1.3 + T1.8), the upkeep dichotomy (T1.5), and the closed form N\* = [ρ^b/((1+ρ)^b − 1)]^{1/(1−a)} | ρ → 0 asymptotic; h = 0, or a > b with upkeep; the level's (a_L, b_L) when the technologies differ. The −1 special case (a = b) is prior art (V&W 2007; VZR 2001) | **None.** Simulations are circular; SENSING2's one risky world (EVO_A) was a locked in-model **kill** with documented caveats |
| O2 | **The technology, not the loss function, sets the exponent under bundled decisions** (T4), and in Kalman technologies N\* is exactly loss-independent (D2) | Gaussian closure, independent phases, small ρ; the proof is a sketch for R1 (two-sided bounds owed); α-stable open | **None.** The informative simulation contrast (SENSING2 QUART_R) was not cleanly run |
| O3 | **The exact vigilance formula and its floor**: V(N\*) = ½(1 + (1+ρ)^{−1/2})(1 + √(1 + 4h′(√(1+ρ) − 1)/(rρ))); V(N\*) ≥ 1 + (1+ρ)^{−1/2} for every upkeep and price; **price invariance at h = 0** (T5.4); **V > 1 for all (ρ, h, r) iff a ≥ b** | γ = ½ (R1 Brownian or R2), common technology, separable costs, component readability; comparator = a flat member | **No fair test.** PIAAC and Enron measured a mis-mapped quantity (supervisor vs supervisee, received mail, self-report). Price invariance has never been tested |
| O4 | **The ordering threshold κ\* = (1−a)/(1−b) = 1/\|e_g\|**: hierarchies fill top-down iff sharing thins slower than n^{−κ\*} | Iff at h = 0; at h > 0 only sufficient, with a gap; κ\* is the level's class | **None** |
| O5 | **The closed-form freeze/hold/lookup band**: a hold band exists iff μuH_l > 2c + hH_l; a shared store widens it N² (N^{(1−a)/b} in general); the lookup edge has elasticity 1/b in u; with whole-item lookup, pooled levels dissolve before private holding (E4) | R1 quadratic (power class for the general widening); lookups return current values | **None** for the band or the widening. The related Theorem G freeze-or-hold passed on measles (H9), with caveats and as a postdiction |
| O6 | **Measure one member (or the level's technology), predict the group**: the corrected DP1 programme. Measure the level technology's quadratic-loss exponents or its price structure independently of onset, then predict e_g and κ\* | Needs a substrate where the class can be measured independently and onset observed in a regime where prize ≫ decision noise (P10, G4) | **None**; never run on real data |

Also apparently new but minor: the per-read broadcast threshold ρ_b = 4t/(1−t)² (T2); T3's sign at every ρ (common technology); the lookup counterexample to accretion (F3); the resolution floor ρ ≲ ε/b (P10).

---

## 3. What would make it profound (fair, non-circular next tests)

**3.0 Required before any public novelty claim (owed, not run).**
1. **Forward-citation sweep of Marschak & Radner 1972 ch. 7 §5** (periodic recovery of delayed complete information, eq. 5.13), and of the ch. 7 §6 group-size result. Use Google Scholar "cited by", Semantic Scholar and OpenAlex. Search terms: periodic information recovery, team size, common component, square root, onset or threshold, exponent. Target an earlier statement of e_g = −(1−b)/(1−a), of the closed form N\*, or of V at onset.
2. **Forward-citation sweep of Van Zandt & Radner 2001** (Economic Theory 17:545), plus Van Zandt's real-time decentralized information-processing line and MOVZ 2001 full text.
3. Also owed: Veldkamp 2011 ch. 8 (returns to scale in information; paywalled, TOC only), Maćkowiak, Matějka & Wiederholt 2023 JEL survey in full, Vayanos 2003 in full, Alvarez–Lippi–Paciello 2011 full text, Sims 2003 re-read, and the inventory-pooling line (Eppen 1979; Maister 1976) for the √N vigilance and pooled-onset statements.
4. Cite in every draft: M&R 1972 ch. 7, VZR 2001, V&W 2007, Aoki 1986, AALVZ 2007, Bloom et al. 2014, Wolman et al. 1999, Mayer et al. 2016, Mora & Nemenman 2019, Beer's VSM, Dessein & Santos 2006, and Topkis / Milgrom & Roberts.

**3.1 Process fixes (apply to every future lock).**
1. **External hash timestamp for every future lock, before any outcome is pulled.** Options are an OSF registration, a Zenodo draft DOI, a public gist, or an RFC 3161 timestamp authority / OpenTimestamps. Each sends a hash outside the box and some are public, so **each needs Chad's explicit go.** Chad waived timestamping for night 1 (t1895); that waiver is not permission to post.
2. Retain every pre-amendment file and hash the code at lock (LAYERS1 did not; VIGIL-2's pre-edit code is lost).
3. Dry-run every estimator on synthetic data with known truth, including floors and ceilings, before locking. That would have caught VIGIL P2's misspecification, the logistic floor bias and SENSING2's flat-arm bug.
4. Keep raw data or checksummed download scripts (the PIAAC folder is now empty).
5. One master table of every locked prediction, with by-construction ones flagged and family-wise accounting (about 40 locked sub-predictions tonight).
6. A blind, independent analyst for real-data tests.

**3.2 A fair-kill measurement spec for vigilance (proposed; to be locked before any data are pulled).**

It uses only results that survived the math review (E6–E8), so a kill cannot be rescued by invoking upkeep or prices.
- **Unit of analysis.** A **named shared driver** g, fixed before data: for example a specific upstream API, a supplier price, a regulation, or a named market index. Members' decisions demonstrably load on it.
  - **The level** is the role or person that holds the tracker other members use for g (documented consumption of its estimate), not the boss by title.
  - **The comparator** is the *flat* comparator: members of matched units with **no** such level, tracking g within their own targets, or the same members before the level existed. It is **not** the lead's own current members, who in 𝓜 do not sample g at all (math Issue 10).
- **Effort.** All-channel sampling events of g per unit time: reads, queries, system or API access logs, calls and meetings tagged to g. Use calendar plus log data, or a structured diary in the manner of Bandiera, Prat, Hansen & Sadun (data not yet obtained). Normalize per unit of g's own drift: divide by √q̂_g, with q̂_g measured from g's own time series.
- **Class gate (measured first, independently of onset).** On lone or flat units, estimate the drift and stakes elasticities of sampling effort.
  - Proceed with the class-R/γ = ½ prediction only if b̂ ∈ [0.4, 0.6] and |â − b̂| < 0.1.
  - Also measure g's Hurst exponent, and proceed only if Ĥ ∈ [0.4, 0.6].
  - Otherwise use the general-(a, b) formulas, or declare the case out of scope **before** looking at V.
- **Shared share.** Estimate ρ̂ = q̂_g / q̂_u from the variance decomposition of members' targets.
- **Prediction (class R, any upkeep, any price ratio, any N ≥ N\*):** V_obs ≥ 1 + (1+ρ̂)^{−1/2}. That is ≥ 1.95 for ρ̂ ≤ 0.1, and ≥ 1.71 for ρ̂ ≤ 1.
- **Kill.** In the pre-declared class-R units, the pooled upper 95% bound of V_obs/(1 + (1+ρ̂)^{−1/2}) is < 0.8. Equivalently, for ρ̂ ≤ 0.1, the upper bound of V_obs is < 1.56.
  - Any V_obs ≤ 1 with CI excluding 1 kills outright for every class with a ≥ b.
- **Growth test (secondary).** Across levels of different pooled N, the slope of ln V_obs on ln N should lie in [0.3, 0.7] for class R. Kill if the CI excludes 0.3 and includes 0.
- **Price invariance (only where upkeep is negligible).** Use exogenous variation in the lead's monitoring cost, such as a tooling change for the lead only. The prediction is that V at onset does not move. Kill if |elasticity of V w.r.t. p_g/p| > 0.2 with CI excluding 0.
- **Selection gate.** Declare in advance which settings count as strongly selected: the prize at the observed N exceeds the measured decision noise (P10, G4). Misses there count fully, and settings outside the gate are not analysed.
- **Validity criteria are fixed before the data**, so "the mapping was wrong" is not an available rescue once those criteria are met.
- Candidate data: firm calendar or log metadata via a partner; a lab or online team experiment where the driver and channel are designed; or an LLM multi-agent system with sensing costs paid in real tokens (see 3.3).

**3.3 Non-circular onset test (the O1/O6 relation).**
- Agents **not given the cost function**: RL, evolved, or LLM agents with sensing paid in real compute or tokens, not a formula.
- Manipulate ρ experimentally over ≥ 1.5 decades in a regime where the prize is much larger than the decision noise.
- Measure the **level's** (a_L, b_L) on the level itself, separately.
- Include a mixed-technology arm (level class ≠ member class) to separate "members set the exponent" from "the level's technology sets it". That is the contrast SENSING2 never ran cleanly.
- Third-party lock (3.1.1) and a blind analyst.

**3.4 T3 opposite signs, factorial.** Vary shared and private volatility independently in lab teams, agent systems or ant colonies. Predict opposite signs on centralization of tracking, within a common technology or small ρ (B10). Contingency theory predicts one sign for total volatility.

**3.5 T4 contrast, fixed design.** Rerun the quartic/absolute bundled-loss arm with the level **re-optimized under φ₂** and the SENSING2 flat-arm bug fixed. A clean −1 versus −½ separation is a real in-model test of O2. A physical system with measurably non-quadratic loss would make it physically interesting.

**3.6 Lookup and AI (O5, F19).** A natural experiment in firms adopting retrieval tools, with roles coded **before** outcomes by an external coder. Test whether relay roles shrink before frontline private expertise erodes, and whether central stores grow.

**3.7 Physics.** Either derive one bound in physical units for one sensing system (for example ATP per nat for a named receptor network) and show it fixes the class, or drop "energy / second law" from public language (J10–J11).

**3.8 Math owed.**
- T4 as a limit with two-sided bounds, using the Kalman route where possible.
- T5 for R1 with fBm drift.
- The bundled exponent for α-stable drift.
- Analytic Π\* under the subtract readability scheme (P11), and vigilance there.
- T4 with phase-locked reads.
- A definition of "class R".

---

## 4. Lock integrity (applies to every PASSED/KILLED above)

The physics/statistics referee re-verified every hash and found **no sign that any outcome was seen before a lock**. Every sequence that can be checked is clean. But:

- **Every lock is self-attested.** Commits are local and author-dated. Nothing is third-party timestamped (Chad waived this for night 1).
- **Body times contradict lock records.**
  - ANTS1 body "~10:45 PM" vs commit 22:21:16.
  - theory-v3 PREDICTIONS "~23:55" vs commit 23:46:35, with SCALEFREE derivations committed after the lock.
  - POOLSIM "about 00:45" vs lock 00:42:14.
  - SENSING body "about 01:26" vs lock 01:28:27.
- **POOLSIM.** The PREREG.sha256 sidecar was rewritten at 01:16, after the outputs. run_analysis.py was unlocked and edited (disclosed).
- **VIGIL-2 (Enron).** The code was edited **6 s after the original lock** (01:51:23 → 01:51:29), then a dry run, then an amended lock at 01:51:40. The pre-edit code was not retained, so the "dry-run-only edit" claim cannot be verified.
- **LAYERS1.** The code was **not hashed** (same mtime as the lock), and the P3 series count was rescaled after the fact.
- **VIGIL (PIAAC).** **Raw data deleted**, so the analysis cannot be re-run on the box. PRIOR_ART.md was not hashed, and RESULTS.md post-dates the replication output, contrary to the prereg's order.
- **ANTS1.** The analysis code was committed after the run started (disclosed). Mtimes were reset by the VM restore. The resume was verified deterministic: 1,201/1,201 results identical, and 3/3 re-run jobs bit-identical.
- **P1.** Runner identity was checked only on a 388-row slice. The locked CI was "unavailable", now resolved by the independent re-fit.
- **Multiplicity.** About 40 locked sub-predictions tonight, with no family-wise accounting.

## 5. Open decisions for Chad

1. **Title.** "A Theory of Adaptive Organization" collides with Dessein & Santos 2006, "Adaptive Organizations" (JPE). Options: keep it and cite D&S prominently, or differentiate (the prior-art referee suggests something like "a tracking-cost theory of adaptive organization"). The repo was **not** renamed.
2. **External timestamping** of future locks (OSF, Zenodo, gist or OpenTimestamps). This is a public or external act, so it needs your go.
3. **Public language.** The repo now says "falsifiable causal theory" and never "law". Decide whether "energy / second law" stays anywhere public (the physics referee calls it decorative).
4. **Public corrections.** Any earlier public statement that implied "levels watch at least 2× as hard", a confirmed vigilance result, or novelty of the onset relation would need a correction. Any X post needs your go and an independent fact-check first.
5. **Data access.** Whether to try the Bandiera et al. CEO-diary archive through a real browser (it is behind a Cloudflare 403 for the box; a paid mirror exists and was not used), or to seek a partner firm for calendar/log data for the §3.2 spec.
6. **Next test to fund with remaining usage.** The cheapest fair one is the §3.3 non-circular agent test with a mixed-technology arm, plus the §3.0 citation sweeps.
