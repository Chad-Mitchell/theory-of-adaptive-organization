"""Own MC: replicate-measurement IV slope for stakes w (cost = w e^2 + noise) under additive vs multiplicative
error-measurement noise. Analytic: additive u indep of e -> IV = w; multiplicative e_obs = e(1 + c xi) -> IV = w/(1+c^2)."""
import numpy as np
rng = np.random.default_rng(2026); w = 2.0; n = 200000
e = rng.standard_normal(n); cost = w*e**2 + 0.5*rng.standard_normal(n)
for label, f in [("additive sd 0.7", lambda: e + 0.7*rng.standard_normal(n)),
                 ("multiplicative c=0.5", lambda: e*(1 + 0.5*rng.standard_normal(n))),
                 ("multiplicative c=1.0", lambda: e*(1 + 1.0*rng.standard_normal(n)))]:
    e1, e2 = f(), f()
    ols = np.cov(cost, e1**2)[0, 1]/np.var(e1**2); iv = np.cov(cost, e2**2)[0, 1]/np.cov(e1**2, e2**2)[0, 1]
    print(f"{label:22s} OLS {ols:.3f}  IV {iv:.3f}  (true 2; multiplicative analytic IV {w/(1+0.25) if '0.5' in label else (w/2 if '1.0' in label else w):.3f})")
