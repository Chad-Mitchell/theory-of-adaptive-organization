diff --git a/theory/store_noise/threshold_check.py b/theory/store_noise/threshold_check.py
index b944f11..c497774 100644
--- a/theory/store_noise/threshold_check.py
+++ b/theory/store_noise/threshold_check.py
@@ -1,28 +1,44 @@
 """Check of the interlacing premise (THEORY v2.5.4, CLAIM_MAP v2.64), Model S+ E1-a (theory/STORE_NOISE.md).
 One OU mode (rate lam, variance sig2), one store with memory tau, store noise referred to the input V(tau) = V0 (tau0/tau)^(2-2s).
 Explained variance EV = (sig2 A)^2 / (sig2 A + V), A = 1/(1 + lam tau).  Low SNR: EV ∝ tau^(2-2s)/(1+lam tau)^2.
 d/dx [a ln x - 2 ln(1+x)] = 0, x = lam tau, a = 2-2s  =>  a(1+x) = 2x  =>  x* = a/(2-a) = (1-s)/s.
-x* < 1 (store faster than its mode) iff s > 1/2; x* = 1 at s = 1/2; x* > 1 iff s < 1/2.  Full optimum checked numerically below."""
+x* < 1 (store faster than its mode) iff s > 1/2; x* = 1 at s = 1/2; x* > 1 iff s < 1/2.
+Any positive SNR (review 29): with rho = 1/snr, g(x) = A^2/(A + rho x^-a), the first-order condition is exactly
+A^2 = rho x^(-a-1) (a - 2 A x), so at any interior optimum a > 2Ax, i.e. x* < (1-s)/s.  For 0 < s < 1, g -> 0 at both
+ends, so an interior optimum exists.  Hence s >= 1/2 gives x* < 1 at every positive SNR.  Checked symbolically and on a grid.
+E2 (speed price) is not checked here; see checks.py section 4."""
 import json, os
 import numpy as np, sympy as sp
 from scipy.optimize import minimize_scalar
 x, s = sp.symbols('x s', positive=True)
 crit = sp.solve(sp.diff((2 - 2*s)*sp.log(x) - 2*sp.log(1 + x), x), x)
 assert len(crit) == 1 and sp.simplify(crit[0] - (1 - s)/s) == 0
 assert sp.solve(sp.Lt((1 - s)/s, 1), s) == sp.solve(sp.Gt(s, sp.Rational(1, 2)), s)
+rho, xx, aa = sp.symbols('rho x a', positive=True); A = 1/(1 + xx)
+g = A**2/(A + rho*xx**(-aa))
+ident = A**2 - rho*xx**(-aa - 1)*(aa - 2*A*xx)                               # (d/dx ln g) * (A + rho x^-a) = -ident
+assert sp.simplify(sp.diff(sp.log(g), xx)*(A + rho*xx**(-aa)) + ident) == 0
 out = {'closed_form': 'lam*tau* = (1-s)/s', 'faster_than_mode_iff': 's > 1/2',
        'ecoli_s': {str(v): round((1 - v)/v, 3) for v in (0.24, 0.31, 0.37)}, 'numerical': {}}
 S = (0.2, 0.31, 0.45, 0.5, 0.55, 0.7)
 for snr in (1e-3, 1e-2, 1e-1, 1.0):           # snr = sig2 / V(tau0), lam = 1, tau0 = 1/lam
     row = []
     for sv in S:
         f = lambda lt: -((1/(1 + np.exp(lt)))**2 / (1/(1 + np.exp(lt)) + np.exp(lt)**(-(2 - 2*sv))/snr))
         row.append(float(np.exp(minimize_scalar(f, bounds=(-12, 12), method='bounded', options={'xatol': 1e-10}).x)))
     out['numerical'][str(snr)] = dict(zip(map(str, S), [round(r, 4) for r in row]))
 lo = out['numerical']['0.001']
 assert all(abs(lo[str(v)] - (1 - v)/v) < 0.01*(1 - v)/v for v in S)          # low SNR: closed form within 1%
 for snr, r in out['numerical'].items():                                       # s >= 1/2: never slower than the mode
     assert all(r[str(v)] <= 1 + 1e-3 for v in S if v >= 0.5)
     assert all(r[str(v)] < (1 - v)/v + 1e-3 for v in S)                        # higher SNR only shortens the memory
+grid_max = 0.0                                                                # dense grid: x*(snr) < (1-s)/s for all
+for sv in np.linspace(0.05, 0.95, 37):
+    for snr in 10.0**np.linspace(-4, 2, 13):
+        f = lambda lt: -((1/(1 + np.exp(lt)))**2 / (1/(1 + np.exp(lt)) + np.exp(lt)**(-(2 - 2*sv))/snr))
+        xs = float(np.exp(minimize_scalar(f, bounds=(-14, 14), method='bounded', options={'xatol': 1e-11}).x))
+        grid_max = max(grid_max, xs/((1 - sv)/sv)); assert xs < (1 - sv)/sv*(1 + 1e-6)
+        if sv >= 0.5: assert xs < 1 + 1e-6
+out['grid_37x13_max_ratio_to_closed_form'] = round(grid_max, 5)
 json.dump(out, open(os.path.join(os.path.dirname(__file__), 'threshold_check.json'), 'w'), indent=1)
 print(json.dumps(out, indent=1)); print('ALL PASS')
