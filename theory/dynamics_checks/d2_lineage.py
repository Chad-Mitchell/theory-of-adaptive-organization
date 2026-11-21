"""DYNAMICS §3 checks: lineage (geometric-growth) objective vs per-unit J; bet-hedging optimum; when they agree.
Written independently of the wide-net scan (compares to its C2 numbers at the end).
Run: nice -n 19 python3 d2_lineage.py -> d2_results.json, prints ALL D2 CHECKS PASS."""
import json, math, os
import numpy as np
from scipy.optimize import minimize_scalar

HERE = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(1966)
R, ok = {}, []

# Two designs. Lean: factor a1 in calm, a0 under a shock. Robust: b1 calm, b0 shock. Shock prob beta.
beta, a1, a0, b1, b0 = 0.05, 1.30, 0.0, 1.05, 0.90

# ---- D2a. Shared shock (hits every unit in the generation): lineage growth with robust share q
def G_shared(q):
    calm = (1 - q) * a1 + q * b1; shock = (1 - q) * a0 + q * b0
    return (1 - beta) * math.log(calm) + beta * (math.log(shock) if shock > 0 else -math.inf)
res = minimize_scalar(lambda q: -G_shared(q), bounds=(1e-9, 1), method="bounded", options={"xatol": 1e-10})
q_num = float(res.x)
q_closed = min(1.0, beta * a1 / (a1 - b1)) if a0 == 0 else None   # FOC with a0 = 0: beta*a1 = q*(a1-b1)
R["D2a_q_star_numeric_vs_closed"] = [q_num, q_closed]
ok.append(abs(q_num - q_closed) < 1e-6)
R["D2a_G_pure_lean_pure_robust_mix"] = [G_shared(0.0), G_shared(1.0), G_shared(q_closed)]
ok.append(G_shared(q_closed) > G_shared(1.0) + 0.05 and G_shared(0.0) == -math.inf)

# Per-unit expected factor (the J-like objective: an expectation over units and shocks) is linear in q,
# so its optimum is a pure design whatever the correlation.
EF = lambda q: (1 - q) * ((1 - beta) * a1 + beta * a0) + q * ((1 - beta) * b1 + beta * b0)
qs = np.linspace(0, 1, 101); ef = np.array([EF(q) for q in qs])
R["D2a_per_unit_expectation_linear_in_q"] = bool(np.allclose(np.diff(ef, 2), 0, atol=1e-12))
ok.append(R["D2a_per_unit_expectation_linear_in_q"])
R["D2a_per_unit_expectation_argmax"] = float(qs[np.argmax(ef)])     # 0 -> lean
ok.append(R["D2a_per_unit_expectation_argmax"] == 0.0)

# ---- D2b. Independent shocks (each unit hit independently w.p. beta): in a large population the lineage
# factor each generation is the arithmetic mean -> G = ln EF(q), maximized at a pure design (here lean).
G_indep = lambda q: math.log(EF(q))
R["D2b_indep_argmax"] = float(qs[np.argmax([G_indep(q) for q in qs])])
ok.append(R["D2b_indep_argmax"] == 0.0)
# finite-population simulation check (N = 5000 units, 400 generations)
def sim(q, rho, N=5000, T=400):
    # shock shared w.p. rho (all units hit together), otherwise independent per unit; marginal prob beta
    logW = 0.0
    for _ in range(T):
        if rng.random() < rho:
            hit = np.full(N, rng.random() < beta)
        else:
            hit = rng.random(N) < beta
        robust = rng.random(N) < q
        f = np.where(robust, np.where(hit, b0, b1), np.where(hit, a0, a1))
        m = f.mean()
        if m <= 0: return -math.inf
        logW += math.log(m)
    return logW / T
R["D2b_sim_indep_G_lean_vs_q026"] = [sim(0.0, 0.0), sim(0.26, 0.0)]
ok.append(R["D2b_sim_indep_G_lean_vs_q026"][0] > R["D2b_sim_indep_G_lean_vs_q026"][1])

# ---- D2c. Partly shared shocks: robust share rises from 0 with the shared fraction rho.
def G_rho(q, rho):
    # large-N limit: w.p. rho*beta all hit; w.p. rho*(1-beta) none hit; w.p. (1-rho) a beta fraction hit
    calm = (1 - q) * a1 + q * b1; shock = (1 - q) * a0 + q * b0
    mix = (1 - beta) * calm + beta * shock
    val = rho * (1 - beta) * math.log(calm) + (1 - rho) * math.log(mix)
    if rho > 0: val += rho * beta * (math.log(shock) if shock > 0 else -math.inf)
    return val
qstar_rho = []
for rho in (0.0, 0.05, 0.2, 0.5, 1.0):
    r_ = minimize_scalar(lambda q: -G_rho(q, rho), bounds=(0, 1), method="bounded", options={"xatol": 1e-9})
    qstar_rho.append([rho, round(float(r_.x), 4)])
R["D2c_qstar_vs_shared_fraction"] = qstar_rho
ok.append(qstar_rho[0][1] < 1e-3 and all(qstar_rho[i][1] <= qstar_rho[i + 1][1] + 1e-6 for i in range(4)) and qstar_rho[-1][1] > 0.2)

# ---- D2d. Per-unit ruin constraint (each unit must survive w.p. 1-eps over its life) excludes lean
# entirely (a lean unit dies in any shock), so per-unit J with ruin picks pure robust: G = G_shared(1).
R["D2d_per_unit_ruin_pick_G"] = G_shared(1.0)
R["D2d_lineage_gain_over_best_pure"] = G_shared(q_closed) / G_shared(1.0)
ok.append(R["D2d_lineage_gain_over_best_pure"] > 2.5)

# ---- D2e. Per-unit J reproduces the lineage optimum when the objective is evaluated per unit on log scale
# with the shock shared? No: a single unit's log factor with a pure design is -inf (lean) or the robust value.
# The mixture's gain exists only at the level of the lineage (the mean over units inside a generation).
R["D2e_note"] = "the gain is a property of the lineage mean within a generation; no unit-level design attains it"

# ---- compare with the scan (C2): q*=0.260, G=0.1279, pure robust 0.0411, arithmetic 1.235 vs 1.0425
R["compare_scan_C2"] = [round(q_closed, 3), round(G_shared(q_closed), 4), round(G_shared(1.0), 4), round(EF(0), 4), round(EF(1), 4)]
ok.append(R["compare_scan_C2"] == [0.26, 0.1279, 0.0411, 1.235, 1.0425])
R["checks_passed"] = int(sum(ok)); R["checks_total"] = len(ok)
json.dump(R, open(os.path.join(HERE, "d2_results.json"), "w"), indent=1, default=str)
for kk, v in R.items(): print(kk, v)
print("ALL D2 CHECKS PASS" if all(ok) else "D2 FAIL: %s" % [i for i, x in enumerate(ok) if not x])
