# Gate reader paper check (not T1): KKT local check at the best symmetric design, feasible directions only.
import sys; sys.path.insert(0,'.')
import numpy as np
from paper_two_judge import symbest, antiH, Jtot
for w,wx in [(10,0.5),(10,1),(10,2),(3,1),(30,1)]:
    r=symbest(w,wx,'heat'); lg,c=r.x; x0=np.array([lg,c,lg,c]); f0=Jtot(x0,w,wx,'heat')
    H,_=antiH(r.x,w,wx,'heat'); ev,V=np.linalg.eigh(H)
    h=1e-4
    gA=(f0-Jtot(x0-np.array([h,0,0,0]),w,wx,'heat'))/h   # backward (feasible) dJ/dlnγ_A
    gB=(f0-Jtot(x0-np.array([0,0,h,0]),w,wx,'heat'))/h
    # (cA,cB) Hessian at lnγ fixed on cap
    def F(a,b): return Jtot(x0+np.array([0,a,0,b]),w,wx,'heat')
    Hc=np.zeros((2,2)); e=[np.array([1,0]),np.array([0,1])]
    for i in range(2):
        for j in range(2):
            d1,d2=e[i]*h,e[j]*h
            Hc[i,j]=(F(*(d1+d2))-F(*(d1-d2))-F(*(-d1+d2))+F(*(-d1-d2)))/(4*h*h)
    print(f"w {w} wx {wx}: antiH eig {ev.round(4)} small-eig vector (dlng,dc)={V[:,0].round(4)} | one-sided dJ/dlng_A={gA:.5f} dJ/dlng_B={gB:.5f} | (cA,cB) Hessian eig {np.linalg.eigvalsh(Hc).round(3)} | anti-c curvature {(Hc[0,0]-2*Hc[0,1]+Hc[1,1]):.2f}")
# leader-copier slice, both on cap (analytic): J=g c^2/2 + (1/g)[2w(2-c+c^2/2)+wx(2+c^2/2)]
g=np.exp(5)
for w,wx in [(10,1),(3,1)]:
    cs=np.linspace(0,0.2,200001); J=g*cs**2/2+(2*w*(2-cs+cs**2/2)+wx*(2+cs**2/2))/g
    i=J.argmin(); print('leader-copier on cap w',w,'wx',wx,'best cB=%.5f J=%.5f'%(cs[i],J[i]),'numeric check',Jtot((5,0,5,cs[i]),w,wx,'heat'))
