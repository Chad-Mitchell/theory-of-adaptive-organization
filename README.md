# A Theory of Adaptive Organization

Private working repository for a general theory of **any adaptive organization** — cells, immune systems, ant colonies, people, firms, and cities. It is **not** a theory of everything. The bet is narrower: once acting late is costly, the same tradeoff between what a system remembers, what it predicts, and what that costs shapes efficient design at every scale. How the world's change is spread over timescales fixes the optimal design exponents, but that part is classical filtering and approximation theory plus a price, not new; GTAO's open bet is that real systems sit near those optima once the inputs are measured on the same system. Only the cost currency changes (heat in a cell, attention in a person, money in a firm). The physical floors are literal at every scale, but above the cell they do not bind; there the exponents come from information theory and competition, not from heat (`THEORY.md` §2.3).

This repository holds the theory (`THEORY.md`), the theorem notes with their code checks, the tests (locked predictions, code, and results), a literature map, and reviews. It is **private** until the author says otherwise. Nothing here is a published paper.

**Author:** Chad Mitchell. Working name: GTAO (A Theory of Adaptive Organization).

## Start here

**[`THEORY.md`](THEORY.md) is the one canonical statement of the theory (v1.4.1 draft, 15 November 2026, America/New_York).** Where anything else disagrees, it governs. [`STATUS.md`](STATUS.md) says where the work stands, with commits; [`QUEUE.md`](QUEUE.md) is the live work queue. This README is a summary.

## In plain words

An adaptive organization has to stay solvent in a changing world. It can hold a fact, check it, correct it, let it fade, or make the world itself change less. Each of those costs something, and acting late also costs something. One budget covers all of them.

How the world's change is spread over timescales (its drift spectrum, slope α) sets the optimal design exponents: read rate, precision effort, memory time, the shape of forgetting, and the number of memory stores (`THEORY.md` §2.2). **That map is known mathematics** (optimal filtering and approximation theory plus a price on effort), credited in `THEORY.md` §0 and §10:
- In a Markov world (α = 2) the square-root rules hold and one memory store suffices (Kalman/Muth; Mora & Nemenman 2019; Lee, Flack & Krakauer 2024 as an application).
- In a scale-free world (α ≠ 2) the exponents become 1/α and its relatives, forgetting kernels have power-law tails, and the number of stores grows with log-span and log stakes/upkeep.
- The mode-spectrum part (§2.2 Regime C: model size ∝ Q^{1/β}, an interior minimum of the model's budget share iff β < 1, a minimum viable size from unstable modes) is PROOF under stated assumptions with known tools and was not reviewed by the spectrum-map referee.

**GTAO's open bet is empirical and untested:** real systems at every scale sit near these optima once α, the drift level, the sensing noise and the stakes are measured on the same system, with the same relations (not the same constants) holding from cells to cities. In the model, the same three costs at every level is an axiom (Axiom 5; CLAIM_MAP J16), so the model alone cannot test it. As a claim about real systems it is testable through its consequences: at each level the three costs can be measured separately, and the claim fails if a level's design needs a fourth kind of cost to be explained, or if design does not respond to the measured prices of the three as the relations require (J6).

Two corrections to earlier drafts:
- **Reduce drift, not just track it.** Homeostasis, niche construction, buffering and contracts lower σ, and that substitutes for watching.
- **"No one in charge" is narrowed.** No one needs to be in charge *when* keeping up shared memory is privately rewarded. Otherwise expect enforcement (free riders; Ostrom).

Optimality is claimed only where selection is strong. Below Lynch's drift barrier, misses are expected.

## Honest status

**Update, 15 Nov 2026 (v1.4.1):** GTAO is a falsifiable causal theory.
- No field test so far measured GTAO's quantities validly, so field results are "passed / failed on proxy X", not kills or confirmations (`measurement/`).
- The formal layer is proved in-model, with corrections ("V ≥ 2" is wrong as stated), and mostly builds on published team theory and inventory pooling. Its constants are functions of the world's drift spectrum (`THEORY.md` §2.5).
- The spectrum-to-design map is now derived and refereed (`reviews/night2/SPECTRUM_MAP_REFEREE.md`): it is classical, so it is no longer the headline. What remains open is whether real systems sit near it once its inputs are measured (`QUEUE.md`).

See `THEORY.md` (status block, §2.5, §8b–8c) and `measurement/CLAIM_MAP_v2.md` (v2.4).

- **There is no new theorem of large scope.** Most individual rules are known results, placed side by side. The math notes label what is known, what is a calculation, and what fails. The one new proof worth keeping (a quantitative internal-model bound) is modest, and its novelty is unconfirmed.
- **This is a working hypothesis under test**, not a finding. Nothing here has been peer reviewed. An independent review of the DECISIVE and F1 tests is in `reviews/DECISIVE_F1_REVIEW.md` (14 November 2026, America/New_York); the scoreboard below follows its verdict. That review was not fully blind (the reviewer had the results and write-ups). Most other tests have not had an independent review.
- The literature sweep (`litmap/`, 14 November 2026; not independently reviewed) is the basis for "already published" versus "looks new". It cannot rule out an obscure precursor.

### Already published (credited in `THEORY.md` §10)

- The design rules, taken one by one (decision theory, Kalman/Muth, append-only logs, stigmergy, inattention).
- **The square-root memory scaling** is Kalman/Muth filtering; for a sensing cell it is Mora & Nemenman 2019. Lee, Flack & Krakauer 2024 derive optimal memory ∝ τ_E^{1/2} with an energy cost (an application), and treat stigmergy as outsourced memory that invites free riders. The same √ form is in EOQ and inattention models (Reis 2006; Alvarez, Lippi & Paciello 2011).
- **The whole spectrum-to-design map:** fractional filtering (Afterman et al. 2022; Kleptsyna et al. 2020), fBm/ARFIMA prediction kernels (Nuzman & Poor 2000; Hosking 1981; Gatheral, Jaisson & Rosenbaum 2018), exponential-sum approximation (Jiang et al. 2017; Benna & Fusi 2016).
- **The "temperature"** (shock × √(time to fix) ÷ buffer) is the inverse of the textbook safety-stock factor (Silver, Pyke & Thomas). Its exact first-passage form is **Black & Cox's (1976)** default probability; Merton's terminal version is off by a factor of 2, and earlier "Merton" wording is superseded.
- **Layers and power-law forgetting:** Anderson & Schooler 1991; Fusi, Drew & Abbott 2005; Benna & Fusi 2016; Shankar & Howard 2013 (log-spaced memory is optimal for power-law signals); Brand's pace layers; Holling's panarchy.
- **The information and thermodynamic floors:** Mitter & Newton 2005; Horowitz & Sandberg 2014; Stratonovich's value of information; the data-rate theorems (Nair & Evans 2004; Tatikonda & Mitter 2004); Polani; Shalizi & Crutchfield 2001; Kussell & Leibler 2005.

### What still looks new (each with a kill condition in `THEORY.md` §1)

*This is the v1.0 list, kept as history. The current list of what looks like the theory's own is `THEORY.md` §8b; statuses are in `measurement/CLAIM_MAP_v2.md` (v2.4).*

Pending targeted searches, and none yet confirmed by a locked, reviewed test:

1. **√N fade of shared memory**, with a sign flip against Lieberman et al. 2007: pooled independent deposits make faster turnover optimal for drifting targets, while use preserves forms for stable ones. Untested.
2. **The T3a threshold** for when a new shared level pays: N > (√(1+ρ)+1)²/ρ. Untested.
3. **The fixed-spread sign:** at fixed observed spread, slower correctors cross boundaries *less* often (ε_τ = −1). The sign held; the size did not, and the literal joint kill fired. The independent review finds the sign itself follows from dimensional analysis, so it is not theory-specific.
4. **Geometric layers if and only if drift is scale-free (T7b)**, with level count ∝ (log-span)^(2/3). The locked test was inconclusive. *(Withdrawn in v1.4: replaced by a prior-art store-count form; CLAIM_MAP K12.)*
5. **Watching effort rises, then collapses** once any bounded fallback exists. Untested across domains.
6. **The spectrum-to-exponent relation** (the core hypothesis). The item-level news test P1 failed on proxy "headline-word recurrence as need" on 15 Nov 2026. *(v1.4: the relation is derived and is prior art, CLAIM_MAP K13; the open bet is measured-input optimality, N13.)*
7. **A quantitative internal-model bound** (solvent agents carry a near-copy of the world's causal states). Proved and self-checked; novelty unconfirmed, probably folklore.

## Test scoreboard

Dates are America/New_York, 13–14 November 2026. For DECISIVE and F1, the verdicts below follow the independent review in `reviews/DECISIVE_F1_REVIEW.md`, not the tests' own more generous labels. Other tests follow their locked rules and have not had an independent review unless noted.

The preregistration commits for these tests lived only in local, unpushed git repos. Adding their histories to this private repository (as `tests/<name>/history.bundle` where a bundle could be shipped without excluded data, and as `tests/<name>/history.txt` receipts for every test) gives them an **external timestamp only from today**. The author dates inside those histories are self-attested.

| Test | What it asked | Verdict (after review, where one exists) | Plain reading |
|---|---|---|---|
| **DECISIVE / banks** | Does slower correction raise failure risk at fixed shock and buffer? (7,837 banks, 2008–14) | **Sign-only, not a HIT** | β = +0.20 [0.11, 0.29], ≈ 15% higher hazard per doubling; adds to the Z-score. The sign holds only for detrended τ; the specified own-mean τ is null. The exact identity, ε_B = −ε_σ and the horizon test all failed. |
| **DECISIVE / glucose** | Fixed-spread sign (224 adults with type 1 diabetes) | **Sign right, size off; MATH_ATTACK literal joint kill fires on the full sample** | Slope −0.46 vs implied −0.82 and literal −1. Collapse across cohorts failed. The test's own prereg, scored against a lowered sampling-corrected target, does not kill; those targets rewrote the kill rule after MATH_ATTACK wrote it. The cold regime is not evaluable (n = 2). |
| **DECISIVE / populations** | Fixed-spread sign (274 GPDD series) | **MATH_ATTACK literal joint kill fires on any reading** | Slope −0.21 vs −0.34. Cold-regime slope has the wrong sign, where the theory says the effect should be strongest. The test's own prereg against the sampling-corrected target does not kill, but those targets rewrote the rule. The result is fragile (half the series are fur-harvest records; source fixed effects, taxon clustering, or dropping clipped series remove significance) and should not be cited as support. |
| **F1** | Same index on ≈ 4,100 US public firms | **Inconclusive; not a theory-specific hit** | All four directions held; the main link is published. τ mostly measures fixed-cost share (operating leverage), not correction speed, so construct validity fails. The novel interaction p = 0.055. Data prefer a τ weight near 1 over ½ (suggestive only). The prereg kill rules did not fire. |
| **C3** | Same index on 896 open-source projects | **Inconclusive / miss** | τ added nothing; the design could not have seen it. It rejects the reset-clock mechanism at that scale (predicted ≈ 11× per doubling, measured ≈ 1.0). |
| **BIO1** | Drift matching at biological scales (literature) | Kill not triggered; one contradiction | Holds, but almost entirely as prior art. The neural slope ≈ 1 comes from periodic switching, which v1.4 places outside the spectrum map. |
| **COLLAPSE1** | Memory time vs world time across substrates | Mixed (two proxy fails, weak passes) | The immune "contradiction" was largely a measurement-age artifact under power-law waning. Code re-edit need decays as a power law (≈ 0.6). |
| **MATCH1** | Need vs memory exponents in the same system; freeze-or-hold | Match **failed**; freeze-or-hold **passed**; layer count inconclusive | News memory 0.24 vs need 0.71. Measles antibodies stay nearly flat (0.11) while measles-return odds fall at 2.15. Need exponents 0.6–0.8 replicate across code, Wikipedia and news. The redness correlation had the opposite sign to the prediction; v1.4: that prediction was mis-derived (CLAIM_MAP H19). |
| **DRIFT1** | Is drift scale-free? | Kill not triggered | City 311 looks scale-free; Wikipedia and filings have cadences. Supports T7 only as a conditional claim. A person-scale arm is withheld (`tests/DRIFT1/REDACTION.md`). |
| **ANTS1, C3b** | √N trail fade (simulation); exogenous shocks in open source | Not finished | — |

**Overall (following the DECISIVE/F1 review):** the numbers reproduce and every sign is right. That is not enough. The τ (time-to-fix) term as a theory-specific claim **failed on these proxies** under MATH_ATTACK's literal joint kill rule (CLAIM_MAP K4 PROXY-FAIL): it fires for populations on any reading and for glucose on the full sample; banks are sign-only, not a hit. "Fewer crossings at fixed spread with slower correction" follows from dimensional analysis and standard first-passage results (Siegert 1951; Black–Cox 1976). The theory-specific structure — the −1 exponent, the √τ weighting, the identities, the τ-buffer interaction, and one collapse curve — failed. F1's τ mostly measures fixed-cost share. The lowered sampling-corrected targets rewrote the kill rule after it was written; this scoreboard leads with the literal verdict. C3 rejected a fixed-clock version. Reading the missed exponents as "½ is the single-timescale special case of the spectrum relation" is post hoc and must be tested in its own right.

## Repository layout

```
THEORY.md         The theory, v1.4.1 draft (start here)
theory/           Theorem notes, the math attack, and their code checks
tests/            Preregistered tests: predictions, code, results (raw data excluded)
litmap/           Literature map, prior-art table, threats, and DOI verification
reviews/          Hostile and independent reviews, including the DECISIVE/F1 review
applications/     How this theory is applied (AI memory; Looper; ants) — no personal data
LICENSE.md        Placeholder: no license chosen yet (TODO for the author)
```

## Applications (separate from the theory)

- **AI memory**, worked out as math and a toy simulation in the public repository [`Chad-Mitchell/adaptive-memory-levels`](https://github.com/Chad-Mitchell/adaptive-memory-levels). That repo is one application. It is not this theory, and its toy results are not evidence that the theory is true.
- **Looper** is a personal-assistant application of the same hypothesis. It is developed separately. This repository does not contain Looper code, store contents, or any personal data.
- **Ants:** the field-literature check is in BIO1; a code-ant simulation of the √N claim is ANTS1 (unfinished).

## How this should be read

Do not treat locked predictions as findings, and do not treat a support that is already in the literature as a new confirmation. Formal misses and inconclusives stay on the board. Wording in public-facing documents needs the author's go, and this repository stays private until that go is given.

## License

See `LICENSE.md`. No license has been chosen.
