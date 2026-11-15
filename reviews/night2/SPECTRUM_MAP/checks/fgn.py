"""Exact fGn / fBm generation by Davies-Harte (circulant embedding). Davies & Harte 1987, Biometrika 74:95."""
import numpy as np
def fgn_acov(k,H):
    k=np.abs(k).astype(float)
    return 0.5*((k+1)**(2*H)-2*k**(2*H)+np.abs(k-1)**(2*H))
def fgn(n,H,rng,size=1):
    m=2*n
    r=fgn_acov(np.arange(n+1),H)
    c=np.concatenate([r,r[-2:0:-1]])          # length 2n
    lam=np.fft.fft(c).real
    if lam.min()< -1e-10: raise ValueError("embedding not PSD")
    lam=np.clip(lam,0,None)
    Z=rng.standard_normal((size,m))+1j*rng.standard_normal((size,m))
    W=np.fft.fft(np.sqrt(lam/m)*Z,axis=1)
    return W.real[:,:n]                        # each row exact fGn(H), unit variance
def fbm(n,H,rng,size=1):
    x=fgn(n,H,rng,size)
    return np.concatenate([np.zeros((size,1)),np.cumsum(x,axis=1)],axis=1)  # B(0..n), Var B(k)=k^{2H}
if __name__=="__main__":
    rng=np.random.default_rng(1)
    for H in (0.25,0.5,0.75):
        B=fbm(4096,H,rng,size=400)
        for k in (1,16,256,2048):
            v=np.mean(B[:,k]**2); print(f"H={H} k={k} Var/k^2H={v/k**(2*H):.3f}")
