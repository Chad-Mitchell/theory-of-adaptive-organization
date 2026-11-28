# Gate read: `theory/bicausal-a-2026-11-27/PREREG.md`

*Friday 27 November 2026 (America/New_York). Reads the `Gate` section of `PREREG.md` (lock commit `eb0540e308e65eab06ca86c6e3d9d9d2e9a350ce`, sha256 `b69b92a13a68f04ea9120f13ba65ea8a55aaa5a09ec8ad9b6c67f5a6dc26bf29`) and the formulas it cites, per `process/PREREG_GATE.md` section 2. **Limit, stated up front:** this is a separate pass by the same agent that wrote the prereg, made after the lock and before any scored run. It is not an independent reader. It checks order and the five fields; it does not make the gate independent.*

| ID | G1 | G2 | G3 | G4 | G5 | Pass or stop |
|---|---|---|---|---|---|---|
| BA-C1 | — | Fails, as labeled: the values follow from `theory/two-route-2026-11-25/RESULTS.md:38` and the W2 identities (\(\Sigma_{xx}=D/a\), \(\dot Q_X=0\) at \(m\equiv0\)); checked: \(21/14.0087-1=0.4991\), \(22/16.1186-1=0.3649\) | — | — | — | Logged only, not run |
| BA-C2 | — | Fails, as labeled: Horowitz 2015 additivity of flows plus AT-learn give \(P_1\ge J_{\mathrm{dir}}\) | — | — | — | Code gate only |
| BA-T1 | Named: `potential` at any \(w_x\); odds 0.15, not about 0 | Passes: no file on `main` computes the cross-partials; `PREREG_4.md:16` asserts non-potential without a proof | Passes: the one-object reading predicts `potential`; the outcomes are exclusive and exact | (b) `CORE.md:127`, ledger row BICAUSAL | Different after a hit (counterexample, move to CA5) and a miss (write \(\Psi\)) | **Pass** |
| BA-T2 | Named: \(\hat K^*\notin[12,48]\) at any \(w\); odds 0.60 | Passes: exact optimum has no closed form; the PAPER estimate uses an approximate member heat | Passes: free-link reading \(\hat K^*=2\), copy-costs-a-read null none up to 128; both outside the band by more than one grid step | (b) `CORE.md:43`, `:155` | Different after a hit (state in the CORE §1 table after review, second class) and a miss (exact member infimum, or the null stands) | **Pass** |

**Outcome: PASS, 0 blocking.**

**Non-blocking notes.**

1. BA-T2 is one-sided by design: a confirmed design proves pooling pays at that \(K\), but a \(K\) with no design found is not a proof that none exists. A `miss high` or `none` outcome is therefore weaker evidence than a hit or a `miss low`, because an optimizer that misses good designs pushes \(\hat K^*\) up. The half-tolerance rerun with twice the polished starts is the only check on that. The results should say so if the outcome is high or none.
2. Class LINK lets each memory's mobility vary at fixed temperature (the convention of `theory/INFO_PHYSICS_ATTAINABILITY.md` §4). With a fixed mobility the level could not be made smooth, and the threshold could be different or absent. The result is scoped to the stated class and should not be read beyond it.
3. BA-T1's witness is one exact point with \(\Delta\neq0\). That rules out a weighted potential on the whole domain. It does not rule out a potential on a sub-domain, which `CORE.md:127` does not ask for. The results should say this.
4. "All costs in class LINK are heats" is true by construction (prereg §4). Only the threshold value carries information; a headline that says "the link price is derived" without that scope would run past it.
5. The prereg's §0 records that Route A as locked did not address \(L\) or \(A\), and that A-T3 was retired on 25 November. A brief that cited A-T1 and A-T3 as the step that turns \(L\) and \(A\) into heat was working from a summary of the record, not the record.
