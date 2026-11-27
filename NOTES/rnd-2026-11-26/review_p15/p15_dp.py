"""Check 2: brute counterexample search for P15's claim
   min_policy [sum_t loss + lam*sum_t g(d_t)] (disk) <= same (regular n-gon, all effects),
for angle-only losses, several monotone step costs g, deterministic and Markov worlds.
Polygon distances by LP (p15_core); disk on a grid of M angles containing every tested
polygon's vertices (so the disk value used is an UPPER bound on the true disk value).
Also reports exact ties (strictness)."""
import numpy as np
from p15_core import reg_poly, op_dist_lp
rng = np.random.default_rng(1515)
NS = [3, 4, 5, 6, 8, 9, 10, 12]
def poly_D(n):
    V, a = reg_poly(n)
    row = np.array([0.0] + [op_dist_lp(V, V[0], V[k]) for k in range(1, n)])
    idx = (np.arange(n)[None, :] - np.arange(n)[:, None]) % n
    return row[idx], a
PD = {n: poly_D(n) for n in NS}
def disk_D(M):
    a = 2*np.pi*np.arange(M)/M
    dif = a[None, :] - a[:, None]
    return np.abs(np.sin(dif/2)), a
gfun = {"d^2": lambda d: d**2, "d": lambda d: d, "sqrt d": np.sqrt, "d^4": lambda d: d**4, "zero": lambda d: 0*d}
def rand_loss():
    kind = rng.integers(0, 6)
    if kind == 0:   # random Fourier, rotation-invariant f(phi-theta)
        K = rng.integers(1, 6); c = rng.normal(size=K); s = rng.normal(size=K); ph = rng.uniform(0, 2*np.pi)
        return "fourier", lambda x: sum(c[k]*np.cos((k+1)*x) + s[k]*np.sin((k+1)*x) for k in range(K))
    if kind == 1:
        return "wrapped sq", lambda x: np.angle(np.exp(1j*x))**2
    if kind == 2:
        return "abs", lambda x: np.abs(np.angle(np.exp(1j*x)))
    if kind == 3:
        dl = rng.uniform(0.05, 1.5); return "miss>%.2f" % dl, lambda x: (np.abs(np.angle(np.exp(1j*x))) > dl).astype(float)
    if kind == 4:
        tb = rng.normal(size=64); return "random step", lambda x: tb[(np.mod(x, 2*np.pi)/(2*np.pi)*64).astype(int) % 64]
    tgt = rng.uniform(0, 2*np.pi); kap = rng.uniform(1, 5)   # negative-valued loss (a reward bump)
    return "neg bump", lambda x: -np.exp(np.cos(x - tgt)*kap)
def solve_det(D, ang, theta, f, lam, g):
    G = lam*g(D); V = np.zeros(len(ang))
    for t in range(len(theta)-1, -1, -1):
        V = np.min(G + (f(ang - theta[t]) + V)[None, :], axis=1)
    return V[0]                      # start at angle 0 (v0)
def solve_markov(D, ang, wang, P, f, lam, g, T, w0):
    G = lam*g(D); K = len(wang); V = np.zeros((len(ang), K))
    for t in range(T):
        Q = np.stack([np.min(G + (f(ang - wang[w]) + V[:, w])[None, :], axis=1) for w in range(K)], 1)
        V = Q @ P.T                  # V(r,w_prev) = sum_w' P[w_prev,w'] Q(r,w')
    return V[0, w0]
viol = 0; ties = 0; tot = 0; worst = 9; tie_kinds = {}
Dd, ad = disk_D(720)
for trial in range(3000):
    name, f = rand_loss(); gname = rng.choice(list(gfun)); lam = float(rng.choice([0.1, 1, 10]))
    T = int(rng.integers(1, 9))
    theta = np.cumsum(rng.normal(0, rng.uniform(0.05, 1.5), T)) + rng.uniform(0, 2*np.pi)
    if rng.random() < 0.3: theta = np.where(rng.random(T) < .5, 0.0, np.pi) # world on 0/pi (antipode-like)
    vd = solve_det(Dd, ad, theta, f, lam, gfun[gname])
    for n in NS:
        D, a = PD[n]; vp = solve_det(D, a, theta, f, lam, gfun[gname]); tot += 1
        worst = min(worst, vp - vd)
        if vp < vd - 1e-9:
            viol += 1; print("VIOLATION", name, gname, lam, n, vp, vd)
        elif abs(vp - vd) < 1e-9:
            ties += 1; k = ("odd" if n % 2 else "even", name.split()[0].split(">")[0]); tie_kinds[k] = tie_kinds.get(k, 0) + 1
print("DETERMINISTIC world: %d comparisons, violations(poly<disk) %d, exact ties %d, min(poly-disk) %.3e" % (tot, viol, ties, worst))
print("ties by (n odd?, loss kind):", dict(sorted(tie_kinds.items())))
# Markov world
Dd, ad = disk_D(360); K = 24; wang = 2*np.pi*np.arange(K)/K
viol = ties = tot = 0; worst = 9
for trial in range(150):
    name, f = rand_loss(); gname = rng.choice(list(gfun)); lam = float(rng.choice([0.1, 1, 10]))
    P = rng.dirichlet(np.full(K, 0.3), K); T = int(rng.integers(1, 6)); w0 = int(rng.integers(K))
    vd = solve_markov(Dd, ad, wang, P, f, lam, gfun[gname], T, w0)
    for n in NS:
        D, a = PD[n]; vp = solve_markov(D, a, wang, P, f, lam, gfun[gname], T, w0); tot += 1
        worst = min(worst, vp - vd)
        viol += vp < vd - 1e-9; ties += abs(vp - vd) < 1e-9
print("MARKOV world (adapted policies): %d comparisons, violations %d, exact ties %d, min(poly-disk) %.3e" % (tot, viol, ties, worst))
# a forced tie with motion: even n, world jumping 0 <-> pi, wrapped-sq loss, quadratic cost
f = lambda x: 5*np.angle(np.exp(1j*x))**2
theta = np.array([np.pi, 0, np.pi, 0.0])
Dd, ad = disk_D(720)
print("tie example (world alternates 0/pi, loss 5*err^2, cost d^2): disk %.6f, square %.6f, hexagon %.6f, pentagon %.6f" % (
    solve_det(Dd, ad, theta, f, 1, gfun["d^2"]), *(solve_det(*PD[n], theta, f, 1, gfun["d^2"]) for n in (4, 6, 5))))
