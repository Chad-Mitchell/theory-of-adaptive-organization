# C1: free-fermion square-lattice vacua at half filling (infinite plane via a twisted k-grid), 2x2 magnetic/mass cell.
# P(i,j) = <i|P_occ|j>; entropies of regions from eigenvalues of P restricted (same spectrum as <c_i^dag c_j>).
import numpy as np
SUB=lambda x,y:(x%2)+2*(y%2)
def bloch(k1,k2,flux,m):
    # k1,k2: arrays of cell momenta. Returns H(k) of shape (...,4,4). Cell = 2x2 sites; site (x,y), x,y in {0,1}.
    H=np.zeros(k1.shape+(4,4),complex)
    for x in range(2):
        for y in range(2):
            a=SUB(x,y)
            H[...,a,a]+=m*(-1)**(x+y)
            # x-bond to (x+1,y): t=1 ; y-bond to (x,y+1): t=(-1)^x if flux else 1
            for (dx,dy,t) in [(1,0,1.0),(0,1,(-1.0)**x if flux else 1.0)]:
                x2,y2=x+dx,y+dy; b=SUB(x2,y2); D1,D2=x2//2,y2//2   # cell displacement
                ph=np.exp(1j*(k1*D1+k2*D2))
                H[...,a,b]+=-t*ph; H[...,b,a]+=-t*np.conj(ph)
    return H
class Vacuum:
    def __init__(s,flux,m,K=256,dlt=(0.31,0.67)):
        n=np.arange(K); k1=2*np.pi*(n[:,None]+dlt[0])/K*np.ones((1,K)); k2=2*np.pi*(n[None,:]+dlt[1])/K*np.ones((K,1))
        E,U=np.linalg.eigh(bloch(k1,k2,flux,m))
        occ=(E<0).astype(float); s.minabsE=np.abs(E).min(); s.filling=occ.mean()
        Pk=np.einsum('...ai,...i,...bi->...ab',U,occ,U.conj())
        # G_ab(X,Y) = (1/K^2) sum_k e^{i k.R} P_ab(k); k = 2pi(n+d)/K -> phase e^{i 2pi d X/K} * ifft2
        G=np.fft.ifft2(Pk,axes=(0,1))   # includes 1/K^2 and e^{+i 2pi n X/K}
        X=np.arange(K); X=np.where(X>K//2,X-K,X)
        ph=np.exp(1j*2*np.pi*(dlt[0]*X[:,None]+dlt[1]*X[None,:])/K)
        s.G=G*ph[:,:,None,None]; s.K=K
    def P(s,sites):
        xs=np.array([p[0] for p in sites]); ys=np.array([p[1] for p in sites])
        cx,cy=xs//2,ys//2; a=(xs%2)+2*(ys%2)
        DX=(cx[:,None]-cx[None,:])%s.K; DY=(cy[:,None]-cy[None,:])%s.K
        return s.G[DX,DY,a[:,None],a[None,:]]
def S_bits(P):
    if len(P)==0: return 0.0
    l=np.clip(np.linalg.eigvalsh(P),1e-15,1-1e-15); return float(-np.sum(l*np.log2(l)+(1-l)*np.log2(1-l)))
VACUA={"V1 NN critical (Fermi surface)":(False,0.0),"V2 NN + mass 0.5 (gapped)":(False,0.5),
       "V3 pi-flux critical (Dirac)":(True,0.0),"V4 pi-flux + mass 0.5 (gapped Dirac)":(True,0.5)}
