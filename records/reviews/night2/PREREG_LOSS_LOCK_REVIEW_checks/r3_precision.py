"""Reviewer's own check of the precision-effort elasticities under |e|^p at alpha = 1.5, 2, 2.5 (the author checked alpha = 2 only).
Causal filtering MMSE of a signal with spectrum S(w) = q|w|^-alpha in white noise of density N (Yovits-Jackson / Kolmogorov form):
  V(q, N) = (N/pi) int_0^inf ln(1 + q w^-alpha / N) dw     (by quadrature, not the closed form)
Gaussian errors => E|e|^p = c_p V^{p/2}. Effort r = 1/N priced linearly: J(r) = c r + w c_p V(q, 1/r)^{p/2}.
r* found numerically; elasticities by central differences in ln w, ln q.
"""
import numpy as np, json
from scipy.integrate import quad
from scipy.optimize import minimize_scalar
from scipy.special import gamma
def V(q, N, alpha):
    f = lambda x: np.log1p(q*x**(-alpha)/N)
    s = (q/N)**(1/alpha)
    I = quad(f, 0, s, limit=400, epsabs=0, epsrel=1e-12)[0] + quad(f, s, np.inf, limit=400, epsabs=0, epsrel=1e-12)[0]
    return N/np.pi*I
def cp(p): return 2**(p/2)*gamma((p+1)/2)/np.sqrt(np.pi)
def rstar(w, q, p, alpha, c=1.0):
    J = lambda lr: c*np.exp(lr) + w*cp(p)*V(q, np.exp(-lr), alpha)**(p/2)
    res = minimize_scalar(J, bounds=(-12, 12), method='bounded', options=dict(xatol=1e-11))
    return np.exp(res.x)
out = []
for alpha in (1.5, 2.0, 2.5):
    # scaling check of V against closed form q^{1/a} N^{1-1/a}/sin(pi/a)
    v1 = V(2.0, 0.3, alpha); cf = 2.0**(1/alpha)*0.3**(1-1/alpha)/np.sin(np.pi/alpha)
    print(f'alpha={alpha}: V quad {v1:.10f} vs closed form {cf:.10f}')
    for p in (0.5, 1.0, 2.0, 4.0):
        h = 0.02
        ea = (np.log(rstar(np.e**h, 1, p, alpha)) - np.log(rstar(np.e**-h, 1, p, alpha)))/(2*h)
        eb = (np.log(rstar(1, np.e**h, p, alpha)) - np.log(rstar(1, np.e**-h, p, alpha)))/(2*h)
        ath = 2*alpha/(2*alpha+p*(alpha-1)); bth = p/(2*alpha+p*(alpha-1))
        print(f'  p={p}: a={ea:.5f} (th {ath:.5f})  b={eb:.5f} (th {bth:.5f})')
        out.append(dict(alpha=alpha, p=p, a=ea, a_th=ath, b=eb, b_th=bth))
json.dump(out, open('r3_precision.json', 'w'), indent=1)
