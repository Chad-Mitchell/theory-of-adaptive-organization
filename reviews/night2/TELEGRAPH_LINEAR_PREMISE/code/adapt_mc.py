"""TELEGRAPH-LINEAR-PREMISE: adaptation time after a switch, four filters on common noise. In-model only.
Units of Conti & Mora 2022 (C&M; arXiv 2011.09958v2): y = +-1, switching rate 1/(2 tau), ds = y dt + sqrt(theta) dW.
Filters:
 F1 exact discrete-time Bayes (C&M eq. 11; tanh addition in half-LLR Lam, x = tanh Lam), computed stably.
 F2 exact continuous Wonham filter, Ito SDE in full LLR L (x = tanh(L/2)): dL = (2/theta) ds - (1/tau) sinh(L) dt.
 F3 C&M eq. (20) AS PRINTED, read as Ito, Euler-Maruyama in x: dx = -x/tau dt + (1-x^2)/theta ds (clipped).
 F4 the same printed equation mapped exactly to L by Ito's rule: dL = (2/theta) ds - (1/tau) sinh L dt + (2/theta) tanh(L/2) dt.
Protocol: start at x = 0 with y = +1 for a burn-in of BURN*theta (no switch), then switch to y = -1 at t = 0 and record the
first time x < 0 (first passage), censored at TMAX*theta. Primary statistic: mean first-passage time (C&M approximate tA by it).
Seed 20261115 (+ index of tau). Usage: python3 adapt_mc.py [dt] [reps] [outfile]"""
import numpy as np, json, sys, time
from scipy.special import expit
theta = 1.0
dt = float(sys.argv[1]) if len(sys.argv) > 1 else 0.005
REPS = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
OUT = sys.argv[3] if len(sys.argv) > 3 else "../out_adapt.json"
TAUS = [10, 30, 100, 300, 1000, 3000, 10000]
BURN, TMAX = 100.0, 200.0

def f1_step(Lam, ds, tau):
    k = dt / (2 * tau); c = 1 - 2 * k
    a = np.abs(Lam); sg = np.sign(Lam)
    u = 2 * expit(-2 * a)                      # 1 - tanh(a), stable
    pre = 0.5 * (np.log(1 + c - c * u) - np.log(2 * k + c * u))   # atanh(c tanh a) for a >= 0
    return sg * pre + ds / theta               # half-LLR increment s dt/sigma^2 = ds/theta

def f2_step(L, ds, tau):
    return L + (2 / theta) * ds - (1 / tau) * np.sinh(L) * dt

def f3_step(x, ds, tau):
    x = x - x / tau * dt + (1 - x * x) / theta * ds
    return np.clip(x, -1 + 1e-15, 1 - 1e-15)

def f4_step(L, ds, tau):
    return L + (2 / theta) * ds - (1 / tau) * np.sinh(L) * dt + (2 / theta) * np.tanh(L / 2) * dt

res = {"dt": dt, "reps": REPS, "theta": theta, "burn": BURN, "tmax": TMAX, "runs": {}}
for i, tau in enumerate(TAUS):
    t0 = time.time()
    rng = np.random.default_rng(20261115 + i)
    Lam = np.zeros(REPS); L2 = np.zeros(REPS); x3 = np.zeros(REPS); L4 = np.zeros(REPS)
    for _ in range(int(BURN / dt)):
        ds = 1.0 * dt + np.sqrt(theta * dt) * rng.standard_normal(REPS)
        Lam = f1_step(Lam, ds, tau); L2 = f2_step(L2, ds, tau); x3 = f3_step(x3, ds, tau); L4 = f4_step(L4, ds, tau)
    pre = {"F1_x": float(np.mean(np.tanh(Lam))), "F2_x": float(np.mean(np.tanh(L2 / 2))),
           "F3_x": float(np.mean(x3)), "F4_x": float(np.mean(np.tanh(L4 / 2))),
           "F1_L_full": float(np.mean(2 * Lam)), "F2_L": float(np.mean(L2)), "F4_L": float(np.mean(L4))}
    cross = {k: np.full(REPS, np.nan) for k in ("F1", "F2", "F3", "F4")}
    t = 0.0
    for n in range(int(TMAX / dt)):
        ds = -1.0 * dt + np.sqrt(theta * dt) * rng.standard_normal(REPS)
        Lam = f1_step(Lam, ds, tau); L2 = f2_step(L2, ds, tau); x3 = f3_step(x3, ds, tau); L4 = f4_step(L4, ds, tau)
        t += dt
        for k, v in (("F1", Lam), ("F2", L2), ("F3", x3), ("F4", L4)):
            new = np.isnan(cross[k]) & (v < 0); cross[k][new] = t
        if n % 200 == 0 and all(not np.isnan(c).any() for c in cross.values()):
            break
    r = {"pre_switch": pre}
    for k, c in cross.items():
        cens = float(np.mean(np.isnan(c))); cc = np.where(np.isnan(c), TMAX, c)
        r[k] = {"mean_fpt": float(np.mean(cc)), "se": float(np.std(cc) / np.sqrt(REPS)),
                "median_fpt": float(np.median(cc)), "censored_frac": cens}
    res["runs"][str(tau)] = r
    print(tau, {k: round(r[k]["mean_fpt"], 3) for k in cross}, "censored", {k: r[k]["censored_frac"] for k in cross},
          f"{time.time()-t0:.0f}s", flush=True)

lt = np.log(np.array(TAUS, float))
def fits(key):
    m = np.array([res["runs"][str(t)][key]["mean_fpt"] for t in TAUS])
    big = lt >= np.log(300)
    slope_big = float(np.polyfit(lt[big], m[big], 1)[0])
    quad = np.polyfit(lt, m, 2)                         # m = c2 ln^2 + c1 ln + c0
    ll = float(np.polyfit(lt[lt >= np.log(1000)], np.log(m[lt >= np.log(1000)]), 1)[0])
    return {"slope_vs_lntau_tau>=300": slope_big, "quad_coef_ln2": float(quad[0]), "quad_coef_ln": float(quad[1]),
            "quad_const": float(quad[2]), "loglog_slope_tau>=1000": ll}
res["fits"] = {k: fits(k) for k in ("F1", "F2", "F3", "F4")}
# leading-order prediction for the exact filter: (theta/2) ln(4 tau/theta); C&M eq. (36): (theta/4) ln^2(tau/theta)
res["reference"] = {str(t): {"single_log_lead": 0.5 * theta * np.log(4 * t / theta),
                             "CM_eq36_lead": 0.25 * theta * np.log(t / theta) ** 2,
                             "linear_CM_eq30": float(t * (theta / t) * (1 + np.sqrt(1 + 2 * t / theta)) / 2 *
                                                     np.log(2 * np.sqrt(1 + 2 * t / theta) / (1 + np.sqrt(1 + 2 * t / theta))))}
                    for t in TAUS}
print(json.dumps(res["fits"], indent=1))
json.dump(res, open(OUT, "w"), indent=1)
