# NOTES_SO_FAR: sources for a "layers" section (read-only notes; no THEORY edits)

Written 19 Nov 2026, about 9:55 PM ET, from a clone of origin/main at 5b65c1e (THEORY v2.0). This is a scratch file in /workspace/gtao-v21 on branch v2.1-layers. It is not committed. Nothing was edited, pushed or merged.
Baseline on this clone: `tools/check_consistency.py` gives RESULT: PASS (main text 4,729 words, cap 5,500; README 561, cap 900; Appendix C has 31 rows, matching 31 in CLAIM_MAP §O). `pytest` gives 51 passed (137 s).

## 1. Self-similar architecture: theory/THEOREMS.md T7 (lines 175–204)
- Header: "PROOF of three conditional propositions; FAILS as an unconditional claim".
- **T7a** (l.179, proved, known): the cost of using interval T instead of T* depends only on T/T*: penalty cosh(ln(T/T*)) − 1. This is the α = 2 case of THEORY CT13, (k + 1/k)/2.
- **T7b** (l.181–186, "Roundy-type, known in substance"):
  - Setting: items with natural intervals spread log-uniformly over log-span L, served by K shared clocks, each with upkeep h.
  - Penalty of a level of log-width Δ set at its log-center: φ(Δ) = (2/Δ)sinh(Δ/2) − 1.
  - Equal log-widths are optimal for fixed K, because ψ(Δ) = Δφ(Δ) = 2 sinh(Δ/2) − Δ is strictly convex (Jensen). The levels are therefore geometric, with ratio e^{L/K}.
  - At ratio 2 this gives 2.01% mean and 6.07% edge penalty, the same integral as Roundy 1985 (whose 1.02 is a worst-case bound).
  - Unstated premises I noticed:
    - items are weighted equally, in relative penalty;
    - the proof uses the α = 2 (cosh) penalty only. At other α the CT13 penalty is asymmetric, and equal widths are not proved there.
  - The level count K* ≈ (C·L²/(12h))^{1/3} is **superseded/withdrawn** (l.186, l.197; CLAIM_MAP K12).
- **T7c** (l.188–192, elementary proof): closure under aggregation. Sums of independent random walks are random walks. If a unit's check cost ∝ n^γ, its stakes ∝ n^δ and its aggregate drift variance ∝ n^{2H} (H = ½ independent, 1 fully shared), then **T*(n) ∝ n^{(γ−δ)/2 − H}** (α = 2, square-root rule). Note that γ and H collide with THEORY Appendix A notation.
- **What fails** (l.199–204, 19 Nov erratum: conditions are *sufficient*, necessity not proved; "only if" was replaced). Self-similarity needs all three of:
  1. scale-free drift (mean reversion, seasonality or regime lengths break it);
  2. costs that are power laws in size (fixed setup costs break it);
  3. the same loss form at every level.
  The text calls T7b "close to tautological … the optimal architecture inherits whatever scale structure the world has". Calendars are not evidence.
- Testable forms (l.194–197): (i) the same drift exponent at every level; (ii) one straight log(interval) vs log(size) line; (iii) geometric cadences under a log-uniform spread.
- CLAIM_MAP **K12** (l.335): "Geometric layers iff scale-free drift; level count", **MATH-CORRECTED**. **G20 LAYERS1 P2 span invariance: SIM-FAIL** (l.239), a locked in-model fail, 6/12.
- `theory/REACH.md` §3 items 1–6 (l.155–162) already state the "layers of agents" claim with the right conditionals. It says "time is fractal" is withdrawn (N46), while the claim about *the spectrum of change of the tracked world* stands conditionally.

## 2. Which scales carry a level: reviews/night1/formal/THEOREMS.md Theorem 7 (l.256–281); checks/s6_depth.py, .out
- Setting:
  - members sit in a nested tree, with groups of size n_s at scale s;
  - drift at scale s is q_s = q₀·n_s^{−κ}. This κ is a drift-sharing exponent, **not** THEORY's κ (price per nat);
  - a level costs (N_tot/n_s)(φ(n_s w, q_s) + h);
  - the level technology is P(a, b), and member costs are concave.
- κ* = (1−a)/(1−b) = 1/|e_g|.
- (a) Exact ordering:
  - if c̃(n)/q(n) is decreasing, optimal sets are upper sets (**top-down**); if increasing, they are lower sets (bottom-up);
  - at h = 0: **top-down iff κ < κ\***, bottom-up iff κ > κ*;
  - at h > 0: top-down if κ < min(κ*, 1), and bottom-up if κ > max(κ*, 1).
- (b) κ* = 1 for reset reads (R1) and Kalman/info (R2); κ* = 1/(1+θ) for priced precision A_θ. So κ = 0.7 gives top-down with reset sensing and bottom-up with averaging sensing.
- (c) First-order location rule: sufficient only (F9 iff KILLED → F10).
- The proof is an interchange argument on the mean of ψ′.
- Checks: 0/120 and 0/150 non-upper sets. Class A was thin (no levels formed at n ≤ 2¹⁴).
- Prop 7.1 depth avalanches: NUMERICAL only (F6 OPEN).
- CLAIM_MAP rows (§F, l.195–199):
  - F7 T7(a) PROVED (in-model); κ has a measurement procedure in FRAMEWORK §3.9, spec §6.5;
  - F8 PROVED (h = 0 only);
  - F9 MATH-CORRECTED;
  - F10 PROVED;
  - F11, "knife edge κ = 1 in general", MATH-CORRECTED (true only for a = b).
- M1 (l.350): the rank-gradient a − κb coincides with T7's top-down condition for class R; not independently reviewed.
- Related: **Theorem 6** (l.223–252), with rows F1–F3, F5:
  - levels are complements (submodular);
  - the lattice: as upkeep falls, levels are only added;
  - stakes accretion;
  - **cheaper lookup can dissolve levels** (counterexample).

## 3. Store count ("old N4") and the one-store knife edge
- `reference/THEORY_v1.4.29.md` l.85 (§1 N4 row) and l.127 (§2.2 store row):
  - finitely many exponential stores are exact iff the spectrum is rational (KNOWN);
  - otherwise K* ≈ (ln 8R/2π²)·ln(stakes/upkeep) for span R. The **rate is conjectural**, numerically supported within about 10–25%;
  - one store suffices iff ψ·c(α−2)² ≲ 1 (in-model, leading order near α = 2), where ψ = stakes·error/upkeep and c depends on span and store model: about 0.18 as α → 2 for one EWMA with no free taps, and 0.005–0.11 with four taps;
  - the kill: the store count does not rise with measured span or stakes/upkeep where α ≠ 2.
- CLAIM_MAP K12 row (l.335) and the v2.27 note (l.95) give the constants.
- `reviews/night2/SPECTRUM_MAP_REFEREE.md` §4 (l.84–108):
  - exactness iff rational is CONFIRMED (KNOWN);
  - the Braess–Hackbusch rate is verified for 1/x, but the kernel differs, so the squared rate is a CONJECTURE;
  - the ln(stakes/upkeep) short form drops an O(ln ln R) term;
  - K* ∝ ln span·ln(stakes/upkeep) is prior art (Jiang et al. 2017, doi 10.4208/cicp.OA-2016-0136; Benna & Fusi 2016);
  - the measured K* (2, 3, 3, 4) is too coarse to show linearity in ln R.
- In THEORY v2.0 this survives only as one clause in Lemma B2 (l.316): "the number of stores grows with the span … (rate conjectural)".
- v1.4.29 l.182, "Two axes, one rule": levels lie across members, stores lie across timescales, and both come from the same cost comparison. The file says that is "the only sense in which GTAO is 'fractal'".

## 4. Shared-level onset: T3a / Result 4
- `theory/THEOREMS.md` T3a (l.69–80):
  - nested is cheaper when √N·√(2cwq_u)·[√N(√(1+ρ) − 1) − √ρ] > h;
  - at h = 0: N > N* = (√(1+ρ)+1)²/ρ ≈ 4/ρ;
  - this is a sufficient condition, not a cutoff;
  - it assumes the driver can be read from its own source.
- T3b clocks: at most 29% saving. T3c (NUMERIC): decoupled nesting is near-optimal only with time-scale separation, and loses when scales collapse.
- Formal Theorem 1 (l.56–90): the exact iff within 𝒜₁, N* = [ρ^b/((1+ρ)^b−1)]^{1/(1−a)}, small-ρ exponent −(1−b)/(1−a), upkeep dichotomy, scale effects, and mixed technologies (the level's class sets e_g).
- THEORY v2.0 already carries this as Result 4 = CT14–CT16 (§5.3, Appendix B.4, l.318–348). CLAIM_MAP B1–B3, B9, N12, CT16.

## 5. DRIFT1 (tests/DRIFT1/RESULTS.md; CLAIM_MAP H20 OPEN; FRAMEWORK §4.9 l.524–528)
- It measured **event-rate distributions, not target drift q**. That fails MV2 for T7's condition, so FRAMEWORK calls it "weak support".
- NYC 311:
  - per type×board rates are SCALE_FREE **only after post hoc dequantization** (the prereg'd verdict was BUNCHED). They form a plateau over 2.5 decades (q05–q95) and 3.2 decades (q01–q99), and the text asks for "a second reader";
  - 185 complaint types are about 4 decades log-uniform (post hoc, small n);
  - **in time the hourly series is NOT scale-free**: a break near 22 h (slopes −0.48 / −1.49). So 311 is scale-free *across items*, not in time.
- Wikipedia: per-article rates are NARROW (characteristic, about 1 edit / 160 days). The aggregate stream is a single 1/f^0.34 over 3.6 decades, with one non-calendar peak at 7.8 h.
- SEC EDGAR: NARROW (regulated cadence, about 1 filing / 6 days), with a broken spectrum and calendar harmonics.
- GitHub: not shown (floor-truncated).
- Person-scale arm: withheld.
- Verdict in the text (l.47–54): "no domain passes both"; evidence for T7's *conditional* statement, against "fractal at every scale". One author, no blind review.

## 6. Other repo evidence on how widespread scale-free change is
- `litmap/LEFT_ON_THE_TABLE.md` #1 (l.27–46) cites these as prior art. I checked only their DOIs, not their content:
  - environmental variability is a red/1/f continuum (Huybers & Curry 2006 Nature 10.1038/nature04745; Vasseur & Yodzis 2004 Ecology 10.1890/02-3122; Inchausti & Halley 2001 Science 10.1126/science.293.5530.655). DOIs are verified in `litmap/verify/VERIFIED_DOIS.txt` l.39, 154, 123;
  - power-law need and retention (Anderson & Schooler 1991);
  - geometric store cascades (Fusi et al. 2005; Benna & Fusi 2016);
  - log-spaced optimal memory (Shankar & Howard 2013; LITMAP l.208).
- `litmap/THREATS.md` B1 (l.55–62): the neural adaptation slope of about 1 (Fairhall 2001; Wark 2009) is an anomaly for single-timescale theories and points to the scale-free branch. This is an unchecked reading, and any rescue must be preregistered.
- Rows that are NOT evidence or are proxy-only:
  - CLAIM_MAP N4 (SELF P1, item change scale-free): OPEN, regime not established; burstiness ≠ a scale-free spectrum;
  - FRAMEWORK §4.9: the D1/E1 need exponents measure use recurrence, not drift (NOT EVIDENCE);
  - the GTAO estimators (`measurement/estimators/RESULTS*.md`) estimate α on DGS10/VIX series. I did not read their α values.
- No valid (MV-gated) measurement of a scale-free drift spectrum q(τ) in a tracked world exists in the repo.

## 7. Wording constraints found
- THEORY v2.0 §9 l.184 says "time is fractal (N46, withdrawn as framing)". N46 (CLAIM_MAP l.406) itself says "the fractal-time claim is conditional on a scale-free world (T7)". The bare §9 line is the one Chad objected to.
- REACH §3.3 says "THEORY §1 N4 withdraws the 'iff scale-free' layering claim" (v1.4.27).
