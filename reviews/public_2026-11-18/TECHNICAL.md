# TECHNICAL referee report (math, physics, biology, prior art)

Repo: Chad-Mitchell/theory-of-adaptive-organization at main abd56e5 (fresh clone, /tmp/rev-tech, deleted after review). Reviewed Wed 18 Nov 2026, evening ET. Read-only. Compute at nice 19.
Scope read: README.md; THEORY.md §0, §1 (N-table), §2.2–2.5, §6, §8b; theory/BOOKENDS.md; theory/SCALE_ENDS.md; theory/THEOREMS.md; CLAIM_MAP_v2.md rows N24–N35. Line numbers are in the abd56e5 files.

## VERDICT: READY-WITH-FIXES

Blockers (2). Both are one-clause fixes:
- B1: README/THEORY state black-hole information return with no unitarity premise.
- B2: README/THEORY give the "price of a bit" floor with no erasure/Landauer qualifier.

The math I could recheck is correct, and every PROVED (in-model) label I traced carries its condition where it appears. Prior-art credit is unusually honest. The remaining issues are wording and calibration. A hostile physicist or biologist reading the first screen would find B1 and B2 first.

## What I checked and found CORRECT (so the author knows what is solid)

Numbers recomputed (nice 19):
- Horizon entropy S_dS = πc⁵/(Għ H_Λ²) is 3.31×10¹²² nats for H0=67.4, Ω_Λ=0.685. It is 3.0×10¹²² for H0=70. "About 3×10¹²²" is right. Egan–Lineweaver's current-horizon 2.6×10¹²² is correctly distinguished from the asymptotic value (SCALE_ENDS:207).
- T_dS = 2.20×10⁻³⁰ K, so kT_dS ln2 = 2.10×10⁻⁵³ J. "≥ ~2×10⁻⁵³ J" holds as arithmetic.
- BH (1 M☉): S = 1.049×10⁷⁷ nats, T_H = 6.17×10⁻⁸ K. Energy per nat is 2kT_H (Smarr plus Bekenstein saturation; the code check prints 2.000).
- Lifetime t = G²M³/(3αħc⁴) with α = 3.747×10⁻⁵ gives 1.159×10⁶⁷ yr. Naive photon-only 5120π gives 2.10×10⁶⁷. Page 1976 α = 2×10⁻⁴ gives 2.17×10⁶⁶. All match SCALE_ENDS:164.
- Page fraction 0.646 (half-radiated) reproduced; 0.538 t_ev and 1.4847 are Page's published values.
- Proton Bekenstein capacity 25.1 nats = 36 bits ✓. CMB-absorption delay ≈ 3×10¹¹ yr ✓. Half Earth circumference / c = 0.067 s ✓.
- Laughlin et al. 1998 abstract (re-fetched): "10⁴ ATP molecules to transmit a bit at a chemical synapse, and 10⁶–10⁷ ATP for graded signals… or spike coding" ✓. 2–6×10⁴ range ✓. 10⁴ ATP ≈ 2×10⁵ kT ≈ 2.9×10⁵ kT ln2 ✓.
- Bacterium E_gen ≈ 10¹¹–10¹² kT (10¹⁰ ATP × ~20 kT) ✓.

PROVED (in-model) items:
- **N33** (Azuma). I re-derived it. Y_i = ΔR_i + δ has conditional mean ≤ 0 and |Y_i| ≤ b. Azuma–Hoeffding holds for supermartingales, so P(R_T>0) ≤ exp(−(δT−B)²/(2b²T)) for T>B/δ ✓. Reproduced finite_horizon.py: 0.0034 vs bound 0.1724 at T=1600 ✓. The condition ("conditional mean given the past ≤ −δ") and the Markov/τ_mix OPEN caveat are stated at BOOKENDS:133–140 and CLAIM_MAP:377. N33 appears nowhere on README/THEORY. The label is not overclaimed. The i.i.d. bound for the MATH_LOGIC counterexample (0.00055) reproduces.
- **N26**: scope is pre-Page-time only, with the older-hole case explicitly outside and tied to Harlow–Hayden. This is stated on README:32, THEORY:13, THEORY:130, CLAIM_MAP:370. Good. (Unitarity omitted on reader pages: see B1.)
- **N25**: "partly definitional" is present on README:32, THEORY:13 and THEORY:130 ✓.
- THEOREMS.md algebra re-derived:
  - T1a, T1b, T1c: J*, K²/(1−K)=q/r, cosh form, +6%/+74% ✓.
  - T3a: N* = (√(1+ρ)+1)²/ρ; 5.83, 9.9, 42 ✓.
  - T3b: 5/14/23/29% ✓.
  - T5, T5b ✓.
  - T7b: ψ'' = ½sinh(Δ/2), 2.01% and 6.07% ✓.
  - T7c exponent ✓.
- THEORY §2.2/§2.5 algebra re-derived:
  - Read-rate (wq/c)^{1/α} ✓. e* at α=2 = √(qN) ✓.
  - Precision exponents α/(2α−1) ✓. Onset exponent −(1+θ), a and b ✓.
  - Two-state jump-world elasticities 1/ℓ, 1−1/ℓ, −2+2/ℓ at κ=10⁻³ (0.17/0.83/−1.67) ✓. MSE small-κ form ✓.
  - Regime C Q^{1/β} ✓. Natural-image β=0.905 ✓.
  - I did NOT independently re-derive t_A (the Bayes adaptation-time closed form). It rests on the repo's own code and review.
- Eigen threshold εL ≲ ln σ ✓. Internal-model principle and integral feedback (Francis–Wonham; Yi 2000; Barkai–Leibler) ✓ as stated. Black–Cox vs Merton factor of 2 (reflection principle) ✓.
- Frank 1995: the quoted abstract line ("Self-restraint… is not sufficient: mutual policing and enforcement of reproductive fairness are also required") matches Nature's text ✓.
- Mora & Nemenman 2019: geometric-mean integration time ✓.
- Lee–Flack–Krakauer 2024: public-good / niche destructors ✓.
- Mitchell et al. 2009 (N35): loss of the conditioned response in lab evolution ✓.
- Code: `tools/check_consistency.py` PASS (FAIL 0). `pytest tools/` 50 passed. `theory/bookends_checks/finite_horizon.py` output identical to the committed .out. `theory/scale_ends_checks/physics_numbers.py` output identical to the committed .out.

## BLOCKERS

**B1. Black-hole information return is stated as fact, with no unitarity premise, on the reader-facing pages.**
- README.md:32: "the rest returned scrambled only after about the Page time for every black hole that exists today (N26 PROVED (in-model) for such pre-Page-time holes, conditional on counting lateness as error…"
- The same content is at THEORY.md:13 and THEORY.md:130 ("everything else returns only after about the Page time").
- The only premise named is the lateness mapping. "Unitary evaporation assumed" appears at BOOKENDS.md:153 and CLAIM_MAP:370, but `unitar` occurs in README/THEORY/SCALE_ENDS only once (SCALE_ENDS:243). Whether information returns at all is the unresolved information paradox. A physicist will read this as asserting Page-curve unitarity.
- Fix: add "if evaporation is unitary (the Page-curve assumption; Hawking's original calculation says never)" to README:32 and THEORY:13/130.

**B2. "Price of a bit ≥ ~2×10⁻⁵³ J" is Landauer's erasure bound, but it is stated as the price of a bit generally.**
- README.md:32: "The cosmic horizon caps memory at about 3×10¹²² nats and the price of a bit at ≥ about 2×10⁻⁵³ J."
- THEORY.md:130: "the bit price at ≥ kT_dS ln 2 ≈ 2×10⁻⁵³ J".
- SCALE_ENDS.md:208: "That puts a permanent floor on the price of a bit, kT_dS ln 2 ≈ 2×10⁻⁵³ J. No tracker anywhere in our future can pay less."
- The kT ln2 floor applies only to logically irreversible erasure. SCALE_ENDS:23 itself says "measurement alone can in principle be reversible". It also assumes the dS horizon is the coldest available bath, which is the Krauss–Starkman setup. "No tracker anywhere can pay less" is false for reversible operation and for non-erasing storage.
- Fix: "the price of *erasing* a bit, in a bath at the de Sitter temperature". Drop or hedge "No tracker anywhere in our future can pay less".

## SHOULD

**S1. Shared-fate √r example uses the best-case r and sits awkwardly against the policing citation (biology).**
- THEORY.md:221: "sterile workers *partly* share the colony's fate (relatedness r; watching falls only to about √r of its optimum, ≈ 0.87 for r = 3/4, so under-watching is small, ≈ 13%, but not zero)".
- BOOKENDS.md:309: "≈ 0.87 for full sisters under haplodiploidy, r = 3/4".
- The math is right (f*² ∝ Λ gives √(Λ_i/Λ), MATH_ATTACK:269–275; √0.75 = 0.866).
- Three problems:
  - (a) r = 3/4 is a worker's relatedness to a full sister. Colony fate is carried by the colony's reproductives (queen, new queens, males), so the relevant r is lower. Multiply-mated species (honeybees) are much lower still, so under-watching there is much worse than 13%. "Under-watching is small" holds only at the extreme.
  - (b) Ratnieks 1988, the paper cited at BOOKENDS:309, predicts policing precisely when queens mate more than ~2 times, i.e. when r is below 3/4. I confirmed this from its abstract and secondary sources. So the r = 3/4 illustration is the case where relatedness theory does not predict policing, while the sentence pairs it with Frank/policing as if both apply.
  - (c) "Sterile workers" is false for much of the Hymenoptera. Workers of many species lay male eggs, which is what policing suppresses.
- Also, √r is the α = 2 reset-read exponent. For general α the factor is r^{1/α}, which THEORY's own §2.2 implies.
- Fix: say "r ≈ 3/4 is an upper bound (single-mated sisters); with multiple mating r is lower and √r ≈ 0.55 at r = 0.3". State the α = 2 premise. Change "sterile" to "mostly non-reproducing".

**S2. README's headline physics sentence overstates how much the physics does, given THEORY's own concession.**
- README.md:11: "The costs are physically priced from atoms to the cosmic horizon (Chad, 18 Nov 2026, t1927)".
- THEORY.md:128 concedes: "in the formal layer, the energy / second-law framing is **decorative**. No conserved quantity, entropy production or Landauer-type bound enters any proof". THEORY.md:126: "Not literal above the cell."
- A hostile reader will quote the README line against the THEORY line. The README does add that the floors "do not bind" above the cell.
- Fix: "…asserted (not derived; no proof uses it; THEORY §2.3)".

**S3. "N2 PROOF, an exact iff" contradicts "sufficient condition, not a cutoff".**
- THEORY.md:58, N2 status: "PROOF, an exact iff within the one-source model, generalized to N* = …".
- Same row, claim cell: "A *sufficient* condition, not a cutoff". THEOREMS.md T3a, "**Reading.** This is a **sufficient condition, not a cutoff**" (nested policy is one feasible policy, an upper bound on the best nested cost). The claim text "guaranteed to pay once group size exceeds" is the sufficient reading.
- Reconcile. If the night-1 formal layer has an iff for a different setup, name it. Otherwise delete "exact iff".

**S4. "Atoms are frozen: nothing threatens them" is physically overstated.**
- README.md:32: "Atoms are frozen: nothing threatens them and nothing selects among their responses".
- Atoms ionise, nuclei decay, molecules react. SCALE_ENDS:25 and BOOKENDS:149 use the correct form: lifetime is set by a barrier or conservation law, and nothing the atom does changes whether it persists.
- Fix: "nothing an atom does changes whether it lasts".

**S5. "Light delay binds only off-planet" conflicts with the theory's own test.**
- BOOKENDS.md:104 ("The speed of light is the hard floor, and it matters only off-planet") and BOOKENDS.md:310 ("so **c binds only off-planet**").
- The same section proposes geo-distributed firms as the stronger test (BOOKENDS:310) and cites PACELC. Cross-continental round-trip latency (~100 ms) and HFT microwave links are light-limited on Earth. The 0.07 s figure is a lower bound versus processing times, not a reason c is irrelevant.
- Fix: "c is rarely the binding delay for human organizations on Earth, but is for latency-critical distributed systems".

**S6. Independent-review claims point to reviews the public cannot see.**
- BOOKENDS.md:7–16, THEORY.md:528 (v1.4.20 entry): "two rounds of three independent reviews" whose "review files [are] kept off-repo". README.md:32 and THEORY:130 give "PASS-WITH-FIXES".
- The SCALE_ENDS review is in-repo (reviews/night2/SCALE_ENDS_INDEP_REVIEW.md ✓). The BOOKENDS math/physics/bio reviews are not.
- THEORY:4 ("Not independently reviewed as a whole") and BOOKENDS:30 are honest. Say "review files not in the repo" wherever the verdict is cited.

**S7. Prior-art attribution that does not obviously say what is claimed.**
- THEORY.md:130 and SCALE_ENDS:288: "The three-class split is prior art in substance (Prigogine; Pross; Kolchinsky & Wolpert 2018)". Kolchinsky & Wolpert, as far as I can check from the abstract, define semantic information as what is causally necessary for a system to maintain its existence. I could not confirm a keep/burn/know split there.
- Fix: cite K&W for the semantic-information notion only, as BOOKENDS does at §2.0.2.

**S8. THEORY:16's list of proxy passes omits the one pass that bears on the tracking layer.**
- THEORY.md:16 lists PIAAC, VIGIL_ONA and D3S as proxy passes that "do not support GTAO". §2.4 (line 148) records KERNEL-MEASURE, "Passed on proxy… exploratory, not decisive", resolution 0.049 > locked 0.040.
- The omission is not favourable to the theory, but a reader comparing the two will see an inconsistency.
- Add KERNEL-MEASURE to line 16 with its caveat.

## NIT

- BOOKENDS.md:73: "CM-N26 PROVED (in-model), conditional; its conditions need rewording, §2.0.4". This is stale, since rev 3 did the rewording.
- THEORY.md:126: "A chemical synapse pays at least about 10⁵ times that". One blowfly estimate (≈3×10⁵) is not a lower bound. Use "about 10⁵–10⁶ times".
- THEORY.md:88 and README:26: Mora & Nemenman's world is a geometric random walk (Gaussian in log c), so "α = 2" is true for log-concentration only. One clause fixes it.
- THEORY.md:130: "β_phys" is used without definition on that page (SCALE_ENDS:28 has the context).
- README.md:11 and README:42, THEORY:15, THEORY:129–130: internal turn tags "t1927", "t1908" and the name "Ace" are meaningless to a public reader. THEORY.md:6 also says "Ace's working folders". Replace with dates or drop.
- THEOREMS.md:5 cites `checks/check_all.py` and `../review/…` (REVIEW.md, indep_checks.py). Neither path exists in this repo (`theory/checks/` and `review/` are absent; the checks live in theory/theorems-checks, theory/math-checks and so on). Dangling references.
- THEORY.md:65: "cost condition for acting ahead (pay for a model only if lateness loss exceeds its upkeep)" is listed as "probably this project's own". It is close to the value-of-information / EOQ accounting identity. Hedge as "elementary; may be known", as T2b is.
- SCALE_ENDS.md:25: "readable state (M, J, Q)" is classical no-hair. Add "classically" (soft/quantum hair is debated).
- BOOKENDS.md:3, SCALE_ENDS.md:3 and MATH_ATTACK.md:3 disclose "Grok Bot executor … via Ace". That is a transparency plus, not a defect. Confirm the author intends the tool credits to be public.

## Not checked (stated so nothing is assumed)
- The t_A Bayes-filter closed form (THEORY §2.2). Rests on in-repo code, which passes pytest.
- Regime C theorems, the INTERNAL_MODEL N7 bound, and the Mitter–Newton / Horowitz–Sandberg consistency statement (THEORY:125).
- DOIs and page numbers beyond those cited above.
- The "Ostrom 1990/2010" content: the repo itself says "classic, not re-fetched".
