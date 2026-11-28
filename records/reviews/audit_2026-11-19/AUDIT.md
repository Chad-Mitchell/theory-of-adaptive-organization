# AUDIT of the GTAO repo at v2.1 (read-only)

> **Repository copy (added 19 Nov 2026 with THEORY v2.2).** A dated working record, copied from the working directory with paths updated: `checks/scale_free_checks.py` is now `theory/meq_checks/scale_free_checks.py` (with assertions, run by `tools/test_scale_free_checks.py`); the clone path `/workspace/gtao-audit` was a scratch directory. Written by one executor of the same bot family: a self-check, **not independent**. Its recommendations R1–R8 (section 6) and the small defects (section 7) were applied in THEORY v2.2; THEORY v2.2 governs where this file and it disagree, and its status words ("theorem", "proved in a model", "conjecture") supersede this file's table labels. The word "law" and the "firms ~10¹²" figure appear here only as quoted material under discussion.


Written Thu 19 Nov 2026, about 11:35 PM ET, by a Grok Bot executor for Chad (via Ace), answering t1985u and t1986. **Nothing was committed, pushed, merged or sent. `/workspace/looper` was not touched. All compute ran at nice 19.**

- **Repo:** fresh clone of https://github.com/Chad-Mitchell/theory-of-adaptive-organization in `/workspace/gtao-audit`. **origin/main = `c55e9603861793172b04773599e1f3515517bc7b`** (the merge of PR #106, THEORY v2.1; committed 23:07 ET on 19 Nov). `tools/check_consistency.py`: RESULT: PASS (0 FAIL). `tools/test_meq_derive.py`: 1 passed.
- **Compared against:** `/workspace/gtao-meq/REVIEW.md` (parts 1 and 2), `reference/THEORY_v2.0.md` and `reference/THEORY_v1.4.29.md` (frozen), `history/2026-11-12_X_POST.md` (the archived 12 Nov post), and the v1.0 THEORY (`git show cbe60a5:THEORY.md`).
- **Checks written for this audit:** `theory/meq_checks/scale_free_checks.py` and `.out`.
- **Limit I could not get past.** I could not read the parent chat. `ReadTranscript` and `SearchTranscripts` only see this executor's own run and there was no transcript id to pass, so I could not enumerate Ace's chat messages. I worked from REVIEW.md (which is headed "Ace's ideas (t1974u)" and holds ideas (a)–(k)), from the keywords in the brief, and from the repo. **Anything Ace said to Chad in chat that is not in REVIEW.md or a keyword above is not accounted for here.** The parent should check its own messages against section 1.

---

## 0. Headlines

1. **Accounting.** Almost everything in REVIEW.md reached main, mostly because PR #106 copied REVIEW.md wholesale to `reviews/master-equation_2026-11-19/REVIEW.md` and its Part 2 into `theory/MASTER_EQUATION.md`. In the canonical `THEORY.md` the content is thinner. Genuinely missing or partial: the federation coupling term J_coupling; idea (g) "layers are components of the predictive state worth their upkeep" beyond McMillan degree; the Kelly/ln 2 exchange rate (it is in `theory/GENERAL_THEOREM.md` S5 but absent from THEORY); the over-identification count per revealed-cost test; regime-switching, exploration and indivisible-read limits in the §9 scope list; the 150-word compression with glossary; and the whole "temperature" story in the main text (section 5).
2. **Same energy at every scale.** Nothing can be a single currency. What is **provable now** is that J is scale-free once written in the system's own numeraire. The optimum depends only on dimensionless ratios, and the cost shares at the optimum are currency-free numbers (new, elementary, checked). The Landauer floor is a lower bound for every scale, and the gap to it is one measured number per system. Anything that says firms pay in joules is an **overclaim**. Section 2.
3. **v2.1 vs the old framing.** v2.1 is stronger in structure (one objective, an in-model theorem, a survival lemma that now explains the buffer). It **lost three things worth restoring**: the seven-rule table with its fails-when column, the temperature/firm-volatility prediction as a stated, testable consequence, and the stress-ceiling prediction. The first two are now derivable from J and should be restored as corollaries. Section 6 gives the exact list.

---

## 1. Accounting: every idea, result and proposal

Legend: **IN** = on main in a named place; **PARTLY** = some of it; **MISSING** = not on main. "Repo copy of REVIEW" = `reviews/master-equation_2026-11-19/REVIEW.md`, which is dated working record, not the canonical text. THEORY.md governs.

### 1a. REVIEW.md part 1

| # | Item | Status | Where on main, and what it says |
|---|---|---|---|
| 1 | Equation is a definition, not a theorem | **IN** | THEORY §3 last paragraph: "It is the theory's statement of the problem, not a theorem." §4: "A **definition**: the cost J." |
| 2 | Master Theorem (i) existence, (ii) monotone comparative statics, (iii) layer cap, (iv) survival, (v) special cases | **IN** | THEORY §5 and B.9 (CT20–CT22); `theory/MASTER_EQUATION.md` §1; table of nine special cases in §5 (v); `theory/meq_checks/meq_derive.py`. Quote: "The best layer count never falls as stakes rise relative to upkeep (w/h)… This part holds for every world and every loss." |
| 3 | "Hostile view / steelman": every behavior is optimal for some cost; content only from price-free structure and measured prices | **IN** | THEORY §4: "least action has no free prices and J does, so the principle says something only through structure that holds for every price (§5 (ii)–(iii)) and through prices measured independently". |
| 4 | Theorem L misstated; large buffer ⇒ slack ⇒ EOQ is the new Lemma (iv) | **IN** | THEORY §5, "**Theorem L, stated correctly.** … Its best interval does not depend on the buffer… The large-buffer statement is (iv)." CT22. |
| 5 | World enters through its measured law; (q, α) is the scale-free special case | **IN** | THEORY §3: "The drift level q and spectral slope α are the scale-free special case." |
| 6 | Read term widened to information-acquisition spend A; link/telling/lookup L (κ_b, d, u) | **IN** | THEORY §3 bullets for A(𝒟) and L(𝒟). |
| 7 | g = 0 in every theorem; g is an open lever | **IN** | THEORY §3 "Open lever" and §9 "Worlds that respond". |
| 8 | CT7 is a floor on J, not a solution | **IN** | THEORY §5 table: "J\* ≥ σ√(2kT·w): **a floor on J, not a solution of it**". CT7 text at Appendix B (l.241). |
| 9 | Reword "layers at the world's time scales" (option a, verbatim plus gloss) | **IN** | THEORY §2: "*At the world's time scales* means: one layer for each separated time scale the world changes on that the stakes can pay for, each with a memory set by that scale and the sensing noise (usually much shorter… a 90-day mode gets a 6–12-day store)." Also README. |
| 10 | Special-case table (CT12, L1–L3, LAT-1, Result 4…) and the mismatches it found | **IN** | `theory/MASTER_EQUATION.md` §1a (full), THEORY §5 table. |
| 11 | κI_mem + hK: say which holding term each result uses | **PARTLY** | THEORY §5 table's "J restricted to" column names κ only for P3/CT4 and h for layers, but never says in words that no layer theorem uses κ and h together. |
| 12 | Prior art table with Crossref-checked DOIs; verdict "modest synthesis" | **PARTLY, deliberately** | Full table and DOIs: repo copy of REVIEW §2 and `theory/meq_checks/crossref.out`. THEORY §10 gives the credits without DOIs table and replaces the verdict with "Known parts, new claim". `theory/MASTER_EQUATION.md` header says the verdict words are superseded. This is a choice by Chad (t1976), not a loss. |
| 13 | Worked engineering example (demand forecast, hypothetical numbers) | **IN** | `theory/MASTER_EQUATION.md` §3 (it sits under a duplicated, empty heading, see section 7). Linked from THEORY §7. |
| 14 | Inputs ranked by hardness to measure (q, α easy … κ hardest) | **IN** | `theory/MASTER_EQUATION.md` §3. THEORY §7 only says "the bottleneck is measurement". |
| 15 | Scope: where assumptions fail (8 items) | **PARTLY** | THEORY §9 has worlds that respond (CX2), linear-Gaussian only, one currency, "should be built". **Not in THEORY §9:** regime shifts / non-stationary law (N16), goals beyond tracking (exploration, play), indivisible reads (Prop 9), costs that do not add (S4 is only in Lemma B12). Full list is in the repo copy of REVIEW §4. |
| 16 | "What 'every scale' can mean": same problem, own prices, not one exchange rate | **IN** | THEORY §9: "'Every scale' means the same problem solved with each system's own measured inputs and prices, not one exchange rate." |
| 17 | Idea (a): variational principle, "sit near argmin J" | **IN, with one caution** | THEORY §4 principle. REVIEW advised dropping "like least action" from public text because it invites a comparison it loses; THEORY §4 keeps it but states the difference ("least action has no free prices and J does"). Chad's call. |
| 18 | Idea (b): cost-free exponent tests (N51), and that "layer spacing set by α alone" fails | **IN** | THEORY §8 table (N51); §6 item 5 says "roughly log-spaced (exactly geometric for shared clocks, CL12)" and CL12 is proved for every α in (1,3). |
| 19 | Idea (c): revealed costs; only ratios identified; a test only when over-identified | **IN, count missing** | THEORY §7 Diagnosis: "That is a test, not a circle, only when observed features outnumber the free price ratios: one system seen at several exogenous drift levels, several items under one clock, or one read technology across layers." `theory/MASTER_EQUATION.md` §3 (c) still contains REVIEW's own to-do ("the repo should state the over-identification count for each test"). **The count is not stated.** |
| 20 | Idea (d): price of survival μ_s, unifies Theorem L, μ=0 end is EOQ | **IN** | THEORY §5 (iv), CT22: "μ_s = −m′/θ′ > 0, the marginal expected cost of survival exponent… μ_s = 0.0052 per unit θ at B = 0.5. μ_s carries the system's own units." |
| 21 | Idea (e): recursion/closure under coarse-graining | **IN** | THEORY §6 "Two axes, one rule": "A pooled level faces the same problem as a member (closure under coarse-graining, T7c), which is the precise sense of 'every scale'." |
| 22 | Federation needs a coupling-cost term: federate iff Σ J_i\* + J_coupling < J\*_single | **MISSING** | `rg "J_coupling"` finds nothing. THEORY mentions federation only via LAT-1 (reach cap). CLAIM_MAP/CX2 covers the coupled-levels case but not this inequality. |
| 23 | Idea (f): one currency only as inequalities; Kelly ln 2 is the only currency-free rate | **PARTLY** | THEORY §3 and §9 say one currency per system, floors only, "in a synapse… 10⁵–10⁶ times the floor (Laughlin et al. 1998), and in a firm far more". The Kelly exchange rate (a nat buys one nat of log-growth) is only in `theory/GENERAL_THEOREM.md` S5 and its §0 item 6; THEORY cites Kelly 1956 only as a credit in §10. |
| 24 | Idea (g): layers = components of the world's predictive state worth their upkeep; cap by statistical complexity (Crutchfield & Young) or predictive information beyond LG; first test a two-state switching world | **PARTLY** | THEORY §5 (iii) has the McMillan-degree cap in 𝓜_LG. "Predictive state", statistical complexity and the G4 switching-world test appear only in the repo copy of REVIEW §5 (g). |
| 25 | §6 "What this equation makes possible" (claim map, calculator, sign predictions, two ways around G3, price of survival, kill rule) | **IN** | Spread over THEORY §7 (Design, Diagnosis), §5, §8. |
| 26 | §7 top fixes (9 items) | **IN except #8** | #8 (independent review of CT20–CT23, L1–L3) is open: STATUS "Next: Independent review of the Master Theorem and L1–L3 (GAPS G8)". |
| 27 | §8 recommended statement for the top of the core | **IN, changed** | Claim and equation are in README and THEORY §2–§3. The 150-word "problem / theorem / bet" block with glossary is not reproduced; README's "What follows" bullets carry the theorem content. |

### 1b. REVIEW.md part 2

| # | Item | Status | Where on main |
|---|---|---|---|
| 28 | (h) Dimensionless groups; the brief's examples were not dimensionless; T₀ = (c/wq)^{1/α}, J₁ = c^{(α−1)/α}(wq)^{1/α} | **IN** | THEORY B.9 "Dimensionless groups": "a parametric world's design is fixed by about 5–7 groups: the spectrum's shape, h/J₁, ℓ/T₀, μu/J₁, y/J₁, θB, and (N, ρ)." Table and rescaling check (identical designs at ε₁ = 2.2302%, K\* = 2) in `theory/MASTER_EQUATION.md` §4. |
| 29 | Counter-check: same R, different noise share gives R\* = 135, 45, 21 | **PARTLY** | In `theory/MASTER_EQUATION.md` §4 and `theory/meq_checks/part2.out`; not in THEORY (B.9 says only "the spectrum's shape"). |
| 30 | (i) Phase diagram, order of regions follows from (ii) and P0; positions are model-specific; no real system placed | **IN** | THEORY §5 figure `theory/meq_checks/phase.png` and caption: "*Illustrative only:*… The **order** follows from (ii) and Theorem P in every world; the **positions** are this world's. No real system has been placed". Boundary table (ℓ = 0.01, 0.14, 2.2, 30) only in MASTER_EQUATION §4 / `phase.out`. |
| 31 | (j) Dynamics: redesign is the slowest layer, 10–100×, N54 | **IN** | THEORY B.9 "Dynamics", §8 table, CLAIM_MAP N54. |
| 32 | (j) Design scatter ∝ 1/√(α−1), N55 | **IN** | THEORY B.9, §8 table, CLAIM_MAP N55 ("the curvature is exact (meq_derive); the spread-from-curvature premise… not derived for a specific selection model"). |
| 33 | (j) Rates move before structure, with hysteresis (Dixit 1989) | **IN** | THEORY B.9 Dynamics, last sentence. |
| 34 | (k) Local regret ½δᵀHδ; 2× drift error costs 3.8–6.1%; three exceptions | **IN** | THEORY §4 and CT23 with the exceptions: "a wrong layered design can be worse than no layering (7.0% against 2.2%); fitting α far from the decision's scales (up to 29%); and near feasibility edges… A missing cost term is not a perturbation". |
| 35 | "Two kinds of wrong" | **IN** | THEORY §4 second paragraph; README "How it dies". |
| 36 | Compression (the exact short statement + glossary) | **PARTLY** | README first screen; no glossary block. |
| 37 | Law only in the hypothesis sentence | **IN** | THEORY §3: "**The law of adaptive organization (hypothesis): strongly selected systems minimize the cost of judgment.**" §4 calls the rest a principle and theorems. |
| 38 | CX2 coupled levels open theorem | **IN** | THEORY §9 first bullet; CLAIM_MAP CX2 (OPEN). |
| 39 | N56 killing test; CT20–CT23 rows | **IN** | THEORY §8; CLAIM_MAP v2.50 rows (l.457–460, 416–418). |
| 40 | Diagnosis use | **IN** | THEORY §7 "Diagnosis" (five bullets). |

### 1c. Not found in REVIEW.md, expected from the brief's keywords
"four ideas" I take to be (h)–(k): dimensionless, phase diagram, dynamics, robustness; all four are on main (rows 28–35). "same currency" is row 23, "universal" appears only as the named rival "a universal exponent of ½" (THEORY §8) and `process/QUEUE.md` rivals. If Ace proposed anything else in chat (e.g. a specific CX2 construction, or other N-numbers), I could not see it.

---

## 2. The physics question: one currency, or a scale-free form?

### 2a. What the repo and REVIEW say now

- **Dimensionless groups, "partly hold".** Time scaled by T₀ = (c/(wq))^{1/α}, cost by J₁ = c^{(α−1)/α}(wq)^{1/α}. For a parametric world the design is fixed by about 5–7 groups: α or the spectrum's shape, Π_h = h/J₁, Π_ℓ = ℓ/T₀, Π_u = μu/J₁, Π_y = y/J₁, Π_B = θB, and (N, ρ). "Partly" because equal groups give equal designs **only if the world's shape also matches**; a general shape is a whole function (REVIEW (h), counter-check R\* = 135/45/21).
- **Theorem S** (`theory/GENERAL_THEOREM.md` §6, THEORY Lemma B12): S1 currency invariance (degree-1 homogeneity), S2 time covariance, S3 exponents depend on (p, H) only, **S4 covariance fails when two cost components scale differently** (fixed plus size-proportional cost; Landauer floor is one fixed-unit component), **S5 the only currency-free exchange rate** is Kelly: "In multiplicative persistence, a cue is worth at most I(E; C) nats of growth per generation… The physical dual: measurement-based work extraction gives at most kT ln 2 per bit (Vinkler, Permuter & Merhav 2016). … It needs multiplicative dynamics".
- **CT7, the kT-per-nat floor** (THEORY B.1, `theory/MATH_ATTACK.md` §1.2): holding mean squared error D of a random walk dissipates at least kT·σ²/(2D); with stakes w the least cost is **J\* = σ√(2kT·w)**, "a floor on J, not a solution of it". Same function as EOQ with c → kT. Caveats in the text: needs no feedback from tracker to signal; with one cost scale dimensional analysis forces the form, only the √2 is informative. Still et al. (2012) is for nonpredictive memory only, kT·(I_mem − I_pred); `theory/SCALE_ENDS.md` E3 shows the floor can approach 0 for quasi-static passive coupling.
- **κ** = price per nat held per unit time (hardest to measure; "almost never measured outside cells"). **h** = upkeep per layer, store or shared level (accounting-level, fuzzy for people). **w** = stakes: cost per unit squared error (units cost per x²·time); needs exogenous variation in error cost to measure (G3), never validly measured. **μ_s** = the price of survival, the multiplier on the ruin constraint: zero for B ≥ B_slack, rising to the feasibility edge B_min; it "carries the system's own units". **Shadow prices** in the repo: μ_s, and "only price ratios (w/c, h/w) are identified" (THEORY §7). The term "shadow price" itself is not used anywhere in the repo (`rg shadow`: none).
- **The efficiency gap is already in the repo**, under another name: β_phys = actual cost ÷ thermodynamic floor (`measurement/FRAMEWORK.md` §3.11; cells "measurable in principle", synapses 10⁵–10⁶, "ant, person, firm, city: astronomically above 1"), and "c_eff/kT at each scale" (`litmap/LEFT_ON_THE_TABLE.md` #10, `theory/MATH_ATTACK.md` §1.2 "firms are ~10¹² above it"). That last figure has no derivation or source in the repo and should not be repeated (see section 7).

### 2b. First principles: three candidates, checked

Script: `checks/scale_free_checks.py` (output `checks/scale_free_checks.out`, nice 19). Setting for the exact checks: the repo's CT12 single tracker, J(T) = c/T + wqT^{α−1}/α.

**Candidate 1: write every term in the system's own numeraire, so only dimensionless ratios appear. PROVABLE NOW (elementary).**
- J is positively homogeneous of degree 1 in the prices (c, w, h, κ…). So the argmin is invariant under any currency rescaling (S1), and with time and amplitude rescaling (S2 + Buckingham π) the optimum is a function of dimensionless groups only.
- Checked: T\*/T₀ = (α/(α−1))^{1/α} and J\*/J₁ = (α/(α−1))^{1−1/α} to 1.9×10⁻⁸ across random currency, time and amplitude rescalings spanning **18 decades of currency**, at α = 1.3, 1.6, 2.0, 2.5, 2.9.
- **Something sharper that is not in the repo, and is currency-free:** by the envelope theorem each term's share of J\* equals the elasticity of J\* in that price, and by Euler the shares sum to 1. In CT12: sensing share = **(α−1)/α**, error share = **1/α**, so at the optimum **spend on looking ÷ cost of being wrong = α − 1**, in any currency, at any scale (α = 2 is the EOQ "equal costs"). Checked numerically at α = 1.5, 2, 2.5 (elasticity = share = closed form, sum = 1.000000). This is the right sense of "same energy across scales": a **scale-free accounting identity**, testable on a system's own books, needing no exchange rate. It does need w to price error, so it inherits G3, but the sensing-share part has the same status as N51.
- **What it does not give:** same numbers across systems. Equal groups give equal designs only for equal world shape, and S4 says covariance breaks when cost lines scale differently.

**Candidate 2: shadow prices (Lagrange multipliers) as the system's own marginal costs. PROVABLE NOW in the convex single-tracker class; conjecture beyond.**
- If a system faces its own budget instead of a given price, the stakes w are the reciprocal of the shadow price of that budget. Checked: minimizing error subject to read-cost rate ≤ B gives T = c/B, and the multiplier λ = −de\*/dB satisfies λ·w = 1.000000 with the w that makes the J-optimum equal c/B (α = 1.5, 2, 2.5). With two trackers and one budget the marginal error saved per currency unit equalizes (2.498146 for both) and that single number is the system's shadow price.
- Meaning: w, h, c need not be primitive prices. For a system with a binding resource constraint they are **that system's own multipliers**, and the Master Theorem's price ratios are ratios of multipliers. The survival price μ_s is already a multiplier of this kind. This also supplies the over-identification count the repo owes (rows 19): a system with a K-way budget and equalized margins gives K−1 testable equalities.
- **Conjecture, not proved:** that real organizations' internal prices (transfer prices, attention budgets) equal their multipliers. Needs convexity (duality can fail at fixed costs, S4) and a binding, optimally allocated budget.

**Candidate 3: Landauer / Still et al. as a floor with a per-scale inefficiency multiplier. PROVABLE as a bound; the multiplier is measured, not predicted.**
- J\* is nondecreasing in every price (envelope: ∂J\*/∂c = reads per unit time > 0). So any real price per nat λ ≥ kT gives **J\* ≥ the floor**. Writing λ = β·kT, symbolically: J\*(β) = σ√(2βkT·w), ratio to the floor √β at α = 2; for general α the ratio is **β^{(α−1)/α}** (checked, to 4 digits, β = 1, 10, 10⁶).
- The cost **shares at the optimum do not depend on β** (checked: 0.3333, 0.5, 0.6 for all β). Only the scales move: the read interval by β^{1/α}, J by β^{(α−1)/α}. So the gap to the floor changes the **size** of a system's cost, not the **shape** of its design trade-off. That is a clean statement of "physics is a floor, not a constraint, above the cell".
- β (= FRAMEWORK's β_phys) is one dimensionless number per system and the theory predicts nothing about it. Measuring it needs an exchange rate from the system's currency to joules, which is exactly what firms do not have at the margin.
- Limits already in the repo and re-confirmed: Still et al. apply to nonpredictive memory with no feedback; the floor can approach 0 for slow drift (E3); "kT per nat acquired or erased" in THEORY §3 is the Landauer/Sagawa–Ueda reading, narrower than Still's nonpredictive-memory statement.

**A single measurable exchange rate per system that makes the equation scale-free.** Not needed, and not generally available. Scale-freeness comes from homogeneity (candidate 1), which needs only a numeraire, not a conversion to joules. A conversion rate matters only if one wants the floor-gap β, and for money/attention systems it is not defined at the margin. The only exact cross-currency rate is S5 (Kelly): for multiplicative-growth systems, one nat of predictive information is worth at most one nat of log-growth, checked again (gain = mutual information to 8 digits on three random 4×3 joint laws). That removes w as a free parameter **only** for a cue priced in growth units, under proportional betting and fair odds.

### 2c. Verdict, in plain words

| Class | Statement |
|---|---|
| **Provable now** | The master equation is scale-free in the sense that matters: the design depends only on dimensionless ratios (Buckingham π + degree-1 homogeneity). At the optimum, cost shares equal price elasticities and sum to 1 (new, elementary): for one tracker, looking : being wrong = α − 1 in any currency. The Landauer floor bounds J from below at every scale, with inefficiency multiplier β^{(α−1)/α} on cost and shares unchanged. The parameters w, h, c are the system's own shadow prices when it has a binding budget. Kelly gives one exact currency-free rate in growth systems. |
| **Conjecture** | That real systems' internal prices equal their multipliers (needs convexity, a binding allocated budget). That the shape of the world (spectrum) is the only thing that differs across scales, so that equal groups mean equal design in practice. That the cost shares are testable and universal functions of the world's roughness in strongly selected systems (this is the equipartition-like prediction; **it has not been run and is not in the repo**). Extending the shares result beyond one tracker (layers, pooling) is not done. |
| **Overclaim (do not say)** | That firms, cities or people "pay in joules" or that one energy currency runs through every scale. That J is conserved or "the same energy" in any Noether sense. That physics fixes the prices above the cell (the gap to the floor is orders of magnitude and unmeasured; S4 says one fixed-unit component breaks covariance). That a universal constant or universal exponent follows (the exponents depend on (p, H) and the world's shape). That the law is proved. |

**Safe sentence to use:** "Written in each system's own units the equation is the same problem at every scale: only dimensionless ratios matter, physics sets a floor under the price of information, and the distance to that floor is one measured number per system." (Uses "law" nowhere; says nothing about joules for firms.)

**Worth building in:** the share identity ("at the optimum a tracker spends α − 1 on looking for every 1 it loses to being wrong") as a CT-numbered result with a test row. It is exactly the kind of currency-free, cross-scale prediction Chad is asking for, and it costs one paragraph. It needs independent review like everything else new.

Citations used above that are new to this audit: none. Kelly 1956, Donaldson-Matasci et al. 2010, Vinkler et al. 2016, Still et al. 2012, Barato et al. 2014, Landauer 1961 resolve on Crossref today (checked 19 Nov: titles and authors match); all are already in the repo's DOI files except Vinkler 2016, whose DOI 10.1088/1742-5468/2016/04/043403 I confirmed and which is **missing from `litmap/verify/VERIFIED_DOIS.txt` and `crossref.out`** (the repo cites it in GENERAL_THEOREM S5 without a DOI). Rivoire & Leibler's repo DOI is 10.1007/s10955-011-0166-2 (verified in the repo file; my guess 10.1007/s10955-011-0143-2 did not resolve, so do not use it).

---

## 3. Scope of an independent review of v2.1

Reviewer must be independent of the authoring bot family if at all possible; the repo itself says every theorem "has been refereed at most once, by the same bot family, and no human expert has read the theory."

**Must cover (new math and claims):**
1. **Master Theorem CT20** (THEORY B.9; `theory/MASTER_EQUATION.md` §1): (i) existence with compact rate set; (ii) the Topkis/Milgrom–Shannon argument, including that E_K is nonincreasing over **nested** classes and that the f\* statement needs error growing with age. Does "every world and every loss" survive the nesting assumption?
2. **Layers L1–L3 = CT21** (`theory/LAYERS.md` §2, `theory/layers_checks/`): spectral factorization, the claim "no pole–zero cancellation: degree exactly J", R\* = min_K (K−1)/(Δ₁−Δ_K), L3 (no finite exact design for non-rational spectra, and K\*→∞ requires E_K→E_∞), and the time-constant claim "each layer's time constant is 1/b_j, set by mode and noise".
3. **L4 = CL12** (geometric clocks at every α in (1,3)): strict convexity of ψ(Δ), Jensen, envelope step.
4. **Survival lemma CT22**: the Lundberg bound as a sufficient constraint, B_min, B_slack, KKT with the multiplier μ_s, monotonicity of the feasible set in B, and the claim that Theorem L's argmax does not depend on B (L3 of Lemma B9). Re-derive the numbers (0.486, 0.508, 0.267→0.316, μ_s = 0.0052).
5. **CT23 local regret and the exceptions**; the exact one-layer formula [(α−1)m^{−1/α} + m^{(α−1)/α}]/α − 1.
6. **Dynamics (N54, N55)**: the 2/(aδ²) record length (Monte Carlo 0.55/0.30/0.15), the curvature α − 1, and the unproved premise that spread is set by curvature.
7. **Dimensionless groups paragraph**: that the seven groups are complete for the parametric class, and the noise-share counter-check.
8. **The equation's terms (THEORY §3)**: whether A and L cover Results 4 and 8; the sense of κ·I_mem versus h·K (no theorem uses both); the one-currency premise; g = 0 consistency; whether "P(ruin) ≤ ε_r" and the Lundberg form are consistent in 𝓜_LG; the claim that CT7 is a floor and the √2 coefficient.
9. **The hypothesis sentence and §4 wording**: "law" appears only in the hypothesis; "sit near the minimum" is defined; the three tests that would make it a law; the "two kinds of wrong" claim that regret is second order **except** near cliffs.
10. **The checks:** run `theory/meq_checks/` (`meq_derive.py`, `meq_checks.py`, `meq_checks2.py`, `meq_roots.py`, `part2.py`, `phase.py`) and `theory/layers_checks/` at nice 19 and compare to the committed `.out` files; re-check `crossref.out` and add Vinkler 2016.
11. **Anything added from this audit**, if Chad approves it (section 6): the share identity, the temperature/survival corollary, the restored rule table.

**Files:** `THEORY.md` (§2–§5, §8, B.1 CT7, B.6 CT18, B.9, Appendix C); `theory/MASTER_EQUATION.md`; `theory/LAYERS.md`; `theory/GENERAL_THEOREM.md` §5–§6 (Lemma B9, Theorem S); `theory/meq_checks/*`; `theory/layers_checks/*`; `measurement/CLAIM_MAP_v2.md` rows CT20–CT23, CL12, CX2, N54–N56 (and that no existing row changed status); `reviews/master-equation_2026-11-19/*` (REVIEW, GAPS G4 G8, VERDICT, IMPLICATIONS); `tools/check_consistency.py`, `tools/test_meq_derive.py`; `README.md`.

**Out of scope for this review round** (say so to the reviewer): the field tests and prereg folders, REACH/COSMIC_WEB/WORMHOLES/TORUS, the Looper repo (must not be touched).

---

## 4. (a) The seven rules

**Sources compared.** The 12 Nov post (`history/2026-11-12_X_POST.md`, items 1–7); the v1.0 design-rule table (`git show cbe60a5:THEORY.md` §3, with prior art and "fails when"); the v2.0 table (`reference/THEORY_v2.0.md` §5, columns "Follows from" and "Fails when"). **The repo has no separate Looper "seven requirements" list.** The only seven-item list that descends from the memory/prediction/cost tradeoff is these seven rules; any separate Looper requirements list would live in the Looper repo, which I was told never to touch, so I did not look. If Chad means a different list, it is in Looper, not here.

**What v2.1 does with them.** THEORY §7 "Design" contains one parenthetical sentence: "The seven design rules of the 12 November post (act early; keep what pays and let the rest fade, recoverably; move a belief by the signal's reliability; keep prior versions until a correction proves out; act from the current model, not a copy; record whether each prediction was used; watch more as drift × stakes rises) are solutions of J in particular cases, each with the condition under which it fails (`reference/THEORY_v2.0.md` §5)." So all seven are **still stated** but only as a pointer to a frozen file. The "fails when" column and the per-rule derivation are not in the canonical text.

| # | Rule (12 Nov post) | Derived in v2.1? | Where | Still needed? |
|---|---|---|---|---|
| 1 | Return early; interrupt unasked iff stake × chance relevant + what the outcome teaches > cost of interrupting | **PARTLY.** The "late buys nothing" half is in J: "Lateness counts as error" (§3 w·E[ℓ]) and LAT-1/CT19. The interrupt inequality is a one-step comparison of J terms (stake × error saved vs read price c). **"What the outcome would teach" is not a J term**: J prices tracking, not the value of learning for redesign (N54's slowest layer is the nearest thing). | THEORY §3, CT19, CT10 (effort rises with stakes) | **Needed, as a stated corollary plus an honest flag** that the learning term lives outside J. Near-tautology (v2.0 said so). |
| 2 | Keep a fact while need × miss cost > upkeep that rises with drift; fade recoverably | **YES, theorem.** Hold or fade: CT9 (G2): "Some periodic schedule beats fading iff λ·c < Φ…"; freeze/hold/look-up band: CT11 (T8); first bit must pay: CT4. | THEORY §5 table rows "Freeze, hold or look up", "First bit must pay"; B.2 | **Subsumed** by J. Keep as a named corollary. |
| 3 | Move a belief by the signal's reliability | **YES in substance, not stated as a rule.** L1 (Kalman–Bucy filter of a first-order state is one exponential store) and "each layer's time constant is 1/b_j, set by its mode **and** the noise" make the gain a function of signal-to-noise. Known (Kalman 1960; Muth 1960). | THEORY B.9 CT21, §2 | **Subsumed.** The v1.0/v2.0 "fails when" (heavy-tailed noise, Cauchy) is no longer stated; CT21 is linear-Gaussian and says so. |
| 4 | Keep prior versions until a correction proves out | **NO.** Not derived; v1.0 and v2.0 both say "near-tautology (cheap frozen history)". In J terms it is a low-κ archive plus an asymmetric loss for a wrong overwrite; J as written has symmetric squared loss and no recoverability term. | Only the §7 parenthetical; practiced in this repo (`reference/`, `history/`) | **Still needed as an engineering rule**, not as a theorem. Label it "design heuristic, outside J" rather than leave it implied to be derived. |
| 5 | Act from the current model, not a copy: copy error grows with hops and drift since last check | **YES, theorem.** CT8 (G1): "a chain of copies with independent noise at each hop has risk nondecreasing in the number of hops"; staleness monotone; LAT-1/CT19 error ≥ q·ℓ^{α−1}. | THEORY B.2, B.7, §5 table "Reach" | **Subsumed.** Fails-when (non-Markov observed variables, seasonality) not in the main text. |
| 6 | Record whether each prediction was used, ignored or late; Hebbian/ant-trail reinforcement, "same mechanism at every level" | **NO.** v2.0 rated this "Weak (information has nonnegative value)" and "the mechanism does not follow from the budget". Hebb and ants appear nowhere in THEORY v2.1 or README (`rg`: no match); they survive in the frozen post, `litmap/` and `theory/REACH.md`/INTERNAL_MODEL. The nearest derived content is "who must be in charge" (CL-level J9 / THEORY §6 item 7), a different claim. | — | **Partly needed.** Recording outcomes is how the design layer gets w (G3, stakes measurement) and the world's law, so it is the input side of N54 and the revealed-cost tests. The Hebb/ant "same mechanism at every level" is a **hypothesis**, never derived; either state it as one, or drop it. |
| 7 | Watch more as drift × stakes rises; most where shocks are large relative to buffers; stop past a point when a cheaper fallback exists; (v2.0 fails-when: buffer sets survival effort, not the cost-optimal interval; Cho & Garcia-Molina) | **YES, theorem, and stronger.** Read rate ∝ (w·q/c)^{1/α} (CT12); effort rises with stakes (CT10); rise-then-fall with a fallback (Lemma B1, G3); band-widening cliff cited to Cho & Garcia-Molina 2003 (THEORY l.276). **The v2.0 caveat is now a theorem:** the buffer's role is the survival multiplier μ_s (CT22), which is 0 for B ≥ B_slack and rises toward B_min. | THEORY §5, §8 table row "Watching effort rises with drift, then collapses once a bounded fallback exists", Lemma B1, CT22 | **Subsumed, and improved.** |

**Net:** rules 2, 5, 7 are theorems of J (and 3 follows from L1); rule 1 half; rules 4 and 6 are not derived and v2.1 does not label them as such. Nothing was deleted dishonestly, but the canonical file now **claims** "solutions of J in particular cases" for all seven (the quoted sentence), and that is **true for 2, 3, 5, 7, half-true for 1, and not true for 4 and 6.** That sentence should be corrected (section 6, item R1).

---

## 5. (b) Temperature, the firm-volatility prediction, and stress

**What was in the 12 Nov post.** (i) "Temperature beyond molecules": the typical shock a part faces relative to the buffer it holds; Drăgulescu & Yakovenko (2000) analogy; "if shocks are independent, their accumulated spread grows with the square root of time"; measured in dollars or orders, not kelvin. (ii) Firm prediction: "where shocks are large relative to buffers, slow error-fixers fall apart faster than fast ones, with risk tracking shock size × √(time to fix) ÷ buffer, the form of Merton's distance to default… First test: open-source projects." (iii) "Stress strengthens a system up to a ceiling, and faster error correction raises the ceiling."

**What v2.1 has.**
- **The temperature identity survives, but only in the appendix.** THEORY B.6, CT18, "PROVED (in-model)": "the hazard is **ν = F(z)/τ with z = B/(σ√τ)**… ε_B = −ε_σ and ε_τ = ε_σ/2 − 1. Slow fixing raises the hazard iff ε_σ > 2, and at a fixed observed spread s = σ√τ, ε_τ = −1." Appendix A lists "z = B/(σ√τ) (temperature = 1/z)". **Not in §1–§9**: the word "temperature" appears only in the notation table, B.6's heading and CT18. The square-root-of-time spread is inside CT18's proof, not stated as an idea.
- **Drăgulescu & Yakovenko:** nowhere in the repo except the archived post. (It was an analogy, not a result.)
- **The wording "Merton's distance to default" is superseded** and should not return: B.6 Lemma B8 says per-window ruin is erfc(z/√2) = 2Φ̄(z), "Black & Cox's (1976) default probability at zero drift. Merton's (1974) terminal-default version is off by a factor of 2." (v1.0 §4: "Earlier wording that called this 'Merton's distance to default' is superseded.")
- **The firm-volatility prediction is not a prediction in v2.1.** It is CLAIM_MAP K4 ("Risk ∝ shock × √(time to fix) ÷ buffer; ε_τ = −1 | KILLED → **PROXY-FAIL** | All five τ tests fail MV2 to varying degrees (H11–H15); **out of scope for the structural core**"). THEORY §9 mentions it once: "The 12 November post's lead prediction got every sign right but failed on proxy in its τ-specific structure (K4)." The §8 predictions table has no τ row. Open-source first test = C3 (H15): "INCONCLUSIVE/MISS", τ = issue-close habit (fails MV2); the conditional reading (v2.49) is that C3 excludes only a deterministic exogenous reset clock at that proxy; sign held at banks, glucose, populations (DECISIVE, H11–H13), size failed, literal −1 kill rule fired in two cases, firms F1 inconclusive (H14).
- **Stress strengthens up to a ceiling:** CLAIM_MAP K7, status OPEN, "Unchanged". Nowhere in THEORY.

**Derivable from v2.1? Mostly yes. The survival lemma is the missing bridge (checked).**
- The ruin constraint P(ruin) ≤ ε_r in the diffusive-reset class is **erfc(z/√2) ≤ ε ⇔ z = B/(σ√τ) ≥ z_ε**, with z_ε = 2.5758, 3.2905, 4.8916 for ε = 10⁻², 10⁻³, 10⁻⁶ (`checks/scale_free_checks.out` §6). So **"risk ∝ shock × √(time to fix) ÷ buffer" is exactly the survival constraint** of the master equation in that class, and its multiplier μ_s prices it. The buffer B_min of CT22 is this threshold with the best fix speed. A Monte Carlo of the closed form (1,000 steps, 40,000 paths, continuity-corrected) gives 0.1047 against 0.1096; the 4% residual is discretization, and the closed form is textbook reflection. This is a **corollary**, not a new theorem.
- **"Faster correction raises the ceiling"** follows in-model: with B and ε fixed, the largest shock the unit can survive is σ_max = B/(z_ε√τ), so the ceiling scales as τ^{−1/2} (checked: ceiling × √τ constant). That is a derivable statement of the post's last clause.
- **"Stress strengthens"** is **not** implied. It needs an adaptation law (redesign responds to measured stress), which is the dynamics of (j): redesign is the slowest layer and runs on tens of that scale, so strengthening can only follow stress after about that delay and can only go up to the viability edge B_min, beyond which no design survives (CT22). As a hypothesis that is coherent with v2.1, but nothing proves "strengthens". Keep K7 as OPEN and say so.
- **Pooling and coarse-graining rules** (z′ = z√(N/(1+(N−1)ρ)) up to the ceiling z/√ρ; the weakest link heats, z′ ≈ √(z² − ln N); heterogeneous fix speeds mispredict by 1.4–2.4×; fix-mechanism tail classes e^{−z²/2}, e^{−z²}, e^{−√2z}) are in v1.0 §4 and `theory/GENERAL_THEOREM.md`; **CT18 in v2.1 keeps only the tail classes**, not the pooling rules.

**Dropped (baby with bathwater)?** The identity and its proof were kept; the **story that makes it a prediction** (temperature as a cross-scale index, the firm test, the ceiling) was cut from the main text on the ground that the field tests failed MV2. That is defensible for the **τ-measurement** tests, but with the survival lemma the **index is now a corollary of J**, so the framing "out of scope for the structural core" in K4/H15 is out of date. The right status: "derivable from the survival constraint; field tests so far fail validity gates; first valid test still needs a τ that is a measured fix time".

---

## 6. (c) Overall: is v2.1 strictly more powerful? What to restore

**More powerful (gains):** one objective that holds the old results as special cases (nine, derived by `meq_derive.py`); an in-model theorem with world-free monotone structure; the layer cap from the world's predictive degree and the exact R\*; a survival lemma that fixes a v2.0 misstatement of Theorem L and gives μ_s; local regret as the formal "re-measure, don't kill"; dimensionless groups and a phase diagram; testable N54–N56; a stated kill rule; coupled levels named as the open theorem (CX2).

**Lost or weakened (not strictly more powerful):**
1. The seven-rule table, with prior art and a **fails-when** column, is now a pointer to a frozen file, and the pointer sentence over-claims for rules 1, 4, 6.
2. The temperature / firm-volatility prediction and the stress-ceiling prediction are no longer in the predictions table, though the first is now a corollary of the survival constraint.
3. The pooling/coarse-graining cooling rules and the "hot regime" statements of CT18.
4. The ε-style kill rows about the fixed-spread sign (N3, ε_τ = −1) and the scope notes (a hit on sign at four scales with size failures) are in CLAIM_MAP only.
5. Scope limits in the §9 list (regime shifts N16, exploration/goals beyond tracking, indivisible reads, S4 crossovers).
6. Much of v1.4.29's "regime" tables (forgetting kernel, precision effort, number-of-stores exponents). These are frozen in `reference/` and not "lost", but the main text no longer states any of them. I do not recommend restoring them; they are known and, per THEORY, "All KNOWN. GTAO does not claim any of it".

**Recommend restoring exactly this (each is a small, reversible edit; all need Chad's go, and anything new needs independent review before it counts):**

- **R1. A short "Design rules as consequences" table in THEORY §7** (replace the one parenthetical sentence): seven rows, columns *Rule / Status in v2.1 (theorem of J: CT-number; known; or heuristic outside J) / Fails when*. Statuses from section 4: 2 → CT9, CT11, CT4; 3 → CT21 (L1), known; 5 → CT8, CT19; 7 → CT10, CT12, Lemma B1, CT22; 1 → half (lateness in J; learning value outside); 4 → heuristic; 6 → hypothesis (not derived). Correct the sentence that currently says all seven are "solutions of J in particular cases".
- **R2. Restore the temperature as a corollary, one paragraph, in §5 after the survival bullet (iv):** "In the diffusive-reset class the ruin constraint is z = B/(σ√τ) ≥ z_ε (CT18, Lemma B8): the buffer needed grows as shock × √(time to fix); faster correction raises the stress a unit can survive as τ^{−1/2}." Credit Black & Cox 1976 (not Merton), the inventory safety factor, and (as analogy only) Drăgulescu & Yakovenko 2000. Say plainly the analogy gives the √time spread, nothing physical.
- **R3. Put the firm-volatility prediction back in the §8 table** as: "Failure risk at fixed shock and buffer rises with time to fix when ε_σ > 2; at fixed observed spread it falls with slower fixing (ε_τ = −1). Status: survival-constraint corollary; five field tests failed or were inconclusive on proxy (H11–H15); first valid test needs a measured fix time (C3's τ was an issue-close habit)." Update K4/H15 wording in CLAIM_MAP from "out of scope for the structural core".
- **R4. Add the stress ceiling as an explicitly open hypothesis, K7,** with the in-model piece (σ_max ∝ τ^{−1/2}) and the unproved piece (adaptation).
- **R5. Add the share identity** (looking : being wrong = α − 1 at the optimum; shares equal elasticities and sum to 1) as a new numbered result with a test row, plus the one-sentence "same equation at every scale" paragraph from section 2c. Both elementary and checked; both new to the repo as far as I could find, not independently reviewed.
- **R6. Fix the §9 scope list** to carry the four missing limits (regime shifts, exploration, indivisible reads, non-additive costs).
- **R7. Add J_coupling and idea (g)** (predictive-state statement and the G4 switching-world first test) as clearly labelled conjectures.
- **R8. State the over-identification count** for each revealed-cost test (section 2b, candidate 2 gives the count K−1 for a K-way allocation).

**Do not restore:** the old "bill" language, the pre-v2.0 forgetting-kernel and store-count tables, any "Merton distance to default" wording, any of the "firms ~10¹² above kT" figures.

---

## 7. Other defects found on main (small, mechanical)

1. **Stale status text after the merge.** `STATUS.md`: "on the draft branch `v2.1-master-equation`, for Chad's review before merge" (it is merged); `measurement/CLAIM_MAP_v2.md` v2.50 note: "draft PR from branch `v2.1-master-equation`… before merge"; README and THEORY header still say "draft". Update or confirm intended.
2. `theory/MASTER_EQUATION.md` has an **empty heading** "## 2. Worked engineering example (hypothetical numbers)" immediately followed by "## 3. Is it useful? …" and then a second "## 3. Revealed costs…"; the lettered sections (c), (d), (h)–(k) keep REVIEW's labels and the phrase "**The examples in the brief are not dimensionless.**", and §3(c) retains REVIEW's to-do "the repo should state the over-identification count". Reads as a pasted review, not a polished companion.
3. `theory/MATH_ATTACK.md` §1.2 says firms "are ~10¹² above" the kT floor; I found no derivation or source, and FRAMEWORK says only "astronomically above 1"; THEORY §9 says "far more". Do not use 10¹² publicly.
4. THEORY §3 "at least kT per nat acquired or erased" is the Landauer / Sagawa–Ueda form; Still et al. 2012 bound only **nonpredictive** memory (kT·(I_mem − I_pred)); SCALE_ENDS E3 says it correctly. Consider one clause in THEORY §3.
5. Vinkler, Permuter & Merhav 2016 is cited in GENERAL_THEOREM S5 without a DOI and is absent from `crossref.out` / `VERIFIED_DOIS.txt`. DOI 10.1088/1742-5468/2016/04/043403 resolves on Crossref to the right paper (checked now).
6. `reviews/master-equation_2026-11-19/REVIEW.md` still carries the superseded verdict words ("modest synthesis", "weak for firms", "No" to applying to any system) in its bottom line; the banner flags this. Fine as a dated record; just never quote it as current.

## 8. Reproduce

```
cd /workspace/gtao-audit && git rev-parse HEAD        # c55e960…
nice -n 19 python3 tools/check_consistency.py          # RESULT: PASS
nice -n 19 python3 -m pytest -q tools/test_meq_derive.py   # 1 passed
nice -n 19 python3 checks/scale_free_checks.py         # section 2 and 5 numbers
```
