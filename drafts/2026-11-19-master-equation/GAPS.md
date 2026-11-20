# GAPS: everything between the locked claim and a by-the-book theory, ranked

Written 19 Nov 2026, about 11:00 PM ET. Read-only. Locked claim (Chad, t1969, wording updated t1971; verbatim): **"the claim is that one cost under the second law sets how adaptive systems should be built at every scale: layered, with the layers at the world's time scales."** Parts C1–C6 are defined in `LEDGER.md`.

**Ranking.** Gaps are ranked first by whether the claim fails without them closed (load-bearing), then by how cheaply they could be closed. "Closes with" names the smallest piece of work that would close each one.

## Tier 1: load-bearing, and the claim is not by-the-book until closed

| # | Gap | Kind | Part | Load-bearing? | Closes with |
|---|---|---|---|---|---|
| G1 | **No valid measurement of a tracked world's drift spectrum showing many timescales.** DRIFT1 measured event-rate distributions across items, not drift q in time (fails MV2). The 311 scale-freeness is across complaint categories after post hoc dequantization, and its hourly series breaks near 22 h. The only validated α (DGS10) is 2.00, a single-layer world (L1). | measurement | C6, C5 | **Yes.** "Layers at the world's time scales" needs the world's time scales measured | Run the repo's own Whittle/aliased-power-law estimator (`measurement/estimators/aqn.py`, MV-gated) on 3–5 *tracked* quantities at different scales (a cell signal, a person's task load, a firm's demand, a city's 311 *per-category* time series). Report the spectrum, corners and lines, not just α |
| G2 | **No real system's layers have been compared with its world's spectrum.** N13 and N4's kill ("store count rises with span and stakes/upkeep") are untested; MATCH1 C1 (layer count) was inconclusive | measurement | C5, C6, C3 | **Yes.** It is the empirical content of the whole claim | One same-system test: measure the spectrum (G1), stakes and upkeep, predict layer count and timescales, then compare. Candidates already named in the repo: SAME-SYSTEM-AQN; neural intrinsic timescales (Murray et al. 2014) against stimulus spectra |
| G3 | **Stakes w have never been measured validly** | measurement | C3, C5 | **Yes.** R = wE/h decides whether layers pay (L2) | Exogenous variation in error cost (the repo's STAKES_EXOGENOUS / CAISO designs) |
| G4 | **Layers beat flat is proved only for linear-Gaussian trackers with squared error** (PROOF_A L1–L3, new and unreviewed). There is no result for jump worlds, Bayes trackers, other losses or the ruin objective | proof | C5 | **Yes,** for "at every scale" (most real change is jumpy) | Extend L2 to the two-state switching world already solved in the repo (v1.4.29 l.116); one outside reviewer for L1–L4 |
| G5 | **Stores vs agents.** The math proves separately timed *trackers*. Whether they must be separate *agents* depends on separable reads (Prop 9: indivisible reads ⇒ no clock gain) and on the member axis (N > N\*) | proof / framing | C5 | **Yes,** if the claim is read as "layers of agents" | State the two axes explicitly ("Two axes, one rule", v1.4.29 l.182). Prove the joint version: a nested tree with a time spectrum per scale (formal Thm 7 + L2) |
| G6 | **CX1: "when judgment pays" is proved only for stationary worlds**, while every layer result uses drifting worlds | proof | C2 | **Yes.** It links the X-post opening to the layers | Data-rate bridge (Nair & Evans 2004) for Gaussian random walk/fBm, or restrict the claim's C2 to stationary-increment worlds with a stated premise |
| G7 | **Selection near optimum is assumed, not shown** (THEORY §2.1 "Selection", l.34; Alchian 1950) | assumption / measurement | C3 | Yes for the *descriptive* bet; **No** for the normative "should be built" | Keep "should" normative (a design theory), and test "are built" separately (G2) |
| G8 | **No outside or human reader.** Each theorem has been refereed at most once, by the same bot family; no review covers the whole | review | all | **Yes,** for "by the book" | Two human readers (control/estimation; theoretical biology or organization economics), with Chad's go (a standing constraint) |

## Tier 2: load-bearing for parts of the claim; partly closed

| # | Gap | Kind | Part | Load-bearing? | Closes with |
|---|---|---|---|---|---|
| G9 | **Rate of the layer count** K\* ≈ (ln 8R/2π²)·ln(stakes/upkeep) is a CONJECTURE (referee: the squared rate is unproved for this kernel; an O(ln ln R) term is dropped) | proof | C5, C6 | Partly (the count, not the existence) | Prove for the completely monotone kernel, or state K\* ∝ ln·ln as a numerical regularity |
| G10 | **"At the world's time scales" is approximate.** Each layer runs faster than its mode (L2's b_j, shifted by sensing noise). In scale-free bands spacing is roughly log but not exactly (LAYERS1 P2 SIM-FAIL; PROOF_A Exp3) | proof / framing | C6 | Partly: the wording must say "one layer per separated scale, timed by scale and noise" | A closed form for b_j vs a_j (two-mode case is a quadratic); a short note |
| G11 | **J16: the booking is fixed by definition**, but whether any level needs a fourth cost (coordination, legitimacy, politics) is untested | booking / kill rule | C1 | **Yes** for "one cost" | Name one level per scale and book every cost from an actual budget (cell ATP, firm P&L); the kill is a cost that cannot be booked |
| G12 | **"Under the second law" above the cell:** floors are slack by 10⁵ or more; the open disagreement (THEORY l.52) | framing / measurement | C2 | Partly. The claim survives as "floors + same form", not "heat drives firms" | The cell test THEORY l.52 names (physical price per nat and precision exponent measured in one cell type) |
| G13 | **Formal Thm 7 class A thin** (no levels formed at n ≤ 2¹⁴); depth avalanches only numerical (F6) | proof | C5 | Partly | Larger runs; a proof of P7.1 |
| G14 | **Size of the time-axis gain is modest** (flat penalty 0.2–5% in scale-free bands, ≤ about 20% in the scans; ≤ 29% for an extra clock) | proof / framing | C5 | Partly: it caps how forceful "layered" can be on the time axis alone | State it. The big multipliers are pooling (∝ N), the lookup cliff, and ruin margins (Theorem P: a few % can flip viability), which still need a joint statement |
| G15 | **Real-world fractality premise.** The literature shows wide 1/f-like bands broken by cycles and cadences (VERDICT §(i)) | evidence | C6 premise | Partly. The claim needs "many timescales", not "fractal" | Keep the premise at "many separated or continuous timescales" |

## Tier 3: not load-bearing, but needed for a clean paper

| # | Gap | Kind | Closes with |
|---|---|---|---|
| G16 | Notation clashes: κ (price per nat vs drift-sharing exponent in formal Thm 7), γ/H in T7c, z inverted in GENERAL_THEOREM | framing | One notation table across `theory/` |
| G17 | v2.0 dropped T7, Thm 6, Thm 7, the store count and "two axes" (LEDGER §7) | framing | Restore as the layer section |
| G18 | Prior-art search is not exhaustive (Willsky multiscale trees, Meagher–Orbay–Van Zandt 2001, Kashtan–Alon 2005, Watson et al. 2014 are close) | review | A targeted search on "optimal hierarchy matches environmental timescales" |
| G19 | The lead X-post prediction (K4) PROXY-FAILED and is off the layer spine | framing | Say so plainly; do not lead with it |
| G20 | Rule 6 (use and fade, "no one in charge") does not follow from the cost | framing | Mark it as a hypothesis |
| G21 | Locked simulations: 6 fail, 3 pass, 3 inconclusive (THEORY l.165) | evidence | Report as is; no re-scoring |

## What "by the book" would look like when closed

1. A **theorem section** with L1–L4, formal Thms 1, 6 and 7, T7 and LAT-1, reviewed by one outside expert (closes G4–G6, G8–G10).
2. A **measurement section** with spectra of 3–5 tracked worlds by the gated estimator (G1).
3. **One same-system test** of predicted against actual layer count and timescales (G2, G3).
4. A plain list of what would kill it (G11 and the N4 kill).
