# Hostile review: k=5 local search (reuses c12cg/prec.py's Poly; only extends k), random starts + lifted k=4 optimum.
import sys, json; sys.path.insert(0,'../stepback/c12cg')
from prec import Poly, local
n=int(sys.argv[1]); P=Poly(n)
e4=json.load(open(f"../stepback/c12cg/prec_n{n}.json"))["k4_local"][1]
lift=[[e4[s>>1] for s in range(32)],[e4[s&15] for s in range(32)]]
v,e=local(P,5,starts=int(sys.argv[2]),seed=11,init=lift); print(n,"k=5 local",round(v,9),e,flush=True)
