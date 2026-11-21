"""Checks for theory/SHANNON_2026-11-21.md (converse, achievability, frontier, efficiency).

Scalar Gauss-Markov world x_{t+1} = a x_t + n_t, Var(n) = Q, stationary Var V = Q/(1-a^2).
Reads y_t = x_t + v_t, Var(v) = s2 (the design chooses s2). Action at lead k: predict x_{t+k}.
All information in nats per step. Run: python3 theory/shannon_checks/shannon_checks.py
"""
import math
import numpy as np

FAILS = []
def chk(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (f"  [{detail}]" if detail else ""))
    if not ok:
        FAILS.append(name)

def world(a, Q):
    return Q / (1 - a * a)

def kalman_steady(a, Q, s2):
    """Steady-state filter error P (posterior) and gain K for y = x + v."""
    Pp = Q  # prior
    for _ in range(20000):
        P = Pp * s2 / (Pp + s2)
        Pp_new = a * a * P + Q
        if abs(Pp_new - Pp) < 1e-15 * max(1, Pp):
            Pp = Pp_new
            break
        Pp = Pp_new
    P = Pp * s2 / (Pp + s2)
    K = Pp / (Pp + s2)
    return P, K, Pp

def lead_loss(a, Q, P, k):
    V = world(a, Q)
    return a ** (2 * k) * P + V * (1 - a ** (2 * k))

# Lower-bound resource functions of the filter error P = mmse(x_t | M_t)
def I_min(a, Q, P):          # nats held about the past: I(M;X^t) >= I(M;x_t) >= 1/2 ln(V/P)
    return max(0.0, 0.5 * math.log(world(a, Q) / P))

def R_seq(a, Q, P):          # sequential RD of scalar Gauss-Markov (Tatikonda; Tanaka et al. 2017)
    return max(0.0, 0.5 * math.log(a * a + Q / P))

def kalman_resources(a, Q, s2):
    """Achieved (I_mem, r, P) of the one-layer Kalman design with read noise s2."""
    V = world(a, Q)
    P, K, Pp = kalman_steady(a, Q, s2)
    # xhat_t = sum_j g_j y_{t-j}, g_j = K((1-K)a)^j ; Var(xhat | X^t) = s2 * sum g_j^2
    b = (1 - K) * a
    var_cond = s2 * K * K / (1 - b * b)
    I_mem = 0.5 * math.log((V - P) / var_cond)
    r = 0.5 * math.log(Pp / P)  # directed information rate of the Gaussian read channel
    return I_mem, r, P

def floor_cost(a, Q, k, h, kappa, c, w, grid=4000):
    V = world(a, Q)
    best = (w * V, V)  # act blind: K = 0, no memory, no reads
    Pmin = 1e-6 * V
    for P in np.geomspace(Pmin, V * (1 - 1e-9), grid):
        J = h + kappa * I_min(a, Q, P) + c * R_seq(a, Q, P) + w * lead_loss(a, Q, P, k)
        if J < best[0]:
            best = (J, P)
    return best

def kalman_best(a, Q, k, h, kappa, c, w, grid=4000):
    V = world(a, Q)
    best = (w * V, None)
    for s2 in np.geomspace(1e-6 * V, 1e6 * V, grid):
        I, r, P = kalman_resources(a, Q, s2)
        J = h + kappa * I + c * r + w * lead_loss(a, Q, P, k)
        if J < best[0]:
            best = (J, s2)
    return best

print("== 1. The converse is a lower bound; the Kalman design meets it term by term where it should")
a, Q, k = 0.9, 1.0, 2
for s2 in [0.01, 0.3, 1.0, 10.0]:
    I, r, P = kalman_resources(a, Q, s2)
    chk(f"Kalman s2={s2}: read rate equals R_seq(P) (achievability of the read term)",
        abs(r - R_seq(a, Q, P)) < 1e-9, f"r={r:.6f} R_seq={R_seq(a,Q,P):.6f}")
    chk(f"Kalman s2={s2}: memory >= I_min(P) (converse on the memory term)",
        I >= I_min(a, Q, P) - 1e-12, f"I_mem={I:.4f} I_min={I_min(a,Q,P):.4f} gap={I-I_min(a,Q,P):.4f}")

# Monte Carlo check of I_mem formula and P (Gaussian, so I from covariances)
rng = np.random.default_rng(7)
T = 400000
s2 = 0.5
x = np.zeros(T); n = rng.normal(0, math.sqrt(Q), T); v = rng.normal(0, math.sqrt(s2), T)
for t in range(1, T):
    x[t] = a * x[t-1] + n[t]
y = x + v
P, K, Pp = kalman_steady(a, Q, s2)
xh = np.zeros(T)
for t in range(1, T):
    xh[t] = (1 - K) * a * xh[t-1] + K * y[t]
# noise part of xhat
xv = np.zeros(T)
for t in range(1, T):
    xv[t] = (1 - K) * a * xv[t-1] + K * v[t]
burn = 1000
P_mc = np.var(x[burn:] - xh[burn:])
I_mc = 0.5 * math.log(np.var(xh[burn:]) / np.var(xv[burn:]))
I_th, _, _ = kalman_resources(a, Q, s2)
chk("Monte Carlo: filter error P matches steady state", abs(P_mc / P - 1) < 0.02, f"{P_mc:.4f} vs {P:.4f}")
chk("Monte Carlo: I(xhat; X^t) matches closed form", abs(I_mc - I_th) < 0.02, f"{I_mc:.4f} vs {I_th:.4f}")

print("== 2. Floor vs best one-layer Kalman design across prices (efficiency J_floor / J_design)")
rows = []
for kappa in [0.0, 0.01, 0.1, 1.0]:
    for c in [0.0, 0.1, 1.0]:
        for w in [1.0, 10.0, 100.0]:
            h = 0.1
            Jf, Pf = floor_cost(a, Q, k, h, kappa, c, w)
            if c == 0.0:
                # free reads: exact reads + noisy store M = x_t + noise realises I_min exactly (c6d)
                Jd = Jf
            else:
                Jd, _ = kalman_best(a, Q, k, h, kappa, c, w)
            eff = Jf / Jd
            rows.append((kappa, c, w, Jf, Jd, eff))
            chk(f"floor <= design (kappa={kappa}, c={c}, w={w})", Jf <= Jd + 1e-9, f"eff={eff:.4f}")
effs = [r[5] for r in rows]
print(f"   efficiency of best one-layer Kalman vs floor: min {min(effs):.4f}, median {np.median(effs):.4f}")
chk("kappa = 0: Kalman with tuned read noise attains the floor (to grid accuracy)",
    all(r[5] > 0.999 for r in rows if r[0] == 0.0), "")

print("== 3. Duality: J*(prices) is concave in the prices (support function of the frontier)")
ws = np.linspace(0.5, 50, 60)
Js = np.array([floor_cost(a, Q, k, 0.1, 0.1, 0.1, w, grid=1500)[0] for w in ws])
second = Js[2:] - 2 * Js[1:-1] + Js[:-2]
chk("J_floor concave in w (second differences <= 0)", (second <= 1e-6).all(), f"max {second.max():.2e}")

print("== 4. Price-free first-nat value of the world (CT4 at the floor)")
V = world(a, Q)
# d/dI [w * lead_loss] at I=0 with P = V e^{-2I}: -2 a^{2k} V w ; plus read rate slope
dI = 1e-6
P1 = V * math.exp(-2 * dI)
slope_loss = (lead_loss(a, Q, P1, k) - lead_loss(a, Q, V, k)) / dI
chk("first-nat loss saving equals 2 a^{2k} Var", abs(-slope_loss - 2 * a ** (2 * k) * V) < 1e-3 * V,
    f"{-slope_loss:.4f} vs {2*a**(2*k)*V:.4f}")

print("== 5. Farrell decomposition: cost efficiency = technical x allocative (one example)")
# Inefficient design: Kalman with a deliberately wrong read noise, a wasted nat of memory,
# and reads bought at 1.5x the information they deliver (redundant reads).
kappa, c, w, h = 0.1, 0.1, 10.0, 0.1
I, r0, P = kalman_resources(a, Q, 0.05)
I_w = I + 1.0
r = 1.5 * r0
D = lead_loss(a, Q, P, k)
J_act = h + kappa * I_w + c * r + w * D
# technical (input-oriented, radial on (I, r) at fixed D): smallest theta with theta*(I_w, r) feasible for D
# feasibility at fixed P: I >= I_min(P), r >= R_seq(P)
theta = max(I_min(a, Q, P) / I_w, R_seq(a, Q, P) / r)
Jf, _ = floor_cost(a, Q, k, h, kappa, c, w)
J_tech = h + theta * (kappa * I_w + c * r) + w * D
eta_C = Jf / J_act
eta_T = J_tech / J_act
eta_A = Jf / J_tech
chk("eta_C = eta_T * eta_A", abs(eta_C - eta_T * eta_A) < 1e-12,
    f"eta_C={eta_C:.4f} eta_T={eta_T:.4f} eta_A={eta_A:.4f} theta={theta:.4f}")
chk("technical inefficiency detected (theta < 1) and allocative part < 1", theta < 1 and eta_A < 1, f"theta={theta:.4f}")
# The radial measure is price-free: theta depends on (I_w, r, P) and the world only.
theta2 = max(I_min(a, Q, P) / I_w, R_seq(a, Q, P) / r)
chk("technical efficiency is the same at other prices (price-free)", abs(theta2 - theta) < 1e-15)

print("== 6. Price-free switch-on edge at the floor: a model pays (h = 0) iff kappa + c(1-a^2) < 2 w a^{2k} Var")
def pays(kappa, c, w, a=0.9, Q=1.0, k=2):
    Jf, Pf = floor_cost(a, Q, k, 0.0, kappa, c, w, grid=6000)
    return Pf < world(a, Q) * (1 - 1e-6)
a6, k6 = 0.9, 2
V6 = world(a6, 1.0)
for (kappa, c) in [(1.0, 2.0), (3.0, 0.5), (0.2, 10.0)]:
    wcrit = (kappa + c * (1 - a6 * a6)) / (2 * a6 ** (2 * k6) * V6)
    chk(f"switch-on edge kappa={kappa}, c={c}: no model at 0.97 w_crit, model at 1.03 w_crit",
        (not pays(kappa, c, 0.97 * wcrit)) and pays(kappa, c, 1.03 * wcrit), f"w_crit={wcrit:.4f}")

print()
print("ALL PASS" if not FAILS else f"{len(FAILS)} FAIL: {FAILS}")
raise SystemExit(1 if FAILS else 0)
