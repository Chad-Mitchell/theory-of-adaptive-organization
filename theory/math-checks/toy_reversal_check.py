"""The earlier toy's 'reversal' (slow fixing lowers absolute hazard beyond sigma/B ~ 0.31, tau 4->16)
came from per-window counting h = P_window/tau. Exact renewal hazard for the same fixed-delay model is
h = P_window / E[min(T_hit, tau)]. Compare both. One-sided barrier as in the toy (P_window = 2*Phi(-z))."""
import numpy as np
from scipy import stats, integrate
def p_win(z): return 2*stats.norm.sf(z)
def Emin(B, sigma, tau):
    # one-sided BM first-passage survival S(t) = 1 - 2 Phi(-B/(sigma sqrt t)); E[min(T,tau)] = int_0^tau S
    return integrate.quad(lambda t: 1 - 2*stats.norm.sf(B/(sigma*np.sqrt(t))) if t > 0 else 1.0, 0, tau, limit=200)[0]
B = 1.0
print("sigma/B | naive dh (tau 4->16) = P16/16 - P4/4 | exact renewal dh")
for x in [0.10, 0.20, 0.21, 0.30, 0.31, 0.40, 0.50, 1.0, 3.0]:
    s = x*B
    naive = p_win(B/(s*4))/16 - p_win(B/(s*2))/4
    ex = p_win(B/(s*4))/Emin(B, s, 16) - p_win(B/(s*2))/Emin(B, s, 4)
    print(f"  {x:4.2f}  | {naive: .3e} | {ex: .3e}")

print("\nOne-sided fixed-delay model (symmetric reset also erases favourable deviations): elasticities")
def h1(sigma, B, tau): return p_win(B/(sigma*np.sqrt(tau)))/Emin(B, sigma, tau)
d = 1e-3
for z in [0.3, 0.5, 0.8, 1.0, 1.2, 1.5, 2.0, 3.0]:
    B, s, t = z, 1.0, 1.0
    es = (np.log(h1(s*np.exp(d), B, t)) - np.log(h1(s*np.exp(-d), B, t)))/(2*d)
    et = (np.log(h1(s, B, t*np.exp(d))) - np.log(h1(s, B, t*np.exp(-d))))/(2*d)
    print(f"  z={z}: eps_sigma={es:.3f}  eps_tau={et:.3f}  eps_sigma/2-1={es/2-1:.3f}")
print("=> reversal (eps_tau<0) occurs exactly where eps_sigma<2, as the identity requires.")
