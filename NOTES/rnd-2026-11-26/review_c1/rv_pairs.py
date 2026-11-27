# Is the greedy record at kappa_min a local optimum of J = I - kappa|S| against two-site additions and single-site swaps? (OBSERVED)
import sys, json, itertools, numpy as np
sys.path.insert(0,'../stepback/c1')
from c1_vacua import Vacuum, S_bits, VACUA
T=[(0,0),(1,0),(0,1),(1,1)]
for vi in range(4):
    d=json.load(open(f'../stepback/c1/c1_greedy_v{vi}_c3_n200.json')); sel=[tuple(p) for p in d['sel']]; g=d['gains']
    kap=min(g[:120]); n=0
    while g[n]>=kap: n+=1
    S=sel[:n]; full=set(T)|set(S); flux,m=list(VACUA.values())[vi]; v=Vacuum(flux,m)
    ST=S_bits(v.P(T)); I=lambda X: ST+S_bits(v.P(X))-S_bits(v.P(T+X)); I0=I(S)
    nb=lambda p:[(p[0]+1,p[1]),(p[0]-1,p[1]),(p[0],p[1]+1),(p[0],p[1]-1)]
    ring=sorted({(p[0]+dx,p[1]+dy) for p in full for dx in (-2,-1,0,1,2) for dy in (-2,-1,0,1,2)}-full)
    single={q:I(S+[q])-I0 for q in ring}
    top=sorted(ring,key=lambda q:-single[q])[:40]
    best=max(((I(S+[a,b])-I0,a,b) for a,b in itertools.combinations(top,2)),key=lambda t:t[0])
    # removal of single sites
    rem=min((I0-I([p for p in S if p!=q]),q) for q in S)
    print(f"V{vi+1}: kappa={kap:.5f} |S|={n}; best single add/kappa={max(single.values())/kap:.3f}; best pair add (top-40 singles) = {best[0]/kap:.3f} kappa for 2 sites at {best[1]},{best[2]} -> pair beats 2*kappa: {best[0]>2*kap}; cheapest single removal = {rem[0]/kap:.3f} kappa at {rem[1]}",flush=True)
