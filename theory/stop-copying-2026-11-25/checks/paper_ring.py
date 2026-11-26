# PAPER: 8-judge ring, local analysis at the best symmetric (uniform) design only.
import numpy as np
from scipy.linalg import solve_continuous_lyapunov as lyap
from scipy.optimize import minimize_scalar
n=8; D=1.0
def build(lg,cp,cm):
    g=np.exp(lg); A=np.zeros((n,n))
    for i in range(n):
        A[i,i]=g[i]; A[i,(i+1)%n]-=g[i]*cp[i]; A[i,(i-1)%n]-=g[i]*cm[i]
    return A,g
def Jtot(v,w,wx):
    lg,cp,cm=v[:n],v[n:2*n],v[2*n:]
    A,g=build(lg,cp,cm)
    if np.any(np.linalg.eigvals(A).real<=0): return 1e9
    S=lyap(-A,-2*D*np.eye(n)); J=0
    for i in range(n):
        u=np.zeros(n); u[i]=1; u[(i+1)%n]-=cp[i]; u[(i-1)%n]-=cm[i]
        Q=g[i]**2*(u@S@u)-D*g[i]
        e1=S[i,i]-2*S[i,(i+1)%n]+S[(i+1)%n,(i+1)%n]; e2=S[i,i]-2*S[i,(i-1)%n]+S[(i-1)%n,(i-1)%n]
        J+=Q+w*0.5*(e1+e2)+wx*S[i,i]
    return J
for w,wx in [(10,0.5),(10,1),(10,2),(3,1),(30,1)]:
    f=lambda c: Jtot(np.r_[np.full(n,5.0),np.full(n,c),np.full(n,c)],w,wx)
    r=minimize_scalar(f,bounds=(0,0.4995),method='bounded')
    x0=np.r_[np.full(n,5.0),np.full(n,r.x),np.full(n,r.x)]
    # Hessian over free directions (lg<=5 cap binding: use only c directions + lg decreases are outward-cost; report c-block)
    h=1e-4; idx=list(range(n,3*n)); m=len(idx); H=np.zeros((m,m)); f0=Jtot(x0,w,wx)
    for a in range(m):
        for b in range(a,m):
            def F(da,db):
                x=x0.copy(); x[idx[a]]+=da; x[idx[b]]+=db; return Jtot(x,w,wx)
            H[a,b]=H[b,a]=(F(h,h)-F(h,-h)-F(-h,h)+F(-h,-h))/(4*h*h)
    gl=[(Jtot(x0-np.eye(3*n)[i]*1e-4,w,wx)-f0)/(-1e-4) for i in range(n)]
    print('w',w,'wx',wx,'uniform c=%.4f J=%.5f'%(r.x,f0),'c-block Hessian min eig %.4g'%np.linalg.eigvalsh(H).min(),'dJ/dlng (cap side) max %.4g'%max(gl))
