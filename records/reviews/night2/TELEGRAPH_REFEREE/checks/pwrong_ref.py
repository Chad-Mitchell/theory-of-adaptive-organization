"""C&M eqs. (41)-(42) vs the exact Wonham filter (referee). C&M units: alpha = theta/tau, kappa = lam N/mu^2 = alpha/2.
Pwrong (long after the transient) = (1 - <x>_+)/2 under the quasi-stationary law of L given y=+1:
  exact filter: exp(L - k cosh L); printed eq.(20) as Ito: exp(L - k cosh L + 2 ln cosh(L/2)).
Pwrong,av (all times, incl. transients) = (1 - <xy>)/2 = (1 - <x^2>)/2 = MSE/2 = K0/(K0+K1) exactly (innovations density)."""
import numpy as np, json
from scipy.special import k0e, k1e
def qs(logw, f, L):
    w = np.exp(logw - logw.max()); return np.trapezoid(w*f, L)/np.trapezoid(w, L)
out = []
for al in [1e-1, 1e-2, 1e-3, 1e-4, 1e-5]:
    k = al/2; L = np.linspace(-30, np.log(2/k) + 25, 800001)
    one_minus_x = 2/(1 + np.exp(L))
    pw_ex = 0.5*qs(L - k*np.cosh(L), one_minus_x, L)
    pw_pr = 0.5*qs(L - k*np.cosh(L) + 2*np.log(np.cosh(L/2)), one_minus_x, L)
    pav = k0e(k)/(k0e(k) + k1e(k))
    eq42 = al/8*(np.log(al)**2 + (2*np.euler_gamma - 2*np.log(2) + 1)*np.log(al) + 7.59 + 2)
    out.append({"alpha": al, "Pwrong_exact": pw_ex, "Pwrong_printed_eq20": pw_pr, "CM_eq41_alpha/4": al/4,
                "Pwrong_exact_lead_(alpha/4)(ln(4/alpha)-gamma+...)": al/4*(np.log(4/al) - np.euler_gamma),
                "Pwrong_av_exact=K0/(K0+K1)": pav, "lead_(alpha/2)(ln(4/alpha)-gamma)": al/2*(np.log(4/al) - np.euler_gamma),
                "CM_eq42": eq42})
for r in out: print({a: float(f"{b:.4g}") for a, b in r.items()})
json.dump(out, open("out_pwrong_ref.json", "w"), indent=1)
