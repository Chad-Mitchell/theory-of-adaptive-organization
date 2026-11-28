# Cross-checks with known answers (C12CG §8.3): (a) triangle = classical 3-simplex: optimiser == direct
# fine-grained-read value for every encoding, k=1..3; (b) square k=2 = 2 bits; (c) >= committed binary-read values.
import itertools, numpy as np
from prec import Poly, exhaustive
def H(p): p=np.asarray(p,float); p=p[p>0]; return float(-(p*np.log2(p)).sum())
P=Poly(3); print("triangle BFS (extreme measurements):",len(P.L))
maxdiff=0; bestdirect={}
for k in (1,2,3):
    strings=list(itertools.product((0,1),repeat=k)); best=0
    for enc in itertools.product(range(3),repeat=2**k):
        direct=0
        for j in range(k):
            joint=np.zeros((2,3))
            for s,v in zip(strings,enc): joint[s[j],v]+=1/len(strings)
            direct+=H(joint.sum(0))+1-H(joint.ravel())
        opt=P.total(np.array([enc]),k)[0]; maxdiff=max(maxdiff,abs(opt-direct)); best=max(best,direct)
    bestdirect[k]=best
print("(a) triangle: max |LP optimiser - direct fine-grained| over all encodings k=1..3:",maxdiff,"; best direct per k:",{k:round(v,6) for k,v in bestdirect.items()})
S=Poly(4); print("(b) square k=2 exhaustive:",exhaustive(S,2))
