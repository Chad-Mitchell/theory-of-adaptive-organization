"""Anti-locking spacing check (Chad t2065, 21 Nov 2026). Run: nice -n 19 python3 theory/spacing_checks/antilock.py

Part A (linear model, NUMERICAL): scale-free world tracked by K first-order stores (merged solver
theory/layers_checks/stores.py). Is the error, as a function of the rate ratio between two stores,
smooth, or does it have features at simple rationals? And what ratios does the optimum pick?

Part B (nonlinear coupling, NUMERICAL replication of KNOWN results): two layers whose clocks are weakly
coupled, modelled by the standard sine circle map theta' = theta + Omega - (Kc/2pi) sin(2 pi theta).
Omega = fractional part of the clocks' frequency ratio. For each Omega, find the largest coupling Kc at
which the pair is still unlocked (rotation number not a rational with denominator <= QMAX).
"""
import sys, os, math, json
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'layers_checks'))
from stores import mse_given_b, E_K, scalefree_world

out = {}
print("== Part A: linear stores in a scale-free world")
for alpha in [0.8, 1.2, 1.6]:
    a, v = scalefree_world(alpha, 1e4, per_decade=6)
    N = 1e-2
    res = {}
    for K in [2, 3, 4]:
        e, lb = E_K(a, v, N, K, starts=10)
        rates = np.exp(lb)
        ratios = rates[1:] / rates[:-1]
        res[K] = dict(E=e, ratios=[float(r) for r in ratios])
        print(f"alpha={alpha} K={K}: E_K={e:.5f} adjacent rate ratios={np.round(ratios,2)}")
    # Scan the ratio of 2 stores with the geometric mean held at its optimum: look for structure at rationals.
    e2, lb2 = E_K(a, v, N, 2, starts=10)
    gm = lb2.mean()
    rs = np.linspace(1.2, 60, 3000)
    es = np.array([mse_given_b(a, v, np.exp([gm - math.log(r)/2, gm + math.log(r)/2]), N)[0] for r in rs])
    d2 = np.abs(np.diff(es, 2))
    # roughness near simple rationals vs elsewhere
    simple = [3/2, 2, 5/2, 3, 4, 5, 6]
    near = np.zeros(len(rs)-2, bool)
    for s in simple:
        near |= np.abs(rs[1:-1] - s) < 0.02
    ratio_rough = d2[near].mean() / d2[~near & (rs[1:-1] < 7)].mean()
    print(f"   2-store scan: second-difference near simple rationals / elsewhere (r<7) = {ratio_rough:.3f} (1 = no feature)")
    out[f"A_alpha{alpha}"] = dict(res=res, rough=float(ratio_rough), r_opt=float(rs[np.argmin(es)]))

print("== Part B: circle-map locking robustness of a clock ratio")
QMAX = 12
def rotation(Om, Kc, n=3000, burn=500):
    th = 0.0
    for _ in range(burn):
        th = th + Om - Kc/(2*math.pi)*math.sin(2*math.pi*th)
    t0 = th
    for _ in range(n):
        th = th + Om - Kc/(2*math.pi)*math.sin(2*math.pi*th)
    return (th - t0) / n
def locked(Om, Kc):
    w = rotation(Om, Kc)
    for q in range(1, QMAX+1):
        p = round(w*q)
        if abs(w - p/q) < 2e-4:
            return True
    return False
def crit(Om):
    lo, hi = 0.0, 1.0
    if locked(Om, 1e-9): return 0.0
    for _ in range(14):
        mid = (lo+hi)/2
        if locked(Om, mid): hi = mid
        else: lo = mid
    return lo
res = {}
for Kc in [0.5, 0.8, 0.95]:
    Oms = np.linspace(0.0, 1.0, 4001)
    lk = np.array([locked(Om, Kc) for Om in Oms])
    idx = np.where(lk)[0]
    # distance from each unlocked Omega to the nearest locked Omega (robustness margin of the ratio)
    dist = np.array([np.min(np.abs(Oms[idx] - Om)) if not lk[j] else 0.0 for j, Om in enumerate(Oms)])
    j = int(dist.argmax())
    phi = (math.sqrt(5)-1)/2
    jg = int(np.argmin(np.abs(Oms - phi)))
    frac_locked = lk.mean()
    print(f"   Kc={Kc}: locked fraction (q<={QMAX}) {frac_locked:.3f}; widest unlocked gap centre Omega={Oms[j]:.4f} "
          f"(margin {dist[j]:.4f}); margin at golden 0.618: {dist[jg]:.4f}; rank of golden margin among grid: "
          f"{int((dist > dist[jg]).sum())} points larger")
    res[str(Kc)] = dict(frac_locked=float(frac_locked), best_Omega=float(Oms[j]), best_margin=float(dist[j]),
                        golden_margin=float(dist[jg]), n_larger=int((dist > dist[jg]).sum()))
out["B"] = res
json.dump(out, open(os.path.join(os.path.dirname(__file__), 'antilock.json'), 'w'), indent=1)
