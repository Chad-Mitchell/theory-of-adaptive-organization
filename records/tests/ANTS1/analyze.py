"""ANTS1 analysis: implements the PREREG estimators and scores P1-P8, C0, C1. Usage: python3 analyze.py results.pkl"""
import pickle, sys, json, numpy as np
from scipy.stats import spearmanr
from world import SIGMA_D, SIGMA_OBS, LAMBDA, WORLDS
from meanfield import kstar
EG = np.exp(np.linspace(np.log(3e-4), np.log(1.0), 19)); EG[-1] = 1.0
LE = np.log(EG)
NS = [1, 2, 4, 8, 16, 32, 64, 128, 256]
R = pickle.load(open(sys.argv[1] if len(sys.argv) > 1 else "results.pkl", "rb"))
NB = 1000
rng = np.random.default_rng(12345)
MF = json.load(open("meanfield_pred.json"))

cells = {}
for (a, w, dr, si, N, s), v in R.items():
    cells.setdefault((a, w, dr, si, N), {})[s] = v
SEEDS = sorted({k[5] for k in R})
S = len(SEEDS)
BOOT = rng.integers(0, S, size=(NB, S))   # shared across N/arms -> paired by world seed


def arr(key):
    c = cells.get(key)
    if c is None or len(c) < S:
        return None
    return np.stack([c[s] for s in SEEDS])   # (S, 19, 4)


def estar(curve):
    i = int(np.argmin(curve))
    if i == 0 or i == len(curve) - 1:
        return float(EG[i]), True
    x, y = LE[i - 1:i + 2], curve[i - 1:i + 2]
    A = np.polyfit(x, y, 2)
    if A[0] <= 0:
        return float(EG[i]), False
    xm = -A[1] / (2 * A[0])
    return float(np.exp(np.clip(xm, x[0], x[2]))), False


def est_with_boot(a3, col):
    m = a3[:, :, col].mean(0)
    e, edge = estar(m)
    bs = np.array([estar(a3[b, :, col].mean(0))[0] for b in BOOT[:200]])
    return e, edge, bs, float(m.min())


def slope(N, y):
    return float(np.polyfit(np.log(N), np.log(y), 1)[0])


RES = {"cells": {}, "preds": {}}
def get(arm, w, dr, si, col):
    out = {}
    for N in NS:
        a3 = arr((arm, w, dr, si, N))
        if a3 is None:
            continue
        e, edge, bs, mn = est_with_boot(a3, col)
        bm = np.array([a3[b, :, col].mean(0).min() for b in BOOT[:200]])
        out[N] = dict(e=e, edge=edge, boot=bs, mse=mn, bmse=bm)
    return out

COLS = {"MEAN": 0, "MODE": 1}
cache = {}
for arm in ["IND", "FOL", "LOCK", "PRIV"]:
    for w in WORLDS:
        for dr in range(3):
            for si in range(2):
                for rd, col in COLS.items():
                    g = get(arm, w, dr, si, col)
                    if g:
                        cache[(arm, w, dr, si, rd)] = g
                        RES["cells"][f"{arm}|{w}|{dr}|{si}|{rd}"] = {N: dict(e=v["e"], edge=v["edge"], mse=v["mse"],
                            e_ci=[float(np.quantile(v["boot"], .025)), float(np.quantile(v["boot"], .975))]) for N, v in g.items()}

def K(dr, si, N):
    q, r = SIGMA_D[dr] ** 2, SIGMA_OBS[si] ** 2 + 1 / 12
    return float(kstar(N * q / r))

def exp_ci(g, Nset):
    Ns = np.array(Nset)
    pt = slope(Ns, [g[N]["e"] for N in Nset])
    bs = [slope(Ns, [g[N]["boot"][b] for N in Nset]) for b in range(200)]
    return pt, float(np.quantile(bs, .025)), float(np.quantile(bs, .975))

lines = []
def say(s):
    print(s); lines.append(s)

# C0
ok = tot = 0
for dr in range(3):
    for si in range(2):
        g = cache.get(("IND", "RW", dr, si, "MEAN"), {})
        for N, v in g.items():
            k = K(dr, si, N)
            if 1e-3 <= k <= 0.9:
                tot += 1; ok += (1 / 1.3 <= v["e"] / k <= 1.3)
say(f"C0 (code check) IND/RW/MEAN e* within x1.3 of K*: {ok}/{tot}")
# C1
for dr in range(3):
    for si in range(2):
        g = cache.get(("PRIV", "RW", dr, si, "MEAN"), {})
        if len(g) == 9:
            say(f"C1 PRIV RW d{dr} s{si} exponent {slope(NS, [g[N]['e'] for N in NS]):+.3f}")

# P1 + P3
p1 = []; p3 = []
for dr in range(3):
    for si in range(2):
        Nset = [N for N in NS if K(dr, si, N) <= 0.3]
        for rd in COLS:
            g = cache.get(("IND", "RW", dr, si, rd), {})
            if len(Nset) >= 3 and all(N in g for N in Nset):
                pt, lo, hi = exp_ci(g, Nset)
                ms = slope(Nset, [g[N]["mse"] for N in Nset])
                p1.append(0.3 <= pt <= 0.7); p3.append(-0.6 <= ms <= -0.4)
                say(f"P1/P3 RW drift={SIGMA_D[dr]} obs={SIGMA_OBS[si]} {rd}: N={Nset[0]}..{Nset[-1]} e*-exponent {pt:.3f} [{lo:.3f},{hi:.3f}]  MSE*-slope {ms:.3f}")
say(f"P1: {sum(p1)}/{len(p1)} in [0.3,0.7] (need >=10/12)   P3: {sum(p3)}/{len(p3)} MSE slopes in [-0.6,-0.4]")

# P2
for rd in COLS:
    g = cache.get(("IND", "RW", 2, 0, rd), {})
    Nset = [N for N in NS if K(2, 0, N) >= 0.5]
    if all(N in g for N in Nset):
        pt, lo, hi = exp_ci(g, Nset)
        say(f"P2 RW drift=1.0 obs=4 {rd}: large-gain N={Nset} exponent {pt:.3f} [{lo:.3f},{hi:.3f}] (pred <0.3)")
loc, kk = [], []
for dr in range(3):
    for si in range(2):
        for rd in COLS:
            g = cache.get(("IND", "RW", dr, si, rd), {})
            for a, b in zip(NS[:-1], NS[1:]):
                if a in g and b in g and not g[b]["edge"]:
                    loc.append(np.log(g[b]["e"] / g[a]["e"]) / np.log(2)); kk.append(K(dr, si, (a * b) ** 0.5))
if loc:
    rho, p = spearmanr(kk, loc)
    say(f"P2 pooled: Spearman(local slope, K*) = {rho:.3f} (p={p:.2g}, n={len(loc)}) (pred <0)")
    kk = np.array(kk); loc = np.array(loc)
    for lo_, hi_ in [(0, .1), (.1, .3), (.3, .5), (.5, .7), (.7, .9), (.9, 1)]:
        s_ = (kk >= lo_) & (kk < hi_)
        if s_.sum():
            say(f"    K* in [{lo_},{hi_}): mean local slope {loc[s_].mean():.3f} (n={s_.sum()})")

# P4
r_ok = r_tot = m_ok = m_tot = 0
for dr in range(3):
    for si in range(2):
        gi = cache.get(("IND", "RW", dr, si, "MEAN"), {}); gf = cache.get(("FOL", "RW", dr, si, "MEAN"), {})
        for N in NS:
            if N in gi and N in gf:
                m_tot += 1; m_ok += gf[N]["mse"] >= 2 * gi[N]["mse"]
                if K(dr, si, N) <= 0.3:
                    r_tot += 1; r_ok += 0.7 <= gf[N]["e"] / gi[N]["e"] <= 1.5
        if gi and gf and len(gf) == 9:
            say(f"P4 RW d={SIGMA_D[dr]} o={SIGMA_OBS[si]}: FOL/IND e* ratio " + " ".join(f"{gf[N]['e']/gi[N]['e']:.2f}" for N in NS)
                + " | MSE ratio " + " ".join(f"{gf[N]['mse']/gi[N]['mse']:.1f}" for N in NS))
say(f"P4(a) FOL/IND e* ratio in [0.7,1.5]: {r_ok}/{r_tot} (need >=80%)   P4(b) FOL MSE >= 2x IND: {m_ok}/{m_tot} (need >=90%)")

# P5
a_ok = b_ok = n6 = 0
for dr in range(3):
    for si in range(2):
        gl = cache.get(("LOCK", "RW", dr, si, "MEAN"), {}); gi = cache.get(("IND", "RW", dr, si, "MEAN"), {})
        Nset = [N for N in NS if K(dr, si, N) <= 0.3]
        if len(gl) == 9 and len(gi) == 9:
            n6 += 1
            pt = slope(Nset, [gl[N]["e"] for N in Nset]) if len(Nset) >= 2 else float("nan")
            a_ok += pt > 0.55
            best = min(gl[N]["mse"] for N in NS)
            b_ok += (gl[256]["mse"] > best) and (gl[256]["mse"] > 2 * gi[256]["mse"])
            say(f"P5 RW d={SIGMA_D[dr]} o={SIGMA_OBS[si]}: LOCK e*-exp {pt:.3f}; LOCK e* " + " ".join(f"{gl[N]['e']:.3g}" for N in NS)
                + " | LOCK MSE* " + " ".join(f"{gl[N]['mse']:.3g}" for N in NS) + f" | IND MSE*(256) {gi[256]['mse']:.3g}")
say(f"P5(a) {a_ok}/{n6} (need >=4/6)  P5(b) {b_ok}/{n6} (need >=5/6)")
c_ok = c_tot = 0
for w in ["POIS", "HEAVY"]:
    for dr in range(3):
        for si in range(2):
            for rd in COLS:
                gl = cache.get(("LOCK", w, dr, si, rd), {}); gi = cache.get(("IND", w, dr, si, rd), {})
                for N in [32, 64, 128, 256]:
                    if N in gl and N in gi:
                        c_tot += 1; c_ok += gl[N]["mse"] > 2 * gi[N]["mse"]
say(f"P5(c) jump worlds N>=32 LOCK MSE > 2x IND: {c_ok}/{c_tot} (need >=80%)")

# P6
i_ok = i_tot = 0
for w in WORLDS:
    for dr in range(3):
        for si in range(2):
            for rd in COLS:
                g = cache.get(("IND", w, dr, si, rd), {})
                for N in [1, 2, 4, 8, 16]:
                    if N in g:
                        i_tot += 1; i_ok += not g[N]["edge"]
say(f"P6 interior optimum (IND, N<=16): {i_ok}/{i_tot} (need >=90%)")
# P7
d_ok = d_tot = 0
for w in WORLDS:
    for si in range(2):
        for rd in COLS:
            for N in NS:
                gs = [cache.get(("IND", w, dr, si, rd), {}).get(N) for dr in range(3)]
                if all(gs) and not any(x["edge"] for x in gs):
                    d_tot += 1; d_ok += gs[0]["e"] < gs[1]["e"] < gs[2]["e"]
say(f"P7 e* increases with drift (IND): {d_ok}/{d_tot} (need >=90%)")
# P8
j_ok = j_tot = 0
for w in ["POIS", "HEAVY"]:
    for dr in range(3):
        for si in range(2):
            for rd in COLS:
                g = cache.get(("IND", w, dr, si, rd), {})
                if len(g) == 9:
                    sig_down = 0
                    for a, b in zip(NS[:-1], NS[1:]):
                        diff = g[b]["boot"] - g[a]["boot"]
                        if g[b]["e"] < g[a]["e"] and np.quantile(diff, .975) < 0:
                            sig_down += 1
                    j_tot += 1; j_ok += sig_down <= 1
                    say(f"P8 {w} lam={LAMBDA[dr]} o={SIGMA_OBS[si]} {rd}: e* " + " ".join(f"{g[N]['e']:.3g}{'*' if g[N]['edge'] else ''}" for N in NS)
                        + f" | exp(all N) {slope(NS, [g[N]['e'] for N in NS]):.2f} | MSE* " + " ".join(f"{g[N]['mse']:.3g}" for N in NS))
say(f"P8 jump worlds e* non-decreasing in N: {j_ok}/{j_tot} (need >=80%)")
# exploratory: elasticity of e* to lambda
for w in ["POIS", "HEAVY"]:
    for si in range(2):
        for rd in COLS:
            el = []
            for N in NS:
                gs = [cache.get(("IND", w, dr, si, rd), {}).get(N) for dr in range(3)]
                if all(gs):
                    el.append(slope(np.array(LAMBDA), [x["e"] for x in gs]))
            if el:
                say(f"X  elasticity d ln e*/d ln lambda {w} o={SIGMA_OBS[si]} {rd}: " + " ".join(f"{x:.2f}" for x in el))
json.dump(RES, open("analysis.json", "w"), default=float)
open("analysis_output.txt", "w").write("\n".join(lines) + "\n")
