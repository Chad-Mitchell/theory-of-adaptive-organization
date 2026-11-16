"""Reviewer's own exact grid engine (Q5): best one-pole linear tracker of the sampled two-state (telegraph) world
under three losses, and the Bayes tracker, at pick 35's points A and B. Imports nothing from the author or from the
pick-35 review; the world and the adaptation-time estimator follow the definitions written in
reviews/night2/CAUSAL_NULL_INVARIANCE_REVIEW.md (Method).
World: flip w.p. pf = (1-exp(-2 lam D))/2 each step; y = x mu + sqrt(N/D) eps.
One-pole family: z <- f z + (1-f) y, output c*z with c free (c > 0); f in (0,1). (Sign loss is scale-free.)
Bayes: z = posterior log-odds; prior step z -> logit((1-pf) s(z) + pf (1-s(z))), then + 2 mu y D/N.
Joint (x, z) chain on a cell grid (0 on a cell edge, cell-integrated Gaussian kernel, overflow to end cells),
stationary law by sparse solve. Losses: sign P(z x < 0); squared min_c E(cz - mu x)^2; absolute min_c E|cz - mu x|.
t_A: from the stationary law of z given the pre-switch state, D * E[n] where n >= 1 is the first step with
sign(z) = new state; passages overtaken by another switch are dropped (weight (1-pf)^(n-1)).
"""
import numpy as np, scipy.sparse as sps, scipy.sparse.linalg as spl, json, sys
from scipy.special import ndtr
from scipy.optimize import minimize_scalar
D, Nn = 0.01, 1.0
S = np.sqrt(Nn/D)
PTS = {'A': dict(lam=0.01, mu2=4.0), 'B': dict(lam=0.02, mu2=2.0)}
M = int(sys.argv[1]) if len(sys.argv) > 1 else 6   # cells per kernel sd

def kernel(centers, edges, means, sd):
    n = len(centers); rows, cols, vals = [], [], []
    h = edges[1]-edges[0]; w = int(np.ceil(9*sd/h)) + 2
    for i in range(n):
        m = means[i]; j0 = int(np.floor((m - edges[0])/h))
        lo, hi = max(j0-w, 0), min(j0+w+1, n)
        cdf = ndtr((edges[lo:hi+1]-m)/sd)
        pr = np.diff(cdf)
        pr[0] += cdf[0]; pr[-1] += 1-cdf[-1]   # overflow to the nearest kept cell (negligible: window is 9 sd)
        rows += [i]*(hi-lo); cols += list(range(lo, hi)); vals += list(pr)
    return sps.csr_matrix((vals, (rows, cols)), shape=(n, n))

def build(meanfun, sd, zmax, pf):
    h = sd/M; nh = int(np.ceil(zmax/h)); edges = h*np.arange(-nh, nh+1); c = 0.5*(edges[1:]+edges[:-1])
    Kp = kernel(c, edges, meanfun(c, +1), sd); Km = kernel(c, edges, meanfun(c, -1), sd)
    P = sps.bmat([[(1-pf)*Kp, pf*Km], [pf*Kp, (1-pf)*Km]]).tocsr()
    n2 = P.shape[0]
    A = (P.T - sps.identity(n2)).tolil(); A[0, :] = np.ones(n2); b = np.zeros(n2); b[0] = 1
    pi = spl.spsolve(A.tocsc(), b); pi = np.maximum(pi, 0); pi /= pi.sum()
    n = len(c); return c, pi[:n], pi[n:], Km

def tA(c, pip, Km, pf):
    s = 1-pf; v0 = pip/pip.sum()
    pos = c > 0; neg = ~pos
    w1 = Km.T @ v0; a1 = w1[neg].sum(); g1 = w1[pos]
    Q = Km[pos][:, pos]; r = np.asarray(Km[pos][:, neg].sum(axis=1)).ravel()
    I = sps.identity(Q.shape[0], format='csc'); Aop = (I - s*Q).tocsc()
    lu = spl.splu(Aop)
    x1 = lu.solve(r); x2 = lu.solve(x1)
    S0 = a1 + s*(g1 @ x1); S1 = a1 + s*(g1 @ x2 + g1 @ x1)
    return D*S1/S0

def onepole(pt, f):
    lam, mu2 = PTS[pt]['lam'], PTS[pt]['mu2']; mu = np.sqrt(mu2); pf = (1-np.exp(-2*lam*D))/2
    g = 1-f; sd = g*S
    zsd = np.sqrt(g*S**2/(2-g) + mu2)
    c, pp, pm, Km = build(lambda z, x: f*z + g*mu*x, sd, mu + 9*np.sqrt(g*S**2/(2-g)), pf)
    E_zx = mu*(c@pp - c@pm)/mu  # E[z * sign x]
    Ez2 = (c**2)@(pp+pm)
    err = pp[c < 0].sum() + pm[c > 0].sum()
    mse = mu2 - mu2*E_zx**2/Ez2
    absl = lambda k: (np.abs(k*c - mu)@pp + np.abs(k*c + mu)@pm)
    ra = minimize_scalar(absl, bounds=(0.05, 5), method='bounded', options=dict(xatol=1e-9))
    return dict(err=err, mse=mse, abs=ra.fun, abs_scale=ra.x, mse_scale=mu*E_zx/Ez2, tA=tA(c, pp, Km, pf))

def bayes(pt):
    lam, mu2 = PTS[pt]['lam'], PTS[pt]['mu2']; mu = np.sqrt(mu2); pf = (1-np.exp(-2*lam*D))/2
    sd = 2*mu*np.sqrt(D/Nn)  # sd of 2 mu y D/N
    def mf(z, x):
        sg = 1/(1+np.exp(-z)); pr = (1-pf)*sg + pf*(1-sg)
        return np.log(pr) - np.log1p(-pr) + 2*mu2*x*D/Nn
    zmax = np.log((1-pf)/pf) + 12*sd + 2*mu2*D/Nn*5
    c, pp, pm, Km = build(mf, sd, zmax, pf)
    err = pp[c < 0].sum() + pm[c > 0].sum()
    return dict(err=err, tA=tA(c, pp, Km, pf))

def kalman_pole(pt):
    lam, mu2 = PTS[pt]['lam'], PTS[pt]['mu2']; phi = np.exp(-2*lam*D); Q = mu2*(1-phi**2); R = S**2
    P = mu2
    for _ in range(200000):
        Pm = phi**2*P + Q; K = Pm/(Pm+R); Pn = (1-K)*Pm
        if abs(Pn-P) < 1e-15: break
        P = Pn
    return (1-K)*phi

if __name__ == '__main__':
    out = {'M': M}
    for pt in ('A', 'B'):
        fk = kalman_pole(pt); rk = -np.log(fk)/D
        res = {'kalman_rate': rk}
        b = bayes(pt); res['bayes'] = b
        print(pt, 'Bayes', b, 'Kalman rate', rk, flush=True)
        # scan in ln(rate/rk)
        xs = np.linspace(np.log(0.15), np.log(5.0), 61)
        scan = []
        for xx in xs:
            f = np.exp(-rk*np.exp(xx)*D); o = onepole(pt, f); o['lnrel'] = xx; scan.append(o)
        res['scan'] = scan
        for loss in ('err', 'mse', 'abs'):
            arr = np.array([s[loss] for s in scan]); i = int(np.argmin(arr))
            fn = lambda xx: onepole(pt, np.exp(-rk*np.exp(xx)*D))[loss]
            r = minimize_scalar(fn, bounds=(xs[max(i-2, 0)], xs[min(i+2, len(xs)-1)]), method='bounded', options=dict(xatol=1e-5))
            ob = onepole(pt, np.exp(-rk*np.exp(r.x)*D))
            res['best_'+loss] = dict(lnrel=r.x, rel=float(np.exp(r.x)), **ob)
            print(pt, loss, 'best pole x Kalman', np.exp(r.x), ob, flush=True)
        ok = onepole(pt, fk); res['kalman_onepole'] = ok
        print(pt, 'Kalman pole', ok, flush=True)
        out[pt] = res
    for loss in ('err', 'mse', 'abs'):
        d = np.log(out['B']['best_'+loss]['tA']) - np.log(out['A']['best_'+loss]['tA'])
        out['dln_'+loss] = d
    out['dln_bayes'] = np.log(out['B']['bayes']['tA']) - np.log(out['A']['bayes']['tA'])
    out['dln_kalman'] = np.log(out['B']['kalman_onepole']['tA']) - np.log(out['A']['kalman_onepole']['tA'])
    for k in ('dln_err', 'dln_mse', 'dln_abs', 'dln_bayes', 'dln_kalman'):
        print(k, round(out[k], 4), 'share of Bayes', round(out[k]/out['dln_bayes'], 3))
    json.dump(out, open(f'r4_telegraph_grid_M{M}.json', 'w'), indent=1, default=float)
