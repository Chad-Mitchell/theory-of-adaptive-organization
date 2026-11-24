"""Step 2 check (class CK-I): looks priced by the information they bring in.

Class CK-I. Perfectly regular world phase (rate om, known). Looks arrive as a Poisson stream at rate f, so the
memory cannot predict when. Each look returns the phase plus Gaussian noise of variance r. Reset readout: the
memory adopts the read plus a constant offset. Between looks it advances on a clock (rate w', diffusion D) whose
heat is kap*kT*w'^2/D (TUR, kap >= 1). Each look costs lam*kT*I with lam >= 1 (Sagawa-Ueda: measurement plus
erasure costs at least kT times the information), I = I(theta; Y | memory state).
  Pre-look error = old read noise (var r) + E, E = (delta/f) W + sqrt(2D/f) sqrt(W) Z, W ~ Exp(1), delta = om - w'.
  E is asymmetric Laplace. Exact: I = h(E + G(2r)) - (1/2) ln(2 pi e r). High-SNR limit: I = h(E) - (1/2) ln(2 pi e r).
  Time-averaged loss (age at a random time ~ Exp(f), optimal constant offset): r + delta^2/f^2 + 2D/f.
Claims checked (labels as in theory/CLOCK_TERM_2026-11-23.md section 9):
 (i)   h(E) = 1 + (1/2) ln(mu^2 + 2 sigma^2), mu = delta/f, sigma^2 = 2D/f (closed form vs grid quadrature);
 (ii)  marginal information prices at the no-clock point: b = a/2 exactly with the exact finite-noise
       information, a = mu dI/dmu, b = mu^2 dI/dsigma^2 (to first order a small clock moves the forward scale
       by sigma^2/(2 mu) and adds a backward exponential whose first-order effect is a shift), versus
       a = b = 1 in the naive high-SNR closed form;
 (iii) exact local onset: the no-clock design first loses to a small clock when its look carries
       I0 = 4 kap/lam nats, the same for every read precision r (scale symmetry), several (kap, lam);
 (iv)  global: multistart minimum over (f, w', D) with the exact information at 0.98 and 1.02 x 4 kap/lam;
 (v)   continuity: the clock fraction w'/om rises from 0 above onset;
 (vi)  fixed-price control: Poisson looks with a fixed price c give onset 4 kap kT (= 2Kb/a, a = 1, b = 2);
 (vii) the naive high-SNR closed form would put the onset at (2kap/lam)(1 + sqrt(1 + lam/kap)) = 4.83 nats
       (kap = lam = 1): the two limits (clock -> 0, noise -> 0) do not commute, and (iii) is the right one;
 (viii) scope: at onset a filtering no-clock memory (Kalman, Gaussian-accounted, which overstates the
       information) that also counts looks does not undercut the reset design; the many-weak-looks limit
       costs far more there. Not a bound on what every filtering memory can do.
Run with --quick for the cheap subset that tools/test_clock_term_checks.py reruns.
"""
import warnings
import numpy as np
from scipy.optimize import minimize, minimize_scalar, brentq
from scipy.special import log_ndtr
warnings.filterwarnings("ignore")
kT = 1.0; om = 1.0
LN2PIE = np.log(2*np.pi*np.e)

def s_pm(mu, sig2):
    R = np.sqrt(mu*mu + 2*sig2); sp = (R+mu)/2
    return sp, sig2/(2*sp)  # s+ s- = sig2/2 (stable when sig2 << mu^2)

def _log_tail(a, x, v, s):
    """a*x + a^2 v/2 + log Phi(-(x + a v)/s), stable for large a."""
    z = (x + a*v)/s
    out = np.empty_like(x)
    big = z > 20
    zb = z[big]
    out[big] = -x[big]**2/(2*v) - np.log(zb*np.sqrt(2*np.pi)) + np.log1p(-1/zb**2 + 3/zb**4)
    xs = x[~big]
    out[~big] = a*xs + a*a*v/2 + log_ndtr(-z[~big])
    return out

def h_AL(mu, sig2): return 1 + 0.5*np.log(mu*mu + 2*sig2)

def logpdf_ALG(x, mu, sig2, v):
    sp, sm = s_pm(mu, sig2); s = np.sqrt(v); ap = 1/sp
    if sm > 1e-300:
        am = 1/sm; lA = np.log(ap*am/(ap+am))
        t1 = lA + _log_tail(ap, -x, v, s)
        t2 = lA + _log_tail(am, x, v, s)
        return np.logaddexp(t1, t2)
    return np.log(ap) + _log_tail(ap, -x, v, s)

def h_ALG(mu, sig2, v, n=4001):
    if mu*mu + 2*sig2 < 1e-10*v:  # drift part negligible: Gaussian only
        return 0.5*np.log(2*np.pi*np.e*v)
    sp, sm = s_pm(mu, sig2); s = np.sqrt(v)
    u = np.linspace(np.arcsinh(-(45*sm + 14*s)/s), np.arcsinh((45*sp + 14*s)/s), n)
    x = s*np.sinh(u)  # dense near the kink at 0, wide tails
    lp = logpdf_ALG(x, mu, sig2, v); p = np.exp(lp)
    val = -np.trapezoid(np.where(p > 0, p*lp, 0.0), x)
    return val if np.isfinite(val) else np.inf

def info(f, wp, D, r, exact):
    mu = (om - wp)/f; sig2 = 2*D/f
    if exact: return h_ALG(mu, sig2, 2*r) - 0.5*(LN2PIE + np.log(r))
    return h_AL(mu, sig2) - 0.5*(LN2PIE + np.log(r))

def J(f, wp, D, kap, lam, w, r, exact):
    d = om - wp
    heat = kap*kT*wp*wp/D if wp > 0 else 0.0
    return heat + lam*kT*f*info(f, wp, D, r, exact) + w*(r + d*d/f**2 + 2*D/f)

def J0(kap, lam, w, r, exact, fg):
    res = minimize_scalar(lambda lf: J(np.exp(lf), 0.0, 0.0, kap, lam, w, r, exact),
                          bounds=(np.log(fg)-3, np.log(fg)+3), method="bounded", options=dict(xatol=1e-12))
    return res.fun, np.exp(res.x)

def Jc(kap, lam, w, r, exact, f0, starts=None):
    def obj(p):
        lf, lD, u = p
        return J(np.exp(lf), om/(1+np.exp(-u)), np.exp(lD), kap, lam, w, r, exact)
    best = (np.inf, None)
    starts = starts or [(df, lD, u) for df in (-0.3, 0, 0.3) for lD in (-6, -2, 2) for u in (-5, -1, 2)]
    for df, lD, u in starts:
        opts = dict(xatol=1e-10, fatol=1e-14, maxiter=6000, maxfev=9000) if exact else \
            dict(xatol=1e-12, fatol=1e-16, maxiter=40000, maxfev=80000)
        res = minimize(obj, [np.log(f0)+df, np.log(f0)+lD, u], method="Nelder-Mead", options=opts)
        if exact:  # polish
            res = minimize(obj, res.x, method="Nelder-Mead", options=opts)
        if res.fun < best[0]: best = (res.fun, res.x)
    return best

def Istar(kap, lam): return 2*kap/lam*(1 + np.sqrt(1 + lam/kap))

def w_for_I0(I0, lam, r):
    """Best no-clock design (high SNR): I0 = 1 + ln(om/(f0 sqrt(2 pi e r))), lam kT (I0 - 1) = 2 w om^2 / f0^3."""
    f0 = om*np.exp(1 - I0)/np.sqrt(2*np.pi*np.e*r)
    return lam*kT*(I0 - 1)*f0**3/(2*om*om), f0

def frac(x): return 1/(1+np.exp(-x[2]))


def exact_I0(f0, r): return info(f0, 0.0, 0.0, r, True)

def w_for_exact_I0(target, kap, lam, r):
    """Stake at which the exact best no-clock design's look carries `target` nats."""
    def g(lab):
        w, fg = w_for_I0(lab, lam, r); _, f0 = J0(kap, lam, w, r, True, fg); return exact_I0(f0, r) - target
    lab = brentq(g, target - 0.5, target + 1.0, xtol=1e-9)
    w, fg = w_for_I0(lab, lam, r); return w, fg

def slope(w, fg, kap, lam, r, eps=1e-6, n=80001):
    """d J / d eps along (w' = eps, D = eps d), minimised over d, at the exact no-clock optimum."""
    _, f0 = J0(kap, lam, w, r, True, fg)
    def Jx(wp, D):
        I = h_ALG((om-wp)/f0, 2*D/f0, 2*r, n=n) - 0.5*(LN2PIE + np.log(r))
        heat = kap*kT*wp*wp/D if wp > 0 else 0.0
        return heat + lam*kT*f0*I + w*(r + (om-wp)**2/f0**2 + 2*D/f0)
    base = Jx(0.0, 0.0)
    res = minimize_scalar(lambda ld: (Jx(eps, eps*np.exp(ld)) - base)/eps, bounds=(-14, 14), method="bounded",
                          options=dict(xatol=1e-7))
    return res.fun

def local_onset(kap, lam, r):
    def g(lab):
        w, fg = w_for_I0(lab, lam, r); return slope(w, fg, kap, lam, r)
    lab = brentq(g, 0.6*4*kap/lam + 0.2, 1.3*4*kap/lam + 0.5, xtol=1e-6)
    w, fg = w_for_I0(lab, lam, r); _, f0 = J0(kap, lam, w, r, True, fg)
    return exact_I0(f0, r)

if __name__ == "__main__":
    import sys
    quick = "--quick" in sys.argv
    fails = 0
    print("(i) h(E) closed form 1 + ln(mu^2 + 2 sig^2)/2 vs grid quadrature with a vanishing Gaussian")
    mx = 0.0
    for mu, sig2 in [(1.0, 0.0), (0.3, 0.2), (0.0, 1.0), (2.0, 0.01), (0.05, 3.0)]:
        mx = max(mx, abs(h_ALG(mu, sig2, 1e-10*(mu*mu + 2*sig2), n=80001) - h_AL(mu, sig2)))
    print(f"  5 cases, max |gap| {mx:.0e}"); fails += mx > 1e-4

    print("(ii) marginal information prices at the no-clock point (r = 1e-4)")
    r = 1e-4
    for mu in (0.5, 0.2):
        hm = 1e-4*mu; hs = 1e-7*mu*mu
        Ie = lambda m, s2: h_ALG(m, s2, 2*r, n=80001)
        a = mu*(Ie(mu+hm, 0) - Ie(mu-hm, 0))/(2*hm)
        b = mu*mu*(Ie(mu, hs) - Ie(mu, 0))/hs
        print(f"  mu/sqrt(2r)={mu/np.sqrt(2*r):5.1f}: exact a={a:.4f} b={b:.4f} b/a={b/a:.5f}   naive closed form a=b=1")
        fails += not (abs(b/a - 0.5) < 2e-3)

    print("(iii) exact local onset, information per look of the best no-clock design (target 4 kap/lam)")
    cases = [(1, 1)] if quick else [(1, 1), (2, 1), (1.5, 1), (1, 2), (3, 1)]
    rs = (1e-4,) if quick else (1e-4, 1e-7)
    for kap, lam in cases:
        vals = [local_onset(kap, lam, rr) for rr in rs]
        print(f"  kap={kap}, lam={lam}: onset I0 = " + ", ".join(f"{v:.4f} (r={rr:g})" for v, rr in zip(vals, rs))
              + f"   4kap/lam = {4*kap/lam:.4f}")
        fails += any(abs(v - 4*kap/lam) > 0.006*4*kap/lam for v in vals)

    if not quick:
        print("(iv) global multistart minimum with the exact information at 0.98 and 1.02 x 4kap/lam (r = 1e-4)")
        for kap, lam in [(1, 1), (2, 1), (1, 2)]:
            row = []
            for side in (0.98, 1.02):
                w, fg = w_for_exact_I0(side*4*kap/lam, kap, lam, r)
                j0, f0 = J0(kap, lam, w, r, True, fg)
                st = [(df, lD, u) for df in (0, 1.5, 3) for lD in (-8, -3) for u in (0, 4)]
                jc, x = Jc(kap, lam, w, r, True, f0, starts=st)
                pays = jc < j0*(1 - 1e-9); fails += pays != (side > 1)
                row.append(f"{side}: dJ/J0={(min(jc, j0)-j0)/j0:+.1e} {'clock' if pays else 'none '} w'/om={frac(x) if pays else 0:.3f}")
            print(f"  kap={kap}, lam={lam}: " + " | ".join(row))

        print("(v) clock fraction w'/om above onset, exact information (kap=lam=1, r=1e-4)")
        row = []; prev = 0.0
        for side in (1.02, 1.1, 1.3, 1.6):
            w, fg = w_for_exact_I0(side*4, 1, 1, r); j0, f0 = J0(1, 1, w, r, True, fg)
            st = [(df, lD, u) for df in (0, 1.5) for lD in (-8, -3) for u in (0, 4)]
            jc, x = Jc(1, 1, w, r, True, f0, starts=st)
            fr = frac(x) if jc < j0 else 0.0; fails += not (fr > prev); prev = fr
            row.append(f"{side}x: {fr:.4f}")
        print("  " + "  ".join(row))

    print("(vi) fixed-price control: Poisson looks, perfect reads, price c, onset 4 kap kT")
    def Jfix(p, c, w):
        lf, lD, u = p; f = np.exp(lf); D = np.exp(lD); wp = om/(1+np.exp(-u))
        return kT*wp*wp/D + c*f + w*((om-wp)**2/f**2 + 2*D/f)
    row = []
    for c in (3.9, 4.1):
        for w in (0.1, 10.0):
            f0 = (2*w*om*om/c)**(1/3); j0 = c*f0 + w*om*om/f0**2
            jc = min(minimize(Jfix, [np.log(f0)+a, b, u], args=(c, w), method="Nelder-Mead",
                              options=dict(xatol=1e-12, fatol=1e-16, maxiter=40000)).fun
                     for a in (-0.5, 0, 0.5) for b in (-6, -2, 2) for u in (-4, 0, 3))
            pays = jc < j0*(1 - 1e-10); fails += pays != (c > 4)
            row.append(f"c={c},w={w}: {'clock' if pays else 'none'}")
    print("  " + "  ".join(row))

    if not quick:
        print("(vii) naive high-SNR closed form (a = b = 1): onset at (2kap/lam)(1+sqrt(1+lam/kap)), kap=lam=1, r=1e-6")
        Is = Istar(1, 1); row = []
        for side in (0.98, 1.02):
            w, fg = w_for_I0(side*Is, 1, 1e-6); j0, f0 = J0(1, 1, w, 1e-6, False, fg); jc, x = Jc(1, 1, w, 1e-6, False, f0)
            pays = jc < j0*(1 - 1e-10); fails += pays != (side > 1)
            row.append(f"{side} x {Is:.4f}: {'clock' if pays else 'none'}")
        print("  " + " | ".join(row) + "   (not the onset of the exact class; see (ii)-(iii))")

        print("(viii) scope at onset (kap=lam=1, r=1e-4): filtering no-clock memory that counts looks")
        w, fg = w_for_exact_I0(4.0, 1, 1, r); j0, f0 = J0(1, 1, w, r, True, fg)
        def JK(f):
            q = om*om/f**2; Pm = (q + np.sqrt(q*q + 4*q*r))/2; P = Pm*r/(Pm + r)
            return kT*f*0.5*np.log(1 + Pm/r) + w*(P + q)
        fs = np.exp(np.linspace(np.log(f0)-4, np.log(f0)+12, 4001)); jk = np.array([JK(f) for f in fs])
        k = int(np.argmin(jk)); weak = kT*om/(2*np.sqrt(r))
        print(f"  reset J0={j0:.6g}; filtering min {jk[k]:.6g} (ratio {jk[k]/j0:.4f}); many-weak-looks limit {weak/j0:.1f} x J0")
        fails += not (jk[k]/j0 > 0.98 and weak > 5*j0)
    print(f"FAILS {fails}")
    print("ALL INFO-READ CHECKS PASS" if fails == 0 else "SOME INFO-READ CHECKS FAIL")
