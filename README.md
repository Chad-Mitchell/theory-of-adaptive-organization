# A Theory of Adaptive Organization

Private working repository for a general theory of **any adaptive organization** — cells, immune systems, ant colonies, people, firms, and cities. It is **not** a theory of everything. The bet is narrower: once acting late is costly, the same tradeoff between what a system remembers, what it predicts, and what that costs shapes efficient design at every scale, and the shape of the world's change sets the exponents of that design. Only the cost currency changes (heat in a cell, attention in a person, money in a firm). The physical floors are literal at every scale, but above the cell they do not bind; there the exponents come from information theory and competition, not from heat (`THEORY.md` §2.3).

This repository holds the theory (`THEORY.md`), the theorem notes with their code checks, the tests (locked predictions, code, and results), a literature map, and reviews. It is **private** until the author says otherwise. Nothing here is a published paper.

**Author:** Chad Mitchell. Working name: GTAO (A Theory of Adaptive Organization).

## Start here

**[`THEORY.md`](THEORY.md) is the current statement of the theory (v1.0 draft, 14 November 2026, America/New_York).** It leads with what looks new, credits prior art, and reports every test result, including the failures. This README is a summary of it.

## In plain words

An adaptive organization has to stay solvent in a changing world. It can hold a fact, check it, correct it, let it fade, or make the world itself change less. Each of those costs something, and acting late also costs something. One budget covers all of them.

The central bet of v1.0 is that **the world's drift spectrum sets the exponents of good design**. The drift spectrum is how much change arrives at each timescale, or how "red" the world is.
- A world with **one characteristic pace** calls for a square-root law and one memory timescale. That law is already published (Lee, Flack & Krakauer 2024).
- A world that drifts **at every pace** calls for log-spaced layers of memory, which look like power-law forgetting from outside, and for adaptation times that scale one-for-one with the world's.
- A world whose variation spreads over **many modes** sets how fast a model should grow with throughput: as Q^(1/β), with β read from the environment.

This is a **hypothesis with predictions, not a result.** The direction has some support; every exact exponent tested so far has missed or been inconclusive.

Two corrections to earlier drafts:
- **Reduce drift, not just track it.** Homeostasis, niche construction, buffering and contracts lower σ, and that substitutes for watching.
- **"No one in charge" is narrowed.** No one needs to be in charge *when* keeping up shared memory is privately rewarded. Otherwise expect enforcement (free riders; Ostrom).

Optimality is claimed only where selection is strong. Below Lynch's drift barrier, misses are expected.

## Honest status

- **There is no new theorem of large scope.** Most individual rules are known results, placed side by side. The math notes label what is known, what is a calculation, and what fails. The one new proof worth keeping (a quantitative internal-model bound) is modest, and its novelty is unconfirmed.
- **This is a working hypothesis under test**, not a finding. Nothing here has been peer reviewed. Most tests have not had an independent blind review.
- The literature sweep (`litmap/`, 14 November 2026; not independently reviewed) is the basis for "already published" versus "looks new". It cannot rule out an obscure precursor.

### Already published (credited in `THEORY.md` §10)

- The design rules, taken one by one (decision theory, Kalman/Muth, append-only logs, stigmergy, inattention).
- **The square-root memory law:** Lee, Flack & Krakauer 2024 derive optimal memory ∝ τ_E^{1/2} with an energy cost. They also treat stigmergy as outsourced memory and show it invites free riders. The same √ form is in EOQ, inattention models (Reis 2006; Alvarez, Lippi & Paciello 2011) and Kalman filtering.
- **The "temperature"** (shock × √(time to fix) ÷ buffer) is the inverse of the textbook safety-stock factor (Silver, Pyke & Thomas). Its exact first-passage form is **Black & Cox's (1976)** default probability; Merton's terminal version is off by a factor of 2, and earlier "Merton" wording is superseded.
- **Layers and power-law forgetting:** Anderson & Schooler 1991; Fusi, Drew & Abbott 2005; Benna & Fusi 2016; Shankar & Howard 2013 (log-spaced memory is optimal for power-law signals); Brand's pace layers; Holling's panarchy.
- **The information and thermodynamic floors:** Mitter & Newton 2005; Horowitz & Sandberg 2014; Stratonovich's value of information; the data-rate theorems (Nair & Evans 2004; Tatikonda & Mitter 2004); Polani; Shalizi & Crutchfield 2001; Kussell & Leibler 2005.

### What still looks new (each with a kill condition in `THEORY.md` §1)

Pending targeted searches, and none yet confirmed by a locked, reviewed test:

1. **√N fade of shared memory**, with a sign flip against Lieberman et al. 2007: pooled independent deposits make faster turnover optimal for drifting targets, while use preserves forms for stable ones. Untested.
2. **The T3a threshold** for when a new shared level pays: N > (√(1+ρ)+1)²/ρ. Untested.
3. **The fixed-spread sign:** at fixed observed spread, slower correctors cross boundaries *less* often (ε_τ = −1). The sign held at two scales; the size did not.
4. **Geometric layers if and only if drift is scale-free (T7b)**, with level count ∝ (log-span)^(2/3). The locked test was inconclusive.
5. **Watching effort rises, then collapses** once any bounded fallback exists. Untested across domains.
6. **The spectrum-to-exponent law** (the core hypothesis). Mixed evidence.
7. **A quantitative internal-model bound** (solvent agents carry a near-copy of the world's causal states). Proved and self-checked; novelty unconfirmed, probably folklore.

## Test scoreboard

Dates are America/New_York, 13–14 November 2026. Verdicts follow each test's locked rules. **No test listed here has had an independent blind review** unless noted. An independent review of DECISIVE and F1 was in progress when v1.0 was written; its verdict is not reflected here.

| Test | What it asked | Locked verdict | Plain reading |
|---|---|---|---|
| **DECISIVE / banks** | Does slower correction raise failure risk at fixed shock and buffer? (7,837 banks, 2008–14) | **HIT** on sign | β = +0.20 [0.11, 0.29], ≈ 15% higher hazard per doubling; adds to the Z-score. The exact identity, ε_B = −ε_σ and the horizon test failed; the result depends on how τ is defined. |
| **DECISIVE / glucose** | Fixed-spread sign (224 adults with type 1 diabetes) | **Sign right, size off; literal −1 kill rule fired** | Slope −0.46 vs implied −0.82 and literal −1. Collapse across cohorts failed. |
| **DECISIVE / populations** | Fixed-spread sign (274 GPDD series) | **HIT vs corrected target; literal −1 kill rule fired** | Slope −0.21 vs −0.34. Null in the cold regime, where it should be strongest; heavy reliance on one harvest source. |
| **F1** | Same index on ≈ 4,100 US public firms | **Inconclusive** | All four directions held; the main link is published and mostly fixed costs and thin margins; the novel interaction p = 0.055; data prefer a τ weight near 1 over ½. |
| **C3** | Same index on 896 open-source projects | **Inconclusive / miss** | τ added nothing; the design could not have seen it. It rejects the reset-clock mechanism at that scale (predicted ≈ 11× per doubling, measured ≈ 1.0). |
| **BIO1** | Drift matching at biological scales (literature) | Kill not triggered; one contradiction | Holds, but almost entirely as prior art. The neural slope ≈ 1 fits the scale-free branch better than ½. |
| **COLLAPSE1** | Memory time vs world time across substrates | Mixed (two kills, weak passes) | The immune "contradiction" was largely a measurement-age artifact under power-law waning. Code re-edit need decays as a power law (≈ 0.6). |
| **MATCH1** | Need vs memory exponents in the same system; freeze-or-hold | Match **failed**; freeze-or-hold **passed**; layer count inconclusive | News memory 0.24 vs need 0.71. Measles antibodies stay nearly flat (0.11) while measles-return odds fall at 2.15. Need exponents 0.6–0.8 replicate across code, Wikipedia and news. The redness correlation had the opposite sign to the prediction. |
| **DRIFT1** | Is drift scale-free? | Kill not triggered | City 311 looks scale-free; Wikipedia and filings have cadences. Supports T7 only as a conditional claim. A person-scale arm is withheld (`tests/DRIFT1/REDACTION.md`). |
| **ANTS1, C3b** | √N trail fade (simulation); exogenous shocks in open source | Not finished | — |

**Overall:** the timing term holds in **sign** at banks, glucose, populations and firms. The theory's specific numbers mostly do not: the literal −1 failed at two scales, the identity and ratio tests failed, and C3 rejected a fixed-clock version. The timing idea survives as a direction, not as an exact law. Reading that as "½ is the single-timescale special case of the spectrum law" is post hoc and must be tested in its own right.

## Repository layout

```
THEORY.md         The theory, v1.0 draft (start here)
theory/           Theorem notes, the math attack, and their code checks
tests/            Preregistered tests: predictions, code, results (raw data excluded)
litmap/           Literature map, prior-art table, threats, and DOI verification
reviews/          Hostile and independent reviews of the math and of the AI-memory toy
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
