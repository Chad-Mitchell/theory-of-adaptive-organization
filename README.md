# A Theory of Adaptive Organization (GTAO)

Author: Chad Mitchell — X: [@torusflow](https://x.com/torusflow)

**Everything that lasts has to pay, and anything that must stay matched to a changing world pays one three-part bill: holding memory, being wrong or late, and the reads that keep the memory fresh.** GTAO is a falsifiable theory of how that bill shapes the design of any adaptive organization: a cell, an immune system, an ant colony, a person, a firm, a city. Its mathematics is proved only inside the model, and much of it is known mathematics, assembled and credited. Whether real systems follow it is **untested, not refuted**. It is a theory, not a law, and **not a theory of everything**.

*Public working draft since 18 November 2026. Not peer reviewed; not a published paper. Public domain (CC0).*

## The idea in one table

The second law says total disorder rises. Local order can still grow, but only by pushing disorder out somewhere else. That law, together with gravity, the speed of light, quantum physics and the universe's low-entropy start, sets the stage; **GTAO adds no new physics.** It asks what it takes to last, and finds three ways:

| Way to last | What it pays | Does a model of the world pay? | Examples |
|---|---|---|---|
| **Keep** (frozen) | Nothing: it sits in a state almost nothing can knock loose | **No.** Nothing it does changes whether it lasts, so a model would cost something and buy nothing (CLAIM_MAP N25, PROVED (in-model); partly definitional) | Atoms, crystals, a virus particle; at the extreme, a black hole: the most memory physics allows for its size, almost none of it readable (N26, PROVED (in-model), conditional) |
| **Burn** (held) | A steady flow of energy | **No.** It steadies itself and tracks nothing outside | Stars, flames, hurricanes |
| **Know** (tracks) | A flow of energy *and* the cost of staying matched to a world that changes and can ruin it | **Yes, once acting late is costly.** Then carrying a model and acting ahead pays | Cells, immune systems, ant colonies, people, firms, cities |

The third way is **judgment**: not a new physical principle, but a way of staying alive under the old one (`THEORY.md` §0; the full picture, from chemistry to heat death, is [`theory/BOOKENDS.md`](theory/BOOKENDS.md) §1).

**The bill.** A knower pays one budget in three parts, plus the risk of ruin: (1) holding memory, (2) being wrong, including being late, and (3) the reads and effort that keep the memory current. Only the currency changes: heat in a cell, attention in a person, money in a firm. A knower can also pay to make its world change less (homeostasis, buffers, contracts), and that substitutes for watching (`THEORY.md` §5).

**What the bill implies, inside the model** (status in brackets; details in `THEORY.md`):
- **How often to look, how long to remember, how many memory stores** are set by how the world's change is spread over timescales (spectral slope α), with drift level, sensing noise and stakes. For example, with exact reset reads, read rate ∝ (stakes·drift/price)^{1/α}; one memory store suffices only near α = 2 (a Markov world), and elsewhere the number of stores grows with the span of timescales and with stakes over upkeep. [Known filtering and approximation mathematics plus a price on effort, credited; §2.2.]
- **When to share a model:** once enough members face a common driver, a shared level pays: at zero upkeep, N > (√(1+ρ)+1)²/ρ is sufficient, where ρ is shared over private drift. [PROOF in-model; §6, §1 N2.]
- **Who must be in charge:** no one, *when* keeping shared memory up is privately rewarded; otherwise expect shared fate or enforcement, usually both; shared fate is usually partial (Frank 1995; Ostrom). This narrows the earlier "no one in charge". [HYPOTHESIS; CLAIM_MAP J9 OPEN.]
- **How big one tracker can be:** light delay caps it, so large organizations federate. On Earth this is a latency cost; off-planet it is a hard cap. [Elementary bound; real-system form N27 OPEN.]
- **What to keep, check or let go:** a checked copy beats letting a fact fade only when drift × check cost is below what the fact is worth (Theorem G). Facts that barely drift are frozen; facts that drift fast, or are cheap to look up, are looked up when needed; checked holding pays only in the band between, and the band need not exist. [PROOF in-model; Theorem G, T8; CLAIM_MAP F13.]

## The bet, and how it dies

**The open bet:** strongly selected real systems sit near these optima once the inputs (α, drift level, sensing noise, stakes, prices) are measured on the same system, and the same relations (not the same constants) hold at every level, from cells to cities (CLAIM_MAP N13, J6, both OPEN). It dies if:
- in two or more strongly selected systems at different scales, the measured design misses its measured-input optimum by more than the measurement error allows, *and* a named rival (a fixed budget share; a universal ½) fits better; or, causally, design fails to move with a measured change in its inputs by the preregistered share (`THEORY.md` §1 N6, §9);
- a level's design needs a fourth kind of cost to be explained (J16; inside the model the same three costs at every level is an axiom, Axiom 5, so only real systems can test it);
- design does not respond to the measured prices of the three costs as the relations require (J6).

Optimality is claimed only where selection is strong. Below Lynch's drift barrier misses are expected, and that split must be fixed **before** a test, never used to explain a miss afterward (§7).

## What is new, and what is not

| Layer | Status | Where |
|---|---|---|
| The spine and the keep / burn / know split | A framing. The three-class split is prior art in substance (Prigogine; Pross). Bookend rows are classifications, not predictions: no data could fail them | `theory/BOOKENDS.md`, `theory/SCALE_ENDS.md` |
| Design exponents from the world's drift spectrum | **Known mathematics**, assembled and credited. In a Markov world (α = 2) the square-root rules hold and one store suffices (Kalman/Muth; Mora & Nemenman 2019 for a sensing cell; Lee, Flack & Krakauer 2024 as an application). In a scale-free world (α ≠ 2) the exponents become 1/α and its relatives, forgetting kernels have power-law tails, and the number of stores grows with log-span and log stakes/upkeep (Afterman et al. 2022; Nuzman & Poor 2000; Benna & Fusi 2016; and others). Holds for a Gaussian world or the best linear tracker; the Bayes tracker of a jump world can differ (N16) | `THEORY.md` §2.2, §10 |
| Model size across many modes (Regime C) | Model size ∝ Q^{1/β}, an interior minimum of the model's budget share iff β < 1, a minimum viable size from unstable modes: PROOF under stated assumptions with known tools; not reviewed by the spectrum-map referee | `THEORY.md` §2.2 |
| Levels, vigilance, freeze / hold / look up (the formal layer) | Proved in-model, with corrections ("V ≥ 2" is wrong as stated); mostly built on published team theory and inventory pooling | `THEORY.md` §2.5, §6, §8b |
| The ends of the scale | Atoms frozen (N25) and black holes as the frozen extreme (N26): PROVED (in-model), the first partly definitional, the second conditional on unitary evaporation and on counting lateness as error; the switch-on of selected models is a hypothesis (N28 OPEN) | `THEORY.md` §2.3 |
| A quantitative internal-model bound | PROOF; novelty unconfirmed, probably folklore | `theory/INTERNAL_MODEL.md` |
| **The open bet** | **Untested, not refuted** | CLAIM_MAP N13, J6 |

**There is no new theorem of large scope.** What may be this project's own is the assembly: one budget, priced the same way at every level, with one preregistered falsification program across scales.

## Where the evidence stands

- **No field test so far measured the theory's quantities validly.** No Tier-1 test has run, so there is no field pass and no field fail. Field results are reported as "passed / failed on proxy X", not as kills or confirmations (`measurement/FRAMEWORK.md`).
- **The time-to-fix term (τ) failed on proxies** in the DECISIVE and F1 tests under the literal joint kill rule (CLAIM_MAP K4 PROXY-FAIL), though every sign was right; the sign itself follows from dimensional analysis, so it is not theory-specific. The scoreboard below has every test.
- **The validity gates MV1–MV10 are treated as binding** from 18 November 2026 for every new preregistration (Chad's instruction to proceed without his sign-off; CLAIM_MAP M2). MV9's external timestamp still needs the author's go for each lock.
- **The first real test** of the open bet (SAME-SYSTEM-AQN) is designed and not yet run (`STATUS.md`, `QUEUE.md`).

## Reach: from atoms to the cosmic horizon

The costs are physically priced, as floors, at every scale from atoms to the cosmic horizon. That is the author's scope choice of 18 November 2026, not a finding: no formal proof depends on it, and whether the physics does real work in the proofs is an open disagreement (`THEORY.md` §2.3). Above the cell the floors are literal but do not bind; there the exponents come from information theory and competition, not from heat. What changes along the scale is whether a model is worth carrying (`theory/SCALE_ENDS.md`, independently refereed, PASS-WITH-FIXES; CLAIM_MAP N25–N29):
- **Atoms** are frozen. A model would buy nothing (N25), though atoms still carry physical information (for example ln 4 nats of hyperfine spin).
- **Stars** are held with no model: they burn fuel and track nothing outside.
- **Black holes** are the extreme of the frozen class: the most memory physics allows for their size, three readable numbers (mass, spin, charge), and, if evaporation is unitary (the Page-curve assumption; Hawking's original calculation says information never returns), the rest returned scrambled only after about the Page time, for every black hole that exists today (N26, PROVED (in-model) for such pre-Page-time holes; older holes rest on a conjecture). GTAO does not derive why black holes exist, the area law or the Page curve (N29 WITHDRAWN as framing).
- **Selected models** switch on only with heredity below Eigen's threshold, a world-dependent action, trackable drift and a first nat that pays (N28 OPEN); survival-relevant information and the simplest models (integral feedback) may come earlier.
- **Light delay** caps what one tracker can hold, so large organizations federate (N27 OPEN; prior art Simon 1962, PACELC). The **cosmic horizon** caps memory at about 3×10¹²² nats and the price of erasing a bit at ≥ about 2×10⁻⁵³ J (Landauer's bound in a bath at the de Sitter temperature).
- **Viruses:** a virus particle is frozen and pays nothing, while an infected cell and the viral lineage are alive, so GTAO says a virus is alive as a lineage, not as a particle, and treats "alive" as a ledger of who pays for what. That is a restatement of published views (Forterre's virocell is the closest), with a common ledger (`theory/REACH.md` §1). The cosmic web, wormholes, the torus, dark matter and energy, and fractal time are worked in [`theory/REACH.md`](theory/REACH.md) and three companion notes; the theory makes no prediction that wormholes exist or about the shape of the universe.

## Start here

**[`THEORY.md`](THEORY.md) is the one canonical statement of the theory (v1.4.27 draft, 19 November 2026, America/New_York).** Where anything else disagrees, it governs. [`STATUS.md`](STATUS.md) says where the work stands; [`QUEUE.md`](QUEUE.md) is the live work queue; [`BRIEF.md`](BRIEF.md) is a plain-words brief of the whole record, checked against the files; `measurement/FRAMEWORK.md` says how quantities are measured, and `measurement/CLAIM_MAP_v2.md` (v2.46) gives one status per claim. `python3 tools/check_consistency.py` checks versions, wording and claim statuses across these files. This README is a summary.

**Reading paths** (each about an hour):
- **Physicist:** `THEORY.md` §2.3 (where the physics is literal and where it is not) → `theory/SCALE_ENDS.md` → `theory/BOOKENDS.md` §2 → `theory/WORMHOLES.md`, `theory/COSMIC_WEB.md`. Expect classifications given published physics, not new physics.
- **Biologist:** `theory/BOOKENDS.md` §1 → `THEORY.md` §2.2 Regime A (the sensing case is Mora & Nemenman 2019) → `theory/REACH.md` §1–§2 (viruses, what counts as alive) → `prereg/SENSE-CELL/` (CLAIM_MAP N24).
- **Organization theorist or economist:** `THEORY.md` §6 (levels, shared memory, who is in charge) → §4 and §8 (failure risk, and the τ tests that failed on proxies) → §5 (reducing drift) → LAT-1 in §2.3. Closest prior art: Marschak & Radner 1972; Van Zandt & Radner 2001; Veldkamp & Wolfers 2007; Simon 1962.
- **Curious generalist:** `theory/BOOKENDS.md` §1 ("The picture in plain words") → the scoreboard below → `BRIEF.md`.
- **Skeptic:** `measurement/CLAIM_MAP_v2.md` (every WITHDRAWN and MATH-CORRECTED row) → `reviews/` → `reviews/lock_2026-11-18/LOCK_AUDIT.md`.

## Honest status, in detail

GTAO is a falsifiable causal theory. No Tier-1 test has run: there is no field pass and no field fail, so the theory is untested in the field, not refuted.
- No field test so far measured GTAO's quantities validly, so field results are "passed / failed on proxy X", not kills or confirmations (`measurement/`).
- The formal layer is proved in-model, with corrections ("V ≥ 2" is wrong as stated), and mostly builds on published team theory and inventory pooling. Its constants are functions of the world's drift spectrum (`THEORY.md` §2.5).
- The spectrum-to-design map is now derived and refereed (`reviews/night2/SPECTRUM_MAP_REFEREE.md`): it is classical, so it is no longer the headline. What remains open is whether real systems sit near it once its inputs are measured (`QUEUE.md`).

See `THEORY.md` (status block, §2.3, §2.5, §8b–8c) and `measurement/CLAIM_MAP_v2.md` (v2.46).

- **There is no new theorem of large scope.** Most individual rules are known results, placed side by side. The math notes label what is known, what is a calculation, and what fails. The one new proof worth keeping (a quantitative internal-model bound) is modest, and its novelty is unconfirmed.
- **This is a working hypothesis under test**, not a finding. Nothing here has been peer reviewed. An independent review of the DECISIVE and F1 tests is in `reviews/DECISIVE_F1_REVIEW.md` (14 November 2026, America/New_York); the scoreboard below follows its verdict. That review was not fully blind (the reviewer had the results and write-ups). Most other tests have not had an independent review.
- **Every review so far covered part of the work**, and every reviewer was an AI executor of the same family as the authors; `THEORY.md` has not been independently reviewed as a whole, and no human domain expert has reviewed it (`reviews/lock_2026-11-18/LOCK_AUDIT.md`, B1).
- The literature sweep (`litmap/`, 14 November 2026; not independently reviewed) is the basis for "already published" versus "looks new". It cannot rule out an obscure precursor.

## Already published (credited in `THEORY.md` §10)

- The design rules, taken one by one (decision theory, Kalman/Muth, append-only logs, stigmergy, inattention).
- **The square-root memory scaling** is Kalman/Muth filtering; for a sensing cell it is Mora & Nemenman 2019. Lee, Flack & Krakauer 2024 derive optimal memory ∝ τ_E^{1/2} with an energy cost (an application), and treat stigmergy as outsourced memory that invites free riders. The same √ form is in EOQ and inattention models (Reis 2006; Alvarez, Lippi & Paciello 2011).
- **The whole spectrum-to-design map:** fractional filtering (Afterman et al. 2022; Kleptsyna et al. 2020), fBm/ARFIMA prediction kernels (Nuzman & Poor 2000; Hosking 1981; Gatheral, Jaisson & Rosenbaum 2018), exponential-sum approximation (Jiang et al. 2017; Benna & Fusi 2016).
- **The "temperature"** (shock × √(time to fix) ÷ buffer) is the inverse of the textbook safety-stock factor (Silver, Pyke & Thomas). Its exact first-passage form is **Black & Cox's (1976)** default probability; Merton's terminal version is off by a factor of 2, and earlier "Merton" wording is superseded.
- **Layers and power-law forgetting:** Anderson & Schooler 1991; Fusi, Drew & Abbott 2005; Benna & Fusi 2016; Shankar & Howard 2013 (log-spaced memory is optimal for power-law signals); Brand's pace layers; Holling's panarchy.
- **The information and thermodynamic floors:** Mitter & Newton 2005; Horowitz & Sandberg 2014; Stratonovich's value of information; the data-rate theorems (Nair & Evans 2004; Tatikonda & Mitter 2004); Polani; Shalizi & Crutchfield 2001; Kussell & Leibler 2005.

<details>
<summary><b>What looked new in v1.0 (kept as history)</b></summary>


*This is the v1.0 list, kept as history. The current list of what looks like the theory's own is `THEORY.md` §8b; statuses are in `measurement/CLAIM_MAP_v2.md` (v2.46).*

Pending targeted searches, and none yet confirmed by a locked, reviewed test:

1. **√N fade of shared memory**, with a sign flip against Lieberman et al. 2007: pooled independent deposits make faster turnover optimal for drifting targets, while use preserves forms for stable ones. Untested.
2. **The T3a threshold** for when a new shared level pays: N > (√(1+ρ)+1)²/ρ. Untested.
3. **The fixed-spread sign:** at fixed observed spread, slower correctors cross boundaries *less* often (ε_τ = −1). The sign held; the size did not, and the literal joint kill fired. The independent review finds the sign itself follows from dimensional analysis, so it is not theory-specific.
4. **Geometric layers if and only if drift is scale-free (T7b)**, with level count ∝ (log-span)^(2/3). The locked test was inconclusive. *(Withdrawn in v1.4: replaced by a prior-art store-count form; CLAIM_MAP K12.)*
5. **Watching effort rises, then collapses** once any bounded fallback exists. Untested across domains.
6. **The spectrum-to-exponent relation** (the core hypothesis). The item-level news test P1 failed on proxy "headline-word recurrence as need" on 15 Nov 2026. *(v1.4: the relation is derived and is prior art, CLAIM_MAP K13; the open bet is measured-input optimality, N13.)*
7. **A quantitative internal-model bound** (solvent agents carry a near-copy of the world's causal states). Proved in-model and self-checked; novelty unconfirmed, probably folklore.

</details>

## Test scoreboard

Dates are America/New_York, 13–15 November 2026. For DECISIVE and F1, the verdicts below follow the independent review in `reviews/DECISIVE_F1_REVIEW.md`, not the tests' own more generous labels. Other tests follow their locked rules and have not had an independent review unless noted.

The preregistration commits for these tests lived only in local, unpushed git repos. Adding their histories to this repository (as `tests/<name>/history.bundle` where a bundle could be shipped without excluded data, and as `tests/<name>/history.txt` receipts for every test) gives them an **external timestamp only from 14 November 2026**. The author dates inside those histories are self-attested.

| Test | What it asked | Verdict (after review, where one exists) | Plain reading |
|---|---|---|---|
| **DECISIVE / banks** | Does slower correction raise failure risk at fixed shock and buffer? (7,837 banks, 2008–14) | **Sign-only, not a HIT; PROXY-FAIL (CLAIM_MAP H11)** | β = +0.20 [0.11, 0.29], ≈ 15% higher hazard per doubling; adds to the Z-score. The sign holds only for detrended τ; the specified own-mean τ is null. The exact identity, ε_B = −ε_σ and the horizon test all failed on this proxy. |
| **DECISIVE / glucose** | Fixed-spread sign (224 adults with type 1 diabetes) | **Sign right, size off; MATH_ATTACK literal joint kill fires on the full sample** | Slope −0.46 vs implied −0.82 and literal −1. Collapse across cohorts failed on proxy (CLAIM_MAP H12 PROXY-FAIL). The test's own prereg, scored against a lowered sampling-corrected target, does not kill; those targets rewrote the kill rule after MATH_ATTACK wrote it. The cold regime is not evaluable (n = 2). |
| **DECISIVE / populations** | Fixed-spread sign (274 GPDD series) | **MATH_ATTACK literal joint kill fires on any reading** | Slope −0.21 vs −0.34. Cold-regime slope has the wrong sign, where the theory says the effect should be strongest. The test's own prereg against the sampling-corrected target does not kill, but those targets rewrote the rule. The result is fragile (half the series are fur-harvest records; source fixed effects, taxon clustering, or dropping clipped series remove significance) and should not be cited as support. |
| **F1** | Same index on ≈ 4,100 US public firms | **Inconclusive; not a theory-specific hit** | All four directions held; the main link is published. τ mostly measures fixed-cost share (operating leverage), not correction speed, so construct validity fails. The novel interaction p = 0.055. Data prefer a τ weight near 1 over ½ (suggestive only). The prereg kill rules did not fire. |
| **C3** | Same index on 896 open-source projects | **Inconclusive / miss** | τ added nothing; the design could not have seen it. It rejects the reset-clock mechanism at that scale (predicted ≈ 11× per doubling, measured ≈ 1.0). |
| **BIO1** | Drift matching at biological scales (literature) | Kill not triggered; one contradiction | Holds, but almost entirely as prior art. The neural slope ≈ 1 comes from periodic switching, which v1.4 places outside the spectrum map. |
| **COLLAPSE1** | Memory time vs world time across substrates | Mixed (two proxy fails, weak passes) | The immune "contradiction" was largely a measurement-age artifact under power-law waning. Code re-edit need decays as a power law (≈ 0.6). |
| **MATCH1** | Need vs memory exponents in the same system; freeze-or-hold | Match **failed on proxy** (H2 PROXY-FAIL); freeze-or-hold **passed on proxy** "town-level measles recurrence" (H9 PROXY-PASS; substance prior art, Mayer et al. 2016); layer count inconclusive | News memory 0.24 vs need 0.71. Measles antibodies stay nearly flat (0.11) while measles-return odds fall at 2.15. Need exponents 0.6–0.8 replicate across code, Wikipedia and news. The redness correlation had the opposite sign to the prediction; v1.4: that prediction was mis-derived (CLAIM_MAP H19). |
| **DRIFT1** | Is drift scale-free? | Kill not triggered | City 311 looks scale-free; Wikipedia and filings have cadences. Supports T7 only as a conditional claim. A person-scale arm is withheld (`tests/DRIFT1/REDACTION.md`). |
| **ANTS1** | √N trail fade (simulation) | Finished 15 Nov; passes by construction (G13–G14 NOT EVIDENCE); three locked in-model failures (G15–G17 SIM-FAIL) | `reviews/night1/ANTS1_WRITEUP.md`; limits √N pooling to linear readouts |
| **C3b** | Exogenous shocks in open source | Not finished; the MV10 power gate is not met at the largest n the frame supplies, so it cannot give a verdict as preregistered (`reviews/night2/C3B_GATE_ADDENDUM.md`) | — |

**Overall (following the DECISIVE/F1 review):** the numbers reproduce and every sign is right. That is not enough. The τ (time-to-fix) term as a theory-specific claim **failed on these proxies** under MATH_ATTACK's literal joint kill rule (CLAIM_MAP K4 PROXY-FAIL): it fires for populations on any reading and for glucose on the full sample; banks are sign-only, not a hit. "Fewer crossings at fixed spread with slower correction" follows from dimensional analysis and standard first-passage results (Siegert 1951; Black–Cox 1976). The theory-specific structure — the −1 exponent, the √τ weighting, the identities, the τ-buffer interaction, and one collapse curve — failed on these proxies (H11–H15 PROXY-FAIL; out of scope for the structural core). F1's τ mostly measures fixed-cost share. The lowered sampling-corrected targets rewrote the kill rule after it was written; this scoreboard leads with the literal verdict. C3 rejected a fixed-clock version. Reading the missed exponents as "½ is the single-timescale special case of the spectrum relation" is post hoc and must be tested in its own right.

## Repository layout

```
THEORY.md         The theory, v1.4.27 draft (start here)
STATUS.md         Where the work stands (rewritten, not appended)
BRIEF.md          Plain-words brief of the whole record, checked against the files
QUEUE.md, queue/  Live work queue and ledger
measurement/      FRAMEWORK (gates MV1–MV10, tiers, anti-rescue rule) and CLAIM_MAP_v2 (one status per claim)
tools/            check_consistency.py (versions, wording, statuses, tally, tables, review independence)
theory/           Theorem notes, the math attack, and their code checks
tests/            Preregistered tests: predictions, code, results (raw data excluded)
litmap/           Literature map, prior-art table, threats, and DOI verification
reviews/          Hostile and independent reviews (independence stated per file), and the lock audit
applications/     How this theory is applied (AI memory; Looper; ants) — no personal data
LICENSE.md        CC0 1.0: public domain, free for any use
```

## Applications (separate from the theory)

- **AI memory**, worked out as math and a toy simulation in the public repository [`Chad-Mitchell/adaptive-memory-levels`](https://github.com/Chad-Mitchell/adaptive-memory-levels). That repo is one application. It is not this theory, and its toy results are not evidence that the theory is true.
- **Looper** is a personal-assistant application of the same hypothesis. It is developed separately. This repository does not contain Looper code, store contents, or any personal data.
- **Video:** a new explainer is on hold while the theory is finalized. An earlier draft (v7) was removed on 18 November 2026; it is in Git history.
- **Ants:** the field-literature check is in BIO1; a code-ant simulation of the √N claim is ANTS1 (finished 15 Nov; `reviews/night1/ANTS1_WRITEUP.md`).

## How this should be read

Do not treat locked predictions as findings, and do not treat a support that is already in the literature as a new confirmation. Formal misses and inconclusives stay on the board. This repository is public as of 18 November 2026; posts and other outside acts still need the author's go.

- AI agents (Grok Bot; the author's assistant is named Ace) helped draft, compute and review these files under the author's direction. Every claim status is in `measurement/CLAIM_MAP_v2.md`.
- `tNNNN` tags are turn ids in the author's working log. Review and lock records dated before 18 November 2026 say "private" because the repository was private then.

## License

Public domain under CC0 1.0 (`LICENSE.md`): anyone may use, change and share any of this for any purpose, without asking or crediting.
