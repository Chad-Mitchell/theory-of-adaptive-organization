"""Expected-information SE(alpha) of the 3-parameter Whittle fit (own code) vs the proposed rule 1/sqrt(M), M = n*min(wc,pi)/(2pi)."""
import numpy as np, sys
sys.path.insert(0, '.')
from ownlib import f_inc
def se(a, wc, n, fix_noise=False):
    w = 2*np.pi*np.arange(1, (n-1)//2+1)/n; th = np.array([0.0, a, -a*np.log(wc)])
    G = []
    for i in range(3):
        e = np.zeros(3); e[i] = 1e-5
        G.append((np.log(f_inc(w, *(th+e)))-np.log(f_inc(w, *(th-e))))/2e-5)
    G = np.array(G)
    if fix_noise: G = G[:2]
    return np.sqrt(np.linalg.inv(G@G.T)[1,1])
print("alpha  wc     n      M     SE(3-par)  1/sqrt(M)  ratio  | SE if noise known/absent")
for a in (1.4, 2.0, 2.6):
    for wc in (0.05, 0.5, 3.0, 50.0, 1e4):
        for n in (8192, 32768):
            M = n*min(wc, np.pi)/(2*np.pi); s = se(a, wc, n); s2 = se(a, wc, n, True)
            print(f"{a:4} {wc:7} {n:6} {M:7.0f}  {s:.4f}    {1/np.sqrt(M):.4f}    {s*np.sqrt(M):.2f}  | {s2:.4f} ({s2*np.sqrt(M):.2f})")
