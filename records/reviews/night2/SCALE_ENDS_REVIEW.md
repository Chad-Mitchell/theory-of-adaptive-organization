# SCALE_ENDS_REVIEW: hostile physics and math referee pass on `theory/SCALE_ENDS.md`

Wednesday 18 November 2026, about 12:25 to 12:45 PM ET (America/New_York). QUEUE SCALE-ENDS-REVIEW, out of cycle and unscored (ledger 193 claim, 194 outcome). Private.

**Independence (disclosed).** No separate subagent could be launched from this executor. This pass was run as a separate step by **the same executor that wrote SCALE_ENDS.md**. It used only SCALE_ENDS.md and the cited sources, and every number was recomputed with a **different code path**: `scipy.constants`, the surface-gravity route to T_H, numerical integration of evaporation, a first-law finite difference, and Page's 2013 radiation-entropy factor (`SCALE_ENDS_REVIEW_checks/recheck.py`, `.out`). It also built a counterexample model (`e3_counterexample.py`, `.out`). **This is not an independent review in the t1916 sense.** A fresh reviewer who did not write the file is still owed before any THEORY.md or CLAIM_MAP text in SCALE_ENDS §9 is applied.

**Verdict: PASS-WITH-FIXES.** All the numbers check out except one Page-time value. The classification results hold. One derived lemma, **E3, is false as stated**, and a counterexample is given below. One application of E1 is partly definitional. Four labels or wordings overclaim. None of the fixes changes the bottom line (§0 items 1–6), but E3's fix changes how the atomic case is argued.

## 1. Numbers (recomputed independently)

| Item | SCALE_ENDS value | Re-derived | Verdict |
|---|---|---|---|
| T_H(1 M☉) | 6.17×10⁻⁸ K | 6.170×10⁻⁸ K (surface gravity κ = c⁴/4GM, T = ħκ/2πck) | OK |
| S(1 M☉) | 1.05×10⁷⁷ nats, 1.5×10⁷⁷ bits | 1.049×10⁷⁷ nats; 1.513×10⁷⁷ bits (A/4ℓ_p²). Page 2013 abstract: 4πM₀² = 1.049×10⁷⁷ (M₀/M☉)² | OK |
| First law: kT_H per nat | stated | finite difference dE/(kT dS) = 0.9999995 | OK |
| Energy per nat = 2kT_H = Bekenstein minimum at R = r_s | stated | ħc/(2πr_s kT_H) = 2.000 | OK |
| t_ev, photons only | 2.1×10⁶⁷ yr | 2.096×10⁶⁷ yr; ODE matches the M³ law (M(0.9 t_ev)/M₀ = 0.46416 vs 0.46416) | OK |
| t_ev, Page 1976 massless set | 2.2×10⁶⁶ yr | 2.160×10⁶⁶ yr (P = 2.011×10⁻⁴ ħc⁶G⁻²M⁻²) | OK; the bracket is correctly labelled species-dependent |
| **Page time** | "(1 − 2^{−3/2}) t_ev ≈ 0.65 t_ev" | That is the *half-initial-entropy-radiated* point (Hayden–Preskill's "half-way"). The **Page time proper** (radiation entropy = BH entropy) is **0.5381 t_ev**, at S_BH/S₀ = 0.5975, because radiation carries 1.4847× the BH entropy loss (Page 2013, arXiv 1301.4995, abstract fetched; re-derived: 0.5381, 0.5975) | **FIX 1** |
| Scrambling time 1 M☉ | 3.5 ms | 3.494 ms ((β/2π) ln S) | OK (O(1) prefactor conventions noted) |
| Proton Bekenstein | 36 bits | 36.24 bits (R = 0.8409 fm) | OK |
| 1 kg BH bits | 3.827×10¹⁶ | 3.8273×10¹⁶ (matches Lloyd) | OK |
| T_dS, S_dS | 2.2×10⁻³⁰ K; 3.3×10¹²² nats | 2.198×10⁻³⁰ K; 3.307×10¹²² | OK |
| **S_dS vs Egan & Lineweaver** | "agrees… to within its uncertainty plus our choice of parameters" | 3.3 vs 2.6 ± 0.3 ×10¹²² is **not** within the stated uncertainty. The gap is physical: their value is the *current* cosmic event horizon, which is smaller than the asymptotic de Sitter horizon and grows toward it | **FIX 2** (wording) |
| Hydrogen ionization factor at 300 K | 10^−228.5 | consistent (E/kT = 526) | OK |
| E_gen in kT | 10¹¹–10¹² kT | 2.7×10¹⁰ ATP × ~19.4 kT/ATP (50 kJ/mol at 310 K) = 5.2×10¹¹ kT | OK |
| Smolin quote, neutron-star masses | 1.5 / 2.5 M☉; 2.08 ± 0.07; 2.35 ± 0.17 | quote checked in the fetched PDF §6.3; masses checked in the abstracts | OK; "troubling, not 'certainly' refuting" is a fair reading |
| Isi et al. 2019 | ~10% (mass, spin), ~20% (overtone) | abstract | OK |
| Rosenband 2008 α̇/α | (−1.6 ± 2.3)×10⁻¹⁷ /yr | abstract | OK |
| T8 band closure | closes at c > (μuH_l − hH_l)/2 | (10 − 1)/2 = 4.5, matches the grid (4.4 open, 4.6 closed) | OK |
| Lateness MC | q(T/2 + ℓ) | 1.2107 vs 1.2050 including the grid bias, within MC error | OK |

## 2. Logic

**E3 is false as stated (major; FIX 3).** As written: "a structure at zero entropy production… can carry information only about variables that do not drift… Any information it holds about a drifting variable decays." Counterexample (`e3_counterexample.out`): a two-state receptor in instantaneous equilibrium with a slowly drifting binding energy (amplitude 2 kT). As the drive slows (ω/γ from 1 to 0.01), the dissipated work per cycle falls from 1.27 kT to 0.026 kT, roughly ∝ ω, while I(state; phase) *rises* to 0.18 nats. Passive equilibrium coupling tracks slow drift at vanishing dissipation. This agrees with Still et al. 2012: dissipation ≥ kT·(memory − predictive information), and for quasi-static driving the retained information is predictive. So the thermodynamic floor of *tracking* is not "kT per nat of mutual information".

What does hold:
- (a) An **uncoupled** (frozen) structure's information about a drifting variable cannot increase, and it decays as the variable decorrelates (data processing). DERIVED.
- (b) Keeping it requires coupling, an inflow (I5).
- (c) The price of that inflow is at least kT per nat for **measure-and-erase feedback cycles** (Sagawa–Ueda), and at least kT·(nonpredictive information retained) for **driven** systems (Still et al.). It can approach 0 for quasi-static passive coupling, a "lookup-like" instantaneous correlation that carries no memory beyond the present state.
- (d) A structure's information about anything is capped by its own state entropy, I(X; Y) ≤ H(X). For a ground-state atom, H(X) is set by the excited-state occupancy, about 4e^{−395} = 10^−171 at 300 K for hydrogen's n = 2 level. So the atom *cannot* carry information about its surroundings. That is the correct atomic argument, and it is stronger than the original E3.

**E1 applied to atoms is partly definitional (moderate; FIX 4).** "No action whose payoff depends on Y" is decidable only once "action" is defined. Every physical response (polarization, absorption) could be relabelled as an action. The non-circular content is E1 *as conditioned on Axiom 7*: an "action" is an alternative over which a selection process operates. For atoms there is no selection over responses, so E1 holds by that definition. The independent, non-definitional reasons are E2 (blind-viable) and the corrected E3(d) (no state entropy). SCALE_ENDS §3.2 should rest on E2 + E3(d) and give E1 as the Axiom-7 reading. Under Chad's t1927 scope call (costs at every scale), this is exactly where the band's "no selection" frozen corner comes from, and it should be labelled that way.

**SE10's label (moderate; FIX 5).** "DERIVED given published physics" needs one more qualifier. It depends on a **mapping hypothesis**: the black hole's read cost c is identified with retrieval latency (Page time; Hayden–Preskill) or decoding complexity (Harlow–Hayden, conjectural). The conservative route (latency ∝ M³ alone) is enough. Relabel as "DERIVED conditional on the mapping read cost ↔ retrieval latency; the complexity route is conjectural."

**"h < 0 today" (minor; FIX 6).** Net CMB absorption is an energy *inflow* to a structure that pays nothing to persist. Calling it negative upkeep is an analogy. Use "h = 0 (nothing paid to persist); net energy inflow from the CMB today."

**§3.4 S4 omits the fixed machinery cost (minor; FIX 7).** The real cost of a sensing pathway is dominated by building it (protein burden), κ₀, not by Landauer. The condition should read I·(1 − β_phys kT/E_gen) > κ₀/E_gen. That strengthens the conclusion that the floor does not bind existence (the machinery does). Also, by FIX 3(c) the Landauer term is a per-cycle *measure-and-erase* cost; passive coupling can cost less. The inequality stays a lower-bound argument, so the conclusion is unaffected.

**LAT-1 wording (minor; FIX 8).** "Could track only drift slower than about its light-crossing time" should read "could centrally hold only targets whose change over one light-crossing time (~10⁵ yr) stays within tolerance."

**Checked and fine.** The E2 logic; the Theorem 8 limit (and brute-force "lookup only" at c = 10³); the three-class ladder (stars as held structures with no model is a correct and useful split); the imposter list (in particular, refusing Still et al.'s bound for black holes and refusing ER = EPR as a read channel); the CNS reading as non-discriminating; the heat-death relabel as prior art; and the "Fails" paragraph on what GTAO does not derive. These are honest.

**What is still unfixed and owed.**
- (i) An independent referee who did not write either file.
- (ii) LAT-1's prior-art sweep (delayed control; teleoperation; PBS).
- (iii) A literature check of whether the three-class persistence ladder is stated elsewhere. Candidates: Pross on dynamic kinetic stability; Kauffman.

## 3. Under Chad's scope decision (t1927, received mid-review)

Chad's call resolves FRAMEWORK §1.2 item 4 in his direction: the three costs apply from atoms to the cosmos, and the theory must say what black holes are. The MV gates stay binding. This review checked that SCALE_ENDS does not use the scope decision to relax any gate.
- The design predictions at both ends still fail MV1 (no tracker, target or pool) and MV8-ii (no selection over designs, outside Smolin's hypothesis).
- The ends therefore enter as **derived corners of the band** (frozen where there is no selection) and as **known-group calibrations** (MV7), not as passes.

That is consistent with the scope call. Truth-status labels are unchanged by it.
