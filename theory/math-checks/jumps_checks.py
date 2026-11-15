"""Task 2 corrections: jumps and heavy tails. Fixed-delay fix (model A: full reset every tau).
Two-sided diffusion barrier |X|>=B plus downward compound-Poisson jumps.
Report the doubling elasticity eps_tau ~ ln(h(2tau)/h(tau))/ln 2 at fixed sigma, B, jump law.
Claim (principle of a single big jump): when failures come mainly from single jumps > B,
h -> lambda*P(J>B), independent of tau, so eps_tau -> 0."""
import numpy as np
rng = np.random.default_rng(7)

def mfpt(tau, sigma=1.0, B=1.0, lam=0.0, jump=None, npaths=6000, spt=300, tmax=4000.0):
    dt = tau/spt
    x = np.zeros(npaths); t = np.zeros(npaths); tw = np.zeros(npaths)
    alive = np.ones(npaths, bool); T = np.full(npaths, np.nan); cause = np.zeros(npaths, int)
    while alive.any() and t[alive].min() < tmax:
        idx = np.where(alive)[0]; x0 = x[idx]
        x1 = x0 + sigma*np.sqrt(dt)*rng.standard_normal(idx.size)
        pu = np.where((x0 < B) & (x1 < B), np.exp(-2*(B-x0)*(B-x1)/(sigma**2*dt)), 1.0)
        pl = np.where((x0 > -B) & (x1 > -B), np.exp(-2*(B+x0)*(B+x1)/(sigma**2*dt)), 1.0)
        hitd = (rng.random(idx.size) < pu) | (rng.random(idx.size) < pl)
        hitj = np.zeros(idx.size, bool)
        if lam > 0:
            nj = rng.random(idx.size) < lam*dt
            if nj.any():
                J = jump(nj.sum())
                x1[nj] -= J
                hitj[nj] = x1[nj] <= -B
        hit = hitd | hitj
        t[idx] += dt
        T[idx[hit]] = t[idx[hit]]; cause[idx[hit & hitj & ~hitd]] = 1
        alive[idx[hit]] = False; x[idx] = x1
        tw[idx] += dt
        rs = idx[tw[idx] >= tau - 1e-12]; x[rs] = 0.0; tw[rs] = 0.0
    done = ~np.isnan(T)
    return np.nanmean(T), cause[done].mean(), (~done).sum()

def pareto(alpha, xm):
    return lambda n: xm*(1 - rng.random(n))**(-1/alpha)
def expo(m):
    return lambda n: rng.exponential(m, n)
def sym_expo(m):
    # symmetric (+/-) small jumps: zero mean, adds variance lam*2m^2 per unit time
    return lambda n: rng.exponential(m, n)*rng.choice([-1.0, 1.0], n)

B, sigma = 1.0, 0.5   # z = B/(sigma sqrt(tau)) = 2 at tau=1, 1.41 at tau=2
cases = [
 ("diffusion only", 0.0, None),
 ("many small symmetric jumps (lam=50, |J|~exp mean .05)", 50.0, sym_expo(0.05)),
 ("Pareto a=1.5, xm=0.05, lam=0.5 (P(J>B)=0.011)", 0.5, pareto(1.5, 0.05)),
 ("Pareto a=1.5, xm=0.2, lam=0.5 (P(J>B)=0.089)", 0.5, pareto(1.5, 0.2)),
 ("Pareto a=1.1, xm=0.3, lam=0.5 (P(J>B)=0.266)", 0.5, pareto(1.1, 0.3)),
]
cases2 = [("Pareto a=1.5, xm=0.2, lam=0.5, sigma=0.3 (diffusion z=3.3)", 0.5, pareto(1.5, 0.2)),
          ("Pareto a=1.5, xm=0.2, lam=0.5, sigma=0.2 (diffusion z=5)", 0.5, pareto(1.5, 0.2))]
print("case | MFPT(tau=1) | MFPT(tau=2) | eps_tau(doubling) | share of failures by single jump (tau=1)")
for name, lam, J in cases:
    m1, c1, u1 = mfpt(1.0, sigma, B, lam, J)
    m2, c2, u2 = mfpt(2.0, sigma, B, lam, J)
    eps = np.log(m1/m2)/np.log(2)
    print(f"{name:48s} | {m1:8.2f} | {m2:8.2f} | {eps:6.2f} | {c1:.2f}  (unabsorbed {u1},{u2})")
for (name, lam, J), sg in zip(cases2, [0.3, 0.2]):
    m1, c1, u1 = mfpt(1.0, sg, B, lam, J)
    m2, c2, u2 = mfpt(2.0, sg, B, lam, J)
    eps = np.log(m1/m2)/np.log(2)
    print(f"{name:48s} | {m1:8.2f} | {m2:8.2f} | {eps:6.2f} | {c1:.2f}  (unabsorbed {u1},{u2})")
print("single-jump floor: 1/(lam P(J>B)) = 1/(0.5*0.0894) =", 1/(0.5*0.2**1.5))
print("Reference: pure diffusion model A doubling elasticity from F_A: ln(F_A(2)/F_A(1.414)*... ) computed in fpt_checks")
