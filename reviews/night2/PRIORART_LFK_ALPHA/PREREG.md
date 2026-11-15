# PRIORART-LFK-ALPHA — search protocol and decision rule (locked before any search result of this item is read)

Executor queue-pick5 (for Ace; Chad t1914), 15 Nov 2026, ~11:10 AM ET. Queue pick 5, rule slot (ledger 32–34).
Not a proxy test; a prior-art sweep. Prior exposure declared: SPECTRUM_MAP_REFEREE §5 (title-only screen of 6 LFK citers; one PLL hit).

## Claim under search (THEORY.md v1.4.2, §2.2 Regime B, "Memory time (filter bandwidth)" row; CLAIM_MAP v2.5 N11)
Regime B (scale-free over a band, α ≠ 2), white observation noise of density N, drift level q:
- (B1) memory time / filter bandwidth τ ∝ (N/q)^{1/α} — THEORY credits it as KNOWN to Afterman et al. 2022 and Kleptsyna et al. 2020.
- (B2) its fixed-variance re-parameterisation τ_m ∝ τ_E^{1−1/α} (single EWMA store: min(1−1/α, 2/3)) — N11, "PRIOR ART in substance; the τ_E form new only as a re-parameterisation".
Regime A (α = 2) form τ ∝ τ_E^{1/2}: Mora & Nemenman 2019 (credited).

## Hostile checks (author's checks not trusted)
H1. Do Afterman et al. 2022 / Kleptsyna et al. 2020 actually state a bandwidth / memory-time / integration-time scaling (B1), or only the error rate? Read the texts.
H2. Is Mora & Nemenman 2019 really the earliest α = 2 sensing statement in τ_E^{1/2} form? Check whether earlier work (e.g. Kalman/Wiener bandwidth statements in τ_E form; Berg–Purcell with changing concentration) already has it. Search only; do not assert classics not read.

## Sources (fixed set)
S1. OpenAlex forward citations of LFK 2024 (doi 10.1098/rspb.2024.1606) and the preprint DOI 10.1101/2022.09.01.506204 / arXiv 2209.00476: full text where open access, else abstract.
S2. OpenAlex forward citations of Afterman et al. 2022 (10.1137/20M1360359), Kleptsyna et al. 2020 (10.1134/S0005117920030030), Mora & Nemenman 2019 (10.1103/PhysRevLett.123.198101): screen title+abstract by keyword (integration time, memory, bandwidth, timescale, fractional, power-law, 1/f, Hurst, long-range), full text of hits.
S3. Engineering: PLL / clock-steering / GPS-disciplined-oscillator loop bandwidth or time constant against power-law oscillator noise; Allan-deviation crossover rule. Web + OpenAlex search; read texts for any general-α scaling statement.
S4. Nonparametric: minimax bandwidth h ∝ (noise)^{1/(2s+1)} for Hölder-s signals (check the mapping to (N/q)^{1/α}; s = (α−1)/2 gives 1/α).
S5. Sensory/biological adaptation: integration/adaptation time vs stimulus correlation time with power-law stimulus spectra (e.g. Wark/Fairhall/Rieke 2009; Lundstrom 2008; DeWeese & Zador 1998 already credited) — check for an exponent 1−1/α or (N/q)^{1/α}.
Google Scholar is out of scope (PRIORART-SCHOLAR; no sign-in).

## Decision rule (locked)
D1. If any source read in text states B2 (τ ∝ τ_E^{1−1/α} or equivalent at fixed variance, general α) → N11 label "PRIOR ART (stated: <source, passage>)".
D2. Else if a source states B1 for general α in time/bandwidth form (not only error) → N11 stays "PRIOR ART (in substance)", with that source added as the stated bandwidth credit; if THEORY's current B1 credit (Afterman/Kleptsyna) fails H1, propose a credit correction.
D3. Else (B1 found only as error rate) → N11 stays "PRIOR ART (in substance)" via the one-line corollary; B1 relabelled "ELEMENTARY corollary of the error rate (Afterman et al. 2022)" in a proposed edit.
D4. Any source with the α = 2 τ_E^{1/2} sensing form before 2019 → proposed credit edit for Regime A.
Every citation is recorded with the passage read and how it was accessed (full text / abstract / title). Nothing unread is cited as stating anything.
Outcome for the ledger: status_changed = true iff the N11 CLAIM_MAP status label changes (D1), or a credit-correction row change is applied to N11's evidence (D2/D3 are evidence-text changes, status_changed false unless the status word changes).
