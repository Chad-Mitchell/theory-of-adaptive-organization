"""C5. Scale covariance: what is invariant under change of cost currency and time unit, and what is not."""
import numpy as np, sympy as sp
from scipy import special, optimize
rng = np.random.default_rng(5)
print("== C5a: generalized check interval for loss w|e|^p and self-similar drift e ~ sigma t^H Z ==")
c, w, s, T, p, H, m = sp.symbols('c w sigma T p H m_p', positive=True)
J = c/T + w*s**p*m*T**(p*H)/(p*H+1)
Ts = sp.solve(sp.diff(J, T), T)[0]; print("  T* =", sp.simplify(Ts))
print("  d ln T*/d ln sigma =", sp.simplify(sp.diff(sp.log(Ts), s)*s), "  d ln T*/d ln(c/w) =", sp.simplify(sp.diff(sp.log(Ts), c)*c))
for pp, HH in [(2, sp.Rational(1, 2)), (1, sp.Rational(1, 2)), (2, sp.Rational(3, 4)), (2, sp.Rational(1, 3))]:
    print(f"   p={pp}, H={HH}: exponent on sigma = {sp.simplify(-pp/(1+pp*HH))}, on c/w = {sp.simplify(1/(1+pp*HH))}")
print("  MC check p=1, H=1/2 (|error| loss, Brownian drift): optimum of simulated cost vs formula")
cv, wv, sv = 0.05, 1.0, 1.0; m1 = np.sqrt(2/np.pi)
Tf = (cv*(0.5+1)/(wv*sv*m1*0.5))**(1/1.5)
def Jsim(Tc, n=4000, steps=200):
    dt = Tc/steps; Wp = np.cumsum(np.sqrt(dt)*rng.standard_normal((n, steps)), 1)
    return cv/Tc + wv*sv*np.mean(np.abs(Wp))
grid = Tf*np.array([0.5, 0.7, 0.85, 1.0, 1.2, 1.5, 2.0]); vals = [Jsim(g) for g in grid]
print(f"  formula T*={Tf:.4f}; simulated cost on grid T/T*=[.5,.7,.85,1,1.2,1.5,2]: {np.round(vals, 4)} -> min at T/T*={grid[int(np.argmin(vals))]/Tf:.2f}")
print("== C5b: invariances ==")
k = sp.symbols('k', positive=True)
print("  currency: T*(k c, k w) / T*(c,w) =", sp.simplify(Ts.subs({c: k*c, w: k*w})/Ts), " (invariant)")
print("  only one cost rescaled: T*(k c, w)/T* =", sp.simplify(Ts.subs(c, k*c)/Ts), " (NOT invariant: the exchange rate between cost types matters)")
_r = (Ts.subs({s: s*k**H, w: w*k})/Ts).subs({c: 0.3, w: 1.7, s: 0.9, m: 0.8, p: 2, H: 0.5})
print("  time unit t -> t/k (sigma -> sigma k^H, cost rates -> k x): T* ratio at k=3:", float(_r.subs(k, 3)), "(= 1/k: covariant)")
print("== C5c: two cost components with different size scaling break the power law (crossover) ==")
n_ = np.logspace(0, 6, 13); a1, a2 = 1.0, 1e-3          # check cost = a1 (fixed, e.g. per-check floor) + a2 * n (size-proportional)
cn = a1 + a2*n_; wn = n_; sn2 = n_                       # stakes ~ n, drift variance ~ n (independent parts)
Tn = np.sqrt(2*cn/(wn*sn2)); slope = np.diff(np.log(Tn))/np.diff(np.log(n_))
print("  local slope d ln T*/d ln n across n=1..1e6:", np.round(slope, 3), " (pure power law would be constant)")
print("== C5d: multiplicative persistence (Kelly growth) is exactly currency-invariant and prices information in nats ==")
def kelly_gain(Pxy, odds):
    px = Pxy.sum(1); py = Pxy.sum(0)
    G0 = np.sum(px*np.log(px*odds))                         # proportional betting b=p(x), fair-odds horse race
    G1 = np.sum(Pxy*np.log((Pxy/py[None, :])*odds[:, None]))
    I = np.sum(Pxy*np.log(Pxy/(px[:, None]*py[None, :])))
    return G1-G0, I
for t in range(4):
    Pxy = rng.random((3, 4)); Pxy /= Pxy.sum(); odds = rng.uniform(1.5, 5, 3)
    g, I = kelly_gain(Pxy, odds); print(f"  random env/cue {t}: growth gain = {g:.6f} nats, I(X;Y) = {I:.6f} nats")
print("  wealth-unit change W -> kW adds ln k to log-wealth: growth rate and optimal fractions unchanged. Constant-relative-risk")
print("  (log and power) objectives give currency-invariant policies; additive objectives with a fixed threshold in one unit do not (C5e).")
print("== C5e: additive ruin with a fixed absolute threshold is NOT currency-invariant when part of the cost is fixed in another unit ==")
for scale in [1, 10, 100]:
    # reserve B and shocks sigma in dollars scale with 'scale'; a fixed physical cost per check (e.g. kT ln2 per bit) does not
    Bd, sd = 1.0*scale, 1.0*scale; c_fixed, c_prop = 0.01, 0.04*scale; ww = 1.0/scale
    Tstar = np.sqrt(2*(c_fixed+c_prop)/(ww*sd**2)); print(f"  scale={scale:4d}: T* = {Tstar:.5f}")
print("  => T* drifts with scale only through the fixed-unit component; once it is negligible, the form is scale-free.")
