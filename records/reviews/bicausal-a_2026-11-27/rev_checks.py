# Second read: independent numeric checks (no sympy, no ba_lib). Own Lyapunov via Kronecker solve.
import numpy as np
def lyap(F,Dv):
    n=F.shape[0]; I=np.eye(n)
    A=np.kron(I,F)+np.kron(F,I); q=-2*np.diag(Dv).reshape(-1)
    S=np.linalg.solve(A,q).reshape(n,n); return (S+S.T)/2
# --- BA-T1: Delta by central finite differences of numeric W2 costs
def costs(gam,c,g,wx,w=10,ww=10,a=1,D=1,DM=1):
    S=lyap(np.array([[-a,a*g],[gam*c,-gam]]),[D,DM]); xx,xm,mm=S[0,0],S[0,1],S[1,1]
    ex=xx-2*g*xm+g*g*mm; em=mm-2*c*xm+c*c*xx
    Jm=gam**2*em-DM*gam+w*(xx-2*xm+mm)+wx*xx; Jw=a*a*ex-D*a+ww*ex+wx*xx
    return Jm,Jw
def cross(f,i,x,h=1e-4):
    # d2/dx_i dg, x=(gam,c,g)
    def F(dx,dg):
        y=list(x); y[i]+=dx; y[2]+=dg; return np.array(f(*y))
    return (F(h,h)-F(h,-h)-F(-h,h)+F(-h,-h))/(4*h*h)
for wx,want in [(0.5,27462244677/1506922300),(1,5789210497/301384460),(2,31913668101/1506922300)]:
    x=(19/7,-0.5,3.0); f=lambda gam,c,g: costs(gam,c,g,wx)
    a0=cross(f,0,x); a1=cross(f,1,x)  # each gives (Jm,Jw)
    Delta=a0[0]*a1[1]-a1[0]*a0[1]
    print("BA-T1 w_x=%g: finite-diff Delta %.5f vs exact %.5f"%(wx,Delta,want))
# --- BA-T2: independent heat/error of the confirmed designs read from ba_t2.out
import re
txt=open('theory/bicausal-a-2026-11-27/checks/ba_t2.out').read()
blocks=re.split(r'stake w = ',txt)[1:]
for w,K in [(3,32),(10,24),(100,24)]:
    b=[x for x in blocks if x.startswith('%g:'%w)][0]
    row=[l for l in b.splitlines() if re.match(r'\s+%d\s'%K,l)][0].split()
    lb0,lD0,lb1,lD1=map(float,row[3:7])
    b0,D0,b1,D1=np.exp([lb0,lD0,lb1,lD1])
    F=np.array([[-1,0,0],[b0,-b0,0],[0,b1,-b1]],float); S=lyap(F,[1,D0,D1])
    # heat = <f^2>/D + <df/dx>, f0=-b0(M0-X), f1=-b1(M1-M0)
    e0=S[1,1]-2*S[0,1]+S[0,0]; e1=S[2,2]-2*S[1,2]+S[1,1]
    Q0=b0*b0*e0/D0-b0; Q1=b1*b1*e1/D1-b1; eps=1-S[0,2]**2/S[2,2]
    P=Q0/K+Q1+w*eps; Jd=2*np.sqrt(w)-1
    # entropy-production cross-check: total EP rate = tr(F^T D^-1 F S)+tr(F) per coordinate sum (all baths kT=1)
    Dm=np.diag([1,D0,D1]); EP=np.trace(F.T@np.linalg.inv(Dm)@F@S)+np.trace(F)
    print("BA-T2 w=%g K=%d: per-member %.6f (table %s), direct %.6f, Q0+Q1 %.6f vs total EP %.6f"%(w,K,P,row[1],Jd,Q0+Q1,EP))
for b0,D0 in [(0.7,0.3),(5.0,0.08),(2.0,1.0)]:
    S=lyap(np.array([[-1,0],[b0,-b0]],float),[1,D0]); e0=S[1,1]-2*S[0,1]+S[0,0]
    print("Q0 Lyapunov %.10f closed %.10f"%(b0*b0*e0/D0-b0, b0*b0/((1+b0)*D0)))
