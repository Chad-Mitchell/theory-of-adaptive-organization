# Hostile review of C1: greedy rerun with alternative tie rule / window / vacuum (reuses c1_vacua.Vacuum for P; verified separately in rv_verify.py)
# Usage: python3 rv_greedy.py <vac idx 0-3 | mu=<val> for NN at chemical potential> <cheb> <nmax> <tie: lo|hi> <tag>
import sys, json, time, numpy as np
sys.path.insert(0,'../stepback/c1')
from c1_vacua import Vacuum, S_bits, VACUA, bloch
a=sys.argv; cheb=int(a[2]); nmax=int(a[3]); tie=a[4]; tag=a[5]
if a[1].startswith('mu='):
    mu=float(a[1][3:]); name=f"NN mu={mu}"
    class VacMu(Vacuum):
        def __init__(s,mu,K=256,dlt=(0.31,0.67)):
            n=np.arange(K); k1=2*np.pi*(n[:,None]+dlt[0])/K*np.ones((1,K)); k2=2*np.pi*(n[None,:]+dlt[1])/K*np.ones((K,1))
            E,U=np.linalg.eigh(bloch(k1,k2,False,0.0)); occ=(E<mu).astype(float); s.filling=occ.mean()
            Pk=np.einsum('...ai,...i,...bi->...ab',U,occ,U.conj()); G=np.fft.ifft2(Pk,axes=(0,1))
            X=np.arange(K); X=np.where(X>K//2,X-K,X); ph=np.exp(1j*2*np.pi*(dlt[0]*X[:,None]+dlt[1]*X[None,:])/K)
            s.G=G*ph[:,:,None,None]; s.K=K
    v=VacMu(mu); print("filling",v.filling,flush=True)
else:
    name,(flux,m)=list(VACUA.items())[int(a[1])]; v=Vacuum(flux,m)
T=[(0,0),(1,0),(0,1),(1,1)]; c0=(0.5,0.5); RMAX=30
S_T=S_bits(v.P(T)); I_of=lambda S: S_T+S_bits(v.P(S))-S_bits(v.P(T+S))
sel=[];gains=[];Icur=0.0;occupied=set(T);nties=[];t0=time.time()
def cands():
    out=set()
    for (x,y) in occupied:
        for dx in range(-cheb,cheb+1):
            for dy in range(-cheb,cheb+1):
                p=(x+dx,y+dy)
                if p not in occupied and (p[0]-c0[0])**2+(p[1]-c0[1])**2<=RMAX**2: out.add(p)
    return sorted(out)
while len(sel)<nmax:
    C=cands(); G=np.array([I_of(sel+[p])-Icur for p in C]); gm=G.max()
    idx=np.where(G>=gm-1e-10)[0]; nties.append(int(len(idx)))
    j=idx[0] if tie=='lo' else idx[-1]
    p=C[j]; sel.append(p); occupied.add(p); gains.append(float(G[j])); Icur+=G[j]
    if len(sel)%20==0: print(len(sel),round(G[j],5),round(time.time()-t0),flush=True)
json.dump({"vacuum":name,"cheb":cheb,"tie":tie,"S_T":S_T,"sel":sel,"gains":gains,"nties":nties},open(f"rv_{tag}.json","w"))
print("done",name,len(sel),time.time()-t0)
