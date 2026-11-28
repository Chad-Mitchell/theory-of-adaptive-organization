# K-grid convergence of the C1 V1/V3 correlations and of the greedy gains along the published sequence (OBSERVED)
import sys, json, numpy as np
sys.path.insert(0,'../stepback/c1')
from c1_vacua import Vacuum, S_bits
T=[(0,0),(1,0),(0,1),(1,1)]
for vi,(flux,m) in [(0,(False,0.0)),(2,(True,0.0))]:
    d=json.load(open(f'../stepback/c1/c1_greedy_v{vi}_c3_n200.json')); sel=[tuple(p) for p in d['sel']][:130]; g=np.array(d['gains'][:130])
    pts=T+sel
    Ps={K:Vacuum(flux,m,K=K) for K in (256,1024)}
    P256=Ps[256].P(pts); P1k=Ps[1024].P(pts)
    print(f"v{vi}: max|P256-P1024| over T+first130 = {np.abs(P256-P1k).max():.2e}; max|Im P256| {np.abs(P256.imag).max():.2e}; max|Im P1024| {np.abs(P1k.imag).max():.2e}")
    def gains(v):
        ST=S_bits(v.P(T)); I=lambda S: ST+S_bits(v.P(S))-S_bits(v.P(T+S)) if S else 0.0
        Is=[I(sel[:n]) for n in range(0,131)]; return np.diff(Is)
    g1k=gains(Ps[1024]); g256=gains(Ps[256])
    rel=np.abs(g1k-g256)/np.abs(g256)
    print(f"v{vi}: gains along sequence: stored-vs-recomputed K256 max diff {np.abs(g256-g).max():.1e}; K256 vs K1024 max rel diff {rel.max():.2e} (at step {rel.argmax()+1}, gain {g256[rel.argmax()]:.5f}); median {np.median(rel):.1e}")
