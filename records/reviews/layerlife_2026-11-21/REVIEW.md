# Independent hostile review of draft PR #141

Read-only review of commit `3b94aef` on `layer-lifetime-2026-11-21`, stacked on PR #139 (`7d8690ce`). Saturday 21 November 2026. Computations at nice 19. Every DOI in `theory/layerlife_checks/dois.txt` was resolved on the Crossref API on 21 Nov 2026; all 12 match the note. The hypothesis sentence is unchanged. `CORE.md`, `THEORY.md`, and `OPEN_WORK.md` are not in the diff. The reviewer wrote none of the draft, made no commit, and did not merge.

**READY-WITH-FIXES.** No blocker. The spacing ratio and the shared-only delay crossing are right in the model the proof names. The draft is not ready to lock: the headline is wider than that proof, `DIR1` is not in the repository, and Karim/Girod do not identify P2 or P3.

Commit `3b94aef` on `layer-lifetime-2026-11-21`, parent `7d8690ce` (`shannon-core-2026-11-21`, PR #139). Seven files, +805. `CORE.md`, `THEORY.md`, and `OPEN_WORK.md` are untouched. The hypothesis sentence matches `CORE.md`. No commit was made.

## (1) Spacing ratio and the D5 crossing

The ratio is exact in Model LS at zero discounting. Independent components, equal stake \(w\), and loss \(w(\sum e_i)^2\) give \(E[(\sum e_i)^2]=\sum E[e_i^2]\). Each layer is its own renewal problem: exit time \(b^2/\sigma^2\), accumulated square \(b^4/(6\sigma^2)\), so \(E[x^2]=b^2/6\), \(b^*=(6k\sigma^2/w)^{1/4}\), \(T^*=\sqrt{6k/(w\sigma^2)}\), cost \(2\sqrt{kw\sigma^2/6}\). The ratio follows at once. The script’s spacing check is that identity evaluated on three numbers. The “stack cost is the sum” check compares a sum with itself.

A common discount rate moves the ratio only slightly at the point I solved (equal \(k,w\), variance rates 1 and 4): +0.06% at \(r=0.05\), +1.2% at \(r=1\). “Exact” means the undiscounted case already named in §2.

The fixed-period latency floor is the right object for the policy §5 proves. With observation delay \(\ell\) and a frozen estimate, average mean square is \(\sigma^2\ell+\sigma^2 T/2\), and the optimum separates into \(\sqrt{2k_S(Nw)\sigma^2}+Nw\sigma^2\ell\). The displayed

\[\sigma^{2*}=\left(\frac{\sqrt{2k_L w}-\sqrt{2k_S w/N}}{w\ell}\right)^2\]

matches an independent evaluation at the check prices: \(0.0216142297492\). One crossing, shared cheaper below it, local above it, and no dependence on \(\sigma^2\) at \(\ell=0\), provided \(k_S<Nk_L\).

The optimal barrier under the same observation delay does not flip the sign. The delayed gap is still a Brownian motion, the floor \(Nw\sigma^2\ell\) does not depend on the barrier, and the excess cost is the Dixit cost \(2\sqrt{kw\sigma^2/6}\) instead of \(\sqrt{2kw\sigma^2}\). The crossing is the displayed value divided by 3 (\(0.00720474\)). An action delay that zeros the gap only when the reset arrives, with one order in flight, also keeps a single crossing (shared-only delay, \(\sigma^{2}\approx 0.02494\)).

The sign dies if the same delay sits on local updates. Observation-delay floors cancel and the gap is the \(\sqrt{k}\) gap at every \(\sigma^2\). Action delay with the same \(\ell\) on both sides had no sign change from \(\sigma^2=10^{-4}\) to \(10^{2}\); shared stayed cheaper. “Without latency there is no switch” is true and incomplete. Shared-only latency is the load-bearing premise.

## (2) Layer-count converse

No \(T^*\)-converse was recoverable. One perfect observation of the sum starts the residual at 0, so a short enough hold meets any \(D>0\) with one layer. A second full reset of the same Brownian motion is never used if a cheaper full reset exists. For increment variance \(\propto\tau^{2H}\), one fixed-period balance gives one \(T^*\propto(k/(wC))^{1/(2H+1)}\). The only count lower bound in the note, \(K\ge\#\{i:v_i>D\}\), is a covering bound on a specialized partition and does not use \(T^*\) or the prices. The real layer-count converse already in the repository is CT21 (L3): a non-rational spectrum has no finite exact store set. That is Model S’s \(E_K\). The rerun still gives Dixit lifetime ratio 10 against store-time-constant ratio 47.14 on the two-mode world. The kill stands.

## (3) Prior art and the repository

All 12 DOIs in `dois.txt` resolved on the Crossref API on 21 Nov 2026. Titles, authors, volumes, and start pages match the note. Girod & Whittington: issued 2016-07-11, published-print 2017-05, *Strategic Management Journal* 38(5):1121–1133. The note’s year caveat is right.

Renewal derivation reproduces \(b^*\), \(T^*\), and \(2\sqrt{kw\sigma^2/6}\). Chalkley’s introduction says Dixit’s quadratic approximation (1991, *Review of Economic Studies*) is exact at zero discounting. I did not read Dixit’s printed equation. Alvarez, Lippi & Paciello (NBER w15852) write the same fourth root and call it Dixit’s.

Barro 1972, as cited by those authors and by a secondary account of his random-walk band, is a fourth-root inaction band. The square-root lifetime is the mean exit time of that band. A deterministic inflation menu cost is a cube-root interval. The note’s “square-root refresh” line is the random-walk corollary, which is how `TESTBEDS.md` already uses him.

Roundy 1985 is the 98% integer-ratio paper (*Management Science* 31:1416–1430). The note correctly treats that as a schedule constraint, not this ratio. Willsky 2002 is multiresolution Markov models; the note does not give him \(T^*\). Simon 1962 is *Proceedings of the American Philosophical Society* 106(6):467–482 (12 Dec 1962; no DOI). Near-decomposability there does separate fast within-component dynamics from slow between-component dynamics. The pointer “THEORY §8” is wrong: §8 is “Predictions, and how it dies.” The credit is in §10. Sims 2003 does not give this \(T^*\). Its abstract says a finite Shannon capacity can resemble a signal-extraction problem or an adjustment cost, so “closer to a Kalman filter than to lumpy re-formation” is narrower than the abstract.

`CT35` is the wrong theorem. The factor \(X_S=\nu\cdot\pi\cdot e^{-2\ell/\tau}X_L\) is the OU closed form in THEORY B.11, and `figures/face_placements.md` attributes the fast/slow slogan to CT28 and CT34. `reviews/core_2026-11-20/REVIEW.md` already flagged this mis-citation. There is no file, theorem, or ledger entry named `DIR1`, and no \(n=2\) tally for this sign. LAYERS1 P2 is G20, span invariance of store spacing, SIM-FAIL. Geometric clocks are still CL12 in the shared-clock model. The holographic fail in `core/KEYSTONE_NOTE.md` §5 is real (3/24 primary cells; equal-value CVs failed).

## (4) Mid-scale OU, and whether the prices are special

The quoted errors reproduce: \(T_{\mathrm{bm}}/\tau=0.004472\), relative error \(0.299\%\); and \(0.632\), relative error \(137\%\) (\(T_{\mathrm{opt}}/T_{\mathrm{bm}}-1=1.367\)). Both are fixed-period, as the note says. At the bad point, tracking still pays: \(J=0.9499<w v=1\). Fixed-period OU tracking loses to staying blind only for \(k>wv/(2a)\). Here that threshold is \(2.5\); the check uses \(k=2\). The check named “need not pay” is hard-coded `True` on a case that pays. Loss appears at \(k=3\).

At \(\tau=0.05\), \(\ell=0.5\), shared’s optimum is exactly the blind cost \(Nw v=10\), and local’s cost is \(9.499\). At \(\tau=20\) and \(\tau=200\) both sides are interior. The OU crossing at these prices is \(183\ell\) (Brownian prediction \(185\ell\)). The points \(40\ell\) and \(400\ell\) sit on either side of it. They are not the threshold.

The prices are an interior point, \(k_S/(Nk_L)=0.4\) and \(k_L/(wv\ell)=0.04\), not a one-point trick. The multiples are not invariant. Holding the other check prices fixed, the crossing \(\tau/\ell\) is about 40 at amortization ratio 0.05, 80 at 0.2, 183 at 0.4, 930 at 0.7, and 9500 at 0.9. Scaling both lumps by 10 moves it to about \(16\ell\). Scaling them by 100 makes the fast end a tie: both stay blind, so “local wins when the world is fast” fails. “\(\tau>\ell\) is not sufficient” survives that neighborhood. “40 and 400” do not.

## (5) Karim 2016 and Girod & Whittington 2017

P2 and P3 are not identifiable in either series. Mapping “turbulence” or “dynamism” to \(\sigma^2\) is a rescue lever, and it would still not be enough.

Karim, Carroll & Long 2016 (*Academy of Management Journal* 59:791–817) studied 46 U.S. medical-device and pharmaceutical firms, 1978–1997. The abstract’s result is the one the note quotes: less business-unit recombination during industry dynamism, and also when top-management-team size grows. The paper’s own reading is decision avoidance and delay until dynamism falls and growth returns. There is no local margin, no latency, and no variance rate of the structure being tracked. The negative coefficient is the opposite of the menu-cost frequency prediction (higher \(\sigma^2\), shorter \(T^*\), more resets). It is not, by itself, the opposite of fast-local / slow-shared, because that sign also says to use the shared instrument less when drift is fast.

Girod & Whittington regress Tobin’s Q and ROA on restructuring and reconfiguration. Dynamism is Dess & Beard: the standard error of the rate of change of annual industry sales in the primary industry. Restructuring is a binary structural-change ratio above 0.30 from senior-title changes. Reconfiguration is an annual count of unit additions, mergers, transfers, splits, and deletions. In the 1985 Fortune 50 industrials followed to 2004 they record 136 restructurings and 3,770 reconfigurations (about four reconfigurations a year, restructuring mean 0.147). The hypotheses are performance interactions. That is a fitness ordering. The two counts could become a frequency comparison only after an independent \(k\) and a real \(\sigma^2\). They are incremental versus pervasive change, not \(N\) local trackers versus one shared tracker, and they contain no \(\ell\).

## Should-fixes

**`theory/LAYER_LIFETIME_2026-11-21.md:16`.** Replace the whole item 2 with:

```markdown
2. **Local vs shared (PROVED for a Brownian common driver, fixed-period refreshes, latency on the shared observation only; NUMERICAL for OU).** The same cost, with delay \(\ell>0\) on the shared observation and none on the local ones, gives the fast-local / slow-shared sign. The fixed-period crossing is the \(\sigma^{2*}\) in §5. The optimal barrier under the same observation delay keeps the sign and divides that crossing by 3. An equal delay on local updates cancels the floor, and there is again no switch. "Slower than the latency" is not enough: at the prices in the checks the OU crossing is about \(183\ell\), so shared still lost at \(\tau=40\ell\) and won at \(\tau=400\ell\).
```

**`theory/LAYER_LIFETIME_2026-11-21.md:80`.** Replace the DIR1 / CT35 sentence with:

```markdown
The fast-local / slow-shared sign is already in the repository: at equal read quality, \(X_S=\nu\cdot\pi\cdot e^{-2\ell/\tau}X_L\) (THEORY B.11, OU closed forms; `figures/face_placements.md`, nesting CT28 and CT34). CT35 is the subadditivity map theorem, not this factor. No document named DIR1, and no unscored \(n=2\) tally for this sign, is in the repository.
```

**`theory/LAYER_LIFETIME_2026-11-21.md:88`.** After “no switch when \(\ell=0\).” add:

```markdown
This \(\sigma^{2*}\) is the fixed-period, shared-only-delay object. For the optimal barrier on the delayed gap the floor \(Nw\sigma^2\ell\) is unchanged, the excess cost is \(2\sqrt{kw\sigma^2/6}\) rather than \(\sqrt{2kw\sigma^2}\), the sign is unchanged, and the crossing is this value divided by 3. If local updates carry the same delay, the floor is on both sides and the difference does not depend on \(\sigma^2\).
```

**`theory/LAYER_LIFETIME_2026-11-21.md:90`.** Replace the OU paragraph with:

```markdown
**OU companion (NUMERICAL).** The same prices and \(\ell=0.5\): local won at \(\tau=0.05\) (shared's optimum was the blind cost \(Nw v\)); shared still lost at \(\tau=20=40\ell\); shared won at \(\tau=200=400\ell\). The crossing at these prices is about \(183\ell\), against the Brownian fixed-period prediction \(2v/(\sigma^{2*}\ell)\approx 185\). Those multiples move with \(k_S/(N k_L)\) and with \(k/(wv\ell)\). The sign agrees with the OU factor in B.11. The naive rule "share once \(\tau>\ell\)" is **FALSE** at these prices.
```

**`theory/LAYER_LIFETIME_2026-11-21.md:92`.** Replace the rivals paragraph with:

```markdown
**Rivals.** Threat-rigidity (Staw, Sandelands & Dutton 1981) predicts restriction of information processing and constriction of control under threat, defined there as impending harm, with influence concentrated at higher levels. That paper does not state a sign in \(\sigma^2\). A no-response rival predicts no switch.
```

**`theory/LAYER_LIFETIME_2026-11-21.md:74`.** Replace the “Already in the repository” bullet with:

```markdown
- **Already in the repository.** Span invariance of store spacing failed in-model (LAYERS1 P2, CLAIM_MAP G20, SIM-FAIL). Geometric clocks remain proved in the shared-clock model (CL12); they were not withdrawn. A holographic count (layers growing with the log of the scale range, at roughly equal value each) failed in-model (`core/KEYSTONE_NOTE.md` §5). Those were Model S tests, not Model LS, but they are a warning against treating "fractal time \(\Rightarrow\) a stack with geometric lifetimes" as a theorem.
```

**`theory/LAYER_LIFETIME_2026-11-21.md:104`.** Replace the Simon cell’s credit with:

```markdown
Simon 1962 (no DOI; *Proc. Am. Philos. Soc.* 106:467–482; credited in THEORY §10); Simon & Ando 1961
```

**`theory/LAYER_LIFETIME_2026-11-21.md:106`.** Replace the Sims credit with:

```markdown
Sims 2003 (rational inattention). That paper does not give \(T^*=\sqrt{6k/(w\sigma^2)}\). Its abstract says a finite Shannon capacity can resemble a signal-extraction problem or an adjustment cost. It is not the Dixit band.
```

**`theory/LAYER_LIFETIME_2026-11-21.md:114`.** Replace the Karim and Girod sentences with:

```markdown
Karim, Carroll & Long 2016 report that 46 U.S. medical-device and pharmaceutical firms reduced business-unit recombination during industry dynamism, and also when top-management-team size grew. The paper reads that as decision avoidance and delay. The negative coefficient is the opposite of the menu-cost frequency prediction. It is not a local-versus-shared contrast: there is no local margin, no latency, and no variance rate of the structure being tracked. Girod & Whittington (Crossref issued 2016-07-11, print 2017) regress Tobin's Q and ROA on restructuring and reconfiguration, with Dess–Beard dynamism, the standard error of industry-sales growth, as a moderator. That is a fitness ordering. Their counts (about four reconfigurations a year, restructurings about every six years, 1985 Fortune 50 industrials through 2004) are not a regression of frequency on \(\sigma^2\).
```

**`theory/LAYER_LIFETIME_2026-11-21.md:122`.** Replace the sentence that begins “usable for P3” with:

```markdown
not identifiable as P2 or P3. A locked map from industry-sales dynamism onto \(\sigma^2\) would be a rescue lever. The series contain neither the variance rate of the tracked gap, nor a re-forming cost \(k\), nor a shared-update latency \(\ell\). Girod's two counts could support a frequency comparison only after those prices are measured independently. They do not identify P3. Performance stays out of the score.
```

**`theory/layerlife_checks/layerlife_checks.py:282`.** The blind check passes on a case that pays. Replace that `chk` with a case \(k=3\), \(a=0.2\), \(v=w=1\), where \(k>wv/(2a)=2.5\), and assert that the minimized fixed-period cost is not below \(wv\).

**`theory/layerlife_checks/layerlife_checks.py:196`, `:240`, `:305`, `:321`, `:351`, `:417`, `:510`.** Eight of the 33 checks cannot fail: a sum compared with itself, \(T_{\mathrm{red}}\) compared with the expression that defines it, `must == np.sum(v > D)`, three `chk(..., True)`, and `k_S < N*k_L` on the numbers just chosen. Drop them from the pass count, or replace them with a computation, and change `theory/LAYER_LIFETIME_2026-11-21.md:128` to the new count. The K=1 claim can be a one-line hold: mean square of a Brownian sum over a short \(T\) is \((\sum\sigma_i^2)T/2\), which is below any \(D>0\) for small enough \(T\).

## Nits

- The docstring says the script writes `layerlife_checks.out`. It writes only the JSON. The committed `.out` matches stdout; a rerun will not refresh it.
- The OU tags say `T_bm >> tau` at \(T_{\mathrm{bm}}/\tau=0.63\).
- The two-layer counterexample is \(J(k_{\mathrm{cheap}})<J(k_{\mathrm{cheap}})+J(k_{\mathrm{dear}})\). The domination argument is that the dearer full reset is never used.
- The fractional-Brownian balance is written \(k/T+wCT^{2H}\). Mean square over the hold is \(CT^{2H}/(2H+1)\). The exponent \(1/(2H+1)\) is unchanged.
- Dixit 1989 is in the reference line and not used in the body.
- The PR text says pytest 149 passed. Here, without `lake`, the suite is 148 passed and 1 skipped (`tools/test_lean.py:101`).

## Checks

All at nice 19, after installing SciPy 1.18.1, NumPy 2.5.5, pytest 9.2.0, and SymPy 1.14 into the user site. The tree was left clean.

| Command | Result |
|---|---|
| `python3 theory/layerlife_checks/layerlife_checks.py` | ALL PASS, 33/33. Stdout matches the committed `.out` |
| `python3 tools/check_consistency.py` | RESULT: PASS (0 FAIL, 23 INFO) |
| `python3 tools/check_open_work.py` | RESULT: PASS |
| `python3 -m pytest -q tools` | 148 passed, 1 skipped, 127 s |

Independent recomputation reproduced \(\sigma^{2*}=0.021614229749\), the OU costs 9.499, 0.62575 vs 0.87515, and 0.19933 vs 0.17578, the 0.3% and 137% timing errors, and the blind corner at \(\tau=0.05\).


## What was re-derived

Spacing holds under the Model LS premises. The fixed-period shared-only formula is correct, and the check's \(\sigma^{2*}=0.021614229749\) matches. Barrier observation-delay keeps the sign and divides the crossing by 3. One-order action delay keeps one crossing near \(0.0249\). Symmetric delay removes the crossing in both classes. The OU sample points reproduce, including shared blind at \(\tau=0.05\) (\(J_S=10\)) and the interior comparison at \(40\ell\) and \(400\ell\). No layer-count converse falls out of \(T^*\).
