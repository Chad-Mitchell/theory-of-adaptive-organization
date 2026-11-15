"""N12 referee, check 2: fully numerical onset exponent for precision-priced continuous sensing.
No closed forms for (a,b): causal MMSE by quadrature of the Yovits-Jackson integral for S(w)=q|w|^-alpha
(validated against steady-state Kalman (CARE) for alpha = 2, 4, 6), cost minimised numerically over the noise
density r with price c*(1/r)^theta, onset N* solved by root-finding of G(N)=N[phi(w,qg+qu)-phi(w,qu)]-phi(Nw,qg)
(h=0, equal prices; definitions of formal THEOREMS 'Definitions'). Also: mixed spectra (alpha_g != alpha_u)."""
import numpy as np, math
from scipy import integrate, optimize, linalg

def mmse_spec(S, r):
    # causal MMSE = (1/2pi) * r * Int_{-inf}^{inf} ln(1+S(w)/r) dw = (r/pi) Int_0^inf ..., integrated in t = ln w
    f = lambda t: math.log1p(S(math.exp(t))/r) * math.exp(t)
    pts = np.linspace(-80, 80, 81)
    return r/math.pi * sum(integrate.quad(f, pts[i], pts[i+1], epsabs=0, epsrel=1e-13, limit=200)[0] for i in range(80))

def kalman_chain(k, q, r):
    # k-fold integrated white noise (S = q/w^(2k)), observe first state in white noise r
    A = np.diag(np.ones(k-1), 1); B = np.zeros((k,1)); B[-1,0] = 1; C = np.zeros((1,k)); C[0,0] = 1
    P = linalg.solve_continuous_are(A.T, C.T, B @ B.T * q, np.array([[r]]))
    return P[0,0]

print("== validation: Yovits-Jackson quadrature vs Kalman CARE (q=1.7, r=0.3) ==")
for k in (1,2,3):
    al = 2*k
    yj = mmse_spec(lambda w: 1.7*w**(-al), 0.3); kf = kalman_chain(k, 1.7, 0.3)
    print(f" alpha={al}: YJ {yj:.12g}  Kalman {kf:.12g}  rel diff {abs(yj/kf-1):.1e}")

def phi(W, S, theta, c=1.0):
    obj = lambda lr: W*mmse_spec(S, math.exp(lr)) + c*math.exp(-theta*lr)
    res = optimize.minimize_scalar(obj, bounds=(-60, 60), method='bounded', options={'xatol':1e-9})
    return res.fun

def onset(rho, al_u, al_g, theta, qu=1.0, w=1.0):
    qg = rho*qu
    Su = lambda x: qu*x**(-al_u); Sg = lambda x: qg*x**(-al_g)
    flat_gain = phi(w, lambda x: Su(x)+Sg(x), theta) - phi(w, Su, theta)
    G = lambda lN: math.exp(lN)*flat_gain - phi(w*math.exp(lN), Sg, theta)
    return math.exp(optimize.brentq(G, 1e-9, 60, xtol=1e-11))

rhos = [10**-1.5, 10**-2, 10**-2.5, 10**-3, 10**-3.5]
def slopes(al_u, al_g, theta):
    Ns = [onset(r, al_u, al_g, theta) for r in rhos]
    sl = [math.log(Ns[i+1]/Ns[i])/math.log(rhos[i+1]/rhos[i]) for i in range(len(rhos)-1)]
    return Ns, sl

print("\n== onset exponent d ln N*/d ln rho, same alpha for shared and private drift ==")
print(" alpha theta | N* at rho=10^-1.5..10^-3.5 | local slopes | N12 prediction -(1+theta)")
for al, th in [(1.2,1),(1.5,1),(2,1),(2.5,1),(2.9,1),(3.5,1),(4,1),(1.5,0.5),(2.5,0.5),(1.5,2),(2.5,2),(4,2)]:
    Ns, sl = slopes(al, al, th)
    print(f" {al:4} {th:4} | " + " ".join(f"{n:.4g}" for n in Ns) + " | " + " ".join(f"{s:+.4f}" for s in sl) + f" | {-(1+th):+.1f}", flush=True)

print("\n== mixed spectra: alpha_g != alpha_u; slope is d ln N*/d ln q_g at fixed q_u (rho no longer unit-free) ==")
for au, ag, th in [(2,1.5,1),(2,2.5,1),(1.5,2.5,1),(2.5,1.5,1)]:
    Ns, sl = slopes(au, ag, th)
    print(f" alpha_u={au} alpha_g={ag} theta={th} | " + " ".join(f"{n:.4g}" for n in Ns) + " | " + " ".join(f"{s:+.4f}" for s in sl), flush=True)
