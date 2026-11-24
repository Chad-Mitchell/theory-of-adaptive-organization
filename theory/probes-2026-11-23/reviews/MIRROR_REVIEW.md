# Independent hostile review: `mirror-2026-11-23/MIRROR_MEMO.md`

*Reviewer: independent agent; I did not write the memo. Monday 23 November 2026, about 9:25–10:30 PM EST (America/New_York). Memo sha256 at intake `a8137e59e329b668e7373c7a91fad27454e9c30f72b2faa87cf13acf2074d291`; after inline reviewer edits `22f3ae10915d322d9613c6052aab2fd7d645cb31972407f0b1d301c75a95190d`. Fresh clone of GTAO `main` `d592662` in `/workspace/revmirror` (TMPDIR there, nice 19, deleted after). Compared against `CORE.md:52` (A1–A8 priced sum, Theorem R1) and `CORE.md:70` (heat floor Q̇_M ≥ kT·İ_M, steady state, local detailed balance, KNOWN Horowitz–Esposito 2014), and against `INVERT_REVIEW.md` and `WALLS_REVIEW.md`. `THEORY.md` untouched; no PR, no posts. Labels: PROVED (in-model) / KNOWN / CONJECTURE / SPECULATION. Checks are in `mirror_review_checks/` with `SHA256SUMS`.*

## 0. Reproducibility and references

- **M1–M4: PASS.** All 11 hashes in `checks/SHA256SUMS` match. All four `.out` files are byte-identical on rerun at nice 19 (`rerun_m1_m4.txt`).
- **DOIs: PASS.** All 26 memo DOIs resolve on Crossref with matching author, year, venue and pages. My rerun is byte-identical to `checks/crossref.out` (sha `d9789b18…`). One minor point: Crossref dates Chen–Georgiou–Pavon JOTA 169 to 2015 (online); the print issue is 2016. The 9 DOIs I added also resolve (`crossref_review.out`).
- **CODATA: PASS.** physics.nist.gov gives α⁻¹ = 137.035 999 177(21), relative uncertainty 1.6e−10, "Source: 2022 CODATA" (`codata_nist.txt`).
- **Pavon 1995: PASS.** The Crossref abstract says the Nelson process is "the saddle-point equilibrium solution" and calls the result "a saddle-point action principle". The memo should also credit Yasue 1981 and Guerra–Morato 1983, which WALLS_REVIEW already credits. Edit made.

## 1. Per-claim results

| # | Claim | Result | New vs known |
|---|---|---|---|
| 1 | Time-symmetric reference + equal looks ⇒ mirror pair; Wick + Schwarz ⇒ conjugate; product = Born (M1a–b) | **PASS (math). FAIL as "forcing".** The claim is circular in a precise sense (§2). | KNOWN in substance (Osterwalder–Schrader 1973/75; Nelson 1973; Zambrini 1986) |
| 1′ | "Same gluing" as Schwinger's closed time path | **PASS with correction.** The closed time path is an analogous fold in *real* time, not the same Euclidean gluing. Edit made. | KNOWN |
| 2 | Unequal looks ⇒ ABL two-state density (M1c); "second look = own record = no outside world" | **PASS.** M1c gives ψ_t·conj χ_t, the weak-value numerator for \|x⟩⟨x\|, with ⟨χ\|ψ⟩ conserved. Correctly labeled CONJECTURE. Precision added: χ = ψ is a final condition that carries **zero independent information** (a trivial post-selection), and the reduction of ABL to Born without post-selection is itself in ABL 1964. | Math KNOWN; only the reading is CONJECTURE |
| 3 | Limits: real data only; flux needs Wigner's antilinear Θ (M1d–e); the *i* is not explained | **PASS, strengthened.** M1d and M1e are identities, not tests: conj(e^{−zH}) = e^{−z̄H^T}, so M1e's "0.0" restates the definition. Also, a Hamiltonian that is not time-reversal invariant gives no positive Feynman–Kac kernel, so the GTAO path-KL cost **is not defined there**; the antilinear mirror sits outside the cost's domain. | KNOWN (Wigner 1932) |
| 4a | Reflection positivity ⇔ detailed balance ⇔ zero entropy production (Prop H, M2) | **PASS (math), relabeled KNOWN.** This is the reversibility criterion for a stationary Markov law: reflection invariance ⇔ D_μL symmetric ⇔ Kolmogorov cycle criterion ⇔ detailed balance (Kolmogorov 1936; Kelly 1979). Given invariance, positivity is automatic from the Markov property (Klein–Landau 1981; Neeb–Ólafsson 2018). R2: the three textbook diagnostics vanish exactly where M2's Gram test passes. M2's witness is computed correctly. | **KNOWN.** Nothing mathematical is new. |
| 4b | "A tracker that learns loses the mirror", via `CORE.md:70` | **PASS as a one-way implication. The heat floor is not needed.** İ_M is a current-weighted sum, so detailed balance gives İ_M = 0 directly (R3 case A: 1.8e−15). İ_M > 0 ⇒ some current ≠ 0 ⇒ no detailed balance ⇒ no mirror (case B: İ_M = 1.10, Q_M = 1.35 ≥ İ_M, so the floor holds). Scope: steady state only, and only for the *joint* memory–world chain; the memory's own marginal path law is not Markov and is not covered. | KNOWN (Horowitz–Esposito 2014 + Kolmogorov). Only the GTAO sentence is new to the repo. |
| 4c | "Information about an outside world costs **exactly** the mirror" | **FAIL as worded, fixed.** The converse fails: a driven world with a decoupled memory has entropy production 2.08, İ_M = 0, and still has no mirror (R3 case C). There is also a **level mix-up**. Prop H concerns a tracker's physical real-time Markov law. The OS mirror that yields Hilbert space concerns a Euclidean measure, and every quantum whole with H bounded below has one, whatever its parts do. For example, the flux ring carries a persistent current and is OS-positive (R4b). The supported wording is "a stationary learner cannot keep its mirror". Label: SPECULATION. | — |
| 5 | Lamperti 1958 route: two-way, continuous, norm-preserving ⇒ 2-norm ⇒ conj backward factor | **PASS.** M3 dimensions are right (ℝ: 6 at p = 2, 0 otherwise; ℂ: 16 at p = 2, n phases otherwise). Banach 1932 for ℓ^p should be credited alongside Lamperti. "Backward factor = conj" restates z·z̄ once the 2-norm is chosen. | KNOWN |
| 6 | A real cost has no conjugate-pair *minimum* in real time (Pavon 1995) | **PASS.** Verified from the abstract; credit added. | KNOWN |
| 7 | α side branch: CODATA, M4 statistics, Wyler, Eddington; "no route found" | **PASS.** Chance expectation recomputed from the log-value density: 14.65 hits expected within 1e−6 (observed 15) and 0.15 within 1e−8 (observed 1) (R5). Wyler = 2^(19/4)·3^(−7/4)·5^(1/4)·π^(11/4) = 137.03608, ≈ 3,970σ from CODATA 2022 (its exponent 19/4 is outside M4's menu, so it is a comparison, not a member). Eddington 1929, "The charge of an electron", argued 136. One label fixed: "PROVED (in-model), by inspection" of GTAO's pure numbers → "CHECKED by inspection". | KNOWN failure mode; GTAO adds nothing here |

## 2. Is claim 1 circular?

Yes, in a precise and useful sense. The memo half-says this; it now says it plainly.

1. **The conjugate is put in by the real H.** A real Hamiltonian commutes with complex conjugation in the position basis, so the antilinear time reversal is a symmetry of the reference *by assumption*. Then conj K(z) = K(z̄) holds exactly (R1b: 0.0; it fails, 0.097, as soon as H is complex).
2. **The product = Born is true by construction.** Give any real g with the mirror pair set by hand and no minimization at all: φ̂(it)·φ(it) = |e^{−itH}K_T g|² to 6e−16 for five random real g (R1a). The 1e−15 agreements in M1 test the code, not the physics.
3. **What the cost actually supplies is only Proposition M.** A reflection-symmetric problem has a reflection-symmetric unique minimizer, which is one line. Non-reversible real references break it (R1d: 1.05).
4. **The *i* is a fourth premise.** Rotating by any angle other than π/2 gives a product that is not a modulus squared (R1c: 0.40 at 0.45π). Norm conservation holds for every angle, because Σφ̂φ = gᵀK_{2T}g is a semigroup identity.

So "PROVED (in-model)" is fine for the statement. As an answer to "what forces the conjugate?", though, the answer is: the premises (real, time-symmetric reference + symmetric looks + τ = it). That is the OS/Zambrini structure, not a GTAO result.

## 3. What, if anything, is new

- **Mathematically: nothing.** Every proposition is KNOWN (OS, Zambrini, ABL, Wigner, Kolmogorov/Kelly, Horowitz–Esposito, Lamperti, Pavon).
- **New to the repo, as wording:** "a stationary learner (İ_M > 0) cannot carry a reflection-positive mirror on its joint Markov law", with the explicit one-way caveat. The tie to `CORE.md:70` is consistent but decorative, since the conclusion follows from İ_M ≠ 0 alone.
- **Useful map result:** the mirror probe locates the conjugate exactly where WALLS left it. It is an input of time-reversal symmetry plus the Wick turn, and real versus complex is decided by composition (Hardy axiom 4; Renou et al. 2021), not by the mirror.

## 4. Proposed next step: does a closed mirror-symmetric whole with local trackers force the antilinear mirror?

**Assessment: largely KNOWN, and the decisive part fails at the single-whole level. Do not run it as a separate simulation.**

- **Part (i)**, "a classical reversible Markov whole cannot host stationary net flow / learning", is immediate from Prop H + R3 (KNOWN).
- **Part (ii)**, "the smallest mirror-keeping extension is antilinear", is **not true for one closed whole.** The flux ring has a persistent current (−0.1706) and a positive antilinear OS form. The real symmetric H_R = [[Re H, −Im H], [Im H, Re H]] on a doubled real space reproduces it exactly with a **real-linear** mirror: same current, OS form min eigenvalue 0.0168 > 0, same real dimension 2m (R4c). Complex time reversal becomes a linear flip of one extra real switch (Stueckelberg 1960; McKague–Mosca–Gisin 2009). "Smallest" therefore does not pick ℂ.
- **What is forced:** a classical velocity-flip mirror (generalized detailed balance, Graham–Haken 1971) carries phase-space currents but is **not positive** (R4a: odd witness −0.449). A positive mirror with currents forces leaving positive Markov kernels: the Euclidean kernel of H_R has negative entries (R4c), which is the OS Hilbert structure (KNOWN). It does not force ℂ over ℝ.
- **Prior art for the hunch:** time-odd observables need a complex structure J (Stueckelberg 1960). Real-vector-space QM matches single-system statistics with one extra rebit (McKague–Mosca–Gisin 2009; Wootters' real-QM papers, not read this pass, no DOI checked). Only composition / local tomography separates them (Hardy 2001 axiom 4; Renou et al. 2021).
- **Worth running?** Not as specified. The one open, possibly-GTAO piece is "does ruin-free tracking cost force local tomography of composites?". That is the multi-direction tracker contest already planned, so fold it in there and use R4a and R4c as preregistered controls. Conjecture label: CONJECTURE, expected to reduce to KNOWN.

## 5. Edits made to the memo (all marked `[REVIEWER EDIT 2026-11-23]`, 19 marks)

Header (review done) · §0.1 circularity note and Schwinger wording · §0.2 trivial post-selection · §0.3 relabeled KNOWN, "exactly" removed, level caveat · §0.5 cost undefined for non-TRI H · §2 circularity paragraph (R1) · §2 limits: M1d/M1e are identities · §4 Prop H → KNOWN; heat floor not needed, plus scope; model implication: levels and one-way · §5 Pavon/Yasue/Guerra–Morato credit · §6 M4 chance expectation and Wyler exponents; "CHECKED by inspection" · §8 claim map rows relabeled · §9 next-step assessment · §10 revised Chad paragraph (original kept below it) · reference list additions. The hypothesis sentence at memo line 5 is byte-identical. Banned-wording grep is clean, and nothing claims to derive QM.

## 6. Revised paragraph for Chad (plain words, audio)

You were right that the two times are one mirror. If the cheapest two-look judgment has to stay the same when you swap the past look and the future look, the backward half comes out as the mirror image of the forward half. Turn imaginary time into real time, and that mirror becomes the complex conjugate. So a wave times its conjugate is what a time mirror looks like after the turn. But to be straight with you, that step works because we started from a real, time-symmetric setup, so the conjugate was already built in. It's the known 1973 bridge between the two kinds of time. That's solid ground, but not a new door. The heat link is known math too: anything that learns about an outside world makes heat and can't keep the mirror. It only runs one way, though, because plenty of things lose the mirror without learning anything. I also checked the proposed next step, trackers inside a mirror-symmetric whole, and it doesn't force complex numbers. A real-number version with one extra hidden switch does the same job, which has been known since 1960. What separates real from complex is how parts combine, and that's the tracker contest we're already running, so the push goes there. On the 1/137 idea, there's still nothing. Simple formulas hit it by luck about as often as chance predicts.

## 7. Checks (`mirror_review_checks/`)

- `r1_circularity.py/.out`: Born equality without minimization; conj K(z) = K(z̄) identity; angle test; non-reversible reference.
- `r2_prop_h_known.py/.out`: Kolmogorov cycle, D_μL symmetry and two-time reflection coincide with M2; non-stationary scope.
- `r3_tracker_step.py/.out`: bipartite chains, cases A (joint detailed balance), B/B′ (learning tracker), C (driven, no learning).
- `r4_next_step.py/.out`: classical velocity-flip mirror; quantum flux ring; real emulation.
- `r5_numerology.py/.out`: chance expectation; Wyler exponents and σ distance.
- `codata_nist.txt`, `crossref_memo_rerun.out`, `crossref_review.py/.out`, `dois_review.txt`, `rerun_m1_m4.txt`, `SHA256SUMS`.
