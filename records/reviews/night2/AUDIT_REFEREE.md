# AUDIT_REFEREE: hostile independent review of the night-2 divergence audit, THEORY.md v1.2, Proposition SG, and the queue ledger

Sunday 15 November 2026, about 09:20 AM ET (America/New_York). Written by a hostile independent referee subagent for Chad Mitchell (via Ace). Private. Nothing posted or sent.

**Scope.** Repo `<repo>`, current `main` at `d3a6013` (after PR #4 `db6ee2d` and PR #5 `fb920c3`). Sources were read, not summaries. Independent math was re-derived; fBm and SG Monte Carlo were re-run under `nice 19` (scripts and outputs in `reviews/night2/AUDIT_REFEREE_checks/`). Working copies in `<local>/gtao/` were used only as cited artifacts, including frozen backups.

**Verdict at a glance**

| # | Task | Verdict | One line |
|---|---|---|---|
| 1 | \(a=b=1/(1+2H)\) for read-and-hold fBm | **Confirmed** (continuous time); discrete-time elasticity approaches the same limit | Lemma 1(i) is standard EOQ calculus. Path simulations recover the exponent to \(\approx 0.01\) for \(H\ge 0.35\); at \(H=0.20\) a small-\(T\) discrete bias appears and vanishes at large \(T^*\). |
| 2 | Proposition SG derivation and slope | **Corrected** | The decision algebra and \(p_0\) formulas are right. "Slope 1" is the large-age limit, not a fitted identity. The project's 0.995 is the last-three-points window only (all six reported ages: 0.947). Monte Carlo matches. |
| 3 | Divergence table, \(\ge 8\) rows | **Confirmed** on the material conclusions; **corrected** on two details | Rows 1, 2, 3, 7, 8, 10, 11, 13, 14, 15 checked line by line. Two slips: "2 of 165" is 2 of 167; "13 minutes after the referee" is 25 minutes after the report's claimed 08:20 ET (13 minutes after the 08:32 STATE note). |
| 4 | THEORY.md v1.2 internal consistency | **Corrected** | The two-core contradiction in the header is fixed, labels are in place, and GTAO is not called a law. Leftover "KILLED" field wording remains in §1 and §8b. §2.5 misstates Axiom 6. |
| 5 | `sg_rank.py` vs QUEUE, and ledger scoring | **Corrected** (can score later only after fixes) | The index formula matches QUEUE and reproduces `rank_0.out`. The ledger cannot yet support a clean AUC: inconsistent uniform-seed conventions, a declared protocol breach on pick 2, missing stored index values, and a ranking that is almost entirely the judgment product \(w v L/c\), not the SG clock. |

The audit's bottom line (working copies drifted from a two-core text; the SELF \(\sqrt{\,}\) test was a regime-A instance with its premise unmet) survives this review. The corrections below are exact; they do not overturn the audit's main findings.

---

## 1. The claim \(a = b = 1/(1+2H)\)

**What was checked.** THEORY.md v1.2 §2.5 and AUDIT_DIVERGENCE.md §2, against `reviews/night1/formal/THEOREMS.md` Lemma 1(i), `AXIOMS.md` (Axiom 1, class R1), and `ARCH_EQUATION.md` §2.1 / §0 item 2. Then an independent derivation and a path simulation.

**Derivation (continuous time).** Standard fBm with scale \(q\) has \(\mathbb{E}(X_{t+\tau}-X_t)^2 = q\,\tau^{2H}\) (Axiom 1). A reset read returns the current value; the tracker holds it until the next read (R1, zero-order hold). Over an interval of length \(T\), mean squared error is

\[
\frac{1}{T}\int_0^T q\,s^{2H}\,ds = \frac{q\,T^{2H}}{1+2H}.
\]

With upkeep \(c/T\) and squared-error stakes \(W\),

\[
J(T)=\frac{c}{T}+W\cdot\frac{q\,T^{2H}}{1+2H}.
\]

The first-order condition gives \(T^* = \bigl[c(1+2H)/(W q\cdot 2H)\bigr]^{1/(1+2H)}\), refresh rate (effort) \(n^*=1/T^* \propto (Wq)^{1/(1+2H)}\), and minimized cost \(\varphi \propto c^{2H/(1+2H)}(Wq)^{1/(1+2H)}\). So the cost and effort elasticities are \(a=b=1/(1+2H)\), and the information-spend share is \(2H/(1+2H)\). This is exactly Lemma 1(i). At \(H=1/2\) it is the EOQ square-root law. The elasticity identity \(d\log n^*/d\log W = 1/(1+2H)\) is exact for this estimator, not a fit.

**Scope, already stated in the formal layer and correctly repeated in §2.5.** For \(H\neq 1/2\), hold-last-value is a restricted technology (a predictor that uses the path does better). Periodic reading is proved optimal only for Brownian quadratic R1 (Lemma 1(vii)). The claim as stated is about this restricted estimator, not about the optimal linear predictor. That is a real limit on using \(1/(1+2H)\) as "the" spectrum-to-read-rate map; QUEUE item Q2 already lists the optimal-predictor case as owed.

**Numerical check** (`AUDIT_REFEREE_checks/fbm_exponent.py`, Davies–Harte fGn, 48 paths of length \(2^{14}\), seed 20261115, cost \(c=1\), optimize \(T\) on simulated hold-MSE, then fit \(\log n^*\) on \(\log W\) and on \(\log q\)). Hold-MSE on the paths matches the discrete-time mean \(T^{-1}\sum_{k=0}^{T-1} k^{2H}\) to about 1% (better at mid \(H\); a few percent low at \(H=0.85\)). It does *not* match the continuous integral at small \(T\) (at \(T=2\), discrete MSE is \(0.5\), continuous is \(T^{2H}/(1+2H)\approx 1\)). That is the right discrete comparison, not a bug.

| \(H\) | Theory \(1/(1+2H)\) | Fitted \(\hat a\) (sim MSE vs \(W\)) | Fitted \(\hat b\) (vs \(q\)) | Exact discrete-grid \(\hat a\) | Continuous \(J\) numeric min |
|---|---|---|---|---|---|
| 0.20 | 0.7143 | 0.7585 | 0.7585 | 0.7276 | 0.7142 |
| 0.35 | 0.5882 | 0.5853 | 0.5853 | 0.5890 | 0.5881 |
| 0.50 | 0.5000 | 0.4997 | 0.4997 | 0.4990 | 0.4999 |
| 0.70 | 0.4167 | 0.4145 | 0.4145 | 0.4156 | 0.4166 |
| 0.85 | 0.3704 | 0.3698 | 0.3698 | 0.3693 | 0.3703 |

\(\hat a=\hat b\) is identity in this design (MSE scales linearly with \(q\), so varying \(q\) at fixed \(W\) is the same grid as varying \(W\)). For \(H\ge 0.35\), simulated elasticities sit within \(0.01\) of theory. At \(H=0.20\) the small-\(T\) discrete bias is visible. Restricting the exact discrete problem to \(T^*\in[80,2000]\) gives \(\hat a=0.7165\), against 0.7143. The continuous-time claim is confirmed; any discrete implementation should treat \(1/(1+2H)\) as the large-interval limit.

**No error in the stated formula.** No change to Lemma 1(i) or to the "constants are functions of \(H\)" slogan.

---

## 2. Proposition SG

**Statement checked** (AUDIT_DIVERGENCE.md §6, THEORY.md §2.5, `AUDIT_checks/sg_check.py` / `.out`).

An item changes at the events of a renewal process. Age \(a\) is time since the last change, \(S\) the survival function, \(h\) the hazard. New evidence has likelihood ratio \(\Lambda\) for "a change in \((a,a+\Delta]\)". Follow up iff \(w L p > c\), with posterior odds \(p/(1-p)=\Lambda\cdot p_0/(1-p_0)\) and \(p_0=1-S(a+\Delta)/S(a)\).

**Algebra, confirmed.** Rearrangement of \(p>c/(wL)\) (which needs \(wL>c\)) gives exactly

\[
\ln\Lambda^* = \ln\frac{c}{wL-c} - \mathrm{logit}\,p_0.
\]

- Regime A (exponential): \(p_0=1-e^{-\lambda\Delta}\), independent of \(a\). The time since the last *change* is uninformative. Confirmed.
- Regime B (Lomax / Pareto II, \(S(t)=(a_0/(a_0+t))^\gamma\), \(h=\gamma/(a_0+t)\)): \(p_0=1-((a+a_0)/(a+\Delta+a_0))^\gamma\). For \(a\gg \Delta,a_0\), \(p_0\sim \gamma\Delta/a\), so \(\ln\Lambda^* = \mathrm{const} + \ln a + o(1)\). The slope on \(\ln a\) tends to 1. Confirmed as a limit.

**The write-up overstates the slope.** AUDIT §6 and THEORY §2.5 say the surprise needed "grows as \(\ln a\) with slope 1". The project's own check reports "fitted slope … = 0.995" from the last three of the six printed ages (100, 300, 1000). An independent refit (`AUDIT_REFEREE_checks/sg_refit.py`, different seed 20261116) reproduces those six threshold values to the reported three decimals and the 0.995 on that window. It also shows:

| Window | Slope of \(\ln\Lambda^*\) on \(\ln a\) |
|---|---|
| Project last 3 (100, 300, 1000) | 0.9950 |
| All 6 project ages (3 … 1000) | 0.9466 |
| Extended last 3 (1000, 3000, 10000) | 0.9995 |
| Exact \(d\ln\Lambda^*/d\ln a\) at \(a=3\) | 0.7027 |
| Exact derivative at \(a=10\) | 0.8859 |
| Exact derivative at \(a=100\) | 0.9872 |
| Limit \(a\to\infty\) | 1 |

At age 3 (three times \(\Delta\)), the instantaneous slope is 0.70, and \(\gamma\Delta/a\) overstates \(p_0\) by 56%. "Slope 1" should be labelled as the large-age limit. CLAIM_MAP_v2 row N8 ("PROVED (in-model)" that the threshold "rises as \(\ln(\mathrm{dormancy})\) with slope 1") should say the same.

**Monte Carlo.** The project's \(p_0\) check matches to three decimals; the one slightly large gap (age 100: 0.0042 vs 0.0039) is Monte Carlo noise. An independent 2,000,000-draw run is within 1 SE at every reported age except one 2.1 SE fluctuation at age 1, as expected.

**Other limits, not fatal but not written clearly enough.**

1. Expected loss \(w L p\) is a one-shot approximation: it charges the whole horizon \(L\) if a change occurred anywhere in the \(\Delta\)-window, and is not a renewal-reward or Whittle-index optimum. Fine as an elementary rule; not a complete optimal-search theorem.
2. Lomax is a *model* of decreasing hazard, not a derivation from a scale-free spectrum \(S(f)\propto f^{-\alpha}\). The leap from THEORY §2 regime B (spectrum) to a Lomax inter-event law is a modelling choice and should be named as one.
3. Prior art as described (Whittle / restless bandits, crawler revisit policies, Itti & Baldi, information foraging) was not re-audited here beyond the audit's own caveat (three web searches). The "regime-conditional clock" is a plausible candidate increment, not a demonstrated novelty. Q1 already flags this.

**Fit to SELF, as a motivation, is fair:** most later changes were dormant items reawakening, and every *schedule* lost to uniform. That does not confirm SG on new data.

---

## 3. Divergence table, line by line

Sixteen rows were listed. Ten were checked against the cited artifacts (more than the required eight), with emphasis on the seven "material" rows. Night-1 files in the repo and in `<local>/gtao/night1/` were used; chat rows used the parent conversation as relayed plus the frozen STATE file.

**Row 1 — theory-v3 PREDICTIONS P1–P4 + SCALEFREE (14 Nov 23:46). Verdict: confirmed (none).** `<local>/gtao/theory-v3/PREDICTIONS.md` (mtime 23:46) locks a within-item recall slope \(a_c\in[0.5,1.2]\) from "recall odds \(\propto\) need odds with exponent ratio \(d\ge 1\)" (SCALEFREE §2.1), i.e. regime B. CLAIM_MAP_v2 H1 is PROXY-FAIL. "Divergence: none" and "P1 stays PROXY-FAIL" are right.

**Row 2 — night1 CORE_AUDIT (00:40). Verdict: confirmed (minor).** `<local>/gtao/night1/CORE_AUDIT.md` header and repo copy match 00:40. C5 does take the core to include the drift spectrum. Prediction B is a vigilance ratio "about 2" in the small-share free-upkeep regime, and §2.5(e) calls \(\Pi^*\approx 4\) and vigilance \(\approx 2\) "dimensionless constants that are the same on every substrate". Those numbers are the \(H=1/2\) instance. "\(\ge 2\)" (CORE_AUDIT line 151, small-\(\rho\) regime) was already math-corrected: at zero upkeep \(V=1+(1+\rho)^{-1/2}\), which is *less than* 2 at finite \(\rho\) and equals 2 only as \(\rho\to 0\).

**Row 3 — night1 ARCH_EQUATION (01:09). Verdict: confirmed (material, not wrong, unpropagated).** File header "about 00:40–01:10 ET"; gtao copy mtime 01:09. §0 item 2: constants are "universal *functions* of one measurable exponent" and move with \(H\). §0 item 5: layered memory "adds only 'approximation theory plus a price'". THEORY v1.1 §0/§2 did not absorb the demotion. v1.2 states it in §2.5 while keeping log-spaced layers as the regime-B *hypothesis*. That is an honest unpropagation, not a math error. (Citation nit: the audit says "ARCH_EQUATION §0.2"; the file has §0 numbered items, not a subsection 0.2.)

**Row 4 (spot). Verdict: confirmed (minor).** Formal AXIOMS/THEOREMS "final revision 02:22 ET". Theorems are in \((a,b)\); Axiom 1 defaults to Brownian and allows fBm; quoted class-R numbers \(a=b=1/2\) are \(H=1/2\) instances; Lemma 1(i) already has \(1/(1+2H)\).

**Row 7 — night1 SYNTHESIS CLAIM_MAP_FINAL + THEORY v1.1 §8b (03:05). Verdict: confirmed (material).** `<local>/gtao/night1/SYNTHESIS/CLAIM_MAP_FINAL.md` is dated "about 03:00–04:00 AM ET". THEORY at `e76f5a6` (15 Nov 03:04 ET) and at the 08:20 measurement note (`b13f734`) both list the same six formal items under "What is genuinely the theory's own" and zero spectrum-map items, while §0/§2 still call the spectrum the core. v1.2 adds §2.5 rather than rewriting that list; the list is unchanged in the current file. The disagreement was real; the reconciliation is additive.

**Row 8 — FRAMEWORK + CLAIM_MAP_v2 (08:20). Verdict: confirmed (minor), with a count slip.** At `b13f734`, FRAMEWORK §6.7 line 632 says "For class R, \(b=1/2\)" with no \(H\). The current file correctly reads "For class R, \(b=1/(1+2H)\) with \(H\) measured on the same targets (\(\tfrac12\) only at \(H=\tfrac12\); v1.2 correction)". K12 and K13 sit in section K, "Earlier repo claims (THEORY v1.0 and public X posts)", both OPEN. **Count: 167 claim rows in v2.0, not 165** (the file's own "Counts" section says 167; a mechanical count of claim IDs agrees). The "2 of 165" in AUDIT §0 and §4 should be "2 of 167". Current v2.1 has 176 rows (9 added in section N).

**Row 10 — SELF prereg P2, P3b (08:15). Verdict: confirmed (material).** `reviews/night2/SELF/PREREG.md`: "Sensing class for Ace pulls: reset-type … \(a=b=1/2\)" and "Hence GTAO's effort elasticities: 1/2 in drift, 1/2 in stakes (THEOREMS L1 viii)". P2 and P3b are \(\propto\sqrt{\mathrm{drift}\times\mathrm{stakes}}\) as "GTAO R1". The citation does not name the file, the regime, or \(H\). P3a tests persistence but is not a gate on P3b. RESULTS: P3a Spearman \(\rho=-0.06\) (CI \(-0.36\) to \(0.26\)); P3b G/U \(=1.20\) (CI 1.01–1.37). The corrected label "\(\sqrt{\,}\) allocation failed on a statement-time proxy; premise unmet (scope)" matches the referee and CLAIM_MAP N5. This was not a test of the spectrum core.

**Row 11 — SELF P1. Verdict: confirmed (material, over-read).** The prereg equates "scale-free / bursty" and treats a Poisson-CV pass as regime B. RESULTS called P1 a PASS (median CV 0.82 vs Poisson band 0.45–0.76). The referee (`REFEREE/REPORT.md`, claimed 08:20 ET) downgraded it: an observer-schedule null that places events at the times Chad actually told Ace anything gives a 95% band of 0.60–0.92 containing 0.82. Burstiness is not a scale-free spectrum, and this burstiness is explained by the conversation schedule. CLAIM_MAP N4 is now "OPEN (regime not established)". Correct.

**Row 13 — GITHUB-UPSTREAM PREREG (08:37). Verdict: confirmed (material for P1/P2/P6).** `<local>/gtao/night2/GITHUB/PREREG.md` §4 (file 08:37): "class R … \(a=b=1/2\)"; P1/P2 band \([0.35,0.65]\); P6 floor \(1+(1+\hat\rho)^{-1/2}\); drift is "smoothed rate of state changes of the weekly binary state" (event frequency; FRAMEWORK §3.1 lists this as a failure mode). The addendum `reviews/night2/GITHUB_ADDENDUM_REGIME.md` is a pre-outcome gate, as claimed: at writing, only search/file/repo JSON were present; it adds an Allan-factor \(\hat H\) rule and replaces the band with \(1/(1+2\hat H)\pm 0.15\) when regime A is rejected. The addendum is the right kind of fix.

**Row 14 — STATE.md (08:15). Verdict: confirmed (material), with a sharper observation.** Frozen file `<local>/gtao/pre-audit-backup-2026-11-13/STATE_frozen_2026-11-15_0843.md`, header "Updated: 2026-11-15 ~8:15 AM ET". The "Status of claims" section lists only formal-layer items (V formula, onset exponent, \(\kappa^*\), freeze/hold band). No drift-spectrum / regime language in that section. Current `<local>/gtao/STATE.md` is a pointer, as the audit says. The same frozen file, however, already contains an 08:32 note of the referee's burstiness downgrade *and*, below it, an 08:45 "Correction t1910" that still says "P1 bursty PASS (regime B)" and "as current theory expects". The contradiction was inside one working file, not only between chat and referee.

**Row 15 — Ace's t1909s8633 and the t1910 reply (~08:45). Verdict: confirmed (material), time arithmetic corrected.** The t1909 summary presented the \(\sqrt{\,}\) rule as what failed for GTAO. The t1910 reply (parent conversation) correctly withdrew that as a theory failure, then said bursts were "the signature of the scale-free regime" and "the current theory says the \(\sqrt{\,}\) schedule should fail here". THEORY.md does not derive that last claim; the right reason, as the audit later says, is that the stable per-item rate premise failed (P3a). The referee report is claimed at 08:20 ET and is already summarized in STATE at 08:32. The 08:45 correction is **25 minutes after the report's claimed time**, or 13 minutes after the 08:32 STATE note — not "13 minutes after the blind referee had downgraded it" if that points at the report itself.

**Rows 5, 6, 9, 12 (lighter check).** LEARNSIM PREREG/PREREG_2 is an in-model T1.8 test with Brownian drivers declared ("Regime A by design") — "none" is right. VIGIL_ONA H1 is a direction that does not need \(H\); H3's band 0.3–0.7 is the \(a=1/2\) growth band (`FAIR_MEASURE.md`: "grows as \(N^a\) (\(a=1/2\) in class R)"); referee overturned H3 to inconclusive — "none (direction); minor (H3 band)" is right. In-model night-1 sims were not re-run here.

**Counts.** Material 7 (rows 3, 7, 10, 11, 13, 14, 15), minor 5, none 4: the classifications on the rows checked are fair. "None of the in-model mathematics [or] locked numbers" change: agreed, subject to the Axiom 6 wording in §4 below (a wording error, not a changed proof).

---

## 4. THEORY.md v1.2 internal consistency

**What improved (confirmed).** v1.1 at `b13f734` (08:20 ET) really did contradict itself, as the changelog says: a night-2 note that no field test measured validly, and "Title decision (Chad, t1908): keep it", sat above a "Status at a glance" that still said "**Killed on real data:**" and an "**Open decision (title).**" block. v1.2 rewrites the header, names this file as canonical, adds §2.5 (formal layer inside the spectrum core; "regime first"; Proposition SG), states Chad's physics position in §2.3 as an open disagreement with a test, adds §8c, and points §11 at `QUEUE.md`. Labels (KNOWN / PROOF / HYPOTHESIS / POST HOC) are used throughout. GTAO is not called a law; the opening paragraph forbids it. "½ law" / "square-root law" appear as names of scalings, and Lee, Flack & Krakauer are credited for a "universal law" of theirs. That wording is acceptable if it stays attributed or generic.

**What is still inconsistent.**

1. **Field "KILLED" labels were removed from the header and left in the body.** The status block now says no field result is a kill and results are "passed / failed on proxy X". The body still says: N1 "LANG1 on languages was killed"; N6 "The item-level news test P1 was **killed** on 15 Nov"; §8b P1 verdict "**KILLED**"; VIGIL-2 "**KILLED** on this instrument". CLAIM_MAP_v2 already has PROXY-FAIL for H1 (P1) and the corresponding Enron row. Locked *in-model* kills (SENSING class R, SENSING2, LAYERS1 P2, ANTS1) may keep "KILLED" as locked-simulation language; the field ones should match the header.

2. **§2.5 misstates Axiom 6.** Current text: "The formal layer allows one held value per tracker (Axiom 6), so regime B's predicted design (a log-spaced ladder of stores) cannot be expressed there." `reviews/night1/formal/AXIOMS.md` Axiom 6(iv) explicitly includes "clocks (separately timed components) inside a tracker." ARCH_EQUATION treats those clocks as speed layers. The missing piece is a *derivation* of the joint map from a measured spectrum to the number and spacing of those clocks (EXTENSIONS item 6 already says the formal layer does not touch the forgetting-exponent map) — not an inability to express a ladder. Exact fix: replace the "one held value / cannot be expressed" sentence with: "Axiom 6(iv) allows separately timed clocks inside a tracker, but the formal theorems do not derive the joint map from a measured spectrum to the number, spacing and forgetting exponent of those clocks; R1's hold-last-value estimator is also a restriction for \(H\neq 1/2\)."

3. **§8b still lists only the six formal items as "genuinely the theory's own."** §2.5 and the header now say the spectrum map is the headline and the least developed part. That is a remaining pedagogical contradiction, not a numerical one. A one-line pointer at the top of that list would close it.

4. **Proposition SG in §2.5** should say "slope 1 in the large-age limit" (see §2).

None of these revive the v1.1 header contradiction. The "one canonical statement" rule is in place and is the right fix for the process failure the audit diagnosed.

---

## 5. `sg_rank.py`, QUEUE, and whether the ledger can score the rule

**What the code does (confirmed, with one design note).** `queue/sg_rank.py` implements

\[
I_k = w_k\,P_k\,v_k\,L_k / \max(c_k, 0.5)
\]

with untested items at \(P=0.5\) and otherwise the regime-B Lomax prior updated by the locked LR scale, \(\gamma=0.4\), \(a_0=\Delta=1\) day — the formulas in the module docstring and in QUEUE.md step 3b. Running `python3 queue/sg_rank.py queue/items.json` reproduces `queue/rank_0.out` byte-for-byte on the reported ranks and indices (SELF-2 \(P=0.74695\), printed 0.747; ONA-MORE \(P=0.4696\), printed 0.47). Q0 is not in `items.json` and sits above the ranking, as QUEUE says.

The index is not identical to Proposition SG's follow-up test \(w L p/c\): validity \(v\) is an extra judgment factor, and \(P\) for "untested" is a flat 0.5 rather than a renewal prior. That is a reasonable operational extension if logged, which it is.

**What already fails the written protocol.**

1. **Uniform-seed convention is not one rule.** QUEUE.md: "a seeded uniform pick (seed 20261115 + entry number)". Ledger entry 1 logs `uniform_pick_seed20261115: WIKIDATA-BAND`. That value is `random.Random(20261115).choice(items.json order)` — seed *without* adding the entry number, in *file* order. (Seed \(20261115+1=20261116\) in the same order gives GITHUB-UPSTREAM.) Ledger entry 4, added in PR #5, logs `uniform_pick_seed20261119: SPECTRUM-MAP-DERIVE`. That value is `random.Random(20261115+4).choice(sorted(remaining ids))` — now seed *plus* entry number, in *sorted* order. The same Python `choice` on file order gives IMMUNE, not SPECTRUM-MAP-DERIVE. Two picks, two conventions. `sg_rank.py` does not draw the uniform pick at all.

2. **Protocol breach already recorded, correctly flagged.** Entry 3 is an `unaided_order` written *after* `sg_rank.py` was run for pick 2, with `protocol_note` to exclude it from Q0 scoring. Entry 4's timestamp (09:08) is also earlier than entry 3's (09:09). The second unaided ranking is not a usable baseline. The flag is honest; it also shows the "write unaided first" rule failed on the second pick.

3. **Numeric indices are not in the ledger.** Only order lists are stored (plus `rank_*.out` files). AUC "of the rule's index" needs the stored \(I_k\) (or at least ranks) at each ranking, especially once items.json is updated. Ranks can be recovered from the logged order for these two snapshots; that will not stay true if a later entry omits an output file or changes parameters without a `rule_change` line.

4. **The current ranking barely uses the SG clock.** Eight of ten items in `items.json` are `untested` with \(P=0.5\). Only SELF-2 and ONA-MORE use dormancy and surprise. The live order is almost entirely the judgment product \(wvL/c\). A later AUC can still be computed, but a pass would not yet be evidence for Proposition SG's regime-B threshold; it would be evidence for this scoring rule, driven by hand-set \(w,v,L,c\). \(\gamma=0.4\) is a rounding of SELF P1b's \(-0.39\), itself INCONCLUSIVE against the locked \([-1.0,-0.5]\) band and measured on the observer-schedule-confounded statement-time proxy. QUEUE already flags "regime not established"; the locked \(\gamma\) is still a weak premise.

5. **Scoring design is under-specified.** After \(\ge 15\) completed items, AUC of the rule vs Ace vs uniform for "CLAIM_MAP status changed" can be computed *if* each completed item has: the rule index (and rank) at a declared time, Ace's unaided rank from a pre-rule entry, a uniform score generated by one frozen RNG convention, and an `outcome` record (kind `outcome` is specified in QUEUE.md and has not yet appeared). Gaps that will bias or void that test if left as is:
   - Only the rule's top item, or every third time Ace's top, is picked. Items low on both lists may never complete, so AUC on completed items is weakly identified.
   - Re-ranking before every pick changes scores; the prereg should say whether the predictor is the first-seen index, the at-pick index, or something else.
   - Uniform is logged as one pick, not a full ranking. A full random permutation (or a stored uniform score per item) is what "AUC vs uniform" needs.
   - "Status change" will miss useful work that leaves a row OPEN. That is already named as a proxy; keep it, but do not read a pass as "the theory guided us to truth."

**Can the ledger score the rule later?** Yes, in principle, after the exact fixes in §6. As of entries 0–5 it cannot: one of two unaided orders is excluded by the project's own breach flag, the uniform baseline is not generated by one documented procedure, and no outcomes exist. Do not start the \(\ge 15\) clock until the protocol is tightened and applied consistently.

---

## 6. Exact fixes

1. **THEORY.md §2.5 and AUDIT_DIVERGENCE.md §2 (Axiom 6).** Replace "The formal layer allows one held value per tracker (Axiom 6), so regime B's predicted design (a log-spaced ladder of stores) cannot be expressed there" with: "Axiom 6(iv) allows separately timed clocks inside a tracker, but the formal theorems do not derive the joint map from a measured spectrum to the number, spacing and forgetting exponent of those clocks; R1's hold-last-value estimator remains a restriction for \(H\neq 1/2\)."

2. **THEORY.md field language.** In §1 (N1, N6) and §8b (P1, VIGIL-2), replace "killed" / "**KILLED**" with the measurement-layer labels already in CLAIM_MAP_v2 ("failed on proxy X" / PROXY-FAIL). Leave locked in-model simulation failures labelled as such.

3. **Proposition SG slope.** In THEORY.md §2.5, AUDIT_DIVERGENCE.md §6, and CLAIM_MAP_v2 N8, write "grows as \(\ln a\) with slope 1 in the large-age limit (\(a\gg\Delta,a_0\))" and report the all-ages fitted slope (0.947 on the six printed ages) alongside the last-three-points 0.995, or drop the 0.995 as if it were the theorem.

4. **AUDIT count and timing.** "2 of 165 rows" → "2 of 167 rows" (CLAIM_MAP_v2 "Counts" at `b13f734`). "13 minutes after the blind referee" → "25 minutes after the referee report's claimed time (08:20 ET), 13 minutes after the 08:32 STATE note of that downgrade."

5. **QUEUE / ledger / `sg_rank.py` (needed before Q0 can be scored).**
   - Freeze one uniform-draw procedure in the script itself (recommended: `random.Random(20261115 + entry).choice(sorted(ids))`), log seed, item-set hash, and the draw; rewrite the two existing uniform fields to state which convention each actually used, rather than mixing them.
   - Store `index` (and unaided rank) in every `rule_rank` / `unaided_order` entry.
   - Write `unaided_order` in the same commit as, and with an earlier timestamp than, `rule_rank`. Entry 3 stays excluded.
   - Declare the AUC predictor (first-seen vs at-pick index), how unpicked items are handled, and that a pass tests this operational rule (including judgment \(w,v,L,c\)), not the bare SG clock, until enough items have non-flat \(P\).
   - Do not start the "\(\ge 15\) completed items" clock on the present entries 0–5.

6. **Optional, not required for consistency:** note in QUEUE that \(\gamma=0.4\) is a rounded, inconclusive, statement-time estimate; a sensitivity band on \(\gamma\) should be locked before scoring.

No locked prediction, formal proof, or night-1/night-2 numerical result needs to be changed. I am not editing THEORY.md, the audit, or the ledger in this PR; those fixes should be applied in a follow-up docs pass so they are not mixed with the referee record.

---

## 7. Limits of this review

- Prior-art claims for SG and for the formal "genuinely new" list were not independently re-searched.
- Night-1 simulations (POOLSIM, SENSING, ANTS1, LAYERS1) were not re-run; rows 5 and the in-model statuses were accepted from the claim map and write-ups after a targeted read.
- Chat history outside the parent conversation and the frozen STATE file was not available.
- fBm paths used 48 series of length \(2^{14}\). Path-wise \(\mathrm{Var}(B(t))\) is noisy at extreme \(H\); hold-MSE, which is the quantity that enters \(J\), is stable and matches discrete theory.
- This report is itself not a math-journal refereeing of every formal proof; Lemma 1(i) was re-derived, the rest of the formal layer was used as a cited source.

Checks: `reviews/night2/AUDIT_REFEREE_checks/`.
