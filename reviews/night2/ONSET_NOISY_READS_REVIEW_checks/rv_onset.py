# Reviewer's own onset code (imports only rv_f.py, the reviewer's own file).
import numpy as np, json
from scipy.interpolate import CubicSpline
from scipy.optimize import minimize_scalar, brentq
from rv_f import f_cond, p_before_read_szego, g_alpha
out={}
def build_f(a):
    zl=np.logspace(-6,2,33); fl=[f_cond(a,z)[0] for z in zl]
    f0=f_cond(a,0.0)[0]
    _,u1=f_cond(a,100.0); corr=u1-fl[-1]
    zh=np.logspace(2.25,9,28); fh=[p_before_read_szego(a,z)-corr for z in zh]
    Z=np.log(np.r_[zl,zh]); F=np.log(np.r_[fl,fh]); sp=CubicSpline(Z,F)
    g=g_alpha(a); b=1-1/a
    def f(z):
        if z<=1e-6: return f0+(fl[0]-f0)*z/1e-6
        if z>=1e9: return g*z**b*np.exp(F[-1])/(g*1e9**b)
        return float(np.exp(sp(np.log(z))))
    return f,f0
def phi(f,a,w,q,s2):
    obj=lambda lt: 1/np.exp(lt)+w*q*np.exp(lt)**(a-1)*f(s2/(q*np.exp(lt)**(a-1)))
    # coarse grid then refine
    lts=np.linspace(-40,10,501); v=[obj(t) for t in lts]; i=int(np.argmin(v))
    r=minimize_scalar(obj,bounds=(lts[max(i-1,0)],lts[min(i+1,500)]),method='bounded',options={'xatol':1e-10})
    return r.fun, np.exp(r.x)
def Psi(f,a,x,s): return phi(f,a,x,1.0,s)
for a in [1.5,2.0,2.5]:
    f,f0=build_f(a); g=g_alpha(a); b=1-1/a
    D0=(a-1)**(1/a-1)*f0**(1/a)
    hq=1e-4; Dnum=(phi(f,a,1,1+hq,0)[0]-phi(f,a,1,1-hq,0)[0])/(2*hq)
    K=(2*a-1)/(a-1); C=(K/D0)**((2*a-1)/(a-1))*(g*(a-1)/a)**(a/(a-1)); X0=a**(a/(a-1))
    def X(s,D=D0): return brentq(lambda x: x*D-Psi(f,a,x,s)[0],1e-3,1e9,xtol=1e-12,rtol=1e-12)
    sc=X0/C; rhoc=C/X0
    def e(s,h=0.02): return -1-(np.log(X(s*np.exp(h)))-np.log(X(s*np.exp(-h))))/(2*h)
    s15=brentq(lambda s: e(s)+1.5,1e-3,1e2)
    Tsc=Psi(f,a,X(sc),sc)[1]; zL=sc/Tsc**(a-1)
    row=dict(f0=f0,g=g,D0_closed=D0,D0_numeric=Dnum,X0_closed=X0,X_s_1em6=X(1e-6),C_closed=C,
             X_over_Cs={str(s):X(s)/(C*s) for s in [10,100,1000]}, rho_c_over_s2=rhoc,
             s_c=sc,e_at_s_c=e(sc),s_at_e_minus1p5=s15,zL_at_s_c=zL,
             e_large_s={str(s):e(s) for s in [10,100]},
             sum_asym_err_at_sc=(X0+C*sc)/X(sc)-1)
    # members' own noise shifts D: D(s2) for s2 in member units
    row["D_ratio_noisy_members"]={str(s2):((phi(f,a,1,1+hq,s2)[0]-phi(f,a,1,1-hq,s2)[0])/(2*hq))/D0 for s2 in [1e-3,1e-2,1e-1]}
    # curvature over a finite window: local slope at s_c*10^(+-0.5) (one decade of rho centred on rho_c)
    row["e_window_1dec"]=[e(sc*10**-0.5),e(sc*10**0.5)]
    row["e_window_half_dec"]=[e(sc*10**-0.25),e(sc*10**0.25)]
    # direct onset with noisy members (same s2), full equation, referee c3 reproduction
    def Nstar(rho,s2):
        flat=lambda N: N*(phi(f,a,1,1+rho,s2)[0]-phi(f,a,1,1,s2)[0])-phi(f,a,N,rho,s2)[0]
        return brentq(flat,1.0001,1e14,rtol=1e-12)
    s2=1e-3; r1,r2=1e-2,10**-2.5
    row["slope_rho_1e-2_to_1e-2.5_s2_1e-3"]=np.log(Nstar(r2,s2)/Nstar(r1,s2))/np.log(r2/r1)
    row["collapse_Nrho_at_s10"]={str(s2):Nstar(s2/10,s2)*s2/10 for s2 in [1e-5,1e-4,1e-3]}
    row["X_s10_D0"]=X(10.0)
    row["Nstar_rho2_over_s2_at_rho_1e-5_s2_1e-3"]=Nstar(1e-5,1e-3)*1e-10/1e-3
    out[str(a)]=row; print(a,json.dumps(row,default=float)); 
json.dump(out,open("rv_onset.json","w"),indent=1,default=float)
print("27*sqrt2/8 =",27*2**0.5/8, " 27*sqrt2/2 =",27*2**0.5/2)
