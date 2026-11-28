# FINAL_VERIFY: PR #86 (branch `bookends`, head 341a4ed59ef24bc2a683c04bac0023a36b84eff9)

Fresh independent hostile verifier. Wed 18 Nov 2026, evening ET. Fresh clone in /tmp/rev-final. Nothing pushed, merged or commented.

## Verdict: **MERGE-AFTER-FIXES**
All fixes are wording only. No status label needs to change. No further review round is needed if the edits below are made as stated.

## Checks
1. **Round 2 fixes in BOOKENDS rev 3: all present, verified against the text.**
   - MATH R2-1: conditional mean ≤ −δ and supermartingale (l.134); "evidence" placed under the condition (l.136); τ_mix caveat with the counterexample and Markov form OPEN (l.137).
   - MATH R2-2: class 2 and class 3 "response" (BK-P1/P3; SCALE_ENDS class table).
   - MATH R2-3: N26 pre-Page scope, in CLAIM_MAP, THEORY, SCALE_ENDS, BRIEF and README.
   - MATH R2-4: "physical argument, not computed" (l.149, N25).
   - MATH R2-5 and PHYS R2-2: hurricane wording (l.91).
   - MATH R2-6: r·Λ (l.309).
   - MATH R2-7: "IMP-like"; D_ℓ′ = D_ℓ; same time index (l.143).
   - PHYS R2-1 and BIO R2-4: BK-G2 arms T/S/C/L, Arnold tongue and PRC premise, not preregistered (l.174–185).
   - PHYS R2-3: Lan and Cao (l.166, l.272, kill (ii)).
   - PHYS R2-4: hedges (l.71, Q5).
   - PHYS R2-5: (a)–(c) (l.239).
   - PHYS R2-6: Lilly condition (l.204).
   - PHYS R2-7: "extends by analogy"; Chen & Benton kept out of canonical files.
   - PHYS proposal edits P2, P4, P6, P9, P11 and P13: present.
   - BIO R2-1: own ruin variable and regulator without stakes.
   - BIO R2-2: partial fate and Frank's "not sufficient".
   - BIO R2-3: BK-IMP (a)–(c).
   - BIO R2-5: kill (iii).
   - BIO L1–L3: present.
   - One residual is in a fix itself; see required fix 1 (Ma quote).
2. **Canonical diff.**
   - No silent status changes: CLAIM_MAP status columns main→bookends differ only by the new N30–N35. N26's scope narrowing is declared.
   - N30 DECIDED, N31 and N32 OPEN, N34 PRIOR ART and N35 OPEN are correct.
   - **N33 PROVED (in-model), supermartingale scope, Markov OPEN: honest.**
     - One-sided Azuma–Hoeffding for a supermartingale with bounded differences is valid, and {survive to T} ⊆ {R_T > 0}.
     - It matches the CLAIM_MAP convention for elementary in-model derivations (M1, M3).
     - The caveat sits in the row.
   - **Recomputed:**
     - `finite_horizon.py` reproduces its .out exactly (T = 1600: 0.0034 vs bound 0.1724; δ = 0.05).
     - `markov_counterexample.py` reproduces: p = 0.001, T = 1600 gives 0.2687 vs 0.0005; p = 0.01, T = 1600 gives 0.0684 vs 0.0005. This matches BOOKENDS l.137.
   - **Remaining contradictions:** see required fixes 2–6.
3. Never "law" or "theory of everything" (BOOKENDS l.34; README l.9). No field evidence claimed; "untested, not refuted" kept. No claim that the theory explains ants. Consciousness is out of scope (l.254; N34 imposter line).
4. No personal data, no box paths, no private content in added lines (grep of the whole diff for /workspace, /home, /tmp, /cursor, emails, names, Looper and Nelnet: clean).
5. The README spine (second law as backbone; judgment = acting ahead to stay alive under it) matches THEORY §0 and BOOKENDS §0.1 and BK-P9 verbatim. Newcomer flow is coherent, apart from fix 3.
6. Tooling:
   - `check_consistency.py`: PASS (FAIL 0; N1..N35; 169 refs, 0 mismatches).
   - `test_check_consistency.py`: PASS.
   - `pytest tools/`: 50 passed.
7. Citations opened (Europe PMC and arXiv abstracts):
   - Lan 2012: OK.
   - Frank 1995: OK.
   - Lilly 2013: OK (the condition is quoted correctly).
   - Yachi & Loreau 1999: OK.
   - Barkai & Leibler 1997: OK.
   - Cao 2015: OK.
   - **Ma 2009: misrepresented** (fix 1).

## Required fixes
1. **Ma 2009 quote is selective.** The abstract says both cores "emerge as **robust** solutions"; the BOOKENDS text drops this. It does not support "IFFLs generally adapt only in tuned regions", and it means BK-IMP (b) alone cannot separate IFFL from integral feedback.
   - Where: theory/BOOKENDS.md:127 (BK-IMP (b) cell); measurement/CLAIM_MAP_v2.md:375 (N31 "Incoherent feedforward loops can adapt in tuned regions"); litmap/LITMAP.md:49 (Ma row).
   - Fix: quote "only two major core topologies emerge as robust solutions" in full. Say that robustness (b) does not by itself exclude an IFFL, so the structural check (c) is what separates feedback from feedforward. Drop "generally only in tuned regions" unless a source for it is opened.
2. **√r wording is inverted.** "under-watching shrinks to about √r (≈ 0.87)" reads as 87% under-watching.
   - Where: theory/BOOKENDS.md:309, theory/BOOKENDS.md:376 (BK-P10 text), THEORY.md:221.
   - Fix: "watching falls only to about √r of its optimum (≈ 0.87 for r = 3/4), so under-watching is small (≈ 13%) but not zero".
3. **README contradicts THEORY §6 (BK-P10).**
   - Where: README.md:34, which reads "Otherwise expect enforcement (free riders; Ostrom)".
   - Fix: "Otherwise expect shared fate or enforcement, usually both (shared fate is usually partial; Frank 1995; Ostrom). CLAIM_MAP J9 OPEN."
4. **Label mismatch for the same result.** BOOKENDS calls it DERIVED; CLAIM_MAP N33 calls it PROVED (in-model).
   - Where: theory/BOOKENDS.md:133, "(DERIVED, elementary, …)".
   - Fix: "(PROVED (in-model) in CLAIM_MAP N33 terms; elementary; supermartingale scope; Markov form OPEN)".
5. **Withdrawn level count is still listed as a contribution.**
   - Where: litmap/PRIOR_ART.md:27, "T7b (…; K\* ∝ L^{2/3})".
   - Fix: append "(L^{2/3} count withdrawn in THEORY v1.4; CLAIM_MAP K12; THEOREMS T7(iii))", matching LITMAP, THREATS and LEFT_ON_THE_TABLE.
6. **The §9 applied-text block in SCALE_ENDS still states the pre-BOOKENDS wording.** It says "Stars are held without a model (h = luminosity; feedback on their own state)" and "Models switch on only with heredity…".
   - Where: theory/SCALE_ENDS.md:286 (§9 header, l.284).
   - Fix: add "*(As applied in v1.4.18; superseded in part by v1.4.20: BOOKENDS BK-P5, BK-P7, BK-P11.)*" to the §9 header.

## Recommended (not blocking)
- README.md:40: "Update, 18 Nov 2026 (v1.4.18)" is a stale version label. Change it to v1.4.20 or drop it.
- theory/SCALE_ENDS.md:44: the H80-ladder row lists "stars" as where it applies. Add "(as self-regulation, not the thermostat rung; §4.1)".
- theory/BOOKENDS.md:73: "J9" → "CM-J9".
- theory/BOOKENDS.md:136: state the Monte Carlo parameters (B = 5, δ = 0.05, b = 1) so the 0.003 vs 0.17 can be read against l.137's δ = 0.1.
- After merge, update "branch `bookends`, PR #86, not merged" in THEORY.md:527, measurement/CLAIM_MAP_v2.md:77 and the STATUS and SCALE_ENDS headers to "merged".
