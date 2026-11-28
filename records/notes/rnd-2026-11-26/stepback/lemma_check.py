# Sanity check of PIM_LEMMA bound (not a test): w_j(k)=sum_{t in T}|J_{j-t}(2k)|^2, T={-2..2}
import mpmath as mp
mp.mp.dps=40
T=range(-2,3)
def w(j,k): return sum(abs(mp.besselj(j-t,2*k))**2 for t in T)
for k in [2,4,8,16]:
    for kap in [1e-2,1e-4,1e-6]:
        Rstar=0
        for d in range(1,int(mp.e**2*k)+40):
            if w(2+d,k)>=kap: Rstar=d
        bound=max(mp.e**2*k, 0.5*mp.log(5/kap))
        print(f"k={k} kappa={kap:g} R*={Rstar} bound={float(bound):.2f} ok={Rstar<=bound}")
