"""DYNAMICS §5 (a'), added after independent review of PR #117 (blocker B2): the Bode verdict for periodic or
sampled reads. For the steady-state discrete-time Kalman one-step predictor, x_{k+1} = A x_k + w_k, y_k = C x_k + v_k,
xhat_{k+1} = A xhat_k + K e_k, e_k = y_k - C xhat_k, the observation-to-innovation map is
    S(z) = [1 + C (zI - A)^{-1} K]^{-1},   det-form: S(z) = det(zI - A) / det(zI - A + K C)   (scalar output).
With A Schur-stable (a stationary world) and A - KC Schur-stable (steady-state predictor), and S(inf) = 1,
Jensen's formula gives (1/2pi) * integral_{-pi}^{pi} ln|S(e^{iw})| dw = 0 exactly (a waterbed identity; discrete Bode,
Sung & Hara 1988). S is not identically 1, so |S| > 1 on a band. Also |S|^2 = (C P C' + R) / Phi_y(w): |S| > 1 exactly
where the observed spectrum falls below the one-step prediction-error variance. In continuous time (d4a) |S|^2 = N/Phi_y <= 1.
Checks: (1) the reviewer's four scalar AR(1) worlds (max|S| 1.045-1.436); (2) 40 random worlds with 1-3 AR(1) modes.
Run: nice -n 19 python3 d5_bode_discrete.py -> d5_results.json, prints ALL D5 CHECKS PASS."""
import json, os
import numpy as np
from scipy.linalg import solve_discrete_are

HERE = os.path.dirname(os.path.abspath(__file__))
R, ok = {}, []
om = np.linspace(-np.pi, np.pi, 8001)


def predictor_S(A, C, Q, Rn):
    P = solve_discrete_are(A.T, C.T, Q, Rn)
    Sinn = (C @ P @ C.T + Rn)[0, 0]
    K = A @ P @ C.T / Sinn
    n = A.shape[0]; I = np.eye(n)
    S = np.array([1.0 / (1.0 + (C @ np.linalg.solve(np.exp(1j * w) * I - A, K))[0, 0]) for w in om])
    Phi = np.array([((C @ np.linalg.solve(np.exp(1j * w) * I - A, np.eye(n))) @ Q
                     @ (C @ np.linalg.solve(np.exp(1j * w) * I - A, np.eye(n))).conj().T)[0, 0].real + Rn[0, 0] for w in om])
    stable = max(abs(np.linalg.eigvals(A - K @ C))) < 1
    return np.abs(S), Phi, Sinn, stable


def summarize(S, Phi, Sinn):
    mean_ln = float(np.trapezoid(np.log(S), om) / (2 * np.pi))
    ident = float(np.max(np.abs(S ** 2 - Sinn / Phi)))
    return float(S.max()), float(abs(om[S.argmax()])), mean_ln, ident


# (1) the reviewer's scalar AR(1) worlds (a, q, r)
scal = []
for a, q, r in [(0.95, 0.1, 1.0), (0.5, 1, 0.1), (0.99, 0.01, 1), (0.9, 1, 1)]:
    S, Phi, Sinn, st = predictor_S(np.array([[a]]), np.array([[1.0]]), np.array([[q]]), np.array([[r]]))
    mx, at, ml, idn = summarize(S, Phi, Sinn); scal.append([a, q, r, mx, at, ml, idn]); ok.append(st)
R["D5a_scalar_AR1_a_q_r_maxS_at_meanlnS_identityerr"] = scal
ok.append(all(1.04 < s[3] < 1.44 for s in scal))
ok.append(all(abs(s[5]) < 1e-6 and s[6] < 1e-8 for s in scal))

# (2) random worlds: K independent AR(1) modes summed, read with white noise each period
rng = np.random.default_rng(1988)
rows = []
for trial in range(40):
    Km = int(rng.integers(1, 4)); a = 1 - 10 ** rng.uniform(-2.5, -0.05, Km); v = 10 ** rng.uniform(-1, 1, Km)
    A = np.diag(a); Q = np.diag(v * (1 - a ** 2)); C = np.ones((1, Km)); Rn = np.array([[10 ** rng.uniform(-2, 0.5)]])
    S, Phi, Sinn, st = predictor_S(A, C, Q, Rn)
    mx, at, ml, idn = summarize(S, Phi, Sinn); rows.append([Km, mx, ml, idn, at]); ok.append(st)
R["D5b_random_worlds_maxS_min_max"] = [min(r[1] for r in rows), max(r[1] for r in rows)]
R["D5b_random_worlds_max_abs_mean_lnS"] = max(abs(r[2]) for r in rows)
R["D5b_random_worlds_max_identity_err"] = max(r[3] for r in rows)
R["D5b_random_worlds_argmax_freq_min"] = min(r[4] for r in rows)
ok.append(all(r[1] > 1 for r in rows))
ok.append(all(abs(r[4] - np.pi) < 1e-9 for r in rows))
ok.append(R["D5b_random_worlds_max_abs_mean_lnS"] < 1e-6 and R["D5b_random_worlds_max_identity_err"] < 1e-6)
R["D5_reading"] = ("continuous observation (Kalman-Bucy, d4a): |S| <= 1, no waterbed. Periodic or sampled reads: the "
                   "predictor obeys integral ln|S| = 0 and |S| > 1 on a high-frequency band in every world checked (maximum at Nyquist in all 44). Whether that "
                   "changes argmin J is OPEN: S maps observations to innovations and is not a cost J pays.")
R["checks_passed"] = int(sum(ok)); R["checks_total"] = len(ok)
json.dump(R, open(os.path.join(HERE, "d5_results.json"), "w"), indent=1)
for kk, vv in R.items(): print(kk, vv)
print("ALL D5 CHECKS PASS" if all(ok) else "D5 FAIL: %s" % [i for i, x in enumerate(ok) if not x])
