# Hostile prior-art review of GTAO ("A Theory of Adaptive Organization")

Reviewer brief: an independent referee covering information economics and team theory, organization science, rational inattention (RI), the theoretical biology of collective behavior, and control and estimation.
Inputs: `FORMAL/THEOREMS.md`, `FORMAL/EXTENSIONS.md`, `ARCH_EQUATION.md`, `CORE_AUDIT.md`, `VIGIL/PRIOR_ART.md`, all read in full.
Written 15 Nov 2026, about 02:40 ET. Private only. Nothing was posted, sent or committed.

## 0. Source-status legend (every citation below carries one of these markers)

- **[FULL]**: I read the relevant sections of the actual text this session. Copies are in `src/`.
- **[OCR]**: Marschak & Radner 1972. The Cowles PDF is a scan, so I OCR'd it (`src/mr_ocr.txt`, 355 pages, rapidocr). I quote the OCR. Symbols in the equations are garbled, but the prose is clean.
- **[ABS]**: abstract only (Europe PMC, IDEAS/RePEc, or the publisher's page).
- **[SEC]**: content known only through a secondary source, which is named.
- **[BIB]**: bibliographic details verified, content not verified.
- **[UNVERIFIED]**: a pointer from my own memory. It is listed so someone can check it, and is **not** relied on for any verdict.

Verdict scale:
- **KNOWN**: a published prior statement of the same result, or of the same result in substance.
- **PARTIAL**: the mechanism or a special case is published, but GTAO's form, generality or sign is not found.
- **APPARENTLY NEW**: nothing found after a targeted search. Unless noted otherwise, every new item is *elementary*: a few lines of algebra on known models.

---

## 1. Bottom line (one paragraph)

GTAO's core is a **recombination of known machinery**:
- team theory's value of pooled information (Marschak–Radner; Arrow's informational economies of scale as formalized by Van Zandt & Radner 2001);
- EOQ- and inattentiveness-type square-root sampling laws (Harris; Marschak–Radner ch. 7 §5; Keller 1974; Sheridan 1970; Reis 2006);
- the information-market onset of Veldkamp & Wolfers 2007;
- Topkis-style complementarity (Milgrom & Roberts 1990);
- hold-versus-fetch caching economics (Gray & Putzolu; Wolman et al. 1999; Cho & Garcia-Molina 2003);
- strategy phase diagrams in theoretical biology (Rogers 1988; Kussell & Leibler 2005; Mayer et al. 2016).

What survives as apparently new is a set of **elementary corollaries**, mostly of the form "the exponent is set by the sensing technology's (a, b) elasticities":
- the onset exponent law −(1−b)/(1−a) and its upkeep dichotomy;
- the bundled-loss theorem T4;
- the vigilance-at-birth bounds, with the a ≥ b criterion and price invariance;
- the ordering threshold κ\* = 1/|e_g| of T7;
- the closed-form hold band and its N² widening;
- the measurement programme: measure (a, b) on lone units, then predict collective exponents across substrates.

None of these is deep. Together they make a coherent, checkable *synthesis*, not a new theory.

Four claims made in the project's own files are **wrong**:
1. CORE_AUDIT says "team theory is static". It is not (M&R ch. 7; Aoki 1986; Van Zandt & Radner 2001).
2. FORMAL cites Alonso–Dessein–Matouschek 2008 for "centralize common, decentralize local". That citation is inaccurate.
3. CORE_AUDIT says "nobody has stated them across substrates". At the qualitative level, Beer's Viable System Model makes exactly such a cross-substrate, recursive claim.
4. The title collides with **Dessein & Santos 2006, "Adaptive Organizations," JPE**.

---

## 2. Per-result verdicts

### Lemma 1 — sensing classes (R1 periodic EOQ; R2 entropy-priced; A_θ precision-priced averaging) and the power class P(a, b)

**Verdict: (i), (ii), (vii) and (viii) KNOWN. The (a, b) classification is PARTIAL (a new organizing device built on known formulas).**

- **(i) The R1 square-root law for periodic complete reads in a *team* is in Marschak & Radner 1972, ch. 7 §5, "Periodic recovery of delayed complete information"** [OCR, pp. 259–260].
  - Setting: a Brownian environment, quadratic team payoff, and a fixed cost c each time the team obtains new complete information.
  - Eq. (5.13): optimal cycle b = [2c/L₁(0)]^{1/2}.
  - Their words: "the optimal frequency of recovery of delayed complete information is proportional to the square root of the difference in value between complete and incomplete information, and inversely proportional to the square root of the cost."
  - This is GTAO's R1 tracker with stakes entering as the loss-rate slope L₁(0). It is the closest single prior statement of Lemma 1(i) in an organizational setting. **Credit owed: M&R 1972 ch. 7 §5, explicitly.**
- **The square-root law in observation-cost and inattentiveness models:**
  - Reis 2006, RES 73:793, "Inattentive producers" [FULL]: Prop. 4, d\* = √(2K/G_t); Prop. 5, d\* ≈ √(4κ/(σ²θ(θ−1))).
  - Alvarez, Lippi & Paciello 2011, QJE, τ\* = √(2θ/(Bσ²)) [SEC: search summary; the NBER PDF did not download].
- **Inspection and supervision sampling:**
  - Keller 1974, "Optimum checking schedules for systems subject to random failure", Management Science 21(3):256–260, doi 10.1287/mnsc.21.3.256 [ABS]. It uses a continuous checking density n(t) and a calculus of variations. The known explicit result n(t) ∝ √(c₂f(t)/c₁) is [SEC: search summary].
  - Sheridan 1970, "On how often the supervisor should sample", IEEE Trans. Systems Science & Cybernetics 6(2):140–145 [ABS via NTRS]: "supervisor/monitor sampling frequency maximizing payoff function, using Bayesian preposterior information analysis."
- **(ii) Kalman–Bucy, P = √(qr), is textbook. Duncan 1970 (SIAM J Appl Math 19:215) [ABS]: mutual information = ½ × the time-integrated causal MMSE.** This underlies R2 pricing. Entropy-priced attention: Sims 2003 (not re-read; MMW 2023 [FULL, ECB WP 2570 version] surveys it).
- **Class-A scaling in cells is already published.** Mora & Nemenman 2019, PRL 123:198101 [ABS] derive δc/c ∼ (D a c τ)^{−1/4} for sensing a *changing* concentration. This is an averaging tracker of a drifting target with a −¼ exponent. It is the biological instance of A₁, and EXTENSIONS §3.1 (C1–C3) **must cite it**. The static limit is Berg & Purcell 1977 [ABS, verified; see §4].
- **(vii) Scope caveat (PARTIAL conflict).** "Periodic reading is optimal" holds only if the tracker sees nothing between reads. Åström & Bernhardsson 2002 (IEEE CDC, "Comparison of Riemann and Lebesgue sampling") [SEC: summary] show that event-triggered sampling beats periodic sampling for the same variance, with several-fold fewer samples, when the state is observable continuously and only *acting or transmitting* is costly. Any substrate where members see the environment and only communication is priced (most firms, many collectives) falls outside L1(vii). THEOREMS should state this explicitly.
- **What is new:** stacking the three technologies on one (a, b) chart and noting that drift-invariant pricing forces a = b. Elementary; no prior found.

### T1 — pooling onset N\* = [ρ^b/((1+ρ)^b−1)]^{1/(1−a)}, e_g → −(1−b)/(1−a), upkeep dichotomy, volatility and stakes effects

**Verdict: the ρ^{−1} onset with large upkeep is KNOWN. The general exponent law and closed form are APPARENTLY NEW (elementary). T1.7 (volatility promotes levels) is PARTIAL and conflicts with the delay literature.**

- **Veldkamp & Wolfers 2007, "Aggregate shocks or aggregate information?", JME (NBER w12557)** [FULL], Prop. 2. Buy the aggregate signal iff log(Var z / Var(z|s₀)) − 2ρχ/λ ≥ 0, where λ is the number of buyers. This is a static onset with cost per buyer ∝ 1/λ, i.e. the −1 law in substance (already credited in THEOREMS).
- **Arrow's informational economies of scale, formalized dynamically.** Van Zandt & Radner 2001, "Real-time decentralized information processing and returns to scale", Economic Theory 17:545–575 [FULL].
  - Processes X_it = Y_t + Z_it: a common AR(1) component plus idiosyncratic AR(1) components.
  - They call amortizing a fixed information cost over more decisions "the Arrow effect" (citing Arrow 1974).
  - **Theorem 3:** increasing returns hold when forecasting a common process is a public good.
  - **Theorem 1:** with quadratic loss and common components, firm size is bounded.

  **This is the closest *dynamic* precedent for T1 and T3.** It is not cited anywhere in GTAO's files except my notes. **Credit owed.**
- **Wilson 1975**, "Informational economies of scale", Bell J Econ 6(1):184–195 [ABS; also verified earlier in POOLING_REVIEW]. Arrow & Radner 1979, Econometrica 47(2):361–385 [ABS].
- **Team size and returns to scale in information value.** M&R 1972 ch. 6 §5 and §14, "Interaction, team size, returns to scale" [OCR, pp. 228–230].
  - The value of complete information is analysed as a function of n under constant individual interaction and Selten's constant total interaction n(n−1)q = k.
  - They state (ch. 6) that costs are not explicitly modelled. The ch. 7 §5 fixed cost c is the exception.
  - So there is no cost-thresholded onset in N there.
- **Prior dynamic drift → structure work in the other direction (relevant to T1.7 and F3):**
  - **Aoki 1986**, "Horizontal vs. vertical information structure of the firm", AER 76(5):971–983 [FULL]. An OU environment with forgetting rate h and hierarchical delay Δ. Prop. 1's comparison condition is e^{−2hΔ}/(1+γ) < θβ^{−θ}v(θ, β). A faster-changing environment *penalizes* the vertical (hierarchical) structure because of delay.
  - **Meagher, Orbay & Van Zandt 2001**, "Hierarchy size and environmental uncertainty", CEPR DP 2839 [ABS only; the full text did not download]. Costly managers give an inverted U of staff size against stability.
  - **Radner 1993**, "The organization of decentralized information processing", Econometrica 61(5):1109–1146 [FULL]. Delay grows ∝ log N in efficient networks.
  - GTAO's 𝓜 has **no processing delay**. T1.7's "volatility promotes levels when h > 0" therefore holds *conditional on zero delay*. The literature that does model delay predicts the opposite tendency.
  - **Credit and scope owed:** cite Aoki 1986, MOVZ 2001 and Radner 1993, and state that T1.7 and F3 reverse once delay cost is added.
- **Empirical counter-evidence on F3's direction.** Aghion, Bloom, Lucking, Sadun & Van Reenen, "Turbulence, firm decentralization and growth in bad times", AEJ: Applied 2021 (NBER w23354) [FULL]. Decentralized firms did relatively better in the Great Recession, explained by a "localist" value of local information under turbulence. F3 differs (fixed ρ, upkeep, tracking not authority), but a referee will cite this paper against F3.
- **New:** the class-dependent exponent −(1−b)/(1−a), the exact finite-ρ closed form, the upkeep dichotomy (exponent −(1−b)/(1−a) when h = 0 versus −1 or −γ at large upkeep), and the mixed-technology rule. Each is a two-line calculation, and none was found.

### T2 — broadcast break (onset becomes a ρ threshold, ρ_b = 4t/(1−t)²)

**Verdict: PARTIAL. The mechanism (communication cost limits pooling and hierarchy) is KNOWN. The closed form is apparently new.**

- Garicano 2000, "Hierarchies and the organization of knowledge in production", JPE 108(5):874–904 [ABS, IDEAS]. Knowledge hierarchies form "when matching problems with those who know how to solve them is costly". The quantitative content is [SEC].
- Bolton & Dewatripont 1994, "The firm as a communication network", QJE 109(4):809–839 [ABS; the PDF has no text layer].
- Radner 1993 [FULL]: communication and processing costs limit the gain from aggregation.
- In collective sensing: Fancher & Mugler 2017, "Fundamental limits to collective concentration sensing in cell populations", PRL 118:078101 [ABS, verified]. Communication improves precision, and a trade-off between communication strength and signal cross-correlation sets an optimal cell spacing. This is a physical analogue of "the cost of communicating limits pooling".
- **Credit owed:** Garicano 2000 and Bolton & Dewatripont 1994 in the statement of T2, not only in its status line. The ρ-threshold form appears to be GTAO's own.

### T3 — shared and private drift have opposite effects at every ρ

**Verdict: the qualitative content is KNOWN. The signed comparative static at every ρ in 𝓜 is PARTIAL (apparently new as an exact statement, elementary).**

- **Acemoglu, Aghion, Lelarge, Van Reenen & Zilibotti 2007**, "Technology, information and the decentralization of the firm", QJE 122(4):1759–1799 [ABS, CEP DP 722]. More public information (more firms sharing the technology) favors centralization; more heterogeneity in the environment favors decentralization. This is T3's sign pattern in an agency setting with empirical support.
- **Van Zandt & Radner 2001** [FULL]: the common component makes forecasting a public good (increasing returns), while idiosyncratic components do not. This is the same opposition in a dynamic team.
- **Veldkamp & Wolfers 2007** [FULL]: agents buy aggregate (shared) information, not idiosyncratic information.
- **Hayek 1945**, "The use of knowledge in society", AER 35(4):519–530 [BIB verified]: knowledge of "particular circumstances of time and place" belongs at the periphery.
- **Geanakoplos & Milgrom 1991** [FULL in CORE_AUDIT]: more uncertainty about individual shops gives smaller spans.
- **Within RI:** Maćkowiak & Wiederholt 2009 (as surveyed in MMW 2023 [FULL], around line 1274 of `src/mmw2023.txt`) split attention between idiosyncratic and aggregate conditions.
- **Correction:** THEOREMS and EXTENSIONS F2 cite Alonso, Dessein & Matouschek 2008 for this. That is inaccurate (see §4). Replace it with AALVZ 2007, Van Zandt & Radner 2001 and Hayek 1945.

### T4 — bundled loss: the technology, not the loss function, sets the exponent

**Verdict: APPARENTLY NEW as an application. The math core is KNOWN.**

- The proof relies on Gaussian smoothing of a non-smooth loss. The variance derivative of E f(X) for Gaussian X is Price's theorem: Price 1958, "A useful theorem for nonlinear devices having Gaussian inputs", IRE Trans. Inf. Theory [UNVERIFIED volume and pages; the Bonnet/Price identity itself is textbook].
- **Closest contrasting prior:** Van Zandt & Radner 2001 [FULL] show that conclusions about returns to scale depend on the loss (quadratic versus "scalable"). T4 claims that the onset *exponent* does not depend on the loss for bundled decisions. These are different objects, so there is no contradiction, but the authors should discuss the contrast.
- Nothing found stating T4. **Credit:** Price/Bonnet for the tool.

### T5 — vigilance at birth: V > 1 iff a ≥ b; V = 2 at γ = ½; price-invariant; V ∝ ρ^{−θ} in A_θ; V grows as N^a

**Verdict: T5.5 (V grows as N^a, i.e. √N in R1) is KNOWN in substance. The ratio at onset, the a ≥ b criterion and price invariance are APPARENTLY NEW (elementary).**

- **M&R 1972 ch. 7 §5, eq. 5.13** [OCR]: the optimal reading frequency ∝ √(value difference / cost). When a pooled tracker's value difference scales with the number of members it serves (L₁ ∝ N for independent stakes), the frequency ∝ √N. That is T5.5 for R1.
- The same √(aggregate demand) logic underlies pooled ordering in multi-location EOQ: Eppen 1979, Management Science 25(5):498–501 [ABS] (pooling savings depend on correlation); Roundy 1985, Management Science 31(11):1416–1430 [ABS] (power-of-two nested intervals).
- **Qualitative "the tracker at the top watches the environment":**
  - Mintzberg's monitor and liaison roles (VIGIL [FULL]).
  - **Beer's VSM** (Beer, "What is cybernetics?", 2002 text [FULL]; Beer 1984, "The Viable System Model: its provenance, development, methodology and pathology", J Opl Res Soc 35(1):7–25 [UNVERIFIED citation details]). System 4 ("outside and then") is coupled to its environment *at every level of recursion*.
  - Field evidence is mixed: Hambrick 1981 found a null among executives (VIGIL [ABS]).
- **New:** the ≈2 ratio at onset, the a ≥ b criterion, independence from the price p_g/p, and ρ^{−θ} in A_θ. No prior found. The PIAAC test (VIGIL) is weak support only.

### T6 — levels are complements: submodular J, inclusion, lattice, accretion

**Verdict: PARTIAL. The tool is KNOWN; the application is assembly; the lookup counterexample is apparently new.**

- Topkis 1978, "Minimizing a submodular function on a lattice", Operations Research 26(2):305–321 [ABS].
- Milgrom & Roberts 1990, "The economics of modern manufacturing", AER 80(3):511–528 [ABS]: complementarities in organizational design and adoption in coherent clusters.
- Crémer 1980, "A partial theory of the optimal organization of a bureau", Bell J Econ 11(2):683–693 [ABS]: grouping functions into units to minimize the cost of coordinating them.
- Contrast: sensor-placement information gain is usually *sub*modular (diminishing returns), e.g. Krause & Guestrin [UNVERIFIED]. GTAO's result that *levels* are complements in the cost (supermodular saving) is the opposite structure, and that is worth stating.
- **Credit owed:** Topkis 1978 and Milgrom & Roberts 1990 in the theorem statement; Crémer 1980 for the grouping problem.

### T7 — which scales of a nested hierarchy carry a level: top-down iff κ < κ\* = 1/|e_g|

**Verdict: APPARENTLY NEW (elementary).**

- **Neighbours:**
  - Garicano 2000 [ABS] orders *problems* by frequency: common problems are handled at the bottom, rare ones at the top. That is a different primitive.
  - Simon 1962, "The architecture of complexity", Proc. Am. Phil. Soc. 106(6):467–482 [BIB]: near-decomposability.
  - Willsky 2002, "Multiresolution Markov models for signal and image processing", Proc. IEEE 90(8):1396–1458 [FULL]: multiscale tree estimators and the learning of tree structure for model fidelity, but no cost-thresholded choice of which scales to pay for.
  - Williamson 1967 and Beckmann 1977 (§4): hierarchy depth grows with size through span limits.
- No statement found of a decay-exponent threshold that decides between top-down and bottom-up level formation.

### P7.1 — depth avalanches (numerical)

**Verdict: PARTIAL in kind.** Discontinuous joint adoption is the generic signature of supermodular optimization, as Milgrom & Roberts 1990 [ABS] stress ("coherent" clusters change together). The specific avalanche in depth is apparently new and numerical only.

### T8 — freeze / hold / look up; the fallback cliff; band iff μuH_l > 2c + hH_l; N² widening for a shared store

**Verdict: the cliff and hold-versus-lookup in substance are KNOWN. The band's closed form and the N² widening are PARTIAL (qualitatively known for shared caches; the closed forms are apparently new).**

- **Hold versus fetch at a cost break-even:** Gray & Putzolu 1987, the "five-minute rule" (SIGMOD) [BIB/SEC]. It has no drift term.
- **Refresh against a change rate:** Cho & Garcia-Molina 2003, ACM TODS 28(4) [ABS/SEC]. GTAO already credits this for the Poisson cliff.
- **Shared caches against population size:** Wolman, Voelker, Sharma, Cardwell, Karlin & Levy 1999, "On the scale and performance of cooperative Web proxy caching", SOSP [FULL]. Cooperative hit rate rises with the population served and saturates. Caching pays when the request rate dominates the document change rate. This is the qualitative shared-store band in N. **Credit owed** for T8.4/T8.6 and AI1/AI2.
- **Cognition:**
  - Ballard, Hayhoe & Pelz 1995, J Cogn Neurosci 7(1):66–80 [ABS]: people re-fixate (look up) rather than memorize when looking is cheap.
  - Gray & Fu 2004, Cognitive Science 28:359–382 [ABS]: soft constraints trade memory against perceptual access.
  - Sparrow, Liu & Wegner 2011, Science 333:776–778 [ABS, verified]: people remember where to find information rather than the information itself.
  - Risko & Gilbert 2016, TiCS 20:676 [ABS]. Gilbert et al. 2020, JEP:General 149:501 [ABS].
- **Biology phase diagrams by change rate:**
  - **Rogers 1988**, "Does biology constrain culture?", American Anthropologist 90:819–831 [FULL]: social learning is favored when "sufficiently cheap and environmental change sufficiently slow".
  - **Kussell & Leibler 2005**, Science 309:2075 [ABS]: sensing versus stochastic switching by environmental change rate.
  - **Mayer, Mora, Rivoire & Walczak 2016**, "Diversity of immune strategies explained by adaptation to pathogen statistics", PNAS 113(31):8630–8635 [ABS]: immune strategy modes (innate, CRISPR-like, adaptive, etc.) arise as phases set by pathogen frequency and timescale.

  **I1 (freeze/hold/lookup by antigenic drift) is a re-labelling of the Mayer et al. 2016 phase-diagram programme and must cite it.** Related: Mayer et al. 2019 PNAS (memory updating); Schnaack & Nourmohammad 2021 eLife (memory against evolving pathogens) [ABS/SEC].
- **New:** the explicit band condition, the exponent N^{(1−a)/b} (N² in R1 quadratic) for how much faster a shared store survives drift, and the power-class generalization.

### P9 — clock ceiling 1 − K^{−(1−γ)}

**Verdict: KNOWN** (THEOREMS says so). Background: Roundy 1985 [ABS] and joint-replenishment EOQ. The specific ceiling is an elementary EOQ identity. I found no exact citation, so "KNOWN" means known in kind.

### P10 — selection resolution ε ⇒ no level for ρ ≲ ε/b

**Verdict: PARTIAL (new use of a known idea).** Selection cannot resolve small fitness differences: the drift-barrier hypothesis, e.g. Sung, Ackerman, Miller, Doak & Lynch 2012, PNAS 109:18488 [ABS, verified]. In economics, near-rational and menu-cost-style tolerance bands make the same point (Akerlof–Yellen-type arguments [UNVERIFIED]). The ε/b floor itself is new and trivial.

### P11 — readability changes Π\* (4 → ≈7.3), not e_g (numerical)

**Verdict: APPARENTLY NEW, and minor.** No prior found. It is a robustness note rather than a result.

### E1–E5 (limits)

- **E1 depth ∝ log N:** KNOWN in pure span-limited hierarchies (Williamson 1967; Beckmann 1977; see §4). The condition κ < κ\* is new (from T7).
- **E1 bounded fractional saving:** KNOWN in kind. Van Zandt & Radner 2001's bounded firm size with common components is the dynamic analogue.
- **E2–E3:** algebraic limits of T1. N\* ∝ λ^{−b} under upkeep is new and elementary. The calm-world freeze is the "frozen memory" corner of T8 (Rogers 1988; Mayer et al. 2016).
- **E4 dissolution order as lookup cost u → 0, and "tracking moves into a few large shared stores":**
  - Bloom, Garicano, Sadun & Van Reenen 2014, "The distinct effects of information technology and communication technology on firm organization", Management Science 60(12):2859–2885 [FULL]: "better information access pushes decisions down … better communication pushes decisions up."
  - Garicano 2000 [ABS] for the hierarchy flattening as acquisition cost falls.
  - Wolman et al. 1999 [FULL] for concentration in large shared caches.
  - **Verdict: PARTIAL.** The specific order (the pooled level dissolves before private holding under whole-item lookup) is apparently new, and the qualitative claims are known.
- **E5:** AI3 and "cheap central sensing centralizes" (T1.6) match Bloom et al. 2014 [FULL] and the communication-cost side of Garicano 2000. **PARTIAL: known in substance.**

### ARCH_EQUATION — keep source m iff q_m‖B_m‖²_λ − φ_class(W_m, q_m) > h; the eigen and factor reading

**Verdict: PARTIAL.**
- Factor structures with a common factor plus idiosyncratic terms driving an endogenous hierarchy: Vayanos 2003, "The decentralization of information processing in the presence of interactions", RES 70(3):667–695 [FULL]. His r_n = µ + λ_n η + ε_n is static, with no onset.
- Grouping by interaction structure: Crémer 1980 [ABS]. Value of common observations with covariance terms: M&R ch. 6 [OCR].
- The cost-thresholded, shadow-price-weighted loading mass rule is new as written and elementary.

### Substrate implications (EXTENSIONS §3)

| Item | Verdict | Closest prior; credit owed |
|---|---|---|
| C1–C3 (cells: A₁ class, e_g = −2, shared sensors more vigilant) | PARTIAL | Berg & Purcell 1977 [ABS]; Kaizu et al. 2014 Biophys J 106:976 [ABS]; **Mora & Nemenman 2019 PRL 123:198101 [ABS] (changing-environment class-A scaling)**; Govern & ten Wolde 2014 PNAS [ABS] (resource classes of sensing cost); Fancher & Mugler 2017 [ABS]. The collective-onset mapping is new. |
| I1 immune freeze/hold/lookup | KNOWN in kind | **Mayer et al. 2016 PNAS 113:8630 [ABS]**; Kussell & Leibler 2005 [ABS]; Schnaack & Nourmohammad 2021 [ABS]. The "cliff" (bimodality) sharpening is new. |
| A1/A3 ant trail onset ∝ 1/ρ, opposite effects | PARTIAL, with counter-evidence | Beckers, Goss, Deneubourg & Pasteels 1989, Psyche 96:239 [FULL]: in 98 species, recruitment and trail communication rise with colony size. Beekman, Sumpter & Ratnieks 2001 PNAS 98:9703 [ABS, verified]: small colonies forage in a disorganized way, and larger colonies switch to pheromone trails through a first-order transition with hysteresis when food is hard to find. This is a published *threshold colony size* for a shared store. The figure of about 600 ants is [SEC]. **Credit owed for A1.** **Counter:** Dornhaus, Klügl, Oechslein, Puppe & Chittka 2006, Behav Ecol 17:336 [FULL]: the benefit of recruitment depends on patch quality, density and variability, and "colony size … had no significant effect". |
| P1 RI monitor ≈2× | PARTIAL | RI organizational application: Dessein, Galeotti & Santos 2016 AER (MMW 2023 [FULL] §3.3 cites it as the RI-in-organizations work). DGS is about attention allocation across tasks, not a shared monitor's ratio. The ≈2 ratio is new. |
| P2 offloading by drift | KNOWN qualitatively | Sparrow et al. 2011 [ABS]; Risko & Gilbert 2016 [ABS]; Ballard et al. 1995 [ABS]. The q_c ∝ u^{1/b} law is new. |
| F1 central tracking at N\* ≈ Π\*/ρ | KNOWN in substance | Veldkamp & Wolfers 2007 [FULL]; Van Zandt & Radner 2001 [FULL]; Geanakoplos & Milgrom 1991 (static onset of a manager). |
| F2 | KNOWN qualitatively | AALVZ 2007 [ABS]; VZR 2001 [FULL]; Hayek 1945. **Not ADM 2008.** |
| F3 volatility promotes central tracking | PARTIAL; conflicts with the delay theory and with evidence | Aoki 1986 [FULL]; MOVZ 2001 [ABS]; Aghion et al. 2021 [FULL]; Burns & Stalker (contingency theory; not re-read). |
| F4 vigilance ×2, growing as √N | see T5 | M&R ch. 7 §5 [OCR]; Beer VSM [FULL]; Mintzberg [FULL in VIGIL]. |
| F5 / AI2 / AI3 | PARTIAL | Bloom et al. 2014 [FULL]; Garicano 2000 [ABS]; Wolman et al. 1999 [FULL]. |
| Y2 geometric tiers | KNOWN in kind | Roundy 1985 power-of-two policies [ABS]. Jaques's geometric "time-span" strata (about 3 mo, 1, 2, 5, 10, 20 yr), Jaques 1990, HBR 68(1):127–133, "In praise of hierarchy" [SEC]. |
| Y3 depth ∝ log N | KNOWN in kind | Williamson 1967; Beckmann 1977 (§4). |
| Universality across substrates (CORE_AUDIT "nobody has stated them across substrates") | **Qualitatively KNOWN** | Beer's VSM recursion theorem ("any viable system contains, and is contained in, a viable system") is applied explicitly from cells and organisms to firms and states [FULL, Beer 2002 text]. Also: Galbraith 1974, "Organization design: an information processing view", Interfaces 4(3):28–36 [ABS; scanned PDF]; Tushman & Nadler 1978, AMR 3(3):613–624 [ABS]; Simon 1962 [BIB]. Modularity from environment structure in evolved networks: Kashtan & Alon 2005 PNAS 102:13773 [ABS]; Kashtan, Noor & Alon 2007 PNAS [ABS]; Clune, Mouret & Lipson 2013 Proc R Soc B [ABS]; Watson et al. 2016 Evol Biol [ABS]. **Only the quantitative cross-substrate claim (the same (a, b)-exponent law in each substrate) is apparently new.** |
| "Fractal vigilance" (a tracker at every level watches its own sub-environment) | KNOWN qualitatively | Beer VSM System 4 at every recursion [FULL]. |
| DP1 (measure the class on lone units, then predict the collective exponent) | APPARENTLY NEW as a programme | Nearest is Mora & Nemenman 2019, which computes single-cell exponents but not the collective onset. |

---

## 3. Corrections the project must make

1. **"Team theory is static" (CORE_AUDIT §3.x) is false.** Counter-examples:
   - M&R 1972 ch. 7, "The team in a dynamic environment", includes periodic recovery with a fixed cost and the timeliness-versus-completeness trade-off. Their §6 result: optimal group size grows as n^{1/(h+1)} when delay ∝ g^h, e.g. "only as fast as the square root of the team size" at h = 1 [OCR, pp. 260–265].
   - Aoki 1986 [FULL].
   - Van Zandt & Radner 2001 [FULL].
   - Radner 1993 [FULL].
   - Van Zandt's real-time decentralized information processing line, including MOVZ 2001 [ABS].
2. **The ADM 2008 citation is inaccurate** (see §4). Use AALVZ 2007, VZR 2001 and Hayek 1945 for "centralize common, decentralize local".
3. **Name collision:** Dessein & Santos 2006, "Adaptive Organizations", JPE 114(5):956–985 [FULL]. It is about the trade-off between adaptation to local information and coordination, with specialization. It must be cited, and the GTAO title should be differentiated, e.g. "a tracking-cost theory of …".
4. **"Nobody has stated them across substrates"** (CORE_AUDIT) should become "no one has stated them *quantitatively* across substrates". Beer's VSM, the Galbraith information-processing view and Simon 1962 make qualitative cross-substrate claims.
5. **The I1 and C1–C3 rows** must cite Mayer et al. 2016 and Mora & Nemenman 2019 as prior art in the same programme.
6. **T1.7 and F3** must state that they assume zero processing delay. In the delay literature (Aoki 1986; Radner 1993; MOVZ 2001) faster environments disadvantage hierarchy. Aghion et al. 2021 is direct evidence against the F3 direction at the level of decision rights.
7. **L1(vii)** must state its scope: periodic reads are optimal only without inter-read observation. With continuous observation and costly transmission, event-triggered rules dominate (Åström & Bernhardsson 2002 [SEC]).

## 4. Verification of the "[from memory, not verified]" citations in FORMAL

| Citation as used | Status | Finding |
|---|---|---|
| **Williamson 1967**, "Hierarchical control and optimum firm size", JPE 75(2):123–138, doi 10.1086/259258 | **Bibliography VERIFIED; content VERIFIED [SEC]** via Mookherjee's handbook survey of organization design [FULL, `src/mookherjee.txt`] | Control loss across layers plus a fixed span means growth adds layers, and control loss bounds firm size. Depth ∝ log N follows from fixed span (size ≈ s^{depth}). **Use is accurate.** |
| **Beckmann 1977**, "Management production functions and the theory of the firm", JET 14(1):1–18, doi 10.1016/0022-0531(77)90081-3 | **Bibliography VERIFIED; content [SEC] only** | The publisher shows no abstract. A secondary description fits hierarchical span/layer production functions. **Keep it, but mark the content as secondary.** |
| **Alonso, Dessein & Matouschek 2008**, "When does coordination require centralization?", AER 98(1):145–179 | **VERIFIED [FULL]; MISCITED** | The paper studies strategic cheap-talk communication about *local* conditions under coordination versus adaptation. Its headline is that decentralization can dominate even when coordination needs are large, as long as communication is strategic. It **does not** state "centralize common information, decentralize local information". Replace it as in §3.2, or cite ADM only for "the coordination-versus-adaptation trade-off". |
| **Berg & Purcell 1977**, "Physics of chemoreception", Biophys J 20(2):193–219 | **VERIFIED [ABS]** | Fractional error in concentration ≈ (T c a D)^{−1/2} for counting time T. **Use is accurate** for a static target. For a drifting target cite Mora & Nemenman 2019 as well. |
| Bonus: **Duncan 1970**, SIAM J Appl Math 19(1):215–220 | **VERIFIED [ABS]** | Mutual information = ½ × the causal MMSE (white Gaussian channel). Use is accurate. |
| Bonus: **Topkis 1978; Roundy 1985; Eppen 1979; Cho & Garcia-Molina 2003; Sparrow et al. 2011; Risko & Gilbert 2016** | VERIFIED [ABS/BIB] | Uses are accurate. Roundy supports the "Roundy-type" geometric clocks only in kind. |

## 5. Honest overall novelty assessment

- **The mechanism is not new.** Information decays under drift, re-reading costs money, and pooling the shared part across N users amortizes the cost. This is the Arrow/Wilson informational economy of scale (Wilson 1975; VZR 2001's "Arrow effect"), set in M&R's dynamic team with periodic recovery (1972 ch. 7), with Veldkamp–Wolfers' purchase onset (2007). Every one of these predates GTAO by 18–54 years.
- **The square-root laws are not new.** That covers vigilance ∝ √(stakes), and thus ∝ √N for a pooled tracker: Harris; M&R eq. 7.5.13; Keller 1974; Sheridan 1970; Reis 2006; Alvarez–Lippi–Paciello 2011.
- **The phase diagrams are not new in kind.** That covers freeze/hold/lookup, the cliff and shared caches: Gray–Putzolu; Wolman 1999; Cho & Garcia-Molina 2003; Rogers 1988; Kussell–Leibler 2005; Mayer et al. 2016.
- **The organizational directions are not new.** "Common shocks → centralize; local → decentralize" and "cheap information → down, cheap communication → up" come from Hayek 1945, AALVZ 2007 and Bloom et al. 2014.
- **The cross-substrate, recursive vision is not new qualitatively.** See Beer's VSM, Galbraith 1974 and Simon 1962.
- **What is apparently new** (each elementary, each checkable, none found in ~45 sources read or abstracted):
  1. the (a, b) technology classification as the variable that sets collective exponents: e_g = −(1−b)/(1−a), the upkeep dichotomy, and the class dependence of all constants;
  2. T4: for bundled decisions, the technology rather than the loss shape sets the exponent;
  3. T5: V > 1 iff a ≥ b, V = 2 at γ = ½, price invariance, and V ∝ ρ^{−θ} for averaging;
  4. T7: the top-down versus bottom-up ordering threshold κ\* = 1/|e_g|;
  5. T8: the closed-form hold band and its N^{(1−a)/b} (N²) widening for shared stores;
  6. the E4 dissolution order under whole-item lookup;
  7. the measurement programme DP1 (lone-unit class → collective exponent) as a falsifiable cross-substrate bridge.
- **How a referee would place it.** At a top economics journal, these would read as tidy corollaries of known models. The paper would be judged on whether the (a, b) bridge is *empirically* confirmed, and so far the project's own empirical tests are mixed or killed (P3 killed twice; the PIAAC vigilance result is weak).
- **Where it fits now:** a synthesis or perspective paper in a complexity or theoretical-biology venue, or a notes-style theory paper, with full credit to M&R, VZR, Veldkamp–Wolfers, Aoki, AALVZ, Bloom et al., Wolman et al., Mayer et al., Mora–Nemenman and Beer.
- **Calling it a "law"** or a "general theory" of adaptive organization is not supported by novelty or by evidence at present.

## 6. Search coverage and gaps (stated, not hidden)

- **Read in full or in relevant part this session:**
  - M&R 1972, chs. 6–7 (OCR)
  - Aoki 1986
  - Van Zandt & Radner 2001
  - Radner 1993
  - Vayanos 2003
  - Veldkamp & Wolfers 2007
  - Reis 2006
  - Bloom et al. 2014
  - Aghion et al. 2021
  - Dessein & Santos 2006
  - ADM 2008
  - Mookherjee's survey
  - Willsky 2002
  - Wolman et al. 1999
  - Rogers 1988
  - Beckers et al. 1989
  - Dornhaus et al. 2006
  - Beer 2002
  - MMW 2023 (ECB WP version)
- **Abstract or secondary only:**
  - Meagher, Orbay & Van Zandt 2001 (full text blocked: 404/403)
  - Garicano 2000
  - Bolton & Dewatripont 1994 (scan, no text layer)
  - Galbraith 1974 (scan)
  - Alvarez, Lippi & Paciello 2011 (PDF failed)
  - Keller 1974
  - Sheridan 1970
  - Åström & Bernhardsson 2002
  - Jaques 1990
  - Kashtan & Alon; Clune et al.; Watson et al.
  - all cell and immune papers
  - AALVZ 2007
  - Wilson 1975
  - Crémer 1980
- **Not reached:**
  - Veldkamp 2011 ch. 8 (paywalled; TOC only: returns to scale in information, specialization, information markets). It may contain a closer static N-onset statement than V&W 2007.
  - Sims 2003 (not re-read).
  - Krause–Guestrin and the Akerlof–Yellen pointers (marked UNVERIFIED and not relied on).
  - Google Scholar forward-citation sweeps of M&R ch. 7 §5 and VZR 2001 (not run). These are the most likely places to find a prior statement of the exponent law, and they should be run before any public novelty claim.
- **Files:** downloaded texts are in `REVIEW/priorart/src/`, including `mr_ocr.txt` for M&R.
- Nothing was posted, sent or committed.
