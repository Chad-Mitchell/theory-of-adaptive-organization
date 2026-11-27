# Sanity check (not a test) of the Kapteyn-based bound in PIM_LEMMA.md.
import mpmath as mp
mp.mp.dps=40
T=range(-2,3)
def w(j,k): return sum(abs(mp.besselj(j-t,2*k))**2 for t in T)
def G(n,k):  # n*(arccosh(n/2k) - sqrt(1-(2k/n)^2)), n>=2k
    return n*(mp.acosh(mp.mpf(n)/(2*k)) - mp.sqrt(1-(mp.mpf(2*k)/n)**2))
for k in [2,4,8,16,32]:
    for kap in [1e-2,1e-4,1e-6]:
        Rstar=max([d for d in range(1,4*k+60) if w(2+d,k)>=kap] or [0])
        # bound: smallest d>=2k with 2*G(d,k) > ln(|T|/kap); every larger d excluded since G increasing
        d=2*k
        while not (2*G(d,k) > mp.log(5/kap)): d+=1
        asym=float(2*k + (2*k)**(1/3)*2**(-1/3)*(0.75*mp.log(5/kap))**(2/3))
        print(f"k={k:2d} kappa={kap:g} R*={Rstar:3d} bound={d:3d} ok={Rstar<d} asym~{asym:.1f}")
# direct check of Kapteyn on sample points
bad=0
for n in range(1,120):
    for k in [1,2,4,8,16,32]:
        x=2*k
        if n>=x:
            z=mp.mpf(x)/n; b=(z**n*mp.e**(n*mp.sqrt(1-z*z)))/(1+mp.sqrt(1-z*z))**n
            if abs(mp.besselj(n,x))>b*(1+1e-30): bad+=1
print("Kapteyn violations:",bad)
