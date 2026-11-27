# Review check: is "uniform over horizons" enough to select the disk? Minimax ADDITIVE regret vs minimax RATIO.
# J*(T) >= 1/T (SR-b1(a)) and J*(2)=1/2 (hexagon attains it), so the disk's additive regret is >= disk(2)-J*(2) = 1/2,
# while for a polygon, sup_T [J(n,T)-J*(T)] <= sup_T [J(n,T)-1/T] (rigorous upper bound from exact curves).
import json, numpy as np, math
A={}
for f in ["srb_all.json","srb_big.json","srb_huge.json"]:
    A.update({int(k):np.array(v) for k,v in json.load(open("../stepback/sr_b/"+f)).items()})
disk=lambda T: T*math.sin(math.pi/(2*T))**2
print("disk additive regret >= disk(2)-J*(2) =", disk(2)-0.5)
for n in [6,10,22,50,100,201,301,401,1000,2400]:
    c=A[n]; L=len(c); Ts=np.arange(1,L+1)
    ub=max(np.max(c-1/Ts), c[-1])   # beyond saturation J(n,T)=c[-1] and 1/T -> 0
    ratio_lb=c[-1]*L  # ratio J(n,T)/J*(T) >= J(n,inf)/disk(T) -> unbounded; show J(n,inf)
    print(f"n={n}: sup_T [J(n,T)-J*(T)] <= {ub:.4f}  -> {'polygon strictly better than disk on additive minimax regret' if ub<0.5 else 'not shown'}; J(n,inf)={c[-1]:.4f}")
