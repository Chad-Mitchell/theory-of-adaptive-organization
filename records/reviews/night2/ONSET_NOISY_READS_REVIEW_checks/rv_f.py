# Reviewer's own code (no import from ONSET_NOISY_READS_checks). f_alpha(z): time-averaged MSE (units q T^(alpha-1))
# of the optimal linear predictor of sampled fBm (Var[x(t)-x(s)]=|t-s|^(alpha-1)) from noisy reads every T=1, noise var z.
import numpy as np, json, sys
from math import gamma, sin, pi
from scipy.integrate import quad
def g_alpha(a): return (gamma(a)*sin(pi*(a-1)/2))**(1/a)/sin(pi/a)
def f_cond(a, z, M=1200, nu=24):
    h2=a-1; t=np.arange(1,M+1,dtype=float)
    K=0.5*(t[:,None]**h2+t[None,:]**h2-np.abs(t[:,None]-t[None,:])**h2)
    L=np.linalg.cholesky(K+z*np.eye(M)+1e-12*np.eye(M))
    xg,wg=np.polynomial.legendre.leggauss(nu); u=0.5*(xg+1); wg=0.5*wg
    s=M+u; k=0.5*(s[None,:]**h2+t[:,None]**h2-np.abs(s[None,:]-t[:,None])**h2)
    v=np.linalg.solve(L,k); err=s**h2-np.sum(v*v,0)
    return float(np.sum(wg*err)), float(err[-1])
def p_before_read_szego(a, z, Kal=400):
    # one-step error of x_{n+1} from all past noisy reads, via Kolmogorov-Szego on differenced reads
    C=gamma(a)*sin(pi*(a-1)/2)
    def Sy(l):
        ks=np.arange(-Kal,Kal+1); s=np.sum(np.abs(l+2*pi*ks)**(-a))
        tail=2*(2*pi*Kal)**(1-a)/((a-1)*2*pi)  # integral tail of both sides
        return C*4*np.sin(l/2)**2*(s+tail)
    Sd=lambda l: Sy(l)+z*4*np.sin(l/2)**2
    I=2*sum(quad(lambda l: np.log(Sd(l)),lo,hi,limit=400)[0] for lo,hi in [(1e-14,1e-6),(1e-6,1e-3),(1e-3,1e-1),(1e-1,pi)])
    return np.exp(I/(2*pi))-z
if __name__=="__main__":
    out={}
    # alpha=2 closed Kalman check
    for z in [0,0.1,1,10,1e2,1e4]:
        P=(-1+np.sqrt(1+4*z))/2   # P^2+P-z=0 from P=(P+1)z/(P+1+z)
        fK=P+0.5; fc,_=f_cond(2.0,z,M=800)
        print(f"a=2 z={z:g} Kalman f={fK:.6f} cond f={fc:.6f} sqrt-asym ratio={fK/np.sqrt(z) if z>0 else float('nan'):.5f}")
    for a in [1.25,1.5,2.0,2.5,2.75]:
        g=g_alpha(a); b=1-1/a; f0,_=f_cond(a,0.0)
        row={"g":g,"f0_cond":f0}
        for z in [1e2,1e3,1e4,1e5,1e6]:
            p1=p_before_read_szego(a,z)
            row[f"szego_ratio_z{z:g}"]=p1/(g*z**b)
        for z in [1e2,1e3]:
            fc,e1=f_cond(a,z); row[f"cond_ratio_z{z:g}"]=fc/(g*z**b); row[f"cond_u1_vs_szego_z{z:g}"]=e1/p_before_read_szego(a,z)
        out[a]=row; print(a, {k:round(v,5) for k,v in row.items()}); sys.stdout.flush()
    json.dump(out,open("rv_f.json","w"),indent=1)
