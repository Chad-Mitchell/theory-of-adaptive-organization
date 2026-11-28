# (a) genuine n=2 species greedy (block-diagonal correlation matrix) vs n=1 order; (b) anisotropic pi-flux single-site MI contour aspect vs v_x/v_y (OBSERVED)
import sys, math, numpy as np, scipy.linalg as sl
sys.path.insert(0,'../stepback/c1')
from c1_vacua import Vacuum, S_bits, VACUA, SUB
T=[(0,0),(1,0),(0,1),(1,1)]; c0=(0.5,0.5)
v=Vacuum(True,0.0)
def run(n,steps):
    Pn=lambda R: sl.block_diag(*([v.P(R)]*n)) if R else np.zeros((0,0))
    ST=S_bits(Pn(T)); I=lambda S: ST+S_bits(Pn(S))-S_bits(Pn(T+S)) if S else 0.0
    sel=[];g=[];occ=set(T);Ic=0.0
    for _ in range(steps):
        C=sorted({(x+dx,y+dy) for (x,y) in occ for dx in range(-3,4) for dy in range(-3,4)}-occ)
        G=[I(sel+[p])-Ic for p in C]; j=int(np.argmax(np.array(G)>=max(G)-1e-10*n)); sel.append(C[j]); occ.add(C[j]); g.append(G[j]); Ic+=G[j]
    return sel,np.array(g)
s1,g1=run(1,40); s2,g2=run(2,40)
print(f"(a) V3, 40 greedy steps: same order n=2 vs n=1: {s1==s2}; max|g2-2*g1| = {np.abs(g2-2*g1).max():.1e}",flush=True)
def bloch_aniso(k1,k2,ty):
    H=np.zeros(k1.shape+(4,4),complex)
    for x in range(2):
        for y in range(2):
            a=SUB(x,y)
            for (dx,dy,t) in [(1,0,1.0),(0,1,ty*(-1.0)**x)]:
                x2,y2=x+dx,y+dy; b=SUB(x2,y2); ph=np.exp(1j*(k1*(x2//2)+k2*(y2//2))); H[...,a,b]+=-t*ph; H[...,b,a]+=-t*np.conj(ph)
    return H
class VA(Vacuum):
    def __init__(s,ty,K=256,dlt=(0.31,0.67)):
        n=np.arange(K); k1=2*np.pi*(n[:,None]+dlt[0])/K*np.ones((1,K)); k2=2*np.pi*(n[None,:]+dlt[1])/K*np.ones((K,1))
        E,U=np.linalg.eigh(bloch_aniso(k1,k2,ty)); occ=(E<0).astype(float)
        Pk=np.einsum('...ai,...i,...bi->...ab',U,occ,U.conj()); G=np.fft.ifft2(Pk,axes=(0,1))
        X=np.arange(K); X=np.where(X>K//2,X-K,X); ph=np.exp(1j*2*np.pi*(dlt[0]*X[:,None]+dlt[1]*X[None,:])/K); s.G=G*ph[:,:,None,None]; s.K=K
for ty in (1.0,0.5):
    va=VA(ty); ST=S_bits(va.P(T)); I=lambda B: ST+S_bits(va.P(B))-S_bits(va.P(T+B))
    def prof(axis):
        rs=np.arange(3,41); out=[]
        for r in rs:
            # wedge-average over the sites at distance r+-0.75 within 12 deg of the axis (x or y)
            vals=[]
            for x in range(-r-2,r+3):
                for y in range(-r-2,r+3):
                    d=math.hypot(x-.5,y-.5); a=math.degrees(math.atan2(y-.5,x-.5))%180
                    if abs(d-r)>0.75: continue
                    if (axis=='x' and (a<=12 or a>=168)) or (axis=='y' and abs(a-90)<=12): vals.append(I([(x,y)]))
            out.append(np.mean(vals))
        return rs,np.array(out)
    rx,Ix=prof('x'); ry,Iy=prof('y')
    res=[]
    for r in (4,6,8,12,16,24):
        # radius along x where MI equals MI along y at radius r (log-log interpolation)
        target=Iy[list(ry).index(r)]
        lx=np.interp(-np.log(target),-np.log(Ix),np.log(rx)); res.append(f"r_y={r}: r_x/r_y={math.exp(lx)/r:.2f}")
    print(f"(b) pi-flux t_x=1, t_y={ty} (predicted aspect v_x/v_y={1/ty:.2f}): equal-MI contour aspect: "+'; '.join(res),flush=True)
