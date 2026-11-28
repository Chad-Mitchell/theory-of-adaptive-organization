# Review: SR-b mixtures restricted to ODD polygons (the rule question: M3c uses the antipode for even n). OBSERVED, n<=401 odd + 1001, 2001.
import json, numpy as np
A={}
for f in ["srb_all.json","srb_big.json","srb_huge.json"]:
    A.update({int(k):np.array(v) for k,v in json.load(open("../stepback/sr_b/"+f)).items()})
odd={n:c for n,c in A.items() if n%2==1}
T=np.arange(1,4_000_001,dtype=float); dk=T*np.sin(np.pi/(2*T))**2
def EJ(c,q): L=len(c); Ts=np.arange(1,L+1); return float(np.sum((1-q)*q**(Ts-1)*c)+q**L*c[-1])
for q in [0.5,0.8,0.9,0.95,0.97,0.98,0.99]:
    ed=float(np.sum((1-q)*q**(T-1)*dk)); v={n:EJ(c,q) for n,c in odd.items()}; nb=min(v,key=v.get)
    print(f"q={q}: disk={ed:.6f} best odd n={nb} ({v[nb]:.6f}) -> {'odd polygon' if v[nb]<ed else 'disk'} cheaper, rel margin {(ed-v[nb])/ed:+.4f}")
