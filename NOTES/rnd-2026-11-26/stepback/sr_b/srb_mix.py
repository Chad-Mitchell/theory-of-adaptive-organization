# SR-b mixture analysis (OBSERVED numerics) using srb_J.json. Horizon T>=1, geometric p(T)=(1-q) q^(T-1).
import json, math, numpy as np
D=json.load(open("srb_J.json")); Tmax=D["Tmax"]; J={int(k):np.array(v) for k,v in D["J"].items()}
disk=lambda T: T*math.sin(math.pi/(2*T))**2
print("(A) where each polygon beats the disk: T-range with J(n,T) < disk(T) (strict, 1e-12), T=1..Tmax; saturation means J(n,T)=J(n,inf) beyond")
for n in [5,7,9,15,21,31,41,61,81,101,121,161,201,8,16,40,60]:
    Jn=J[n]; win=[T for T in range(1,Tmax+1) if Jn[T-1]<disk(T)-1e-12]
    sat=int(np.argmax(Jn<=Jn[-1]+1e-12))+1
    cont = win==list(range(win[0],win[-1]+1)) if win else None
    print(f"   n={n:3d}: wins at T in [{win[0] if win else '-'}, {win[-1] if win else '-'}] contiguous={cont} count={len(win)}; sat_T={sat}; J(n,inf)={Jn[-1]:.5f}; first T with disk<J(n,inf): {next(T for T in range(1,100000) if disk(T)<Jn[-1]-1e-12)}")
def EJ(curve, q, Tcut=200000):
    # sum_{T>=1} (1-q) q^{T-1} curve(T); curve constant = curve[-1] beyond Tmax
    s=0.0; w=1-q
    for T in range(1,Tmax+1): s+=w*q**(T-1)*curve[T-1]
    s+=q**Tmax*curve[-1]
    return s
def Edisk(q, Tcut=None):
    s=0.0; T=1; w=1-q; tail=1.0
    while True:
        p=w*q**(T-1); s+=p*disk(T); tail-=p
        if tail<1e-15 or T>2_000_000: break
        T+=1
    return s
print("(B) horizon mixture, price-free (ROUND10's kappa-per-affine-dimension price is equal for all n-gons and the disk): best polygon vs disk")
for q in [0.0,0.3,0.5,0.7,0.8,0.9,0.95,0.97,0.98,0.99]:
    ed=Edisk(q); vals={n:EJ(J[n],q) for n in J}; nb=min(vals,key=vals.get)
    print(f"   q={q:5.3f} mean T={1/(1-q):7.1f}: disk={ed:.6f}  best n={nb:3d} cost={vals[nb]:.6f}  polygon strictly cheaper: {vals[nb]<ed-1e-12}  margin={(ed-vals[nb])/ed:+.4f}")
