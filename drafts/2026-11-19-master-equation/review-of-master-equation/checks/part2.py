"""Part 2 checks: (h) dimensionless invariance, (k) regret, (j) redesign window. nice -n 19 python3 part2.py"""
import numpy as np, sys
sys.path.insert(0,'/workspace/gtao-spine/checks')
from stores import mats, E_inf, E_K
from lead import E_opt, E_K_lead
from scipy.optimize import minimize_scalar
rng=np.random.default_rng(1)

print("== (h) invariance: rescale time by s and amplitude by A; keep R=w*Var/h, shape fixed ==")
a0=np.array([1.0,1/30]); v0=np.array([0.5,0.5]); N0=0.05
for s,A in [(1,1),(7.0,1),(1,13.0),(0.01,1e3)]:
    a=a0/s; v=v0*A**2; N=N0*A**2*s
    Ei=E_inf(a,v,N); e1=E_K(a,v,N,1); e2=E_K(a,v,N,2)
    eps1=e1[0]/Ei-1
    h=1.0; R=300; w=R*h/(v.sum())  # R defined on Var
    Js=[w*v.sum(), h+w*e1[0], 2*h+w*e2[0]]
    print(f" s={s:g} A={A:g}: eps1={eps1*100:.4f}%  K*={int(np.argmin(Js))}  layer taus/s={np.sort(np.exp(-e2[1]))/s}")
print(" -> same groups => same design up to time and amplitude units (Buckingham; Theorem S S1-S2)")
print(" counter-check: same R and alpha-like 'span' but different noise share N*a1/Var changes design:")
for Nn in [0.005,0.05,0.5]:
    Ei=E_inf(a0,v0,Nn); e1=E_K(a0,v0,Nn,1)[0]
    print(f"   N={Nn}: eps1={100*(e1/Ei-1):.3f}%  R*={1/(e1/Ei-1):.1f}")

print("\n== (k1) regret from misjudging q by factor m (single layer, CT13) and the quadratic approximation ==")
for al in [1.3,2.0,2.7]:
    for m in [1.5,2,10]:
        k=m**(1/al); reg=((al-1)/k+k**(al-1))/al-1; approx=(al-1)*np.log(m)**2/(2*al**2)
        print(f" alpha={al} m={m}: regret={reg*100:.2f}%  quadratic approx={approx*100:.2f}%")
print(" curvature of J in ln T at optimum, relative: alpha-1")

print("\n== (k2) regret from misjudging alpha: structure function matched at reference lag tau_ref ==")
c,w,q=1.0,1.0,1.0
for al in [1.5,2.0,2.5]:
    J=lambda T,al=al: c/T+w*q*T**(al-1)/al
    Ts=(al*c/((al-1)*w*q))**(1/al)
    for tr in [Ts,10*Ts,0.1*Ts]:
        out=[]
        for ah in [al-0.3,al+0.3]:
            if not (1<ah<3): out.append("  n/a"); continue
            qh=q*tr**(al-1)/tr**(ah-1)
            Th=(ah*c/((ah-1)*w*qh))**(1/ah)
            out.append(f"{(J(Th)/J(Ts)-1)*100:6.2f}%")
        print(f" true alpha={al}, tau_ref/T*={tr/Ts:5.2f}: regret using alpha-0.3, alpha+0.3 = {out}")

print("\n== (k3) regret from a wrong spectrum, two-store design (true modes tau 1 and 30) ==")
aT=np.array([1.0,1/30]); vT=np.array([0.5,0.5]); N=0.05
Eo=E_inf(aT,vT,N)
def design(a,v,N):
    best=E_K(a,v,N,2); b=np.exp(best[1]); M,r=mats(a,v,b,N); g=np.linalg.solve(M,r); return b,g
def eval_true(b,g):
    M,r=mats(aT,vT,b,N); return vT.sum()-2*r@g+g@M@g
for lab,(a,v) in {"correct":(aT,vT),"slow mode at tau 10":(np.array([1,1/10]),vT),"slow mode at tau 100":(np.array([1,1/100]),vT),
                  "variance shares 0.8/0.2":(aT,np.array([0.8,0.2])),"variance shares 0.2/0.8":(aT,np.array([0.2,0.8]))}.items():
    b,g=design(a,v,N); print(f" belief {lab:26s}: regret in error = {(eval_true(b,g)/Eo-1)*100:6.3f}%")
e1=E_K(aT,vT,N,1)[0]; print(f" believing one mode (K=1 design): regret = {(e1/Eo-1)*100:.3f}%  (= flat penalty eps1)")

print("\n== (j) redesign window: OU rate MLE precision vs record length (Monte Carlo) ==")
a=1/30.0; dt=0.5
for Tn in [10,30,100]:
    T=Tn/a; n=int(T/dt); ests=[]
    for rep in range(300):
        x=np.zeros(n); e=rng.standard_normal(n)*np.sqrt((1-np.exp(-2*a*dt)))
        for i in range(1,n): x[i]=np.exp(-a*dt)*x[i-1]+e[i]
        phi=np.dot(x[1:],x[:-1])/np.dot(x[:-1],x[:-1]); phi=min(max(phi,1e-9),0.999999)
        ests.append(-np.log(phi)/dt)
    ests=np.array(ests)
    print(f" record = {Tn} x slowest tau: rel sd of a_hat = {ests.std()/a:.3f}  (asymptotic sqrt(2/(aT)) = {np.sqrt(2/Tn):.3f})")
