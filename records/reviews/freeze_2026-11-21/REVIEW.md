# Independent hostile review: PR #137 (FREEZE_PROCESS)

**Reviewer:** independent (wrote none of PR #137, `theory/FREEZE_PROCESS_2026-11-21.md`, `theory/freeze_process_checks/freeze_process.py`, or `theory/freeze_process_checks/freeze_process.out`). Same bot family, not a blind second executor.
**Date:** Saturday 21 November 2026, 10:17 AM EST (America/New_York).
**Target:** https://github.com/Chad-Mitchell/theory-of-adaptive-organization/pull/137 (branch `freeze-process-2026-11-21`, head `8d15ada`, base `main` `cd84095`).
**Clone:** fresh `/workspace/rev137` (nothing merged; `/workspace/looper` and `/workspace/gtao-evo` untouched; compute at nice 19).

**Verdict: READY-WITH-FIXES**

The note honestly addresses whether freezing is a continuous limit of holding under the cost equation and checks every regime numerically in `theory/freeze_process_checks/freeze_process.py`. All static derivations (§§2, 3, 7) and the G2/G3 reading against `theory/GENERAL_THEOREM.md` §3 hold under independent symbolic re-derivation. All 13 DOIs listed in `References` resolve on Crossref and match the stored bibliographic records. Proton/crystal claims remain strictly `ANALOGY` (`E1`), `CORE.md` and `THEORY.md` are untouched, the hypothesis sentence is unchanged, `freeze_process.py` reproduces `freeze_process.out` byte-for-byte at nice 19, `tools/check_consistency.py` and `tools/check_open_work.py` pass, and `pytest tools/` passes (`147 passed`).

Three should-fixes (plus two wording nits) belong on this branch before merge. None invalidates the core conclusion that freezing is the continuous slow-world limit of holding when fixed machinery costs are absent, and a freeze-out crossover under cooling.

---

## 1. Independent mathematical re-derivation

All closed-form expressions were re-derived independently with `sympy` and cross-checked with independent Python scripts at nice 19:

1. **Static freeze edge (§2, $h_m = 0$).** Verified. With $J_{\text{int}}(q) = \sqrt{2cWq}$ and $J_F(q) = c/H + WqH/2$, $T^*(q) = \min(\sqrt{2c/(Wq)}, H)$ hits $H$ at $q_f = 2c/(WH^2)$. At $q_f$, $J^*(q_f) = 2c/H$ from both sides, both one-sided slopes equal $WH/2$ ($C^1$ kink), $d^2J^*/dq^2$ jumps from $0$ ($q < q_f$) to $-H^3W^2/(8c)$ ($q > q_f$), and excess effort $f - 1/H$ vanishes linearly with slope $HW/(4c) = 1/(2Hq_f)$. Contrast with Theorem 8 item 5's lookup cliff at $q_c = (\mu u - h)^2/(2cW)$ (effort jump $(\mu u - h)/(2c) \to 0$) is verified.
2. **Abrupt shutdown with machinery fixed cost $h_m > 0$ (§3.1).** Verified. Solving $\sqrt{2cWq} + h_m = c/H + WqH/2$ gives the physical interior-hold branch ($T^*(q^*) < H$):
   $$q^* = \frac{2(\sqrt{c/H} + \sqrt{h_m})^2}{WH}, \qquad T^*(q^*) = \frac{H\sqrt{c/H}}{\sqrt{c/H} + \sqrt{h_m}} < H.$$
   Upkeep jumps $h_m \to 0$, effort $1/T$ jumps down by $\sqrt{h_m/(cH)}$, and $J^*$ is continuous with slope jumping from $WT^*(q^*)/2$ (above $q^*$) to $WH/2$ (below $q^*$).
3. **Ruin-forced melt (§3.2).** Verified, with one nuance. Under $qT \le Q_\varepsilon$, freezing is feasible iff $q \le q_r = Q_\varepsilon/H$. When $h_m = 0$, $T^*(q) = \min(\sqrt{2c/(Wq)}, Q_\varepsilon/q, H)$ and $J^*(q)$ remain continuous at $q_r$. When $h_m > 0$ and $q_r < q^*$, $J_F(q) < J_{H,\text{uncapped}}(q) \le J_{H,\text{capped}}(q)$ for all $q \le q_r$, so freezing occurs as soon as feasible at $q_r$ and $J^*$ jumps at $q_r$. The note correctly qualifies that in S3 ($q_r = q_f/2 < q_f < q^*$) the jump equals $h_m$ because the capped held design sits at $T = H$ at $q_r^+$; for $q_f \le q_r < q^*$, $T_{\text{held}}(q_r^+) = \sqrt{2c/(Wq_r)} < H$, so both $J^*$ (by $J_H(q_r) - J_F(q_r) \in (0, h_m)$) and effort $1/T$ jump.
4. **G2/G3 reading vs `theory/GENERAL_THEOREM.md` §3.** Verified. In `theory/GENERAL_THEOREM.md` lines 182–199, G2's $\lambda_c = \Phi/c$ ($\Phi = \int_0^\infty (r_\infty - r(u))\,du$) is indeed the **high-drift fade edge** where tracking stops paying and the system acts blind; G3 gives $f^*(\lambda) \to 0$ continuously as $\sqrt{\lambda r'(0)/(2c)}$ as $\lambda \to 0$ when $r'(0) < \infty$ (in S4, $r(u) = 1 - e^{-2u}$ gives $\Phi = 1/2$, $\lambda_c = 0.5$). Cooling ($\lambda \to 0$) never crosses G2.
5. **DP freeze-out under $q(t) = q_0 e^{-t/\tau_c}$ (§4, S5) — FIX NEEDED (S1).**
   Differentiating $cN + W \sum_{k=0}^N \int_{t_k}^{t_{k+1}} (u(t) - u(t_k))\,dt$ (with $t_0 = 0, t_{N+1} = \text{Hor}$) with respect to $t_k$ yields the **exact Euler–Lagrange optimality condition**:
   $$u(t_k) - u(t_{k-1}) = q(t_k)(t_{k+1} - t_k) \quad (1 \le k \le N-1), \qquad u(t_N) - u(t_{N-1}) = q(t_N)(\text{Hor} - t_N).$$
   In the adiabatic regime ($t_{k+1} - t_k \ll \tau_c$), this reduces to $t_{k+1} - t_k \approx \sqrt{2c/(Wq(t_k))}$, and onset occurs near $q_{\text{fo}} = 2c/(W\tau_c^2)$. However, two claims in §4 lines 147–149 fail outside the five table runs:
   - **Empirical tail fit `0.6 c/(W τ_c Hor)` fails as $\text{Hor}$ grows.** From the exact last-read condition with $t_N - t_{N-1} \gg \tau_c$, $u(t_N) - u(t_{N-1}) \approx \tau_c q(t_{N-1})$, giving
     $$q(t_N) \approx \frac{\tau_c \, q(t_{N-1})}{\text{Hor} - t_N}.$$
     Independent DP runs at $\tau_c = 20, c = 0.005$ across $\text{Hor} \in [600, 10^6]$ show that total read count $N$ **saturates** at $N = 403$ for all $\text{Hor} \in [1500, 10^6]$, while the single last read $t_N$ drifts logarithmically rightward as $\tau_c \ln(\text{Hor}/\tau_c)$ ($301 \to 341 \to 378 \to 416 \to 454 \to 508$), causing $q(t_{N-1})$ to drift down slowly as $1/\ln(\text{Hor}/\tau_c)$ ($0.187 \to 0.019 \times q_{\text{fo}}$). Consequently $q_{\text{last}} \cdot \text{Hor}$ is **not** constant: `0.6 c/(W τ_c Hor)` already misses `Hor = 1500` by $2.6\times$, and at $\text{Hor} = 20{,}000$ and $10^6$ it misses by $7.9\times$ and $15.7\times$ respectively. What actually stays $O(c)$ as $\text{Hor} \to \infty$ is the tail error cost $W \tau_c q(t_N)(\text{Hor} - t_N) \approx W \tau_c^2 q(t_{N-1}) \lesssim c$, which is why no $(N+1)$-th read ever pays back $c$.
   - **"Exactly two more reads after onset" (line 147)** holds only in the five table runs; at $\text{Hor} = 5000$ and $20{,}000$ there are **3** reads after the first gap $> \tau_c$ (matching S5's own assertion `<= 3`, i.e. $O(1)$ additional reads).
6. **Design freeze-out ODE (§5, S6) — SHARPENS CLAIM 5.2 + CRITICAL BOUNDARY (S2).**
   Claim 5.1 ($\int_0^\infty dt/\tau_a < \infty$; power-law $q \propto (1+t)^{-p}$ converges iff $p\zeta > 1$) is verified. At the critical boundary $p\zeta = 1$, $S(t) \sim \ln t \to \infty$ (no frozen relic), yet the lag $x - x^*$ approaches the nonzero constant $p/\alpha$ rather than shrinking to zero. For exponential cooling $q(t) = q_0 e^{-t/\tau_c}$ with $x^*(t) = -t/(\alpha\tau_c) + x^*(0)$ and $\tau_a = \tau_1 e^{\zeta t/\tau_c}$, substituting $u = e^{-\zeta t/\tau_c}$ integrates the ODE exactly:
   $$x_\infty - x^*(0) = \frac{1}{\alpha\zeta}\int_0^1 S_\infty e^{-S_\infty u}\ln u\,du = -\frac{\ln(\tau_c/(\zeta\tau_1)) + \gamma_E}{\alpha\zeta} + O(e^{-\tau_c/(\zeta\tau_1)}),$$
   where $S_\infty = \tau_c/(\zeta\tau_1)$ and $\gamma_E \approx 0.577216$ is the Euler–Mascheroni constant. This proves Claim 5.2's scaling $f_\infty \propto \tau_c^{-1/(\alpha\zeta)}$ analytically (matching S6's numerical $-2.5912$ at $\zeta = 1, \tau_c = 100$ to 7 digits: $-(\ln 100 + \gamma_E)/2 = -2.591193$).
7. **Hysteresis (§6, S7) — FIX NEEDED ON REHEATING (S2).**
   - §6.1 (no static hysteresis even at $h_m > 0$), §6.2 (deterministic switching-cost band), and §6.4 non-monotone loop area are verified.
   - **§6.4 line 205 overstates reheating:** *"On reheating it re-melts only once $\tau_a(q)$ falls below the heating e-folding time, which is above the $q$ at which it froze."* Independent ODE integration ($\tau_c = 20, q_{\min} = 10^{-6}, \zeta = 1, \alpha = 2$, so $q_{\text{fo}} = 0.05$ and effective relic scale $q_{\text{eff}} = e^{\alpha x_\infty} = q_{\text{fo}} e^{-\gamma_E} = 0.0281$) shows:
     - Reheating resumes when $\tau_a(q) \sim \tau_h$, i.e. $q_{\text{melt}} \sim \tau_h^{-1/\zeta}$. That exceeds $q_{\text{fo}}$ only when reheating is faster than cooling ($\tau_h < \tau_c$), and exceeds $q_{\text{eff}}$ only when $\tau_h \lesssim \tau_c e^{\gamma_E}$.
     - For slow reheating ($\tau_h = 200$), $\tau_a(q) = \tau_h$ occurs at $q = 0.0050 \ll q_{\text{eff}} = 0.0281 < q_{\text{fo}} = 0.0500$. Moreover, while $q < q_{\text{eff}}$ (even at equal rate $\tau_h = \tau_c = 20$), $x^*(q) < x_{\text{relic}}$, so on unfreezing $x$ first **dips further below** $x_{\text{relic}}$ (to $-1.992$ at $q = 0.0187$ for $\tau_h = 20$; to $-2.579$ at $q = 0.0058$ for $\tau_h = 200$) before crossing back above $x_{\text{relic}}$ (at $q = 0.0584$ for $\tau_h = 20$, $q = 0.0337$ for $\tau_h = 200$).
8. **Temperature (§7, S8).** Verified: $T_f = E_a / (k\ln(\nu_0 W H^2 / (2c)))$, elasticity $1/\ln(\nu_0 W H^2 / (2c)) \approx 0.01\text{–}0.016$, $1000\times$ change in $c/W$ shifts $T_f$ by $-9.773\%$. Minor wording nit (line 215): $WH/(2c)$ is called "the price ratio" ($W/c$ is the price ratio; $WH/(2c)$ is the dimensionless lifetime-stake-to-two-reads ratio, with $W$ in cost/time for a dimensionless state).

---

## 2. Targeted prior-art search and novelty downgrades (S3)

The note left a targeted prior-art search for §4 as OPEN (§8 line 246, §9 item 3) and labelled §§2, 3.1, and 4 `UNCONFIRMED novelty`. A targeted search finds direct prior art for §4 and §6.4 (all DOIs verified on Crossref this review):

| Item | Prior art found & verified | Novelty change |
|---|---|---|
| **§4 cooling read schedule & finite-horizon freeze-out** | **Reliability checking schedules:** Barlow, Hunter & Proschan 1963 (*J. SIAM* 11:1078–1095, `10.1137/0111080`); Keller 1974 (*Manage. Sci.* 21:256–260, `10.1287/mnsc.21.3.256`, continuous square-root checking density $n(t) \propto \sqrt{h(t)}$ via calculus of variations); Viscolani 1991 (*RAIRO Oper. Res.* 25:203–208, `10.1051/ro/1991250202031`, finite-horizon checking schedules). **Remote estimation / AoI of Wiener processes:** Rabi, Moustakides & Baras 2012 (*SIAM J. Control Optim.* 50:672–702, `10.1137/090757125`, finite-horizon optimal sampling of Wiener/OU); Sun, Polyanskiy & Uysal 2020 (*IEEE Trans. Inf. Theory* 66:1118–1135, `10.1109/TIT.2019.2937336`, signal-independent AoI–MSE equivalence & Wiener sampling). **Time-varying-demand EOQ:** the objective $cN + W\sum \int_{t_k}^{t_{k+1}}(u(t)-u(t_k))dt$ is the time-reversed deterministic continuous-time replenishment problem with exponentially declining demand (Hollier & Mak 1983, *Int. J. Prod. Res.* 21:813–836, `10.1080/00207548308942414`). **Rational inattention:** Reis 2006 (`10.1016/j.jmoneco.2006.03.001`), Abel, Eberly & Panageas 2007 (`10.1257/aer.97.2.244`) & 2013 (`10.3982/ECTA7624`), Alvarez, Lippi & Paciello 2011 (`10.1093/qje/qjr043`). | Downgrade from `UNCONFIRMED novelty` to **KNOWN in substance (novelty 0–1)**: the square-root schedule, Euler–Lagrange recurrence, finite-horizon stopping, and freeze-out criterion are known. Narrow GTAO framing: expressing $q_{\text{fo}} = 2c/(W\tau_c^2)$ in $(c, W)$ and mapping $H \leftrightarrow \tau_c$ to CT11. |
| **§2 C¹ kink vs lookup cliff** | Elementary corollary of Theorem 8 (CT11) and Cho & Garcia-Molina 2003 (constrained interior-to-boundary minimum vs outside fallback). | Downgrade from `UNCONFIRMED novelty` to **0** (trivial corollary). |
| **§3.1 fixed machinery cost $h_m$** | Elementary fixed-cost non-convexity producing a discontinuous shutdown threshold. | Downgrade from `UNCONFIRMED novelty` to **0** (elementary algebra). |
| **§6.4 dynamic hysteresis peak** | Jung, Gray, Roy & Mandel 1990 (*Phys. Rev. Lett.* 65:1873–1876, `10.1103/PhysRevLett.65.1873`); Chakrabarti & Acharyya 1999 (*Rev. Mod. Phys.* 71:847–859, `10.1103/RevModPhys.71.847`). | Replace uncited parenthetical in §6.4 line 204 with verified citations. |

---

## 3. Crossref DOI check

All 13 DOIs cited in `theory/FREEZE_PROCESS_2026-11-21.md` and all 11 additional prior-art DOIs identified above were queried on the Crossref API (`api.crossref.org/works/<doi>`) on 21 Nov 2026 and resolved cleanly to the stated authors, years, journals, and pages:

- Existing 13: `10.1103/PhysRev.73.803` (Alpher, Bethe, Gamow 1948), `10.1038/nature05120` (Aoki et al. 2006), `10.1103/PhysRev.130.1677` (Brown 1963), `10.1016/0022-5193(66)90188-3` (Cohen 1966), `10.1086/261619` (Dixit 1989), `10.1007/BF00373790` (Dodson 1973), `10.1143/ptp/5.2.224` (Hayashi 1950), `10.1088/0305-4470/9/8/029` (Kibble 1976), `10.1126/science.220.4598.671` (Kirkpatrick, Gelatt, Vecchi 1983), `10.1016/S0031-8914(40)90098-2` (Kramers 1940), `10.1016/j.tree.2009.03.010` (Lahti et al. 2009), `10.1103/PhysRevLett.39.165` (Lee & Weinberg 1977), `10.1038/317505a0` (Zurek 1985).
- Additional 11: `10.1137/0111080` (Barlow, Hunter, Proschan 1963), `10.1287/mnsc.21.3.256` (Keller 1974), `10.1051/ro/1991250202031` (Viscolani 1991), `10.1137/090757125` (Rabi, Moustakides, Baras 2012), `10.1109/TIT.2019.2937336` (Sun, Polyanskiy, Uysal 2020), `10.1080/00207548308942414` (Hollier & Mak 1983), `10.1016/j.jmoneco.2006.03.001` (Reis 2006), `10.1257/aer.97.2.244` (Abel, Eberly, Panageas 2007), `10.3982/ECTA7624` (Abel, Eberly, Panageas 2013), `10.1093/qje/qjr043` (Alvarez, Lippi, Paciello 2011), `10.1103/PhysRevLett.65.1873` (Jung et al. 1990), `10.1103/RevModPhys.71.847` (Chakrabarti & Acharyya 1999). (12 additional DOIs total.)

---

## 4. Consistency, constraints, and checks

- `CORE.md` and `THEORY.md`: unchanged relative to `origin/main` (`cd84095`).
- Hypothesis sentence: verbatim unchanged (`CORE.md:24`, `THEORY.md:41`).
- Proton/crystal status: strictly `ANALOGY` (`FREEZE_PROCESS_2026-11-21.md` §§0, 8, citing `SCALE_ENDS.md` E1).
- `nice -n 19 python3 theory/freeze_process_checks/freeze_process.py`: all checks pass; output byte-identical to `freeze_process.out`.
- `python3 tools/check_consistency.py`: **PASS** (0 FAIL).
- `python3 tools/check_open_work.py`: **PASS** (0 missing).
- `python3 -m pytest tools/ -q`: **147 passed**.

---

## 5. Fixes to apply on this branch (separate commits, no merge)

- **S1 (§4 exact Euler–Lagrange & tail scaling + S5/S6 checks):** Add the exact Euler–Lagrange recurrence $u(t_k)-u(t_{k-1}) = q(t_k)(t_{k+1}-t_k)$ and tail relation $q(t_N) \approx \tau_c q(t_{N-1})/(\text{Hor}-t_N)$ to `theory/FREEZE_PROCESS_2026-11-21.md` §§0 & 4; remove the inaccurate `0.6 c/(W τ_c Hor)` scaling fit in favor of the true $\text{Hor} \to \infty$ asymptotics ($N$ saturates once $W\tau_c^2 q(t_{N-1}) \lesssim c$, $t_N \sim \tau_c \ln(\text{Hor}/\tau_c)$, $q_{\text{last}}\cdot\text{Hor} \propto 1/\ln(\text{Hor}/\tau_c)$); qualify "exactly 2 more reads" as $O(1)$ reads (2 in the five table runs, 3 at $\text{Hor}=5000, 20000$). Add Euler–Lagrange and $\gamma_E$-asymptotic checks to `freeze_process.py` and refresh `freeze_process.out`.
- **S2 (§5 exact relic & §6.4 reheating qualification + §7 nit):** Add the exact asymptotic closed-form $x_\infty - x^*(0) = -(\ln(\tau_c/(\zeta\tau_1)) + \gamma_E)/(\alpha\zeta)$ and the $p\zeta = 1$ boundary (no frozen relic, constant lag $p/\alpha$) in §5. Qualify §6.4 line 205 (re-melting near $\tau_a(q) \sim \tau_h$ is above $q_{\text{fo}}$ only for $\tau_h < \tau_c$, and slow reheating unfreezes below $q_{\text{eff}}$ and dips $x$ toward $x^*(q)$ before rising), cite Jung et al. 1990 and Chakrabarti & Acharyya 1999 in §6.4, and clarify $WH/(2c)$ vs price ratio $W/c$ in §7 line 215.
- **S3 (Prior-art credits and novelty downgrades):** Incorporate the targeted prior-art citations (Barlow et al. 1963, Keller 1974, Viscolani 1991, Rabi et al. 2012, Sun et al. 2020, Hollier & Mak 1983, Reis 2006, Abel et al. 2007/2013, Alvarez et al. 2011) into §§4, 8, and References; downgrade novelty in §§2, 3.1, 4, and 8 from `UNCONFIRMED novelty` to `KNOWN in substance (0–1)` / `0`; update §9 item 3 to note the targeted search was completed in review.

This review does not merge.
