"""N12 referee, check 5: shared drift with a different spectral slope than private drift (alpha_g != alpha_u),
precision-priced continuous sensing, theta = 1. Same numerics as c2 (Yovits-Jackson quadrature, numerical optimum),
extended to smaller q_g to see whether d ln N*/d ln q_g reaches -(1+theta) = -2 when alpha_g - alpha_u >= 1."""
import math
from scipy import integrate, optimize
import numpy as np
def mmse_spec(S, r):
    f = lambda t: math.log1p(S(math.exp(t))/r) * math.exp(t)
    pts = np.linspace(-120, 80, 101)
    return r/math.pi * sum(integrate.quad(f, pts[i], pts[i+1], epsabs=0, epsrel=1e-13, limit=200)[0] for i in range(100))
def phi(W, S, theta=1.0):
    return optimize.minimize_scalar(lambda lr: W*mmse_spec(S, math.exp(lr)) + math.exp(-theta*lr),
                                    bounds=(-60, 60), method='bounded', options={'xatol':1e-9}).fun
def onset(qg, au, ag):
    Su = lambda x: x**(-au); Sg = lambda x: qg*x**(-ag)
    gain = phi(1, lambda x: Su(x)+Sg(x)) - phi(1, Su)
    return math.exp(optimize.brentq(lambda lN: math.exp(lN)*gain - phi(math.exp(lN), Sg), 1e-9, 80, xtol=1e-11)), gain
qs = [10**(-k/2) for k in range(3, 13)]
for au, ag in [(2.0, 2.9), (1.5, 2.5), (1.2, 2.5), (1.2, 2.9)]:
    res = [onset(q, au, ag) for q in qs]
    sl = [math.log(res[i+1][0]/res[i][0])/math.log(qs[i+1]/qs[i]) for i in range(len(qs)-1)]
    gs = [math.log(res[i+1][1]/res[i][1])/math.log(qs[i+1]/qs[i]) for i in range(len(qs)-1)]
    print(f"alpha_u={au} alpha_g={ag} (diff {ag-au:.1f}) q_g=10^-1.5..10^-6\n  d lnN*/d ln q_g: " + " ".join(f"{s:+.3f}" for s in sl)
          + "\n  d ln(flat gain)/d ln q_g: " + " ".join(f"{s:.3f}" for s in gs), flush=True)
