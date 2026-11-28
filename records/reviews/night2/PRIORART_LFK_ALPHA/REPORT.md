# PRIORART-LFK-ALPHA — report (queue pick 5, rule slot; ledger 32–35)

Executor queue-pick5 (for Ace; Chad t1914), 15 Nov 2026, ~11:05–11:20 AM ET. Protocol and decision rule locked first
(`PREREG.md`, commit 44e1963, before any search result of this item). Not a proxy test. Google Scholar not used (PRIORART-SCHOLAR).
Access level is given for every source: **[TEXT]** = passage read in full text this session; **[ABS]** = abstract only; **[SNIPPET]** = search-result excerpt only.

## Claim searched (THEORY.md v1.4.2 §2.2, Regime B row "Memory time (filter bandwidth)"; CLAIM_MAP v2.5 N11)
B1: τ ∝ (N/q)^{1/α} (white observation noise N, drift level q, S(f) ∝ f^−α). B2: its fixed-variance form τ_m ∝ τ_E^{1−1/α}.

## Verdict (decision rule D1 applies, with one premise finding)
1. **B1 and B2 are stated, in mapped form, in Bialek, Callan & Strong 1996** ("Field theories for learning probability distributions",
   PRL 77:4693; arXiv cond-mat/9607180 **[TEXT, arXiv version]**). For a prior with action ∝ ℓ^{2α_B−D}∫(∂^{α_B}φ)² they find the
   estimate "smooths the examples on a scale ξ ∼ (ℓ^{2α_B−D}/NQ)^{1/2α_B}" (text after their eq. 25); for α_B = 1, D = 1:
   "ξ ∼ [ℓ/NP(x)]^{1/2}" (after eq. 16), a geometric mean of the prior scale ℓ and the sample spacing 1/NP.
   *Mapping (mine, checkable):* D = 1 and derivative order α_B give a prior spectrum k^{−2α_B}, so GTAO's α = 2α_B; the noise density is
   N ∝ 1/(NQ); the prior's high-frequency level is q ∝ ℓ^{−(2α_B−1)} = ℓ^{1−α}. Then ξ ∝ (N/q)^{1/α} (B1) and, at fixed noise,
   ξ ∝ ℓ^{1−1/α} (B2), with ℓ the scale at which the dimensionless field changes by O(1) — the role τ_E plays at unit variance.
   Differences: spatial density estimation, two-sided smoothing, massless prior, α = 2α_B even for a local prior (the text notes
   non-integer α_B needs a nonlocal prior). Two-sided vs causal changes only constants at the error level (Kleptsyna, Marushkevych &
   Chigansky 2020, Thm 2.1: "the interpolation and the filtering errors differ asymptotically only by a constant factor" **[TEXT, arXiv 2205.09516]**).
   **N11 label: PRIOR ART (stated in mapped form; Bialek, Callan & Strong 1996), was "PRIOR ART (in substance)".**
2. **H1 failed for THEORY's current B1 credit.** Afterman et al. 2022 Thm 2.5 / eq. (2.8) **[TEXT, arXiv 1911.10062]** and Kleptsyna et al.
   2020 Thm 2.1 **[TEXT]** state the **error** rate (ε/µ²)^{2H/(2H+1)}, not a bandwidth or memory time. No passage in either gives a filter
   time scale. They support the error row, and B1 only as a one-line corollary. Kleptsyna's Remark 2.2 links the rate to the minimax rate for
   Hölder-H deterministic signals (Ibragimov & Has'minskii 1981; Tsybakov 2009 — cited there, **not read by me**).
3. **D4 (earlier α = 2 form).** The geometric-mean form predates Mora & Nemenman 2019 in Bayesian smoothing (BCS 1996, above). Mora &
   Nemenman 2019 **[TEXT, arXiv 1908.04057]** cite Kolmogoroff 1939 for the integrate-long-vs-stay-current trade-off and BCS 1996 / Nemenman &
   Bialek 2002 for sample estimation. For concentration sensing specifically, no pre-2019 statement found. Engineering α = 2: PLL "ideal
   bandwidth" where the flat in-band noise meets the −20 dB/dec VCO noise, "setting L_flat = L_VCO and solving for f", attributed to Banerjee,
   *PLL Performance, Simulation and Design* (1st ed. 1998; 5th ed. pp. 305–306) (Dacus 2019, Microwaves & RF **[TEXT]**; Banerjee **not read**);
   GPSDO loop time constant at the Allan-deviation crossover (EE Times "Disciplining a precision clock to GPS" **[SNIPPET]**). Both are
   intersection rules that give (N/q)^{1/α} for any slope, but are stated only for given slopes.
4. **Premise finding (not in the locked decision rule; reported as a surprise).** Conti & Mora 2022, "Non-equilibrium dynamics of adaptation
   in sensory systems", PRE 106:054404 **[TEXT, arXiv 2011.09958v2]**: in the efficient (fidelity) regime the Bayes-optimal adaptation time
   scales "logarithmic for abrupt changes in the stimulus mean (telegraph process), and square root for continuous ones (Ornstein-Uhlenbeck
   process)". Both worlds have the same Lorentzian spectrum (α = 2 above the corner). **So the spectrum sets the memory-time exponent only for
   Gaussian worlds or linear trackers.** THEORY §2.2 Regime A lists "switching at one rate" as an α = 2 example with τ ∝ (N/q)^{1/2}; that holds
   for the best linear (Kalman/EWMA) tracker, not for the Bayes optimum. LFK's τ_E^{1/2} on a telegraph world is a property of their learner
   class. *Independent in-model check* (`checks/telegraph_check.py`, seed 20261115, θ = 1, τ = 10…3000): Wonham-filter median post-switch
   crossing time 0.75 → 3.2, growing ≈ 0.44 per e-fold of τ (linear in ln τ; local log-log slope falls from 0.40 to 0.13); best EWMA time
   constant log-log slope 0.44 (√ class, grid-limited). Confirms the claim in-model; different adaptation-time definition from theirs.
5. **Forward citations (OpenAlex, `fwd.py`, `fwd_citers.json`).** LFK 2024: 2 citers; LFK preprint: 4; Afterman 2022: 4; Kleptsyna 2020: 3;
   Mora & Nemenman 2019: 49. Full text read: "Decoding the architecture of living systems" (arXiv 2512.22651), the C. elegans forgetting
   paper (Nat Neurosci 2025), the fGn finite-predictor paper (arXiv 2504.01562), Conti & Mora 2022, and the elongated-cell paper
   (arXiv 2405.04810): none states B2 or a general-α memory time. All others screened by abstract **[ABS]**; none states it ("Bayesian gradient
   sensing in the presence of rotational diffusion" 2021 states the α = 2 √ form for rotational diffusion). Not read: "Playing it safe"
   (bioRxiv PDF did not download), "The hierarchical timescale hypothesis" (Cell Systems 2026; no abstract, no OA), Malaguti & ten Wolde 2021
   full text (eLife PDF did not download; abstract read).

## CLAIM_MAP change applied (my item's row only)
N11: PRIOR ART (in substance) → **PRIOR ART (stated in mapped form)**, evidence as in Verdict 1–2. The status word stays PRIOR ART; only the
qualifier changes. My locked rule counts that as status_changed = true (D1). A stricter scorer could count it false; flagged for the
NOISE/AQN referees and for Q0 scoring.

## Proposed THEORY.md edits (NOT applied; independent review first, per Chad t1916)
- **E1 (§2.2 Regime B, memory-time row; §0 credit list):** "KNOWN (Wiener/Kalman bandwidth; Afterman et al. 2022; Kleptsyna et al. 2020)" →
  "KNOWN: stated as a smoothing scale for general exponent by Bialek, Callan & Strong 1996 (ξ ∼ (ℓ^{2α_B−1}/NQ)^{1/2α_B}, α = 2α_B); for
  fractional signals the error rate is Afterman et al. 2022 / Kleptsyna et al. 2020, from which the bandwidth follows in one line. The τ_E
  form at fixed variance is the same statement (ℓ^{1−1/α}) (CLAIM_MAP N11, PRIOR ART stated in mapped form)."
- **E2 (§2.2 Regime A bullets and Regime B premises):** add the premise "Gaussian world, or a linear tracker". Add: "For a jump world
  (switching at one rate) the Bayes-optimal tracker adapts on a time ∝ ln τ, not √τ (Conti & Mora 2022); the √ form is the best linear
  tracker. The spectrum alone does not set the exponent outside the linear/Gaussian class." Consequence for §1 N6 / CLAIM_MAP N13: an
  event-world test must state whether the system is compared with the linear or the Bayes optimum.
- **E3 (§2.2 Regime A, Mora & Nemenman bullet; §10):** "The α = 2 geometric-mean form appears for Bayesian smoothing in Bialek, Callan &
  Strong 1996; Mora & Nemenman 2019 is the concentration-sensing case." Engineering α = 2: PLL ideal bandwidth at the noise crossover
  (Banerjee 1998, cited via Dacus 2019; Banerjee to be read before crediting).

## New queue items (rationale in items.json)
TELEGRAPH-LINEAR-PREMISE (w 3), PRIORART-CREDIT-EDITS (w 1), PRIORART-ENGINEERING-READ (w 1).

## Unresolved
Google Scholar; Banerjee and a clock-steering primary text; Tsybakov / Ibragimov–Has'minskii not read; published PRL text of BCS 1996 not
compared with the arXiv text; the three unread citers above.
