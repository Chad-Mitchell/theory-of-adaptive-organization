# SR-b near q -> 1 (OBSERVED), all computed n (3..401, 300..1001 selected, 1400..2400 selected).
import json, math, numpy as np
A={}
for f in ["srb_all.json","srb_big.json","srb_huge.json"]:
    A.update({int(k):np.array(v) for k,v in json.load(open(f)).items()})
def EJ(n,q):
    c=A[n]; L=len(c); Ts=np.arange(1,L+1); return float(np.sum((1-q)*q**(Ts-1)*c)+q**L*c[-1])
T=np.arange(1,20_000_001,dtype=float); dk=T*np.sin(np.pi/(2*T))**2
def Edisk(q): return float(np.sum((1-q)*q**(T-1)*dk))
for q in [0.99,0.993,0.995,0.996,0.997]:
    ed=Edisk(q); vals={n:EJ(n,q) for n in A}; nb=min(vals,key=vals.get)
    top=sorted(vals,key=vals.get)[:3]
    print(f"q={q}: mean T {1/(1-q):.0f}; disk={ed:.7f}; best n={nb} ({vals[nb]:.7f}); next {top[1:]}; {'polygon' if vals[nb]<ed-1e-12 else 'disk'} cheaper, margin {(ed-vals[nb])/ed:+.5f}; largest n computed = {max(A)}")
