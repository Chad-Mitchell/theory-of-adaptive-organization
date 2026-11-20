"""DYNAMICS §2 checks: redesign cost, inaction band, step-change threshold, layer-count hysteresis,
aggregate smoothing. Written independently of the wide-net scan (it only compares at the end).
Run: nice -n 19 python3 d1_redesign_band.py  ->  d1_results.json, prints ALL D1 CHECKS PASS."""
import json, math, os
import numpy as np
from scipy.integrate import solve_bvp

HERE = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(29)
R, ok = {}, []

# ---- D1a. Brownian gap, quadratic flow loss w*x^2, fixed cost k per reset to 0, band |x| < b.
# Renewal: cost per cycle C(b) = k + w*E int x^2, cycle length E tau = b^2/sigma^2.
# E int_0^tau x^2 from 0 solves (sigma^2/2) f'' = -x^2, f(+-b) = 0 -> f(0) = b^4/(6 sigma^2).
sig, w, k = 1.0, 1.0, 0.01
def f0_numeric(b):
    sol = solve_bvp(lambda x, y: np.vstack([y[1], -2 * x**2 / sig**2]), lambda ya, yb: np.array([ya[0], yb[0]]),
                    np.linspace(-b, b, 201), np.zeros((2, 201)))
    return float(sol.sol(0.0)[0])
b = 0.7
R["D1a_f0_numeric_vs_closed"] = [f0_numeric(b), b**4 / (6 * sig**2)]
ok.append(abs(R["D1a_f0_numeric_vs_closed"][0] / R["D1a_f0_numeric_vs_closed"][1] - 1) < 1e-4)
avg = lambda b: k * sig**2 / b**2 + w * b**2 / 6
bstar = (6 * k * sig**2 / w) ** 0.25
grid = np.linspace(0.05, 2, 20001); bnum = grid[np.argmin(avg(grid))]
R["D1a_bstar_closed_vs_grid"] = [bstar, float(bnum)]
ok.append(abs(bnum / bstar - 1) < 1e-3)
R["D1a_min_avg_cost_equals_2_sqrt_kw_over_6"] = [avg(bstar), 2 * math.sqrt(k * w * sig**2 / 6)]
ok.append(abs(avg(bstar) / (2 * math.sqrt(k * w * sig**2 / 6)) - 1) < 1e-12)
R["D1a_band_ratio_for_k_100x_smaller"] = 100 ** 0.25

# Monte Carlo with exact Brownian-bridge exit correction is overkill; use a fine step and report the bias.
def mc(b, T=300.0, dt=2e-4, reps=4):
    out = []
    for _ in range(reps):
        n = int(T / dt); inc = rng.standard_normal(n) * sig * math.sqrt(dt)
        x = 0.0; c = 0.0
        for e in inc:  # vectorising a reset process is awkward; T is small enough
            x += e; c += w * x * x * dt
            if x >= b or x <= -b:
                c += k; x = 0.0
        out.append(c / T)
    return float(np.mean(out)), float(np.std(out) / math.sqrt(reps))
R["D1a_mc_at_bstar"] = mc(bstar, T=150.0)
ok.append(abs(R["D1a_mc_at_bstar"][0] / avg(bstar) - 1) < 0.08)

# ---- D1b. Step change (not Brownian): the argmin jumps by D once and stays for a regime of length T_reg
# (or forever with discount r). Moving costs k; not moving costs w*D^2 per unit time.
# Move iff w D^2 T_reg > k  ->  D* = sqrt(k / (w T_reg));  discounted: D* = sqrt(k r / w).
Treg = 50.0
Dstar_step = math.sqrt(k / (w * Treg))
Ds = np.linspace(0, 0.2, 2001)
move = w * Ds**2 * Treg > k
R["D1b_step_threshold_closed_vs_grid"] = [Dstar_step, float(Ds[np.argmax(move)])]
ok.append(abs(Ds[np.argmax(move)] - Dstar_step) < 2e-4)
R["D1b_scaling"] = "step: D* ~ k^(1/2); Brownian band: b* ~ k^(1/4). The threshold depends on how the inputs move."

# ---- D1c. Layer-count hysteresis (Dixit 1989 mechanism) by value iteration.
# J*(K, w) = K*h + w*G0/(K+1)  (diminishing returns in K; crossing K->K+1 at w_c = h (K+1)(K+2)/G0).
# The stake follows a reflected random walk on a log grid; switching K costs kK each way; discount r.
h, G0, r, kK = 1.0, 6.0, 0.02, 3.0
lw = np.linspace(math.log(0.5), math.log(20), 400); W = np.exp(lw); n = len(W)
step = 0.01  # sd of d ln w per period
P = np.zeros((n, n)); d = lw[1] - lw[0]
for i in range(n):
    p = np.exp(-0.5 * ((lw - lw[i]) / step) ** 2); p /= p.sum(); P[i] = p
Ks = np.arange(0, 5)
flow = Ks[:, None] * h + W[None, :] * G0 / (Ks[:, None] + 1)
beta = 1 / (1 + r)
def solve(kswitch):
    V = np.zeros((len(Ks), n))
    for _ in range(20000):
        EV = V @ P.T
        cont = flow + beta * EV                      # cost if keep K this period
        Vn = np.min(cont[None, :, :] + kswitch * (np.abs(Ks[:, None, None] - Ks[None, :, None]) > 0), axis=1)
        if np.max(np.abs(Vn - V)) < 1e-9: V = Vn; break
        V = Vn
    EV = V @ P.T; cont = flow + beta * EV
    pol = np.argmin(cont[None, :, :] + kswitch * (np.abs(Ks[:, None, None] - Ks[None, :, None]) > 0), axis=1)
    return pol  # pol[K_now, i] = K chosen
pol0, polk = solve(0.0), solve(kK)
def thresholds(pol, K):
    up = W[np.argmax(pol[K] > K)] if np.any(pol[K] > K) else None          # from K, first w that adds
    down = W[n - 1 - np.argmax(pol[K + 1][::-1] < K + 1)] if np.any(pol[K + 1] < K + 1) else None  # from K+1, last w that drops
    return up, down
wc = h * 2 * 3 / G0   # K=1 -> 2 crossing
u0, d0 = thresholds(pol0, 1); uk, dk = thresholds(polk, 1)
R["D1c_crossing_wc_K1to2"] = wc
R["D1c_no_switch_cost_up_down"] = [float(u0), float(d0)]
R["D1c_with_switch_cost_up_down"] = [float(uk), float(dk)]
ok.append(abs(u0 / wc - 1) < 0.03 and abs(d0 / wc - 1) < 0.03)    # no cost: one threshold at w_c
ok.append(uk > wc * 1.05 and dk < wc / 1.05)                        # cost: add above w_c, drop below it

# ---- D1d. Aggregation (Caballero-Engel): many units with lumpy band policies and dispersed gaps respond
# to a common step in the target smoothly in aggregate, so T_red stays defined for the class average
# even when no single unit moves for small steps.
N = 20000; band = bstar
gaps = rng.uniform(-band, band, N)         # dispersed positions inside the band (idiosyncratic histories)
Dstep = 0.3 * band
moved_frac = []
g = gaps + Dstep
for t in range(400):
    g = g + rng.standard_normal(N) * sig * math.sqrt(0.01)
    hit = np.abs(g) >= band; g[hit] = 0.0
    moved_frac.append(float(np.mean(g)))
R["D1d_aggregate_mean_gap_t0_t100_t399"] = [Dstep, moved_frac[99], moved_frac[399]]
ok.append(abs(moved_frac[399]) < 0.25 * Dstep and moved_frac[99] < Dstep)  # aggregate closes the gap smoothly
R["D1d_single_unit_at_centre_moves_for_step_below_band"] = bool(Dstep >= band)  # False: no immediate move
ok.append(R["D1d_single_unit_at_centre_moves_for_step_below_band"] is False)


# ---- D1e. Convex (smooth) adjustment cost kappa*xdot^2 instead of a fixed cost: no band; after a step the gap
# decays as exp(-t*sqrt(w/kappa)), so T_red = sqrt(kappa/w) (Euler-Lagrange kappa*x'' = w*x). Discrete check:
# minimise sum w x_t^2 dt + kappa ((x_t - x_{t-1})/dt)^2 dt with x_0 = 1 (linear system, long horizon).
kap, dt_, nT = 4.0, 0.01, 4000
from scipy.linalg import solve_banded
ab = np.zeros((3, nT)); bvec = np.zeros(nT)
ab[1, :] = w * dt_ + 2 * kap / dt_; ab[1, -1] -= kap / dt_   # free end
ab[0, 1:] = -kap / dt_; ab[2, :-1] = -kap / dt_
bvec[0] = kap / dt_ * 1.0                   # coupling to the fixed x_0 = 1
xs = solve_banded((1, 1), ab, bvec)
t_e = (np.argmax(xs < math.exp(-1)) + 1) * dt_
R["D1e_Tred_numeric_vs_sqrt_kappa_over_w"] = [float(t_e), math.sqrt(kap / w)]
ok.append(abs(t_e / math.sqrt(kap / w) - 1) < 0.02)

# ---- compare with the scan (C5): scan quotes MC 0.0819 vs theory 0.0816 at b*=0.495
R["compare_scan_C5_theory_at_bstar"] = round(avg(bstar), 4)
ok.append(abs(avg(bstar) - 0.0816) < 5e-4 and abs(bstar - 0.495) < 1e-3)
R["checks_passed"] = int(sum(ok)); R["checks_total"] = len(ok)
json.dump(R, open(os.path.join(HERE, "d1_results.json"), "w"), indent=1)
for kk, v in R.items(): print(kk, v)
print("ALL D1 CHECKS PASS" if all(ok) else "D1 FAIL: %s" % [i for i, x in enumerate(ok) if not x])
