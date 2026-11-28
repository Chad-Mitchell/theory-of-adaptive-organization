"""Q4: independent re-implementation of the locked design (prereg 93a6ca4 text, not its code): MSE-payoff-selected learners
from the F(pp, g) grid + 25 linear members, E = 20 expected switches of experience, t_A on a fresh 200-switch record; R = 24
per arm, NEW seeds; locked rule applied. Own code; nice 19."""
import numpy as np, numba as nb, math, json
from gridengine import kalman_pole
N = 1.0; D = 0.01

@nb.njit(cache=True)
def experience_mse(lam, mu, PP, G, LIN, nsamp, seed):
    np.random.seed(seed)
    C = PP.shape[0]; p = (1 - math.exp(-2 * lam * D)) / 2; s = math.sqrt(N / D)
    L = np.zeros(C); shx = np.zeros(C); shh = np.zeros(C)
    x = 1.0 if np.random.random() < 0.5 else -1.0
    burn = int(3.0 / (lam * D))
    for k in range(burn + nsamp):
        if np.random.random() < p: x = -x
        y = x * mu + s * np.random.standard_normal()
        for c in range(C):
            if LIN[c]:
                L[c] = (1 - 2 * PP[c]) * L[c] + G[c] * y; h = L[c]
            else:
                l = min(max(L[c], -50.0), 50.0); e = math.exp(l)
                L[c] = math.log(((1 - PP[c]) * e + PP[c]) / (PP[c] * e + 1 - PP[c])) + G[c] * y
                h = math.tanh(0.5 * L[c])
            if k >= burn:
                shx[c] += h * x * mu; shh[c] += h * h
    return mu * mu - shx * shx / np.maximum(shh, 1e-300) / nsamp

@nb.njit(cache=True)
def test_tA(lam, mu, pp, g, lin, nsamp, seed):
    np.random.seed(seed)
    p = (1 - math.exp(-2 * lam * D)) / 2; s = math.sqrt(N / D)
    L = 0.0; x = 1.0; burn = int(3.0 / (lam * D))
    tot = 0.0; n = 0; waiting = False; cnt = 0
    for k in range(burn + nsamp):
        if np.random.random() < p:
            x = -x
            if k >= burn: waiting = True; cnt = 0
        y = x * mu + s * np.random.standard_normal()
        if lin: L = (1 - 2 * pp) * L + g * y
        else:
            l = min(max(L, -50.0), 50.0); e = math.exp(l)
            L = math.log(((1 - pp) * e + pp) / (pp * e + 1 - pp)) + g * y
        if waiting:
            cnt += 1
            if L * x > 0: tot += cnt; n += 1; waiting = False
    return D * tot / n

def family(lam, mu):
    p = (1 - math.exp(-2 * lam * D)) / 2; gB = 2 * mu * D / N; pole, _ = kalman_pole(lam, mu, N, D)
    PP, G, LIN = [], [], []
    for a in np.exp(np.linspace(math.log(1 / 8), math.log(8), 13)):
        for b in np.exp(np.linspace(math.log(1 / 16), math.log(4), 13)):
            PP.append(p * a); G.append(gB * b); LIN.append(False)
    for t in np.exp(np.linspace(math.log(1 / 8), math.log(8), 25)):
        PP.append((1 - pole) * t / 2); G.append(1.0); LIN.append(True)
    return np.array(PP), np.array(G), np.array(LIN)

arms = {"A": (0.01, 2.0, 51000), "B": (0.02, math.sqrt(2.0), 52000)}
res = {}
for k, (lam, mu, s0) in arms.items():
    PP, G, LIN = family(lam, mu); rows = []
    for i in range(24):
        m = experience_mse(lam, mu, PP, G, LIN, int(20 / (lam * D)), s0 + i)
        j = int(np.argmin(m))
        rows.append(dict(j=j, lin=bool(LIN[j]), tA=test_tA(lam, mu, PP[j], G[j], LIN[j], int(200 / (lam * D)), 9_000_000 + s0 + i)))
    res[k] = rows
lt = {k: np.log([r["tA"] for r in v]) for k, v in res.items()}
Dh = float(lt["B"].mean() - lt["A"].mean()); sig = float(math.sqrt(lt["A"].var(ddof=1) / 24 + lt["B"].var(ddof=1) / 24))
z = 1.959964; pred = 0.3504
fail = Dh + z * sig < 0.5 * pred; pas = Dh - z * sig > 0 and not fail
out = dict(D=Dh, sigma=sig, verdict="FAILED" if fail else ("PASSED" if pas else "INCONCLUSIVE"),
           frac_lin={k: float(np.mean([r["lin"] for r in v])) for k, v in res.items()},
           sd_log={k: float(lt[k].std(ddof=1)) for k in lt}, mean_tA={k: float(np.exp(lt[k].mean())) for k in lt}, rows=res)
print(json.dumps({k: v for k, v in out.items() if k != "rows"}, indent=1))
json.dump(out, open("q4_learner.json", "w"), indent=1, default=float)
