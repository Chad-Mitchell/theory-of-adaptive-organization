"""DYNAMICS §5 checks: the two OVERREACH verdicts of the wide-net scan, recomputed independently.
(a) Bode: the steady-state Kalman filter's sensitivity S = 1 - H never exceeds 1 (return-difference inequality),
    so there is no waterbed in GTAO's pure-estimation class; the integral is the relative-degree-1 identity.
(b) Barbell: in CT22's continuous model (Lemma B9 setting) mixing two designs under an averaged ruin target gains
    nothing (the cost-vs-log-ruin frontier is convex); with discrete copies a mix gains, but only if the constraint
    binds ex ante (before the randomization), not on the realized design.
Run: nice -n 19 python3 d4_overreach.py -> d4_results.json, prints ALL D4 CHECKS PASS."""
import json, math, os
import numpy as np
from scipy.linalg import solve_continuous_are
from scipy.integrate import quad

HERE = os.path.dirname(os.path.abspath(__file__))
R, ok = {}, []

# ---- (a) random worlds: K OU modes, white sensing noise; Kalman-Bucy steady state
rng = np.random.default_rng(1985)
worst, ints = 0.0, []
for trial in range(40):
    K = rng.integers(1, 4); a = 10 ** rng.uniform(-2.5, 0.5, K); v = 10 ** rng.uniform(-1, 1, K); N = 10 ** rng.uniform(-3, 0)
    F = -np.diag(a); Q = np.diag(2 * a * v); C = np.ones((1, K))
    P = solve_continuous_are(F.T, C.T, Q, np.array([[N]])); L = P @ C.T / N; A = F - L @ C
    H = lambda om: (C @ np.linalg.solve(1j * om * np.eye(K) - A, L))[0, 0]
    om = np.logspace(-6, 4, 3000)
    S = np.array([abs(1 - H(o)) for o in om]); worst = max(worst, S.max())
    if trial < 6:
        I = quad(lambda o: math.log(abs(1 - H(o))), 0, np.inf, limit=800)[0]
        ints.append([I, -math.pi / 2 * (C @ L).item()])
R["D4a_max_abs_S_over_40_random_worlds"] = float(worst)
R["D4a_bode_integral_vs_identity"] = ints
ok.append(worst <= 1 + 1e-9)
ok.append(all(abs(i / p - 1) < 2e-3 for i, p in ints))

# ---- (b1) CT22 / Lemma B9 setting (as reproduced in the scan and in THEORY's check numbers)
y, c, w, s, s0, eps = 1.0, 0.05, 1.0, 1.0, 0.3, 1e-3
m = lambda t: y - c / t - w * s**2 * t / 2
th = lambda t: 2 * m(t) / (s0**2 + w**2 * s**4 * t**3 / 3)
Jt = lambda t: c / t + w * s**2 * t / 2
tE = math.sqrt(2 * c / (w * s**2)); ts = np.linspace(0.05, tE, 20001)
thv = np.array([th(t) for t in ts]); tS = ts[np.argmax(thv)]
R["D4b_Bmin_check_vs_THEORY_0.486"] = math.log(1 / eps) / thv.max()
ok.append(abs(R["D4b_Bmin_check_vs_THEORY_0.486"] - 0.486) < 2e-3)
# frontier between the survival-optimal tS and tE: J as a function of P = exp(-theta*B). Mixing two designs at
# average ruin eps beats the pure design iff J(P) is non-convex there. Check the lower convex hull vs the curve.
gains = []
for B in (0.49, 0.50, 0.505):
    seg = ts[ts >= tS]; Pv = np.exp(-np.array([th(t) for t in seg]) * B); Jv = np.array([Jt(t) for t in seg])
    order = np.argsort(Pv); Pv, Jv = Pv[order], Jv[order]
    # lower convex hull (monotone chain)
    hull = []
    for p_, j_ in zip(Pv, Jv):
        while len(hull) >= 2 and (hull[-1][1] - hull[-2][1]) * (p_ - hull[-2][0]) >= (j_ - hull[-2][1]) * (hull[-1][0] - hull[-2][0]):
            hull.pop()
        hull.append((p_, j_))
    hp = np.array(hull)
    if Pv[0] <= eps <= Pv[-1]:
        Jcurve = float(np.interp(eps, Pv, Jv)); Jhull = float(np.interp(eps, hp[:, 0], hp[:, 1]))
        gains.append([B, Jcurve, Jhull, (Jcurve - Jhull) / Jcurve])
R["D4b_mix_gain_continuous"] = gains
ok.append(all(g[3] < 1e-6 for g in gains))

# ---- (b2) discrete copies (R1-b setting of the scan): P(n) = 1-(1-p^n)^N
p, Nn, eps2 = 0.1, 1000, 5e-4
Pr = lambda n: 1 - (1 - p**n) ** Nn
nR = next(n for n in range(1, 50) if Pr(n) <= eps2)
lam = (Pr(nR - 1) - eps2) / (Pr(nR - 1) - Pr(nR))
R["D4b_discrete_nR_mix_mean_copies"] = [nR, lam, lam * nR + (1 - lam) * (nR - 1)]
R["D4b_realized_P_of_cheaper_arm_vs_eps"] = [Pr(nR - 1), eps2]
ok.append(nR == 7 and abs(lam * nR + (1 - lam) * (nR - 1) - 6.555) < 2e-3 and Pr(nR - 1) > eps2)
R["D4b_reading"] = ("the mix meets eps only averaged over the randomization (ex ante); a system that drew 6 copies "
                    "violates eps itself. It is LP/constrained-MDP randomization, not a safe-plus-speculative barbell.")
R["checks_passed"] = int(sum(ok)); R["checks_total"] = len(ok)
json.dump(R, open(os.path.join(HERE, "d4_results.json"), "w"), indent=1, default=str)
for kk, v in R.items(): print(kk, v)
print("ALL D4 CHECKS PASS" if all(ok) else "D4 FAIL: %s" % [i for i, x in enumerate(ok) if not x])
