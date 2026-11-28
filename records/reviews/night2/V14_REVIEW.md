# V14_REVIEW — hostile independent review of the THEORY.md v1.4 rewrite

Reviewer: Grok Bot executor `v14-review`, for Chad Mitchell via Ace. Sunday 15 November 2026, about 9:55–10:30 AM ET (America/New_York).
Prompted by Chad (t1916): "Please be extra, extra sure before you do a full rewrite of the theory … tread carefully. Causal first principles take."
Object: `THEORY.md` v1.4 (merge `a1d7e02`, PR #12) against v1.3/v1.3.1 (`120c309`). Also read: the full diff (13 files), `reviews/night2/SPECTRUM_MAP_REFEREE.md`,
`reviews/night2/SPECTRUM_MAP/` (README, priorart/NOTES), `measurement/CLAIM_MAP_v2.md` v2.2→v2.3, `reviews/night2/LEARNSIM_REFEREE.md` §7–9,
`reviews/night2/AUDIT_DIVERGENCE.md`, `STATUS.md`, `reviews/night1/formal/THEOREMS.md`, `reviews/night1/REVIEW_MATH.md`, `theory/INTERNAL_MODEL.md`.
The author's `THEORY14_checks/SUBCHECK.md` was **not** relied on. Independent check script: `V14_REVIEW_checks/n12_independent.py` (+ `.out`), run at nice 19.
Private. Nothing posted, sent or made public. THEORY.md was **not** edited; this file recommends edits.

## 0. Verdict in one paragraph

**Keep v1.4, with targeted fixes. Do not revert.** About three quarters of the substantive changes are required by verified evidence (the spectrum-map
referee's §1–§8 list, LEARNSIM referee §8, CLAIM_MAP v2.2), and reverting to v1.3 plus only those changes would reproduce most of v1.4's text anyway.
The causal core survives: v1.4 still says that one budget (holding memory, prediction error including lateness, reads/effort, plus ruin) governs
every level; that the world's drift spectrum and the prices set the optimal design exponents; and that the cross-scale bet is open. What changed honestly
is who gets credit for the *mathematics* of the time axis (classical filtering and approximation theory), which the referee verified and I re-checked
by spot-resolving every new DOI (§5). But the rewrite has **six real problems**, two of them substantive:
1. **Overclaim (new, unrefereed): "the formal layer's exponents do not depend on α".** The algebra is right for the pooling-onset exponent (and so the
   ordering threshold κ\* = 1/|e_g|) and for the small-share vigilance exponent in ρ; I confirmed it independently. It is **false** for the vigilance growth
   exponent (V ∝ N^a, a = 1/α for reset reads — which v1.4's own §6 states, so the file contradicts itself) and for the mixed-technology private-drift
   exponent e_u = (1−b_m)/(1−a_L) = θ + 1 − 1/α. It also silently assumes shared and private drift have the same α.
2. **Mischaracterization (J16): "the 'same three costs' framing is true by construction and is not itself testable."** That is true of the *model's
   Axiom 5*, not of Chad's claim about the world. As a claim about real systems it has testable content (sufficiency: no fourth cost is needed at any
   level; each cost is separately measurable and its price moves design as the relations require). Putting "not testable" in §0 understates the
   theory's central cross-scale claim. It should be reworded, not deleted.
3. **The causal test was dropped.** v1.3's N6 and §9 killed the theory if "the design exponent does not move when the environment's measured spectrum
   moves" (a comparative-statics, i.e. causal, test). v1.4 replaced it with a cross-sectional "sits near the optimum" test whose kill needs two systems
   *and* a rival fitting better. Optimality-at-equilibrium is a weaker, harder-to-kill claim than the causal one. Restore the causal sink alongside it.
4. **Understated scope (Regime C dropped from the headline and from N6).** The model-size result (∝ Q^{1/β}, interior budget-share minimum iff β < 1,
   minimum viable size) was untouched by the referee and is still PROOF under assumptions, yet §0 now reads as if everything spectrum-related is classical.
5. **Missing credit for the new headline bet.** "Real systems sit near the filtering optimum once inputs are measured" is, for single sensory systems,
   established prior art (optimal adaptation: DeWeese & Zador 1998; Wark, Fairhall & Rieke 2009 — the same Wark paper v1.4 cites as data). The open,
   un-found part is the cross-substrate version. v1.4 must say so, or the new headline overclaims in the opposite direction from the old one.
6. **The power-law-need view is left orphaned.** v1.4 correctly separates need hazards from tracking kernels but never says where Chad's
   power-law-need view now lives (the keep rule, §3 rule 2, an item-memory object). Read quickly, v1.4 looks as if it discarded it.
Smaller issues: MATCH1 A1 relabelled "not a GTAO prediction" (retroactive; reword); §1's "not found in prior art" heading now contains prior-art rows;
N7 lost a proved clause; changelog out of order. Exact text for every fix is in §3.

## 1. What the theory claims causes what (first principles), and whether v1.4 preserves it

Causal chain (THEORY §2.1, CLAIM_MAP J15): the world changes → held information decays → re-buying it costs reads/precision/upkeep; error and lateness
cost stakes; ruin ends the system → selection or design keeps the cheapest solvent allocation → **design quantities** (read rate, precision effort,
memory time, kernel shape, store count, model size, levels) are set by (i) the world's statistics (spectrum slope α, level q, cross-member covariance ρ,
mode spectrum β), (ii) the sensing noise N, (iii) stakes, and (iv) the prices of the three costs. Across scales, only implementation and currency change.

Three distinct things can be "the theory": (A) the **math map** from inputs to optimal designs; (B) the **empirical-causal claim** that real systems'
designs are caused by those inputs via selection (so they sit near the optimum *and move when inputs move*); (C) the **cross-scale claim** that the same
relations, with the same three cost types, hold at every level.

- v1.3 presented (A) as the "central new bet". The referee showed (A) on the time axis is classical. **Demoting (A) is required.**
- v1.4 keeps (B) but only in its equilibrium form ("sits near"); it drops the intervention/comparative-statics form. **Partial loss (fix 3).**
- v1.4 keeps (C) as J6 but labels its premise (same three costs) "not testable". **Mischaracterized (fix 2).**
- v1.4 keeps the formal levels layer (across-members axis) and adds a correct but over-generalized result about it. **Fix 1.**
So: the causal core is preserved in substance; its testable causal edge and its cross-scale premise are understated in wording. Both are repairable
with sentences, not a rewrite.

On novelty: the headline does not overclaim novelty *loss* for the tracking math (the referee's verdict "against a rival who sets up the same filtering
model, nothing here is distinctive" is right and I found nothing against it). It does understate two things that are not classical: Regime C as derived
here, and the formal levels layer's cross-scale programme (which §2.2's last paragraph mentions but §0 does not). The assembly of one measured-input
programme across substrates is a legitimate *framing* contribution, not a mathematical one; v1.4 can say that in one line (fix 12).

## 2. Table of substantive changes and verdicts

Key: **(a)** required by verified evidence; **(b)** defensible but optional; **(c)** overcorrection — discards or understates something true or still open;
**(d)** new unsupported content (or content beyond its support).

| # | Location | Change v1.3 → v1.4 | Evidence | Verdict |
|---|---|---|---|---|
| 1 | Header | "not a law … a law could emerge only if …" → "a falsifiable causal theory and nothing more. Its claims become credible only if …" | Standing rule: don't bring in "law" unprompted | (b). "and nothing more" is slightly diminishing; harmless |
| 2 | Status block | New bullet "tracking layer is classical"; sims "four" → "six" locked fails; LEARNSIM line; D3S pass marked non-discriminating | Referee §7; CLAIM_MAP G6, G9, G15–17, G20 (6 SIM-FAIL rows, checked); LEARNSIM referee §7 asked for this update | (a) |
| 3 | Status block, "Proved inside the model" | "their *exponents* do not depend on the spectrum … only their constants do" | My check: true for e_g, κ\*, small-share V; false for V ∝ N^a and mixed e_u | **(d)** overclaim → fix 1 |
| 4 | Labels | Adds ELEMENTARY; novelty sweep reference widened | Referee uses ELEMENTARY | (b), good |
| 5 | §0 headline | "central new bet: shape of the world's change sets the exponents" → "time-spectrum part is not new … classical filtering + approximation + price … GTAO's open bet is empirical" | Referee §7 (verbatim proposed wording); r1–r7 | (a) |
| 6 | §0 credits | √ memory scaling credited to Kalman/Muth, Mora & Nemenman 2019; LFK as application | Referee §5 (verified); I resolved Mora & Nemenman, LFK DOIs | (a) |
| 7 | §0 J16 sentence | "'same three costs' framing is true by construction and is not itself testable (J16)" | J16 existed in CLAIM_MAP v2 (status PRIOR ART, "definitional, Axiom 5"); FRAMEWORK §1 l.401 says the *form* is universal by construction, the relations are testable | **(c)** in §0 wording: true of the model axiom, a mischaracterization of the empirical claim → fix 2 |
| 8 | §0 | Regime C (model size, β) no longer mentioned | Referee §0 scope did not touch Regime C; v1.4 §2.2 itself says "Not affected by the spectrum-map referee" | **(c)** → fix 5 |
| 9 | "What changed" items 1–4 | Headline demoted; credit; regimes restated (A = α = 2; slope 1 and (log-span)^{2/3} withdrawn); kernels ≠ hazards; H19, N10 | Referee §§3–7, CLAIM_MAP K12, K13, H19, N10 | (a) |
| 10 | "What changed" item 5 | "formal layer's exponents do not depend on the spectrum" | as row 3 | **(d)** → fix 1 |
| 11 | §1 intro | "rows … not found stated in the prior art" retained while N1 (math PRIOR ART), N4 (PRIOR ART in form), N5 (core KNOWN) sit in it | internal | (b)/(c) wording inconsistency → fix 8 |
| 12 | §1 N1 status | adds "(K10, outside the theorem's domain)" | CLAIM_MAP K10 says "Out of the theorem's domain" | (a) |
| 13 | §1 N2 status | adds "exponent −1 for reset reads and −(1+θ) at every α"; drops Beekman remark | Algebra confirmed (§4) | (b); fine once N12 is scoped |
| 14 | §1 N3 | drops the critical-slowing-down contrast that motivated the sign; drops "−1, collapse, z-interaction all failed" from the row | §4/§8 still carry the failures | (b); optional restore (fix 10) |
| 15 | §1 N4 | "Geometric layers iff scale-free; (log-span)^{2/3}" → store count K\* ∝ ln span·ln(stakes/upkeep), PRIOR ART in form | Referee §4, K12 MATH-CORRECTED | (a) for the math; placement in a "not-found" table is inconsistent → fix 8 |
| 16 | §1 N6 | "spectrum → exponent relation … leaning against" → "measured-input optimality", kill = ≥2 systems miss AND a rival fits better | Referee §7 recommends this bet | (a) in direction; **(c)** drops the causal (comparative-statics) kill and model size; **(c)** missing prior-art credit for single-system optimal adaptation → fixes 3, 4, 5 |
| 17 | §1 N7 | drops "and its update rule must nearly mirror the world's" | `theory/INTERNAL_MODEL.md` l.23 proves it ("error at most twice that") | (c), minor → fix 9 |
| 18 | §2 title | "The core … (HYPOTHESIS)" → "The tracking layer … (KNOWN and ELEMENTARY), and the empirical bet" | Referee §7 | (a) |
| 19 | §2.1 | adds the causal chain (J15) and the three inputs α, q, N | J15 in CLAIM_MAP; referee §5 (q, N needed) | (a), good |
| 20 | §2.2 Regime A | "one pace" → "α = 2 (Markov)"; knife-edge for "one store" | Referee §4, §7; r4 | (a) |
| 21 | §2.2 Regime B table | per-row premises, α ranges, credits; precision-pricing caveat; τ_E form only at fixed variance; kernel survival τ^{−α/2}; ln·ln credited; rate conjectural | Referee §§1–5, §8 items 1–6 | (a); rows checked against the referee line by line, no discrepancy found |
| 22 | §2.2 "does not predict" | slope 1 withdrawn; "matching exponent" forgetting withdrawn; no single redness for event worlds | Referee §3, §5, §6, R7 | (a); but see row 23 |
| 23 | §2.2 / §2.4 | need hazards declared "a different object" from kernels; no statement of where the power-law-need (keep-rule) view now lives | Referee §3 (correct); AUDIT_DIVERGENCE §1 records Chad's view "power-law need replaced the √ rule" | **(c)** by omission → fix 6 |
| 24 | §2.2 Regime C | unchanged; "√ returns for β ≤ 2" clause dropped | — | (b) |
| 25 | §2.2 "One rule, credited" | rule is classical; GTAO adds the bet and the formal layer | Referee §7 | (a); could add the framing line (fix 12) |
| 26 | §2.3 physics | "§2.5 sharpens … for the onset exponent the physics matters only through which sensing technology the floor selects … and θ" | Formal Cor 4.1: per-nat pricing → (γ, γ); per-precision → θ | (b). Accurate but reads as diminishing Chad's position; the price structure the physics imposes also sets tracking-layer elasticities (fix 11) |
| 27 | §2.4 Fairhall | "supports Regime B" → "outside the map (periodic deterministic switching)" | Referee §7 | (a) |
| 28 | §2.4 Retina | "Mixed" → "regime not established; no prediction" | inputs not measured | (a)/(b) |
| 29 | §2.4 need hazards | "world side of Regime B looks scale-free" → "re-occurrence hazards, not a spectrum slope and not a kernel" | Referee §3, R7 | (a). Optional nuance: a falling pooled hazard rules out one homogeneous Poisson rate but not rate heterogeneity across items |
| 30 | §2.4 MATCH1 A1 | "strong form fails" → "failed on proxy … Under v1.4 the locked equality was not a GTAO prediction" | Referee §3 (objects differ) | (a) for "different objects"; **(c)** for "was not a GTAO prediction" — retroactive; it *was* v1.0's locked prediction → fix 7 |
| 31 | §2.4 C1, D3, DRIFT1, F1 rows | re-read under K12, H19/N10, H20 | Referee §4, §6 | (a) |
| 32 | §2.4 Net | "direction has some support" → "no test measured α, q, N, stakes … untested, not refuted" | Every former "support" is outside the map, post hoc or a different object | (a). Note symmetry: support and failures were both reclassified; that is honest only if N6 gets a hard, locked kill (fix 3) |
| 33 | §2.5 bridge (N7) | extended to rescaling-closed predictors | Referee §1, R1 | (a) |
| 34 | §2.5 N12 | NEW: onset exponent −1 (reset) / −(1+θ) (priced precision) at every α; small-share vigilance ρ^{−θ}; "spectrum enters the formal layer only through constants" | My independent check (§4): first two confirmed; "only through constants" false (V ∝ N^a; mixed e_u); same-α premise unstated. Corrects a real v1.3 error (v1.3 said the onset exponent "moves with the world's spectrum through (a, b)", false for a = b) | **(d)** as written → fix 1. Core algebra is sound and is itself an (a)-grade correction of v1.3 |
| 35 | §2.5 "Two axes" | "how many stores … layers" → "stores"; "fractal" defined as same cost comparison | — | (b) |
| 36 | §2.5 regime-first rule | adds premise checks (exact vs noisy reads, predictor class, pricing, fixed variance vs fixed q) and "which memory object" | Referee §§1–5 | (a), good |
| 37 | §2.5 SG | Ferragut et al. 2018 named; relabel to "application" marked pending | priorart/NOTES; DOI resolved | (a) |
| 38 | §2.5 | v1.3's "What is missing" and the v1.3/v1.3.1 spectrum-map and referee bullets removed | Map now derived and refereed; history in git | (a) |
| 39 | §3 rules 2, 5 | rule 2 failure condition restated via kernel; rule 5 "Markov (α = 2)" | Referee §3 | (a) |
| 40 | §4, §8, README | "falsified/killed" → "failed on proxy" (K4, H11–H15, H17, H18) | Chad t1908 standing rule; CLAIM_MAP | (a) |
| 41 | §6 | vigilance formula scoped to α = 2; r defined; "/(rρ)" declared intended; growth N^a (a = 1/α) | I checked `REVIEW_MATH.md` l.119: the formula has /(rρ) | (a). Note it contradicts rows 3/10/34 |
| 42 | §8b | KILLED → SIM-FAIL; candidates note "exponents depend on technology, not α" | CLAIM_MAP v2 | (a) for labels; candidate-note inherits fix 1 |
| 43 | §8c | LEARNSIM G23–G29 and spectrum-map entries | LEARNSIM referee §8 recommended exactly these rows | (a). Minor: G25 recorded as SIM-INCONCLUSIVE where the referee wrote "NOT PASSED (in-model)" — v1.4 keeps "T1.8 NOT PASSED" in the text, acceptable |
| 44 | CLAIM_MAP v2.3 | new statuses SIM-PASS, SIM-INCONCLUSIVE; rows N12, N13, G23–G29 | Statuses recommended by LEARNSIM referee §8 | (a) for statuses and G rows; N12 (d) until scoped; N13 (a) |
| 45 | §9 | "spectrum relation fails twice: design exponent stays constant as measured spectrum changes" → "measured-input optimality fails twice … and a rival fits better"; new sink "formal exponent tracks the spectrum instead of technology" | Referee §7; my N12 check | first: **(c)** (causal sink removed; fix 3); second: (b) — valid given the algebra, label it in-model and unrefereed |
| 46 | §10 | 14 new citations; LFK demoted from "most important prior art" | All new DOIs resolved by me via Crossref (§5) | (a) |
| 47 | §11 | historical items annotated | — | (a) |
| 48 | §13 | v1.4 entry inserted above v1.2 (out of order) | — | trivial |
| 49 | README (theory repo) | headline and "already published" rewritten to match | follows §0 | (a), inherits fixes 2 and 5 (it is not the Looper README) |
| 50 | SPECTRUM_MAP README | erratum item 1 only; items 2–8 queued | Referee §8 | (a) |

Tally: (a) ≈ 37 rows; (b) ≈ 7; (c) 7 (rows 7, 8, 16, 17, 23, 30, 45a); (d) 3 locations of one overclaim (rows 3, 10, 34).

## 3. Exact recommended edits (THEORY.md unless noted)

**Fix 1 — scope N12 (status block, "What changed" item 5, §2.5 bullet 2; CLAIM_MAP N12).**
- Status block: replace "which also shows (elementary, self-checked) that their *exponents* do not depend on the spectrum for the two sensing
  technologies in §2.2; only their constants do." with: "which also shows (elementary; self-checked and independently re-checked in
  `reviews/night2/V14_REVIEW_checks/`; not refereed for prior art) that the pooling-onset exponent (and so the ordering threshold κ\* = 1/|e_g|) and the
  small-share vigilance exponent do not depend on α for the two sensing technologies in §2.2. The vigilance growth exponent (V ∝ N^a), the
  mixed-technology private-drift exponent e_u, and the constants do depend on α."
- "What changed" item 5: replace with: "**The pooling-onset exponent does not depend on the spectrum** for the two sensing technologies covered (§2.5;
  elementary; not refereed). v1.3's statement that it 'moves with the world's spectrum through (a, b)' was wrong for reset reads (a = b gives −1 at every α).
  Other formal exponents (vigilance growth N^a; e_u with mixed technologies) and the constants do move with α."
- §2.5 bullet 2: title "The formal exponents do not depend on α …" → "The onset exponent does not depend on α …". Replace consequence (ii) with: "(ii) the
  spectrum enters the formal layer through its constants (Π\* = b^{−1/(1−a)}: 3.38, 4, 4.61 at α = 1.5, 2, 2.5 for reset reads; the vigilance floor),
  through the vigilance growth exponent a (V ∝ N^a, a = 1/α for reset reads, §6), and through e_u = (1−b_m)/(1−a_L) when the level and members use different
  technologies (= θ + 1 − 1/α for a precision-priced level over reset-read members); it enters the tracking layer through read rate, memory time, kernel and
  store count;". Append to Scope: "; shared and private drift with the same α (otherwise the flat member's tracked process is not in the power class and the
  (1+ρ)^b structure fails)."
- CLAIM_MAP N12: same narrowing; status stays PROVED (in-model), "algebra independently re-checked (V14_REVIEW); prior art not searched".

**Fix 2 — J16 sentence in §0 (and CLAIM_MAP J16 note).** Replace "The "same three costs" framing is true by construction and is not itself testable
(CLAIM_MAP J16); the testable cross-scale content is that the same measured-input relations hold in each substrate (J6)." with:
"In the model, the same three costs at every level is an axiom (Axiom 5; CLAIM_MAP J16), so the model alone cannot test it. As a claim about real systems
it is testable through its consequences: at each level the three costs can be measured separately, and the claim fails if a level's design needs a
fourth kind of cost to be explained, or if design does not respond to the measured prices of the three as the relations require (J6)."
CLAIM_MAP J16 note: "True by construction of Axiom 5 (definitional), so not itself testable" → "Definitional inside the model (Axiom 5). Empirical
content: sufficiency (no fourth cost type needed at any level) plus J6. OPEN. Recursion qualitatively prior art (Beer's VSM)." Status PRIOR ART →
OPEN (the qualitative recursion is prior art; the three-cost sufficiency claim was not found stated).

**Fix 3 — restore the causal test (§1 N6 "How it dies"; §9).**
- N6, append to "How it dies": "Or, causally: when a system's measured α, q, N or stakes change (natural experiment or intervention), its design quantity
  does not move in the predicted direction after its adjustment lag. A miss in one system is recorded as 'failed on system X'; the theory-level sink needs two."
- §9: keep v1.4's first bullet and add back, as a separate bullet: "**The causal relation fails twice:** at two scales, with locked tests, the design
  quantity stays put while the system's measured spectrum, drift level, noise or stakes change."

**Fix 4 — credit single-system optimal adaptation (N6 status; §10).** Append to N6 status: "Single-system versions — sensory adaptation tuned to measured
stimulus statistics — are prior art (DeWeese & Zador 1998; Wark, Fairhall & Rieke 2009; Lundstrom et al. 2008). Not found: the same measured-input
relations across substrates and scales, with read rate, memory time and store count jointly." Add to §10 (Filtering block), both resolved by this review:
"DeWeese & Zador 1998, 'Asymmetric dynamics in optimal variance adaptation', *Neural Comput* 10(5):1179–1202, doi 10.1162/089976698300017403;
Wark, Fairhall & Rieke 2009, 'Timescales of inference in visual adaptation', *Neuron* 61(5):750–761, doi 10.1016/j.neuron.2009.01.019."

**Fix 5 — Regime C back in §0 and N6.** In §0 after "These are known or elementary results, assembled." insert: "The mode-spectrum part (§2.2 Regime C:
model size ∝ Q^{1/β}, an interior minimum of the model's budget share iff β < 1, a minimum viable size from unstable modes) is PROOF under stated
assumptions with known tools and was not reviewed by the spectrum-map referee." In N6 "The number": add "and model size ∝ Q^{1/β} with β measured (Regime C)".

**Fix 6 — say where the power-law-need view lives (§2.2, after "What this regime does not predict").** Add: "**Two memory objects, both kept.** A
tracking kernel weights past readings of a drifting target (this table). A keep rule decides whether to hold a recurring item at all: keep it while
need × miss cost > upkeep (§3 rule 2), where need is the re-occurrence hazard, which is power-law in the human information environments measured
(Anderson & Schooler 1991; §2.4). The power-law-need view belongs to the second object. Its GTAO-specific form (memory outlasts need when miss cost is high
relative to upkeep) is POST HOC and untested (§2.4)."

**Fix 7 — MATCH1 A1 row (§2.4).** Replace "Under v1.4 the locked equality was not a GTAO prediction: a need hazard and a retention curve are different objects."
with "The locked equality was GTAO v1.0's prediction and it failed as locked. v1.4 judges it mis-specified (a need hazard and a retention curve are different
objects) and makes no replacement prediction for this pair until a kernel, or the keep rule with measured miss cost and upkeep, is specified."

**Fix 8 — §1 heading text and N4.** Replace "These are the rows that, after the sweeps, were not found stated in the prior art." with "Candidate claims: rows
whose application, cross-domain form or test was not found stated in the sweeps. Several rest on prior-art mathematics, marked per row." In N4's status
add: "Candidate content is only the empirical bet (strongly selected systems carry about this many stores), which is part of N6."

**Fix 9 — N7.** Restore after "causal-state machine": ", and its update rule must nearly shadow the world's (error at most twice the bound; `theory/INTERNAL_MODEL.md`)".

**Fix 10 (optional) — N3.** Restore the opening contrast: "Critical-slowing-down work says slower recovery means danger, because at fixed shock size the spread widens."

**Fix 11 (optional) — §2.3 physics.** Replace "so for the onset exponent the physics matters only through which sensing technology the floor selects (reset reads
or priced precision) and, for the latter, its θ." with "so the physics enters through the price structure it imposes: per-nat (entropy) pricing gives the
reset class, per-unit-precision pricing gives θ. That choice sets the onset exponent (−1 or −(1+θ)) and also the tracking layer's effort elasticities
(α/(2α−1) holds only for linear precision pricing)."

**Fix 12 (optional) — §2.2 "One rule, credited".** Append: "Putting the levels layer and the tracking layer into one measurement programme, with the same
inputs (α, q, N, stakes, prices) measured at every level, is this project's framing. It is not a mathematical novelty, and it is the part the open bet tests."

**Fix 13 — housekeeping.** Move the v1.4 changelog entry below v1.3.1 (chronological); add "N12 scoped per V14_REVIEW" to it when fixes land.

## 4. Independent check of N12 (not the author's script)

`V14_REVIEW_checks/n12_independent.py` solves the formal h = 0 onset equation G(N) = N[(1+ρ)^b − 1] − N^aρ^b = 0 by root-finding (no closed form) and
uses the formal vigilance definition V(N) = N^a(ρ/(1+ρ))^b (equal prices), for reset reads (a = b = 1/α) and precision priced ∝ P^θ
(a = αθ/D, b = θ/D, D = α(θ+1) − 1), α ∈ {1.5, 2, 2.5}, θ ∈ {½, 1, 2}. Results (`.out`):
- onset exponent: −1.0000 for reset reads at every α; −1.5000, −2.0000, −3.0000 for θ = ½, 1, 2 at every α. **Confirms N12's onset claim.** By hand:
  1−a = (α−1)/D, 1−b = (α−1)(θ+1)/D, ratio θ+1. For reset reads it is the identity a = b ⇒ −1.
- small-share V(N\*) exponent in ρ: 0 (reset) and −θ (precision) at every α. **Confirms.**
- beyond-onset V growth: N^{0.667}, N^{0.5}, N^{0.4} for reset reads at α = 1.5, 2, 2.5. **α-dependent: refutes "only constants depend on α".**
- mixed technologies (precision level θ = 1, reset members): e_g = −2 at every α, but e_u = +1.333, +1.5, +1.6. **α-dependent.**
- Π\* (reset) = 3.375, 4, 4.605: constant, α-dependent, as v1.4 says.
Not checked: prior art for N12 (the queue item ONSET-SPECTRUM-FREE-REFEREE still owes it); whether the power class itself holds for priced precision at
α ≠ 2 beyond Cor 2′'s single tracker (it does for the cost function used, by construction).

## 5. Citations

Every citation new in v1.4 traces to `SPECTRUM_MAP_REFEREE.md`, `SPECTRUM_MAP/README.md` or `priorart/NOTES.md`. I resolved these via Crossref this
session, and title, authors, journal, volume and pages match the v1.4 text: Afterman et al. 2022 (SIAM J Control Optim 60:1463–1487); Kleptsyna et al. 2020
(Autom Remote Control 81:411–429); Mora & Nemenman 2019 (PRL 123:198101); Malaguti & ten Wolde 2021 (eLife 10:e62574); Jiang et al. 2017 (Commun Comput Phys
21:650–678); Braess & Hackbusch 2005 (IMA J Numer Anal 25:685–697); Benna & Fusi 2016 (Nat Neurosci 19:1697–1706); Bayer & Breneis 2023 (Quant Finance 23:53–70);
Ferragut, Rodríguez & Paganini 2018 (Queueing Syst 88:207–241); Lee, Flack & Krakauer 2024 (Proc R Soc B 291, rspb.2024.1606). **No invented citation
found.** The two I propose adding (fix 4) were resolved this session (DOIs above).

## 6. Recommendation

**Keep v1.4 and apply fixes 1–9 and 13 (required). Fixes 10–12 are optional.** A revert to v1.3 is not warranted. v1.3's headline is refuted as a
*novelty* claim by a verified referee, v1.3's §2.5 contains a math error that v1.4 fixes (the onset exponent does not move with α for reset reads), and
v1.3 + (a)-changes ≈ v1.4 minus the items above. Fixes 1–9 are each one or two sentences. They restore what was true or still open (the causal test, the
testable content of "same three costs", Regime C, the power-law-need view, an N7 clause) and remove the one unsupported generalization (N12's "only
constants"). They do not reopen the referee's verdict on the tracking math. Because the fixes touch §0, apply them in a small v1.4.1 PR. Check any
new sentence against this file's §2 table, not against the author's SUBCHECK.
