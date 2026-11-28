# Independent hostile review: MATH and LOGIC of `theory/BOOKENDS.md`

Reviewer: Grok Bot executor (independent; did not write BOOKENDS). Wednesday 18 Nov 2026, ~6:00–6:45 PM ET.
Scope: fresh clone of the public repo, checked out to branch `bookends` (PR #86, commit 98b7168), in /tmp/rev-math. Nothing was pushed, commented or posted.
Files read: `theory/BOOKENDS.md` (all); THEORY.md (§0 v1.4 notes, §2.3 line 128, §4 lines 180–191, §6 lines 219–221); `theory/GENERAL_THEOREM.md` §0–§2; `theory/THEOREMS.md` T3, T7 and the summary table; `theory/MATH_ATTACK.md` §3.2–§3.6; `theory/SCALE_ENDS.md` (§1, §2 E1–E3 and the class table, §3.3, §4.1, §5 notes, §6b); `measurement/CLAIM_MAP_v2.md` rows B3, B9, C1, E6, F13, H8, I14, J6–J9, J11, J16, K12, K13, N13, N24–N28; `reviews/night1/formal/AXIOMS.md` (Axiom 3 R1, Axiom 7); `reviews/night2/SCALE_ENDS_INDEP_REVIEW.md` (stars bullet).
Not verifiable from the repo: H80, H2, H8, H9 and C13(c) live in Ace's local hypothesis files, so every BOOKENDS statement about "H80's ladder" rests on those files plus SCALE_ENDS line 42. No literature was checked; this is a math/logic review.

Tooling: `python3 tools/check_consistency.py` → RESULT: PASS (FAIL 0, INFO 28; BOOKENDS is not in MAINTAINED, so it is not checked). I re-ran it with BOOKENDS temporarily added to MAINTAINED (scratch copy, deleted afterwards; the working tree is clean): PASS, 126 N-references, 0 mismatches, 0 wording FAILs. `python3 tools/test_check_consistency.py` → PASS (the planted stale pointer is caught). The other `tools/test_*.py` files exit 0 silently. Note that `pytest tools/` gives an INTERNALERROR because check_consistency.py calls sys.exit when it is imported. That is a tooling nit and was not caused by BOOKENDS.

## Verdict: **FAIL (fixable).** The three flagged repo inconsistencies and the layers/governance section mostly hold, apart from finding 9, which is a major: §1 and §3 drop the theorem's "shared fate" route to internalization. The central new claim, "models before heredity" via Theorem P (G2, class 2b, proposals P2–P5 and P7), rests on a silent switch in what "action" means. Under that switch, "model" means any survival-relevant physical correlation, which makes the result near-automatic and also makes flames and hurricanes "models", contradicting BOOKENDS' own §1. As written, it also contradicts the governing THEORY.md line 128 and N28's literal text. Fix the blockers before any §6 proposal other than P1 and P8 is applied. P1 and P8 can be applied now.

---

## Findings

### 1. [BLOCKER] Two incompatible meanings of "action", switched silently
- **Where:** BOOKENDS l.27 (§0.3), l.72 (G2 mapping "action = its state-dependent response"), l.78, l.244 (P3), l.247 (P6). Compare THEORY.md l.128 ("'action' read under Axiom 7 as an alternative that selection acts on"); SCALE_ENDS l.108 (E1), l.251 (IR-FIX10: "S2 presupposes selection"); CLAIM_MAP N25, N26 (both "conditional on the Axiom-7 reading of 'action'").
- **Problem:** The math of Theorem P's P0–P1 does use no selection axiom (GENERAL_THEOREM l.97–116: A1, A2, A5; true). But Theorem P needs an *action* A_t = π(M_t). The repo's canonical mapping of "action" onto physical systems is the Axiom-7 reading, under which an unselected system has no action. G2 swaps in "any state-dependent response" for chemistry while keeping the Axiom-7 reading for atoms and black holes (N25, N26). Under the G2 reading, atoms also have state-dependent responses, so E1 does nothing and atoms rest on E2 alone. P6 half-admits this. N26, however, is stated as *conditional on* the Axiom-7 reading, so the claim "None changes a PROVED status" (l.240, l.30) is unproven.
- **Fix:** Define two terms explicitly: **response** (physical, state-dependent; enough for Theorem P's information bound) and **action** (Axiom-7, selected; needed for design predictions). Restate G2 and class 2b with "response". Then re-derive N25/SE5 and N26 under the response reading, using E2 plus the lateness mapping, and show the classifications survive. If N26 cannot be re-derived that way, say "N26's condition changes" rather than "no status changes".

### 2. [BLOCKER] "Model" redefined so the conclusion is automatic; the criterion contradicts §1
- **Where:** l.28, l.46 ("That is already a model, the simplest one there is"), l.89, l.94, l.131, l.155; contrast l.43 ("a star, a hurricane, a flame … feedback is only on themselves").
- **Problem:** Under the G2 mapping, any structure whose survival depends on an exogenous variable it is physically driven by has I(M;X) > 0 trivially. Its state *is* the coupling. P1 then reads: "if survivors must correlate with X, survivors correlate with X." That is near-tautological once "model" means I_pred > 0. GENERAL_THEOREM itself says P is "weaker than the internal model principle on structure: it says how many bits, not that the bits must replicate the generator" (l.37), and BOOKENDS l.89 concedes the identity-map problem. Applied consistently, the criterion makes a **candle flame** (persistence depends on exogenous O₂ and fuel supply) and a **hurricane** (depends on SST, as l.94 says) class 2b/K2 "models". That contradicts §1 l.43, which lists them with stars as self-only feedback, and the K1 entry for hurricanes and convection cells in the §2.7 table (l.166).
- **Fix:** In every plain-words and canonical-wording place (l.28, l.46, l.89, P7 l.248, P9 l.250, P10 BK-b), replace "is a model / lowest rung of a model" with "carries survival-relevant (semantic) information, the information floor Theorem P requires". Reserve "model" for K3, or for K2 plus a structural condition such as the stochastic-IMP conjecture (§7 item 6). Then reclassify flames and hurricanes consistently (2b candidates, or give a criterion that excludes them) and fix l.43 and l.166.

### 3. [MAJOR] G2 needs a finite-horizon form of Theorem P; the infinite-horizon theorem cannot classify any real structure
- **Where:** l.72, l.81 caveat (c), l.155, l.244 (P3: "blind not viable, structure persists").
- **Problem:** P1 is an almost-sure, infinite-horizon statement: a blind agent with r_∞ > y − c̄ is ruined with probability 1 *eventually* (GENERAL_THEOREM l.105–106). A blind structure with reserve B survives for a time of order B/(r_∞ − y + c̄), so observing persistence for a finite time never implies I_pred > 0. Caveat (c) exempts only "transient structures whose ruin is certain anyway", but under P every blind structure is exactly one whose ruin is certain. P3's class-3 test ("structure persists") is therefore not operational.
- **Fix:** Add a finite-horizon corollary (elementary, by Azuma/Hoeffding under A5): if increments are bounded by b and the blind mean shortfall is δ = r_∞ − (y − c̄) > 0, then P(blind survives to T) ≤ exp(−(δT − B)²/(2b²T)) for T > B/δ. Survival well past B/δ is then evidence for I_pred > 0, with a stated confidence. State BK-G2's prediction in those units.

### 4. [MAJOR] The G2 mapping does not fit P's hypotheses as stated
- **Where:** l.72 ("reserve = free-energy stock; income y = influx; action = state-dependent response"), l.81(b).
- **Problem:** (i) In P, income y is a constant and only ℓ(A, X) depends on the world. In G2, the influx *is* the drifting feed, so y = y(X_t). That can be folded into the loss, ℓ′ = ℓ − (y(x) − ȳ), but ℓ′ must stay bounded below (A5) and D(·) must be recomputed. (ii) P requires A_t to depend on X *only through* M_t (the data-processing step, GENERAL_THEOREM l.102). Physical feedback responds to X_t directly unless the coupled state is declared to be M, and that declaration is what makes finding 2 automatic. (iii) A4 (one currency) is omitted from the hypotheses list at l.72, and it is used.
- **Fix:** Write the mapping as a short lemma with M, A, ℓ′, y explicit and A1, A2, A4, A5 checked one by one. Keep it marked [BK, new, unreviewed] until an independent referee has checked it (as §7 item 1 already asks).

### 5. [MAJOR] "K ≥ K2 requires P = held" is contradicted by SCALE_ENDS E3(c)
- **Where:** l.159 ("K ≥ K2 requires P = held, because holding information about drift needs an inflow (I5; E3(b))").
- **Problem:** E3(b) requires an information inflow (coupling), not paid upkeep h > 0. E3(c) (SCALE_ENDS l.59) says the price of that inflow "can approach 0 for quasi-static passive coupling", and l.62 says "Atoms are passive sensors". Only *memory beyond the instantaneous correlation* costs dissipation (l.62). K2 is defined at k ≈ 0 (reactive, instantaneous), so E3 does not force K2 onto held structures. K3 (memory, k > 0) arguably is forced.
- **Fix:** Change l.159 to "K3 requires P = held (memory beyond the instantaneous correlation costs dissipation, E3 l.62). K2 needs coupling but not necessarily upkeep; whether it is also necessary for *persistence* is decided by E2, not by E3."

### 6. [MAJOR] BOOKENDS says "N28 stands as written", but G2 contradicts N28's and THEORY's literal text; the proposal list misses THEORY l.128
- **Where:** l.77; P5 l.246; P7 l.248. Sources: CLAIM_MAP N28 ("a model switches on only with heredity …"); THEORY.md l.128 ("Models switch on only with heredity …"); SCALE_ENDS l.26, l.118.
- **Problem:** N28 is not textually about "selected, designed" models; that reading is BOOKENDS' reinterpretation. If G2 holds, N28's sentence as written is false for "model" in Theorem P's sense. P7 adds a sentence to THEORY §2.3 but leaves "Models switch on only with heredity" a few lines later, so applying the proposals as listed would leave THEORY self-contradictory.
- **Fix:** Add a proposal to reword THEORY l.128 and N28 to "*Selected* models (design optimization) switch on only with heredity …". Change l.77 to "N28 needs a wording change; its status stays OPEN."

### 7. [MAJOR] Biosphere robustness uses the wrong coarse-graining rule
- **Where:** l.133 ("DERIVED from PROVED (in-model) coarse-graining rules").
- **Problem:** The pooling rule z′ = z·√(N/(1+(N−1)ρ)) is the **pooled, fungible buffer** case and needs C2 ("buffers are fungible, with internal transfers faster than τ"; MATH_ATTACK l.243–251, l.285). Lineages do not share a fungible reserve on the fix time scale. "The biosphere dies only if nearly all lineages die" is a *redundancy* (parallel-survival) aggregation, which the repo does not derive. Separately, MATH_ATTACK labels §3.2 "PROOF + NUMERIC" and the CLAIM_MAP has no PROVED (in-model) row for it, so "PROVED (in-model)" is not the source label. A minor repo-level note: GENERAL_THEOREM l.43 and l.208 define z = σ√τ/B, the inverse of THEORY l.180 and MATH_ATTACK's z = B/(σ√τ). BOOKENDS uses the THEORY convention correctly.
- **Fix:** Relabel l.133 as HYPOTHESIS (analogy to the pooling rule). Either derive a redundancy-aggregation result, where P(all N fail) under correlation ρ also gives "fragile only to correlated shocks", or drop the formula and keep the qualitative statement.

### 8. [MAJOR] The five-step onset is presented as a sequence, which is not derived
- **Where:** l.52 ("first … then … finally systems that act ahead"), l.66–74, l.79.
- **Problem:** No result orders G4 after G3. An entrained oscillator with a phase lead acts ahead (k > 0) with no heredity, and BOOKENDS' own BK-G2 test system is an entrained oscillator. G2 also does not require G1 to be "self-maintaining" in any proved sense. l.79 rightly calls the steps three separately measurable quantities, but l.52 states a historical sequence as fact without a label. Two smaller points: k_max (P2) is a property of the world and the budget, a ceiling rather than "usable lead time" that "rises"; and G4's "a model pays for lateness only when … (P2)" mixes up P2 (viability ceiling) with P3 (pays).
- **Fix:** Label l.52 HYPOTHESIS (the H2 conjecture), and say the axes are partially ordered rather than a ladder. In l.74, change "pays" to "can be viable", and in l.79(iii) use the realized lead k rather than k_max.

### 9. [MAJOR] The governance inference drops "shared fate" (relevant to the ants example)
- **Where:** l.54 ("wherever shared knowledge is a public good, expect someone to be in charge: a monitor, a rule or an owner"), l.187 item 7 ("So governance appears…"). Source: MATH_ATTACK l.273: the whole's failure cost is internalized "by incentives, **shared fate** or a central controller".
- **Problem:** The PROOF covers under-watching. It does not cover enforcement as the only remedy. Shared fate (for example colony-level selection in sterile-worker insects) internalizes Λ_whole without anyone in charge. Item 7's "So" turns OPEN J9 into an apparent consequence. A second gap: MATH_ATTACK's externality is about a part's *own failure hazard* affecting the whole. Reading it as "parts under-watch *shared memory*" (l.186) is an extension that should carry the [BK, new] tag.
- **Fix:** In l.54 and l.187, write "expect either shared fate or enforcement (monitors, sanctions, owners)", keep J9 OPEN, and replace "So" with "Hypothesis:". Tag the shared-memory reading of §3.4 as [BK, new, unreviewed].

### 10. [MINOR] The predictor ladder's order contradicts the K axis, and "frozen" is used in two senses
- **Where:** l.96 ("keep a constant, then run a clock, then react, then predict") versus l.149–150 (K2 = react < K3 = timer/anticipation); l.91, l.145, l.163.
- **Problem:** In H80's cost ladder the clock sits *below* react, while on the K axis it sits *above* it. "Frozen" names a persistence mode (h = 0, axis P), a T8 memory tier (a stored fact with I > 0 that decays), and H80's constant-predictor rung, which as a true constant has I_pred = 0, the "blind" agent of P1 (compare GENERAL_THEOREM's bet-hedging counterexample, l.117–119). l.91's identification of H80's bottom rung with the T8 freeze corner holds only under the second sense.
- **Fix:** Say explicitly that the H80 ladder orders cost and the K axis orders lead time, so they are different orders. Rename the senses: "frozen structure" (P axis), "frozen store" (T8), "constant predictor" (H80).

### 11. [MINOR] R1 is not "exactly" continuous feedback
- **Where:** l.89, l.149.
- **Problem:** Axiom 3's R1 is discrete, costly, *exact* periodic reads with zero-order hold between them (AXIOMS l.54). A thermostat or albedo feedback is continuous and noisy. At best it is a limit of R1 (read interval → 0) or closer to R2 (λ per nat).
- **Fix:** Change "exactly the base sensing class R1" to "analogous to R1 in the limit of frequent reads; its cost class must be assigned separately".

### 12. [MINOR] Labels not kept exactly as the sources state them (BOOKENDS' own rule, l.16)
- **Where:** l.27, l.155: "Theorem P (PROVED (in-model))". GENERAL_THEOREM labels P0 "[PROOF; the ingredients are KNOWN]" and P1 "[PROOF]", and there is no CLAIM_MAP row for Theorem P. l.133: see finding 7. l.184: K12's store count is stated without THEORY N4's "rate conjectural". l.187: "Its quantitative version is PROVED (in-model) (E6)". E6 is "Exact V(N*) formula with upkeep and price" and is not a fractal-vigilance statement, while J7's note says only "Quantitative version untested on a valid instrument".
- **Fix:** Use "PROOF (GENERAL_THEOREM §2)". Add "rate conjectural" to the K12 gloss. Drop the E6 = fractal-vigilance identification, or justify it.

### 13. [MINOR] Identifier collisions
- **Where:** l.156, l.159, l.187; §6.
- **Problem:** "E2", "I5" and "H8" each mean different things in SCALE_ENDS or local files and in CLAIM_MAP. CLAIM_MAP E2 is a MATH-CORRECTED T5.2 claim, I5 is an immune-levels row, and H8 is "vigilance in firms". BOOKENDS' proposals P1–P11 also collide with Theorem P's P0–P3 and with AXIOMS "P11 readability".
- **Fix:** Prefix every ID with its file (SE-E2, IM-I5, CM-H8), and rename the proposals BK-P1 … BK-P11.

### 14. [MINOR] Bottom line says "two places", but three repo inconsistencies are flagged (§0.4 versus §3.4 and P8)
- **Fix:** Change to "three places" and list T7(iii).

---

## Section-by-section verification requested

**(1) PROVED/DERIVED claims.**
- "P needs no selection": true of the mathematics (P0/P1 hypotheses are A1, A2, A5, plus A4 implicitly). The application to unselected systems fails as written (findings 1, 3, 4).
- "Feedback is the simplest model when it responds to an outside variable": true only in the weak sense "carries I_pred > 0". That sense is near-automatic (finding 2) and contradicts §1 on flames and hurricanes.
- Five-step onset: the steps are fine as separate measurements; the ordering is not derived (finding 8).
- Class 2b (P2): coherent once findings 1–5 are fixed; it rests on the response/action split.
- P1–P11:
  - P1 sound.
  - P2–P5 and P7 blocked by findings 1, 2 and 6.
  - P6 incomplete (N26).
  - P8 sound.
  - P9 inherits finding 2.
  - P10 and P11 are fine as procedure.

**(2) The three axes.** P, K and S are a useful decomposition and match the repo's split of design predictions (Axiom 7 / FRAMEWORK §1.2 item 4). The inconsistencies are l.159 (finding 5), the K-axis order versus the H80 order (finding 10), and hurricanes and flames (finding 2).

**(3) The flagged repo inconsistencies.**
- **(a) Stars as H80's thermostat tier: CONFIRMED.** SCALE_ENDS l.75 labels class 2 "(H80's thermostat tier)" with "0 (feedback on its own state only)". l.148 says "H80's feedback tier". l.42 defines the H80 ladder as "cheapest *predictor* whose error stays inside tolerance". So a self-only class is labelled with a predictor tier. The independent review (SCALE_ENDS_INDEP_REVIEW l.65) already called it an analogy. P1 is the right fix.
- **(b) SCALE_ENDS requires selection: CONFIRMED textually, but it is a definitional choice rather than a contradiction.** SCALE_ENDS l.76 and l.118 make "selection over designs (Axiom 7: heredity)" a condition for class 3. Theorem P has no such premise. Under the repo's governing Axiom-7 reading of "action" (THEORY l.128; SCALE_ENDS l.108, l.251), however, P has no action without selection, so the repo is internally consistent and the tension was already flagged in SCALE_ENDS l.251 and l.253 (§6b). The real issue is the definition of "action" (finding 1). It is not an error in SCALE_ENDS.
- **(c) T7(iii) L^{2/3}: CONFIRMED.** THEOREMS.md l.197 reads "The number of levels grows as L^{2/3}" with no pointer. THEORY l.41 says the "(log-span)^{2/3} layers" are withdrawn (K13, K12), and CLAIM_MAP K12 (l.317) is MATH-CORRECTED with "(log-span)^{2/3} withdrawn". Also, l.197 never defines L; P8 should say "L = log-span". P8 is sound.

**(4) Layers and governance: labels preserved?**
- T3a "PROOF; elementary; sufficient condition, not a cutoff": exact (THEOREMS l.69, l.75). The inequality and N* = (√(1+ρ)+1)²/ρ match l.73–74.
- T3b KNOWN and T3c "NUMERIC; principle KNOWN": exact (l.82, l.88).
- B3, B9 and C1 PROVED (in-model): exact.
- T7 "PROOF (conditional); unconditional claim FAILS": exact (l.258). The fractal-only-under-scale-free statement matches l.204.
- Gorman condition c_i/(w_iσ_i²), 51× and 500×, "PROOF + NUMERIC": exact (MATH_ATTACK l.269–272). Strong form FALSE: exact (l.295).
- Externality √(Λ_i/Λ_whole): matches l.273, but the "shared memory" reading and the drop of "shared fate" are findings 9.
- J9 OPEN, J8 WITHDRAWN, J7 PRIOR ART: exact. E6 attribution: finding 12.
- LAT-1/N27 OPEN, formula L_max = c(D*/q)^{1/(α−1)}, and "extrapolating trackers do better at α > 2": exact (CLAIM_MAP N27; SCALE_ENDS l.291).
- City: z ∝ N^{b−H−θ/2}, CONJECTURE: exact (MATH_ATTACK l.277–279).

**(5) Overclaim, circularity and definitional tricks.** Findings 1 and 2 are the definitional problems. Findings 7, 8, 9 and the l.52 narrative are overclaims. No new "law" or "theory of everything" wording was found: the checker passes with BOOKENDS added to MAINTAINED. The field status ("untested, not refuted") is stated correctly.

## Minimum fix set to reach PASS-WITH-FIXES
1. Split "response" from "action" and re-derive N25 and N26 under that split (findings 1 and 6).
2. Replace "model" with "survival-relevant (semantic) information" for K2, and make flames and hurricanes consistent (finding 2).
3. Add the finite-horizon corollary and the explicit G2 lemma (findings 3 and 4).
4. Fix l.159 (finding 5), l.133 (finding 7), and l.52 and l.54/l.187 (findings 8 and 9).

---

# Round 2 (revision 2, commit 49bd64c; reviewed Wed 18 Nov 2026, ~6:10–6:40 PM ET)

I checked out 49bd64cb in /tmp/rev-math and reread every changed section, rather than relying on DISPOSITION.md.
- `tools/check_consistency.py`: PASS (FAIL 0).
- `tools/test_check_consistency.py`: PASS.
- `theory/bookends_checks/finite_horizon.py` reproduces its .out exactly.
- New check, `markov_counterexample.py` (in this folder; output below).

Nothing was pushed or commented.

## Verdict: **PASS-WITH-FIXES**
Both blockers are genuinely fixed. Most majors are fixed. Three issues remain, two of them in the proposals rather than in the synthesis. All need wording edits only, plus one stated condition.

## Status of round-1 findings
| # | Status | Evidence |
|---|---|---|
| 1 action vs response | **FIXED** | §2.0.1 l.105–108. N25 and N26 are re-derived under both readings in §2.0.4, l.133–134. |
| 2 "model" made automatic | **FIXED** (one minor residual: R2-5) | Four notions are defined in §2.0.2. The lemma says the P floor does not imply a model (l.130). Class 2b is withdrawn. Flames and hurricanes are K1 (l.263). |
| 3 finite horizon | **PARTLY FIXED** | Bound correct for i.i.d. increments; the dependent case the theory needs is not covered (R2-1). |
| 4 mapping lemma | **FIXED** | l.123–130. The algebra is correct: y(x) − ℓ = ȳ − ℓ′. Nit: because the shift depends on x only, D_ℓ′(R) = D_ℓ(R) exactly, so "recompute D" is harmless but unnecessary. Use the same time index for y and ℓ, or say y is evaluated at X_{t+k}. |
| 5 K ≥ K2 held | **FIXED** | l.249. Only K2/K3 (memory beyond the instantaneous correlation) need upkeep, consistent with SE-E3(c) and l.62. |
| 6 N28 / THEORY l.128 | **FIXED** | l.150; BK-P5. |
| 7 biosphere pooling | **FIXED** | l.226–229: ANALOGY + PRIOR ART; the redundancy result is OPEN (§7.7). |
| 8 onset order | **FIXED** | l.60, l.91, l.138: HYPOTHESIS, partial order. "Viable" vs "pays" separated (l.147). |
| 9 shared fate | **FIXED** (minor residual R2-6) | l.62, l.93, l.286. |
| 10 two orders / frozen | **FIXED** | l.172–176. The constant predictor is correctly I_pred = 0. |
| 11 R1 | **FIXED** | l.170. |
| 12 labels | **FIXED** | Theorem P is quoted as PROOF. K12 is "rate conjectural" (l.283). The E6 link is withdrawn. |
| 13 ID collisions | **FIXED** (trivial residue) | l.187 "H8's note" and l.286 "J9" are unprefixed. |
| 14 two vs three | **FIXED** | l.65–68. |

## The finite-horizon bound
- **Statement checked.** Suppose increments are independent, or more generally the centred increments form a martingale-difference sequence with |ΔR + δ| ≤ b. Then {survive to T} ⊆ {R_T > 0}, and by Azuma–Hoeffding P(R_T > 0) = P(Σ(ΔR+δ) > δT − B) ≤ exp(−(δT−B)²/(2b²T)) for T > B/δ. **Correct.** δ = r_∞ − (y − c̄) is the *smallest* blind shortfall, and the bound only gets tighter for larger δ, so using it is conservative. The Monte Carlo (symmetric ±b, i.i.d.) is consistent and the bound is loose, as stated. It cannot test the dependent case.
- **R2-1 [MAJOR, required].** The martingale version needs the **conditional** mean of each increment, given the past, to be ≤ −δ. Revision 2 says only "mean −δ". For a blind agent in a Markov world that condition fails: the conditional mean depends on the current world state even when I_pred = 0. A persistent drifting world is exactly the case Q2 and BK-G2 are about.
- **Counterexample (`markov_counterexample.py`).** Setup: blind agent, increment +0.9 in the good state and −1.1 in the bad state, two-state world with flip probability p, B = 5, δ = 0.1, b = 1. Results:
  - p = 0.5: no violation;
  - p = 0.01, T = 1600: simulated survival 0.068 against the bound's 0.0005;
  - p = 0.001: survival 0.41 vs 0.22 at T = 400, and 0.27 vs 0.0005 at T = 1600.

  So l.122's "Survival well past B/δ is therefore evidence … that I_pred > 0" is **false in persistent worlds**.

  **Fix:**
  1. Change "mean −δ" to "conditional mean ≤ −δ given the past (i.i.d. world, or a supermartingale)".
  2. Move the "evidence" sentence under that condition.
  3. Add: "In a Markov world with mixing time τ_mix, blind survival can last of order τ_mix regardless of δ (counterexample in reviews). Only survival ≫ max(B/δ, τ_mix) can count, and the mixing-adjusted exponent is OPEN."
  4. Mark BK-P13's finite-horizon row "DERIVED (i.i.d./supermartingale); Markov form OPEN" (as now), and state the τ_mix caveat in the row.

## Proposals: safe to apply?
- **R2-2 [MAJOR, blocks BK-P1+P2+P3 as a set].** BK-P2 says classes 2 and 3 are split by notion (c), the structural model. But BK-P1 renames class 2 to "self-regulated: feedback on its own state only; no exogenous target", and BK-P3 keeps SCALE_ENDS l.76's other class-3 conditions, including "E1 fails (an *action* with world-dependent payoff)", which is the Axiom-7 reading. Two consequences:
  - (i) Proportional or drive-slaved responses to an *exogenous* variable (K1/K1s: storms, driven chemistry) fall in **no class**.
  - (ii) The carbonate–silicate cycle, BK-P2's own example of (c) without (d), cannot be class 3, because it has no Axiom-7 action, so E1 holds.

  **Fix:** class 2 becomes "held, no structural model (self-regulation, or proportional/drive-slaved response; may carry survival-relevant information)". In BK-P3, change "E1 fails (an action …)" to "a *response* with world-dependent payoff (§2.0.1)", and keep "action" only for the design-prediction clause. With this amendment I withdraw my round-1 approval of BK-P1 *as worded*.
- **R2-3 [MAJOR, BK-P7].** For post-Page-time holes, revision 2 rests the lookup-edge conclusion on the collection and decoding cost, and that rests partly on the Harlow–Hayden *conjecture*. Keeping "PROVED (in-model) … label unchanged" for N26 across all holes would make a PROVED row conditional on a conjecture. **Fix:** in BK-P7, keep PROVED (in-model) for pre-Page holes (all astrophysical holes today), and state post-Page holes as "conditional on decoding cost (Harlow–Hayden, conjectural)", outside the PROVED scope.
- **R2-4 [MINOR, BK-P6].** "Semantic information is 0" for atoms is a physical argument, and l.133 says "not computed". BK-P6 would place it in a PROVED (in-model) row's note without that qualifier. **Fix:** add "(physical argument, not computed)".
- **Safe to apply now (math/logic view):**
  - BK-P5 (THEORY §2.3 and N28 "*Selected* models …");
  - BK-P8;
  - BK-P10;
  - BK-P12;
  - BK-P14;
  - BK-P4 (consistent once R2-2 is applied; apply them together).
- **Apply after fixes:** BK-P1, P2 and P3 (R2-2); BK-P6 (R2-4); BK-P7 (R2-3); BK-P13's finite-horizon row (R2-1).
- **No math objection:**
  - BK-P9 (spine sentence; Chad's call);
  - BK-P11 (physics content; defer to the PHYSICS reviewer).

## New errors introduced (all minor)
- **R2-5.** l.80 says a hurricane's "state follows the world but holds nothing about it", and that a flame needs nothing outside "known". This contradicts l.179 ("Correlation: all have it") and leaves K1s OPEN. **Fix:** "Its state follows the world; whether that information helps it last is an open question with a test (§2.2)."
- **R2-6.** l.286 says sterile workers share colony fate "so Λ_i ≈ Λ_whole". Shared fate through relatedness gives Λ_i ≈ r·Λ_whole, so watching is still low by about √r, roughly 0.87 for full sisters under haplodiploidy. That is mild, but it is not ≈ 1. **Fix:** write "Λ_i ∝ Λ_whole (scaled by relatedness), so under-watching is small".
- **R2-7 (nit).** "A clock entrained to a cycle is an internal model of a periodic world" (l.116) stretches the IMP, which is about error-feedback regulation. Say "IMP-like (an oscillator matched to the signal generator)".

## Required before merge into canonical files
Fix R2-1, R2-2 and R2-3. R2-4 through R2-7 are recommended. The synthesis file itself can stay on the branch as "unreviewed synthesis" with these fixes pending.
