import numpy as np, sys
from scipy.optimize import minimize_scalar, brentq
sys.path.insert(0,'/workspace/gtao-spine/checks')
print("== CT12 numeric check of T* and CT13 penalty at several alpha ==")
for al in [1.3,1.6,2.0,2.5,2.9]:
    c,w,q=0.7,2.0,0.3
    J=lambda T: c/T+w*q*T**(al-1)/al
    r=minimize_scalar(J,bounds=(1e-6,1e3),method='bounded',options={'xatol':1e-12})
    Tst=(al*c/((al-1)*w*q))**(1/al)
    kk=2.0; pen=J(kk*Tst)/J(Tst); pf=((al-1)/kk+kk**(al-1))/al
    print(f" alpha={al}: numeric T*={r.x:.6f} formula {Tst:.6f} | penalty at k=2: {pen:.6f} formula {pf:.6f}")
print("\n== Chance constraint: finer B grid ==")
y,cc,ww,sg,s0=1.0,0.05,1.0,1.0,0.3
m=lambda t: y-cc/t-ww*sg**2*t/2
s2=lambda t: s0**2+ww**2*sg**4*t**3/3
th=lambda t: 2*m(t)/s2(t)
tE=np.sqrt(2*cc/(ww*sg**2)); tS=minimize_scalar(lambda t:-th(t),bounds=(1e-3,3),method='bounded').x
eps=1e-3
for B in [0.45,0.4864,0.49,0.5,0.505,0.508]:
    tmin=np.log(1/eps)/B
    if tmin>th(tS): print(f" B={B}: infeasible"); continue
    if th(tE)>=tmin: print(f" B={B}: slack -> EOQ"); continue
    tb=brentq(lambda t: th(t)-tmin, tS, tE); print(f" B={B}: tau*={tb:.4f}")
print(f" feasibility edge B_min=ln(1/eps)/theta_max={np.log(1/eps)/th(tS):.4f}; slack edge B=ln(1/eps)/theta(EOQ)={np.log(1/eps)/th(tE):.4f}")

print("\n== Engineer example: demand tracker, two modes (fast ~3 d, slow ~90 d) seen in daily noise ==")
from stores import E_inf, E_K
A=[1/3,1/90]; V=[40.0**2,120.0**2]; N=60.0**2*1.0   # units^2, units^2*day
Einf=E_inf(A,V,N); b1=E_K(A,V,N,1); b2=E_K(A,V,N,2)
E1,E2=b1[0],b2[0]
print(f" E_inf={Einf:.1f} E_1={E1:.1f} (tau_1={np.exp(-b1[1])}) E_2={E2:.1f} (taus={np.exp(-b2[1])}) days; eps1={100*(E1/Einf-1):.2f}%")
h=40.0  # $/day upkeep of a second forecasting layer (hypothetical)
wstar=h/(E1-E2)
print(f" second layer pays iff w > h/(E1-E2) = {wstar:.4f} $/(unit^2 day)")
for wv in [0.005,0.02,0.1]:
    print(f"  w={wv}: saving w(E1-E2)={wv*(E1-E2):.1f} $/day vs h={h} -> K*={'2' if wv*(E1-E2)>h else '1'}")
print(" read interval for a hold-last-value dashboard of a fBm-like metric (CT12):")
for al in [1.5,2.0]:
    c=25.0; q=50.0; w=0.02
    Tst=(al*c/((al-1)*w*q))**(1/al)
    print(f"  alpha={al}, q={q}, c=${c}/read, w={w}: T*={Tst:.2f} days; doubling w changes T* by x{2**(-1/al):.3f}")
