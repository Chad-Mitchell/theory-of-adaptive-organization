# PAPER: local analysis at the best SYMMETRIC design only (no asymmetric search).
import numpy as np
from scipy.linalg import solve_continuous_lyapunov as lyap
from scipy.optimize import minimize
from scipy.integrate import quad
D=1.0
def Sig(lgA,cA,lgB,cB):
    gA,gB=np.exp(lgA),np.exp(lgB)
    A=np.array([[gA,-gA*cA],[-gB*cB,gB]])
    if np.linalg.det(A)<=0 or np.trace(A)<=0: return None,None
    return lyap(-A,-np.diag([2*D,2*D])),A
def mirate(A):
    N=np.diag([2*D,2*D])
    def f(w):
        M=np.linalg.inv(1j*w*np.eye(2)+A); S=M@N@M.conj().T
        return -np.log(max(1-abs(S[0,1])**2/(S[0,0].real*S[1,1].real),1e-300))
    return quad(f,0,np.inf,limit=400)[0]/(2*np.pi)
def Jtot(v,w,wx,kind,lam=1.0):
    lgA,cA,lgB,cB=v; S,A=Sig(lgA,cA,lgB,cB)
    if S is None: return 1e9
    gA,gB=np.exp(lgA),np.exp(lgB)
    L=S[0,0]-2*S[0,1]+S[1,1]
    QA=gA**2*(S[0,0]-2*cA*S[0,1]+cA**2*S[1,1])-D*gA
    QB=gB**2*(S[1,1]-2*cB*S[0,1]+cB**2*S[0,0])-D*gB
    info = QA+QB if kind=='heat' else 2*lam*mirate(A)
    return info+2*w*L+wx*(S[0,0]+S[1,1])
def symbest(w,wx,kind,lam=1.0):
    best=None
    for s in [(1,0.5),(3,0.8),(4.9,0.9),(0,0.2)]:
        r=minimize(lambda u:Jtot((u[0],u[1],u[0],u[1]),w,wx,kind,lam),s,method='L-BFGS-B',bounds=((-3,5),(0,0.999)))
        if best is None or r.fun<best.fun: best=r
    return best
def antiH(x,w,wx,kind,lam=1.0,h=1e-3):
    lg,c=x
    def f(a,b): return Jtot((lg+a,c+b,lg-a,c-b),w,wx,kind,lam)
    f0=f(0,0)
    Haa=(f(h,0)-2*f0+f(-h,0))/h**2; Hbb=(f(0,h)-2*f0+f(0,-h))/h**2
    Hab=(f(h,h)-f(h,-h)-f(-h,h)+f(-h,-h))/(4*h*h)
    # one-sided c if at bound
    return np.array([[Haa,Hab],[Hab,Hbb]]),f0
if __name__=="__main__":
     for kind in ['heat','ri']:
      for wx in [0.5,1,2]:
        r=symbest(10,wx,kind,lam=1.0)
        H,f0=antiH(r.x,10,wx,kind)
        print(kind,'wx',wx,'sym best lng=%.3f c=%.4f J=%.4f'%(r.x[0],r.x[1],r.fun),'antisym Hessian eig',np.round(np.linalg.eigvalsh(H),4))
