diff --git a/theory/STORE_NOISE.md b/theory/STORE_NOISE.md
index f27f611..7d0239e 100644
--- a/theory/STORE_NOISE.md
+++ b/theory/STORE_NOISE.md
@@ -53,17 +53,17 @@ J(x) = const − W·x^a/(1+x)² + H/x, W = wσ⁴/(V0 (λτ0)^a), H = h1·λ. Th
 so any h1 > 0 puts the memory beyond E1-a's value (x\* > (1−s)/s). For s < 1/2 any price gives a finite memory; for
 s = 1/2 the right side tends to 1, and at H/W ≥ 1 the best design is not to track (K\* = 0) (checks §4).
 
 **What E. coli implies (post hoc, not a test).** With the measured s = 0.31 [0.24, 0.37] (F2, `theory/measured/ecoli/f2/`),
 E1-a gives 1.9–3.6 s against the measured 9.9 s: the store's own noise closes about 37% of the log gap between Model S's
 1.1 s and 9.9 s. Explaining the rest by E2 alone needs H/W ≈ 0.67–0.74 (speed price comparable to the whole value of
 tracking at that gradient). E1-a alone would need s ≈ 0.10. Neither number is measured; both are stated so they can be.
 
-## 4. What changes in the Master Theorem (proposed; THEORY.md is not edited by this note)
+## 4. What changes in the Master Theorem (proposed; THEORY v2.5.4 takes up only the interlacing premise below, in §1, §6, (iii) and Appendix C; the copy-count reading of (iii) and many-mode interlacing under store noise are not yet taken up)
 - **Scope.** 𝓜_LG's premises "exogenous noise" and "fixed upkeep per layer" are now named as premises, not defaults.
 - **(iii) interlacing.** "At the full optimum every layer is faster than its mode" holds in 𝓜_LG. In Model S+ it holds
   for a one-store layer iff s ≥ 1/2 at h1 = 0 (E1-a); with s < 1/2 or h1 > 0 the optimal store is **slower** than its mode.
   Interlacing is a property of exogenous noise and speed-free upkeep, not of layering. (E. coli: λτ2 = 8.5.)
 - **(iii) count.** "One real mode ⇒ K\* ∈ {0, 1}" must read "one distinct time constant": with independent store noise,
   copies of the one layer pay at high enough stakes (E1-c). That the distinct-time-constant count stays capped by the
   world's degree under store noise is **checked numerically for one mode only, not proved**; for many modes it is open.
 - **(ii) comparative statics.** Unchanged in form (CT33 needs no model class): judgment spend, now including copies and
