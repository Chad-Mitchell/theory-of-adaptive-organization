# Review rerun of the SR-b mixture sweep (OBSERVED), adding exact even-n curves from dpeven.c (curves/*.txt).
import json, glob, math, numpy as np
A={}
for f in ["srb_all.json","srb_big.json","srb_huge.json"]:
    A.update({int(k):np.array(v) for k,v in json.load(open("../stepback/sr_b/"+f)).items()})
src={n:"srb" for n in A}
for f in glob.glob("curves/*.txt"):
    n=int(f.split("/")[-1][:-4]); c=np.loadtxt(f)
    if n in A: assert np.max(np.abs(A[n][:len(c)]-c))<1e-12
    else: A[n]=c; src[n]="review"
Tbig=np.arange(1,40_000_001,dtype=float); dk=Tbig*np.sin(np.pi/(2*Tbig))**2
def EJ(n,q):
    c=A[n]; L=len(c); Ts=np.arange(1,L+1); return float(np.sum((1-q)*q**(Ts-1)*c)+q**L*c[-1])
def Edisk(q): return float(np.sum((1-q)*q**(Tbig-1)*dk))
print("max n computed:",max(A),"; count of n:",len(A))
print("(R1) geometric horizon p(T)=(1-q)q^(T-1)")
for q in [0.99,0.993,0.995,0.996,0.997,0.998,0.999]:
    ed=Edisk(q); vals={n:EJ(n,q) for n in A}; top=sorted(vals,key=vals.get)[:4]; nb=top[0]
    print(f"  q={q}: disk={ed:.8f} best n={nb} [{src[nb]}, n mod 4={nb%4}] ({vals[nb]:.8f}) next {top[1:]}; {'POLYGON' if vals[nb]<ed else 'disk'} cheaper, rel margin {(ed-vals[nb])/ed:+.6f}; best n interior? {nb<max(A)}")
def Jat(n,T): c=A[n]; return c[min(T,len(c))-1]
print("(R2) uniform horizon on 1..H")
for H in [200,500,1000,2000]:
    ed=np.mean([T*math.sin(math.pi/(2*T))**2 for T in range(1,H+1)])
    vals={n:np.mean([Jat(n,T) for T in range(1,H+1)]) for n in A}; nb=min(vals,key=vals.get)
    print(f"  H={H}: disk={ed:.8f} best n={nb} ({vals[nb]:.8f}); {'POLYGON' if vals[nb]<ed else 'disk'} cheaper, rel margin {(ed-vals[nb])/ed:+.6f}")
print("(R3) J*(T)/disk(T) with all n (even curves extend the T range)")
for T in [100,200,500,1000,2000]:
    nb=min(A,key=lambda n:Jat(n,T)); js=Jat(nb,T); dd=T*math.sin(math.pi/(2*T))**2
    print(f"  T={T}: n*={nb} J*/disk={js/dd:.6f}  1-ratio={1-js/dd:.6f}  2/T={2/T:.6f}")
