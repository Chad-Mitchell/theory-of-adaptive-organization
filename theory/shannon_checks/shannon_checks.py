"""Checks for theory/SHANNON_2026-11-21.md (converse, achievability, frontier, efficiency).

Scalar Gauss-Markov world x_{t+1} = a x_t + n_t, Var(n) = Q, stationary Var V = Q/(1-a^2).
Reads y_t = x_t + v_t, Var(v) = s2 (the design chooses s2). Action at lead k: predict x_{t+k}.
All information in nats per step. Run: python3 theory/shannon_checks/shannon_checks.py

The information floor (Theorem S1, after review B1) has no layer charge:
    J >= min_P { kappa * I_min(P) + c * R_seq(P) + w * lead_loss(P) }.
A memoryless read (M_t = Y_t, K = 0) is a legal design and is checked in section 7.
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

def memoryless_resources(a, Q, s2):
    """Achieved (I_mem, r, P) of the K=0 rule M_t = Y_t at read noise s2.

    I_mem = I(Y_t; X^t) = I(Y_t; x_t) = 1/2 ln(V/P).
    r is the directed information rate of the observation process X → Y,
    which equals the Kalman read rate at the same s2 (the channel, not the store).
    """
    V = world(a, Q)
    P = V * s2 / (V + s2)
    I_mem = 0.5 * math.log(V / P)
    _, r, _ = kalman_resources(a, Q, s2)
    return I_mem, r, P

def memoryless_cost(a, Q, k, kappa, c, w, s2):
    """Cost of the memoryless design (K = 0, no layer charge)."""
    I, r, P = memoryless_resources(a, Q, s2)
    D = lead_loss(a, Q, P, k)
    J = kappa * I + c * r + w * D
    return J, I, r, P, D

def floor_cost(a, Q, k, kappa, c, w, grid=4000):
    """Information floor of Theorem S1: no layer charge h."""
    V = world(a, Q)
    best = (w * V, V)  # act blind: K = 0, no memory, no reads
    Pmin = 1e-6 * V
    for P in np.geomspace(Pmin, V * (1 - 1e-9), grid):
        J = kappa * I_min(a, Q, P) + c * R_seq(a, Q, P) + w * lead_loss(a, Q, P, k)
        if J < best[0]:
            best = (J, P)
    return best

def retracted_floor_with_layer_charge(a, Q, k, h, kappa, c, w, grid=4000):
    """The retracted S1 floor that added h whenever P < V. Used only to replay the counterexample."""
    V = world(a, Q)
    best = (w * V, V)
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


def run_checks():
    global FAILS
    FAILS = []

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

    print("== 2. Information floor vs best one-layer Kalman design across prices (efficiency J_floor / J_design, h left out of both sides)")
    rows = []
    assigned_c0 = 0
    for kappa in [0.0, 0.01, 0.1, 1.0]:
        for c in [0.0, 0.1, 1.0]:
            for w in [1.0, 10.0, 100.0]:
                Jf, Pf = floor_cost(a, Q, k, kappa, c, w)
                if c == 0.0:
                    # free reads: exact reads + noisy store M = x_t + noise realises I_min exactly (c6d).
                    # Assigned, not simulated (review S2).
                    Jd = Jf
                    assigned_c0 += 1
                else:
                    Jd, _ = kalman_best(a, Q, k, 0.0, kappa, c, w)
                eff = Jf / Jd
                rows.append((kappa, c, w, Jf, Jd, eff, c == 0.0))
                chk(f"floor <= design (kappa={kappa}, c={c}, w={w})", Jf <= Jd + 1e-9, f"eff={eff:.4f}")
    effs = [r[5] for r in rows]
    both_priced = [r for r in rows if r[0] > 0 and r[1] > 0]
    print(f"   efficiency of best one-layer Kalman vs information floor: min {min(effs):.4f}, median {np.median(effs):.4f}")
    print(f"   {assigned_c0} of 36 prices have c=0 and set J_design = J_floor rather than simulating the store; "
          f"{len(both_priced)} have both kappa>0 and c>0; median 1.0000 reflects the free-memory and free-read edges")
    worst = min((r for r in rows if not r[6]), key=lambda r: r[5])
    chk("worst both-priced (or c>0) efficiency is within 4.3% of the information floor (0.9574 at kappa=c=w=1)",
        abs(worst[5] - 0.9574) < 5e-4 and worst[0] == 1.0 and worst[1] == 1.0 and worst[2] == 1.0,
        f"min eff={worst[5]:.4f} at kappa={worst[0]}, c={worst[1]}, w={worst[2]}")
    chk("w >= 10: every c>0 point is within 0.3% of the information floor",
        all(r[5] > 0.997 for r in rows if r[2] >= 10 and not r[6]),
        f"worst such {min(r[5] for r in rows if r[2] >= 10 and not r[6]):.4f}")
    chk("kappa = 0, c > 0: Kalman with tuned read noise attains the information floor (to grid accuracy)",
        all(r[5] > 0.999 for r in rows if r[0] == 0.0 and not r[6]), "")

    print("== 3. Duality: J_floor is concave in the prices; envelope slope in w equals optimal loss")
    ws = np.linspace(0.5, 50, 60)
    floor_rows = [floor_cost(a, Q, k, 0.1, 0.1, w, grid=1500) for w in ws]
    Js = np.array([J for J, _ in floor_rows])
    second = Js[2:] - 2 * Js[1:-1] + Js[:-2]
    chk("J_floor concave in w (second differences <= 0)", (second <= 1e-6).all(), f"max {second.max():.2e}")
    # Envelope: central difference of J*(w) vs D* at the minimizer. Avoid the very edge of the grid.
    dw = ws[1] - ws[0]
    env_ok = True
    env_worst = 0.0
    for i in range(2, len(ws) - 2):
        slope = (Js[i + 1] - Js[i - 1]) / (2 * dw)
        Dstar = lead_loss(a, Q, floor_rows[i][1], k)
        rel = abs(slope - Dstar) / max(Dstar, 1e-9)
        env_worst = max(env_worst, rel)
        if rel > 0.02:
            env_ok = False
    chk("envelope: dJ_floor/dw equals optimal lead-k loss (central differences within 2%)",
        env_ok, f"worst relative error {env_worst:.2e}")

    print("== 4. Price-free first-nat value of the world (CT4 at the floor)")
    V = world(a, Q)
    # d/dI [w * lead_loss] at I=0 with P = V e^{-2I}: -2 a^{2k} V w ; plus read rate slope
    dI = 1e-6
    P1 = V * math.exp(-2 * dI)
    slope_loss = (lead_loss(a, Q, P1, k) - lead_loss(a, Q, V, k)) / dI
    chk("first-nat loss saving equals 2 a^{2k} Var", abs(-slope_loss - 2 * a ** (2 * k) * V) < 1e-3 * V,
        f"{-slope_loss:.4f} vs {2*a**(2*k)*V:.4f}")

    print("== 5. Farrell identity holds for input cost C = kappa I + c r, not for J_floor/J")
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
    # Retracted J-identity used the floor that included h (the design pays h, and a model is used).
    Jf_retracted, _ = retracted_floor_with_layer_charge(a, Q, k, h, kappa, c, w)
    J_tech = h + theta * (kappa * I_w + c * r) + w * D
    eta_C_J = Jf_retracted / J_act
    false_product = theta * (Jf_retracted / J_tech)
    chk("J_floor/J is not theta times the cost-ratio allocative factor (retracted Farrell-on-J identity)",
        abs(false_product - eta_C_J) > 0.2,
        f"theta={theta:.4f} Jf/J={eta_C_J:.4f} theta*(Jf/J_tech)={false_product:.4f}")
    chk("worked J numbers match the review (0.698, 0.985, 0.694 != 0.985)",
        abs(theta - 0.6979) < 5e-4 and abs(eta_C_J - 0.9854) < 5e-4 and abs(false_product - 0.6939) < 5e-4,
        f"theta={theta:.4f} Jf/J={eta_C_J:.4f} product={false_product:.4f}")

    C_act = kappa * I_w + c * r
    C_min = kappa * I_min(a, Q, P) + c * R_seq(a, Q, P)
    eta_C = C_min / C_act
    eta_A = eta_C / theta
    chk("input-cost Farrell: C_min/C = theta * eta_A",
        abs(eta_C - theta * eta_A) < 1e-12,
        f"C_min/C={eta_C:.4f} theta={theta:.4f} eta_A={eta_A:.4f} C_act={C_act:.4f} C_min={C_min:.4f}")
    chk("worked input-cost numbers match the review (C_act=0.5680, C_min=0.3892, alloc=0.9818, product=0.6852)",
        abs(C_act - 0.5680) < 5e-4 and abs(C_min - 0.3892) < 5e-4
        and abs(eta_A - 0.9818) < 5e-4 and abs(eta_C - 0.6852) < 5e-4,
        f"C_act={C_act:.4f} C_min={C_min:.4f} eta_A={eta_A:.4f} eta_C={eta_C:.4f}")
    # The radial measure is price-free: theta depends on (I_w, r, P) and the world only.
    theta2 = max(I_min(a, Q, P) / I_w, R_seq(a, Q, P) / r)
    chk("technical efficiency is the same at other prices (price-free)", abs(theta2 - theta) < 1e-15)

    print("== 6. Price-free switch-on edge at the floor: a model pays iff kappa + c(1-a^2) < 2 w a^{2k} Var")
    def pays(kappa, c, w, a=0.9, Q=1.0, k=2):
        Jf, Pf = floor_cost(a, Q, k, kappa, c, w, grid=6000)
        return Pf < world(a, Q) * (1 - 1e-6)
    a6, k6 = 0.9, 2
    V6 = world(a6, 1.0)
    for (kappa, c) in [(1.0, 2.0), (3.0, 0.5), (0.2, 10.0)]:
        wcrit = (kappa + c * (1 - a6 * a6)) / (2 * a6 ** (2 * k6) * V6)
        chk(f"switch-on edge kappa={kappa}, c={c}: no model at 0.97 w_crit, model at 1.03 w_crit",
            (not pays(kappa, c, 0.97 * wcrit)) and pays(kappa, c, 1.03 * wcrit), f"w_crit={wcrit:.4f}")

    print("== 7. Reviewer K=0 memoryless counterexample: undercuts the retracted layer-charged floor; sits at or above the corrected floor")
    s2 = 0.2
    h, kappa, c, w = 1.0, 0.1, 0.1, 1.0
    J, I, r, P, D = memoryless_cost(a, Q, k, kappa, c, w, s2)
    J_old, _ = retracted_floor_with_layer_charge(a, Q, k, h, kappa, c, w)
    J_new, _ = floor_cost(a, Q, k, kappa, c, w)
    chk("memoryless resources match the review (P=0.193, I=1.654 nats, r=0.950 nats, D=1.936)",
        abs(P - 0.193) < 5e-4 and abs(I - 1.654) < 5e-4 and abs(r - 0.950) < 5e-4 and abs(D - 1.936) < 5e-4,
        f"P={P:.3f} I={I:.3f} r={r:.3f} D={D:.3f}")
    chk("memoryless J = 2.197 undercuts the retracted floor 3.187",
        abs(J - 2.197) < 5e-4 and abs(J_old - 3.187) < 5e-4 and J < J_old,
        f"J={J:.3f} J_old={J_old:.3f}")
    chk("corrected information floor sits at or below the memoryless design",
        J_new <= J + 1e-9,
        f"J_floor={J_new:.3f} J={J:.3f}")
    # Lead-0 replay from the review
    J0, _, _, _, _ = memoryless_cost(a, Q, 0, kappa, c, w, s2)
    J0_old, _ = retracted_floor_with_layer_charge(a, Q, 0, h, kappa, c, w)
    J0_new, _ = floor_cost(a, Q, 0, kappa, c, w)
    chk("lead-0 memoryless J = 0.453 undercuts retracted floor 1.417 and sits at or above the corrected floor",
        abs(J0 - 0.453) < 5e-4 and abs(J0_old - 1.417) < 5e-4 and J0 < J0_old and J0_new <= J0 + 1e-9,
        f"J0={J0:.3f} J0_old={J0_old:.3f} J0_floor={J0_new:.3f}")

    print()
    print("ALL PASS" if not FAILS else f"{len(FAILS)} FAIL: {FAILS}")
    return 0 if not FAILS else 1


if __name__ == "__main__":
    raise SystemExit(run_checks())
