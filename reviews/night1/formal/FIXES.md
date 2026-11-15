# FIXES: the adversarial pass and every correction made

15 Nov 2026; pass completed 02:22 ET. Private; nothing was posted, sent or committed.

**Stance of the pass.** I re-read every statement and proof after the drafts were finished, starting from "this step is wrong" and trying to break it. For each one I asked:
1. Is there an unstated hypothesis?
2. Is the argument circular?
3. Can a sign or an inequality direction be flipped?
4. Does the check actually test the claim, or only the code?

New scripts from the pass: `checks/s9_attack.py`, `s11_vclosed.py`, `s12_mc_base.py`, plus fixes to `s10_extremes.py`. All scripts s1–s12 were re-run afterwards from a clean shell (log at the end).

**Limit of this pass (stated plainly).** It was done by the same executor that wrote the proofs, with a deliberate adversarial stance. It is **not** an independent review. A fresh reviewer with no access to my reasoning should repeat it before anything is called checked by a second party.

---

## A. Errors in my own drafts, found and fixed (proofs as finally written include these)

| # | Where | Error | Fix | Evidence |
|---|---|---|---|---|
| D1 | T7(a) proof | The first draft used a wrong monotonicity: it treated m(q \| R) as decreasing in q, when it is increasing for concave ψ. | Replaced by an interval-ordering (swap) argument that uses only "ψ′ nonincreasing". Added the h > 0 condition (κ against 1 as well as κ\*). | s6: 0/150 non-upper sets; s9 (3): 0/120 with heterogeneous members |
| D2 | T1.4 | Sign error: the exact elasticity carried a stray factor (−1). That would have made e_g positive. | Removed. The formula now matches the sympy output and its limits (−(1−b)/(1−a) as ρ → 0, and 0 as ρ → ∞). | s2 §4 |
| D3 | T4 step 3 (remainder) | Claimed L″ bounded for p ≥ 2. That is false for 2 < p < 4, where L″ ∝ v^{p/2−2} blows up at 0. | Case analysis: p = 2 exact (R ≡ 0); p > 2 integrable, relative O(ρ); 0 < p < 2 split at V_u = V_g, relative **O(ρ^{p/2})**. The predicted rate matches the numerics: deviation shrink factor 0.55 per decade against 10^{−p/2} = 0.56 at p = ½. | s3 |
| D4 | T7(c) | The first-order location rule had an unspecified "p-dependent constant". | Explicit: n_s^{1−a}q_s^{1−b} > (p_g/p)^{1−a}R^{1−b}/b. | s6, s10 E1 |
| D5 | Prop 11 | Said the shared term lies in "[0, T_g + …]" and implied a lower bound of T_g/2. There is none: members who read more often than the level see less. | Now states only the coincident-reads value, the T_g/T_u → 0 limit (Π\* → 8), and that there is no general lower bound. | s7 (c) |
| D6 | T1.5 proof | Garbled phrase ("NbρA-type savings"). | Rewritten: the root is set by the savings Nbρ against h′. | — |
| D7 | T6(c) | Loose "decreasing differences in (S, −h)" wording. | Stated directly: J(T; h) − J(S; h) is increasing in h for S ⊂ T, then Topkis. | — |

## B. Found by the adversarial pass

| # | Attack | Finding | Fix | Evidence |
|---|---|---|---|---|
| F12 | *Hidden assumption: one technology for level and members.* | T1–T4 and T7 silently assumed a common class. With a level in P(a_L, b_L) over members in P(a_m, b_m): **e_g → −(1−b_L)/(1−a_L)** (the level's class) and **e_u → +(1−b_m)/(1−a_L)**. N\* then depends on q_g and q_u separately, not on ρ alone. The opposite signs of T3 survive. | Added T1.8 with its proof; T7(b) says κ\* is the level's; the one-line summary is corrected. | s9 (1): four mixed pairs exact to 4 d.p. (e.g. level (⅔, ⅓) over members (½, ½): e_g = −2.0000, e_u = +1.5000) |
| F13 | *Hidden assumption in T6 (H1).* | Complementarity needs members to track their **residual as one bundle**. If each unleveled source can be read separately at additive cost, member costs are additive over sources. J is then **modular**: levels are independent, with no complementarity and no avalanches. | H1 now states the bundled-residual requirement and the modular counterexample. | s9 (2): marginal values identical to 2.8 × 10⁻¹⁴ |
| F14 | *Extremes: an unchecked conjecture.* | My working note said "as lookup gets cheap, private holding dissolves first, then levels". With whole-item lookup the **level dissolves first**. Its threshold u_L = φ_r + h + (φ_L + h)/N is strictly above the private threshold u_p = φ_r + h. With component lookup the level is a shared store and survives N^{1−a}-fold lower u. | EXTENSIONS E4 rewritten; CLAIM_MAP R10. | s10 E4: exact edges 1.5285, 1.4642, 0.2010 |
| F15 | *Can upkeep or prices rescue VIGIL's size miss?* | No. At γ = ½ and small ρ, **V(N\*) = 1 + √(1 + 2h′/r) ≥ 2** for all upkeep h′ and price ratios r. The VIGIL estimate ≈ 1.15 cannot come from upkeep or prices in class R. It needs a < b, attenuation, or a mapping failure. | T5.6 closed form added; EXTENSIONS F4 and CLAIM_MAP T5 now call the size a **miss**. | s11: max relative error 3.7 × 10⁻⁶ over 2,000 draws |
| F16 | *Was T5.2 stated too narrowly?* | "V > 1 iff a ≥ b" holds at **any price ratio** and any h, not only equal prices. The proof carries through with M = N\*p/p_g. | T5.2 strengthened, proof rewritten. | s11: 0/20,000 violations, min V = 1.0014 |
| F17 | *Edge case: N\* < 1?* | "N\* > 1 always" is false when p_g < p. A cheaper level technology can pay even at N = 1. That is a better tracker of g, not pooling. | T1.9 restricted to p_g ≥ p, with the counter-case noted. | s11 (first run crashed exactly here: G(1) > 0) |
| F18 | *Notation fixed once?* | κ was used for three things: the R2 information rate, the per-read broadcast cost, and the sharing-decay exponent. | Renamed: R2 rate → ι; per-read broadcast → c_b (t = c_b/c); κ_ℓ listed. AXIOMS notation table updated. | — |
| F19 | *Overclaim in L1.* | The status line and summary table said "drift-invariant pricing ⇔ a = b", but only "⇒" is proved. | Now "⇒ (sufficient; converse not claimed)". | — |
| F20 | *Overclaim in the THEOREMS header.* | It said "every algebra step was checked in sympy". Some identities were checked by 50-digit random-point evaluation because sympy would not simplify them. | Header now says so. Added a first-principles Monte Carlo of the R1 building block, independent of every closed form: simulated mse 0.5099 / 0.1015 / 0.4891 against qT/2 = 0.5 / 0.1 / 0.5; minimized cost 1.419 against √2 = 1.414; a ≈ 0.496, b ≈ 0.491. | s12 |
| F21 | *Overclaim in the one-line summary.* | "(a, b), and nothing else about the members, fix …". After F12 that is wrong. | Rewritten (level's class → e_g and κ\*; members' b → e_u). | — |
| F22 | *Circularity.* | (i) POOLSIM's learners minimize the model's own cost, so its pass is a code-and-consistency check, not evidence about real systems. (ii) "T5 explains POOLSIM W3" is consistency for the same reason. (iii) If a substrate's class were inferred from its onset slope, then "class predicts slope" would be circular. | (i) and (ii) labeled CIRCULAR in CLAIM_MAP. (iii) EXTENSIONS §2 requires measuring the class from **lone-unit effort elasticities** (b = ½ for R, ⅓ for A₁), independently of onset. | — |
| F23 | *Remaining hidden assumptions (scope, not fixed by a theorem).* | (a) Axiom 7: selection finds the optimum, so every result is about optimal design. (b) T1–T5 assume homogeneous members (T6–T7 allow heterogeneity). (c) Drift is exogenous. (d) No strategic behavior or free-riding. (e) T4 assumes independent phases. With phase-locked reads the shared term is still linear in V_g, but the level's optimization couples to T_u. **Not checked: open.** | Listed in AXIOMS scope and EXTENSIONS §3.0 / §4. | — |

## C. Checked hard and found correct (no change)
- T1.1 convexity (G″ = a(1−a)N^{a−2}B > 0) and single crossing.
- T2(b): G/N is strictly increasing, so existence ⇔ the limit is positive, and the boundary is ρ = 4t/(1−t)², re-derived by hand.
- T3: the key inequality reduces to (1+ρ)^{1−b} > 1 (re-derived). G_N(N\*) > 0 holds strictly, so the implicit function theorem applies.
- T5.3 algebra: V = b^{−a/(1−a)}ρ^{(b−a)/(1−a)}, re-derived. A_θ gives ρ^{−θ}.
- T6(b): inclusion inequality direction, using a left derivative of a concave function.
- T7 swap: interval placement [R_L, R_L+q_s] to the right of [R_L−q_{s′}, R_L], with the chain of inequalities re-derived.
- T8: edges, N² factor, cliff height (μu − h)/(2c), and the N^{(1−a)/b} power-class shift.
- P10: Bernoulli bound direction and ρ_min = (1−ε)^{−1/b} − 1 (0.0203 at 1%).
- P11: local slope ln(728/245)/ln(⅓) = −0.991.
- E1: depth grows one-for-one with log N (s10). E3: N\* ∝ λ^{−b} with h > 0 (slopes → −0.485).

## D. Corrections to earlier project documents (what tonight's results overturn)
| # | Document | Earlier claim | Now |
|---|---|---|---|
| C1 | ARCH_EQUATION (DP1) | Predict e_g from a lone member's elasticities under its actual loss | Wrong for bundled decisions. Use the sensing technology's quadratic-loss exponents (T4, Cor 4.1). |
| C2 | POOLING_REVIEW; PROFOUND_v2 | Absolute loss −2, quartic −½, stable −α/p | Separable decisions only (Cor 4.2). Bundled: −1 in R, s3. |
| C3 | ARCH_EQUATION §2.3 | Bundled reads make J non-submodular | False: a concave function of a modular one is submodular (0/93,207). |
| C4 | ARCH_EQUATION | V ∝ √(c/c_g); V ≈ 2 needs equal per-unit costs | At fixed N only. At onset V is price-invariant (T5.4). |
| C5 | night1 summaries; ARCH | Cheaper memory never dissolves a level | True for upkeep h only. Cheaper lookup, or higher stakes with a fallback, can dissolve one (T6 counterexample). |
| C6 | night1 summaries | "About 2× at every rank" | The onset value only. V grows as N^a. |
| C7 | T3a / N2 | Π\* ≈ 4 | Depends on the readability axiom: ≈ 7.3 under the subtract scheme (P11). |
| C8 | ARCH §2.3(f) | Tree knife edge at κ = 1 | κ\* = (1−a)/(1−b), = 1 only for a = b. |
| C9 | CORE_AUDIT | A level is born more vigilant (V > 1) | Only if a ≥ b (T5.2). |
| C10 | repo THEOREMS T3a | Sufficient condition only | An exact iff within 𝒜₁ (T1.2). |
| C11 | implicit | Volatility favors decentralization | In 𝓜, total volatility is neutral at h = 0 and **promotes** levels at h > 0 (T1.7). Shared and private volatility have opposite signs (T3). |
| C12 | my notes | AI: private holding goes first | Levels go first with whole-item lookup (F14). |
| C13 | my notes, summary | The free-energy identity was "killed" | More precisely: **withdrawn**. As stated it is either definitional (Boltzmann-embodied model) or underived. No test was run. CLAIM_MAP X1. |

## E. Still open after the pass
1. The bundled exponent for α-stable drift (no Gaussian closure).
2. P7.1, depth avalanches: numerical only.
3. P11: analytic Π\* under the subtract scheme, and vigilance there.
4. Vigilance under bundled non-quadratic loss.
5. T4 with phase-locked reads (F23e).
6. The empirical class of every real substrate (EXTENSIONS §2).

## G. Dated errata after the pass

| # | Date | Where | Error | Fix | Evidence |
|---|---|---|---|---|---|
| G1 | 15 Nov 2026, about 5:35 PM ET (QUEUE EFFORT-UNITS-ERRATUM, pick 25; found by `reviews/night2/N12_REFEREE.md` C3, earlier flagged as a convention in `reviews/night1/REVIEW_MATH.md` L1(viii)) | Lemma 1(viii); T5 Definition, items 3 and 5 | "Information effort (read rate, information rate, precision) equals spend/price" is false for precision in A_θ at θ ≠ 1: spend/price = r^{−θ} = precision^θ. | Precision elasticities in A_θ are (a/θ, b/θ) = (2/(1+2θ), 1/(1+2θ)); (a, b) are spend/price elasticities. Small-share onset vigilance is ∝ ρ^{−θ} in spend/price units and ρ^{−1} in precision units; growth N^a becomes N^{a/θ} in precision. Signs, b/a, "V > 1 iff a ≥ b" and price invariance are unchanged. Notes added under Lemma 1(viii) and the T5 Definition; proofs left as written. | `reviews/night2/EFFORT_UNITS_ERRATUM_checks/units_check.py` (sympy, plus finite differences at 6 random points, plus first-principles onset at θ = 0.5, 1, 2: slopes −0.500/−1.000/−1.997 in spend units, −1.000/−1.000/−0.998 in precision units) |

## F. Re-run log (all scripts, after all fixes)
Re-run 15 Nov 2026 02:21 ET (finish time), `nice -n 19`, all exit 0; every regenerated output is **byte-identical** to the saved `.out` (all scripts are seeded):
```
s1_classes exit=0 7s
s2_onset exit=0 4s
s3_bundling exit=0 2s
s4_lattice exit=0 2s
s5_phase exit=0 3s
s6_depth exit=0 27s
s7_misc exit=0 128s
s8_broadcast exit=0 0s
s9_attack exit=0 1s
s10_extremes exit=0 0s
s11_vclosed exit=0 1s
s12_mc_base exit=0 0s
```
