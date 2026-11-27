import sys, numpy as np
sys.path.insert(0,'../stepback/c1')
from c1_vacua import Vacuum, VACUA, bloch
class VacMu(Vacuum):
    def __init__(s,mu,K=256,dlt=(0.31,0.67)):
        n=np.arange(K); k1=2*np.pi*(n[:,None]+dlt[0])/K*np.ones((1,K)); k2=2*np.pi*(n[None,:]+dlt[1])/K*np.ones((K,1))
        E,U=np.linalg.eigh(bloch(k1,k2,False,0.0)); occ=(E<mu).astype(float); s.filling=occ.mean()
        Pk=np.einsum('...ai,...i,...bi->...ab',U,occ,U.conj()); G=np.fft.ifft2(Pk,axes=(0,1))
        X=np.arange(K); X=np.where(X>K//2,X-K,X); ph=np.exp(1j*2*np.pi*(dlt[0]*X[:,None]+dlt[1]*X[None,:])/K)
        s.G=G*ph[:,:,None,None]; s.K=K
def vac_for(vi):
    if vi=='mu': return VacMu(-2.0)
    flux,m=list(VACUA.values())[vi]; return Vacuum(flux,m)
