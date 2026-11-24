"""Reviewer check for the sphere follow-up: quantum spin-j covariant readout laws are nonnegative band-limited
(l <= N-1 = 2j) densities with max <= N * mean; for N>=3 the classical set of such densities is strictly larger
(witness rho = I - 2|m=0><m=0| for j=1); for N=2 the two sets coincide (Bloch ball)."""
import numpy as np
from scipy.special import sph_harm_y
from scipy.linalg import expm
rng = np.random.default_rng(7)
def spin_ops(N):
    j=(N-1)/2; m=j-np.arange(N)
    Jp=np.diag(np.sqrt(j*(j+1)-m[1:]*(m[1:]+1)),1); Jx=(Jp+Jp.T)/2; Jy=(Jp-Jp.T)/(2j); Jz=np.diag(m)
    return Jx,Jy,Jz
def coh(N,th,ph):
    Jx,Jy,Jz=spin_ops(N); v=np.zeros(N,complex); v[0]=1
    return expm(-1j*ph*Jz)@expm(-1j*th*Jy)@v
th=np.arccos(rng.uniform(-1,1,3000)); ph=rng.uniform(0,2*np.pi,3000)
def band_resid(N,f):
    cols=[sph_harm_y(l,m,th,ph) for l in range(N) for m in range(-l,l+1)]
    A=np.array(cols).T; c,*_=np.linalg.lstsq(A,f.astype(complex),rcond=None); return np.max(np.abs(A@c-f))
for N in [2,3,4,6]:
    worst_ratio=0; worst_band=0
    for _ in range(30):
        X=rng.normal(size=(N,N))+1j*rng.normal(size=(N,N)); rho=X@X.conj().T; rho/=np.trace(rho).real
        Y=rng.normal(size=(N,N))+1j*rng.normal(size=(N,N)); zeta=np.diag(rng.dirichlet(np.ones(N))).astype(complex)  # covariant POVM on S2 needs a seed commuting with Jz
        Jx,Jy,Jz=spin_ops(N)
        f=[]
        for a,b in zip(th,ph):
            U=expm(-1j*b*Jz)@expm(-1j*a*Jy); f.append(np.real(np.trace(rho@U@zeta@U.conj().T)))
        f=np.array(f); worst_ratio=max(worst_ratio,f.max()/f.mean()); worst_band=max(worst_band,band_resid(N,f))
    print(f"N={N}: random states x random covariant seeds: max(density)/mean <= {worst_ratio:.3f} (bound N={N}); band-limit l<=N-1 fit residual {worst_band:.1e}")
# witness N=3
N=3; Jx,Jy,Jz=spin_ops(N); e0=np.zeros(N); e0[1]=1
rho=np.eye(N)-2*np.outer(e0,e0)
Q=np.array([np.real(np.vdot(coh(N,a,b),rho@coh(N,a,b))) for a,b in zip(th,ph)])
print(f"N=3 witness rho=I-2|0><0|: eigenvalues {np.linalg.eigvalsh(rho)}, trace {np.trace(rho)}; Husimi min {Q.min():.4f} (>=0), max/mean {Q.max()/Q.mean():.3f} (<=3); band residual {band_resid(3,Q):.1e}")
print("  -> a nonnegative l<=2 density obeying the max<=N*mean cap that is NOT the Husimi function of any quantum state; classical restricted sphere rotor's law set strictly contains quantum's for N=3.")
print("Counts: sum_{l<=N-1}(2l+1) =", {N: sum(2*l+1 for l in range(N)) for N in [2,3,4,6,8]})
