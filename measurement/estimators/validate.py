"""Synthetic-truth validation of aqn.py (AQN-ESTIMATORS). Seeds fixed: base seed 20261115 + condition index * 1000 + rep.
Run: nice -n 19 python3 validate.py <block> ; writes results/<block>.json. Blocks: A (power-law Gaussian), B (misspecified
Gaussian: 1/f OU mixture, single OU, corner check size), C (switching world: HMM), P (premise test), E (event worlds), S (stakes)."""
import sys, json, os, numpy as np
from multiprocessing import Pool
import aqn
from math import pi, log
SEED = 20261115
os.makedirs("results", exist_ok=True)

def rng_for(ci, r):
    return np.random.default_rng(SEED + ci * 1000 + r)

# ---------------- A: power-law Gaussian worlds
A_ALPHA = [1.4, 2.0, 2.6]; A_WC = [0.05, 0.5, 3.0]; A_N = [512, 2048, 8192, 32768]
def A_conds():
    out = []
    for a in A_ALPHA:
        for wc in A_WC:
            for n in A_N:
                out.append((a, wc, n))
    return out
def A_job(args):
    ci, r = args
    a, wc, n = A_conds()[ci]
    rng = rng_for(ci, r); q = 1.0; s2 = q * wc ** -a
    y = aqn.powerlaw_signal(n, a, q, rng) + rng.standard_normal(n) * np.sqrt(s2)
    f = aqn.whittle_fit(y)
    res = {"ci": ci, "alpha": f["alpha"], "se_alpha": f["se_alpha"], "logq": f["logq"], "se_logq": f["se_logq"],
           "logs2": f["logs2"], "se_logs2": f["se_logs2"], "at_bound": f["at_bound"]}
    if n in (2048, 8192) and r < 100:
        res["dfa"] = aqn.dfa_alpha(y)
        va, vq, vs = aqn.variogram_nugget(y); res.update({"vg_alpha": va, "vg_logq": log(vq), "vg_logs2": log(max(vs, 1e-300))})
    return res

# ---------------- B: misspecified Gaussian
MIX_CORNERS = np.geomspace(1e-4, 10, 60)
MIX_W = MIX_CORNERS ** -0.5 * np.log(MIX_CORNERS[1] / MIX_CORNERS[0])
MIX_W = MIX_W / MIX_W.sum()
B_N = [2048, 8192, 32768]
def B_conds():
    # kind, n, band
    out = []
    for n in B_N:
        out.append(("mix", n, (2e-3, pi)))
        out.append(("ou", n, None))
        out.append(("fbm2", n, None))   # pure power law for size of the corner check
        out.append(("fbm14", n, None))
    return out
def mix_noise():
    return 2 * pi * aqn.ou_mixture_spec(np.array([0.5]), MIX_CORNERS, MIX_W)[0]
def B_job(args):
    ci, r = args
    kind, n, band = B_conds()[ci]; rng = rng_for(100 + ci, r)
    if kind == "mix":
        s2 = mix_noise(); y = aqn.ou_mixture(n, MIX_CORNERS, MIX_W, rng) + rng.standard_normal(n) * np.sqrt(s2)
    elif kind == "ou":
        s2 = 2 * pi * aqn.ou_mixture_spec(np.array([0.5]), [0.01], [1.0])[0]
        y = aqn.ou_mixture(n, [0.01], [1.0], rng) + rng.standard_normal(n) * np.sqrt(s2)
    else:
        a = 2.0 if kind == "fbm2" else 1.4
        y = aqn.powerlaw_signal(n, a, 1.0, rng) + rng.standard_normal(n) * np.sqrt(0.5 ** -a)
    c = aqn.whittle_corner_fit(y, band)
    b = c["base"]
    return {"ci": ci, "alpha": b["alpha"], "se_alpha": b["se_alpha"], "logq": b["logq"], "se_logq": b["se_logq"],
            "logs2": b["logs2"], "se_logs2": b["se_logs2"], "LR": c["LR"], "corner_alpha": c["alpha"], "w0": c["w0"]}
def B_truth():
    out = {}
    for ci, (kind, n, band) in enumerate(B_conds()):
        if kind == "mix":
            s2 = mix_noise()
            ft = lambda w: 4 * np.sin(w / 2) ** 2 * (aqn.ou_mixture_spec(w, MIX_CORNERS, MIX_W) + s2 / (2 * pi))
        elif kind == "ou":
            s2 = 2 * pi * aqn.ou_mixture_spec(np.array([0.5]), [0.01], [1.0])[0]
            ft = lambda w: 4 * np.sin(w / 2) ** 2 * (aqn.ou_mixture_spec(w, [0.01], [1.0]) + s2 / (2 * pi))
        else:
            a = 2.0 if kind == "fbm2" else 1.4
            out[ci] = [0.0, a, log(0.5 ** -a)]; continue
        out[ci] = list(aqn.pseudo_true(ft, n, band))
    return out

# ---------------- C: switching world (HMM)
C_SIG = [0.5, 1.5, 3.0]; C_LAM = [0.002, 0.01]; C_N = [2048, 8192, 32768]
def C_conds():
    return [(s, l, n) for s in C_SIG for l in C_LAM for n in C_N]
def _lg(x):
    return log(x) if (x is not None and np.isfinite(x) and x > 0) else None

def C_job(args):
    ci, r = args
    s, lam, n = C_conds()[ci]; rng = rng_for(200 + ci, r); mu = 1.0
    y = aqn.telegraph(n, lam, mu, rng) + rng.standard_normal(n) * s
    h = aqn.hmm_fit(y); o = aqn.ou_fit(y)
    nsw = None
    return {"ci": ci, "loglam": _lg(h["lam"]), "se_loglam": h["se_loglam"], "logmu": log(h["mu"]), "se_logmu": h["se_logmu"],
            "logs2": log(h["s2"]), "se_logs2": h["se_logs2"], "logtA": _lg(h["tA"]),
            "se_logtA": h["se_logtA"], "logq": _lg(h["q"]), "se_logq": h["se_logq"], "ou_logq": _lg(o["q"]),
            "ou_loglam": _lg(o["lam_eq"]), "LR": 2 * (o["nll"] - h["nll"])}
def C_truth(ci):
    s, lam, n = C_conds()[ci]; mu = 1.0; N = s * s
    tA = (N / (2 * mu ** 2)) * (log(2 * mu ** 2 / (lam * N)) - aqn.EULER - 1)
    return {"loglam": log(lam), "logmu": 0.0, "logs2": log(N), "logtA": log(tA), "logq": log(4 * lam), "kappa": lam * N}

# ---------------- P: premise test (switching vs Gaussian), parametric bootstrap B=39
P_CONDS = [("tel", 1.5, 0.002, 8192), ("tel", 3.0, 0.002, 8192), ("tel", 3.0, 0.01, 8192), ("tel", 3.0, 0.002, 2048),
           ("ou", 1.5, 0.002, 8192), ("ou", 3.0, 0.002, 8192), ("ou", 3.0, 0.01, 8192), ("ou", 3.0, 0.002, 2048)]
def P_job(args):
    ci, r = args
    kind, s, lam, n = P_CONDS[ci]; rng = rng_for(300 + ci, r)
    if kind == "tel":
        x = aqn.telegraph(n, lam, 1.0, rng)
    else:
        x = aqn.ou_mixture(n, [2 * lam], [1.0], rng)  # same autocovariance e^{-2 lam |tau|}, variance mu^2 = 1
    y = x + rng.standard_normal(n) * s
    lr, p, h, o = aqn.premise_test(y, 39, rng)
    return {"ci": ci, "LR": lr, "p": p}

# ---------------- E: event worlds
E_CONDS = [("cox", 0.5, 8192), ("cox", 5.0, 8192), ("cox", 5.0, 32768), ("mmpp", 0.002, 8192), ("mmpp", 0.01, 8192),
           ("mmpp", 0.002, 32768), ("renewal", 1.5, 8192), ("renewal", 1.5, 32768)]
COX_SD = 0.3
def E_job(args):
    ci, r = args
    kind, par, n = E_CONDS[ci]; rng = rng_for(400 + ci, r); band = (2e-3, pi)
    if kind == "cox":
        z = aqn.ou_mixture(n, MIX_CORNERS, MIX_W * COX_SD ** 2, rng)
        times, c = aqn.cox_times(par * (1 + z), rng)
        f1 = aqn.whittle_counts(c, band); f0 = aqn.whittle_counts(c, band, fix_s2=c.mean())
        go = aqn.gap_order_stat(times, rng, 100)
        return {"ci": ci, "alpha": f1["alpha"], "se_alpha": f1["se_alpha"], "logq": f1["logq"], "se_logq": f1["se_logq"],
                "fano_floor": float(np.exp(f1["logs2"]) / c.mean()), "alpha_fix": f0["alpha"], "se_alpha_fix": f0["se_alpha"],
                "logq_fix": f0["logq"], "se_logq_fix": f0["se_logq"], "gap_r": go[0], "gap_z": go[1], "mean": float(c.mean())}
    if kind == "mmpp":
        lam = par; s = aqn.telegraph(n, lam, 1.0, rng)
        c = rng.poisson(np.where(s > 0, 3.0, 1.0))
        m = aqn.mmpp_fit(c)
        return {"ci": ci, "loglam": log(m["lam"]), "se_loglam": m["se_loglam"], "r0": m["r0"], "r1": m["r1"], "mu": m["mu"]}
    times = aqn.lomax_renewal_times(n, 1.0, par, rng)
    c = np.bincount(times.astype(int), minlength=n)[:n]
    f1 = aqn.whittle_counts(c, band); go = aqn.gap_order_stat(times, rng, 100)
    return {"ci": ci, "alpha": f1["alpha"], "fano_floor": float(np.exp(f1["logs2"]) / c.mean()), "gap_r": go[0], "gap_z": go[1],
            "at_bound": f1["at_bound"]}
def E_truth():
    out = {}
    for ci, (kind, par, n) in enumerate(E_CONDS):
        if kind == "cox":
            ft = lambda w, par=par: par ** 2 * aqn.ou_mixture_spec(w, MIX_CORNERS, MIX_W * COX_SD ** 2) + par / (2 * pi)  # density (var = int f)
            out[ci] = list(aqn.pseudo_true_counts(ft, n, (2e-3, pi)))
    return out

# ---------------- S: stakes
S_CONDS = [(n, ru, endo) for n in (100, 1000) for ru in (0.0, 0.5, 1.0) for endo in (False,)] + [(1000, 0.0, True), (1000, 0.5, True)]
def S_job(args):
    ci, r = args
    n, ru, endo = S_CONDS[ci]; rng = rng_for(500 + ci, r); w = 2.0
    if not endo:
        e = rng.standard_normal(n); wi = np.full(n, w)
    else:
        wi = w * np.exp(rng.normal(0, 0.7, n)); wi *= w / wi.mean()
        e = rng.standard_normal(n) * wi ** -0.5   # high-stakes units track better (self-selected error)
    cost = 0.5 + wi * e ** 2 + rng.standard_normal(n) * 0.5
    em = e + rng.standard_normal(n) * ru * np.std(e); er = e + rng.standard_normal(n) * ru * np.std(e)
    f = aqn.stakes_fit(em, cost, er if ru > 0 else None, B=300, rng=rng)
    f["ci"] = ci; f["w_true_mean"] = float(wi.mean())
    return {k: (float(v) if isinstance(v, (np.floating, float)) else v) for k, v in f.items()}

BLOCKS = {"A": (A_conds, A_job, lambda ci: 200 if A_conds()[ci][2] < 32768 else 100),
          "B": (B_conds, B_job, lambda ci: 100),
          "C": (C_conds, C_job, lambda ci: 100 if C_conds()[ci][2] < 32768 else 50),
          "P": (lambda: P_CONDS, P_job, lambda ci: 40),
          "E": (lambda: E_CONDS, E_job, lambda ci: 100 if E_CONDS[ci][2] < 32768 else 50),
          "S": (lambda: S_CONDS, S_job, lambda ci: 300)}

def conv(o):
    if isinstance(o, (np.floating,)): return float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.bool_,)): return bool(o)
    raise TypeError(type(o))

if __name__ == "__main__":
    blk = sys.argv[1]; nproc = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    conds, job, reps = BLOCKS[blk]
    jobs = [(ci, r) for ci in range(len(conds())) for r in range(reps(ci))]
    jobs.sort(key=lambda j: -j[0])
    with Pool(nproc) as p:
        res = p.map(job, jobs, chunksize=2)
    truth = {"B": B_truth, "E": E_truth}.get(blk, lambda: {})()
    json.dump({"block": blk, "conds": [list(c) for c in conds()], "truth": truth, "results": res},
              open(f"results/{blk}.json", "w"), default=conv)
    print(blk, "done", len(res))
