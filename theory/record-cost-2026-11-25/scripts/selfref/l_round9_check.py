from scipy.optimize import linprog
from scipy.special import sph_harm_y
import numpy as np
import os
exec('def fib'+open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'l_round9.py')).read().split('def fib')[1].split('sphere_capacity(feat_ball')[0])
rng=np.random.default_rng(1); S=feat_12(fib(4000))
octa=np.array([[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1.]])
ico=[]; p=(1+5**.5)/2
for a in (-1,1):
    for b in (-p,p): ico+= [[0,a,b],[a,b,0],[b,0,a]]
ico=np.array(ico,float); ico/=np.linalg.norm(ico,axis=1,keepdims=True)
for N in (5,6):
    cands=[octa[:N] if N==6 else octa[:5]]+[(lambda v: v/np.linalg.norm(v,axis=1,keepdims=True))(rng.normal(size=(N,3))) for _ in range(150)]
    if N==6: cands.append(ico[[0,1,2,3,4,5]])
    print('spin1+2 orbitope N=',N,'any distinguishable config:',any(distinguishable(feat_12(c),S) for c in cands))
# analytic tetrahedron effects
t=np.array([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1.]])/np.sqrt(3); n=fib(100000)
P=np.stack([(1+3*n@ti)**2/16 for ti in t],1)
print('analytic p_i=(1+3 n.t_i)^2/16: min',P.min(),' max |sum-1|',abs(P.sum(1)-1).max(),' p_i(t_j)=',np.round([[(1+3*tj@ti)**2/16 for tj in t] for ti in t],12).tolist())
