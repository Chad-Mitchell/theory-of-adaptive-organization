# PAPER: symmetric two-judge optimum and antisymmetric curvature at each locked setting, and the RI rival at three prices.
from paper_two_judge import symbest,antiH
import numpy as np
for w,wx in [(10,0.5),(10,1),(10,2),(3,1),(30,1)]:
    r=symbest(w,wx,'heat'); H,f0=antiH(r.x,w,wx,'heat')
    print('heat w',w,'wx',wx,'lng=%.3f c=%.4f J=%.5f'%(r.x[0],r.x[1],r.fun),'antisym eig',np.round(np.linalg.eigvalsh(H),4))
for lam in [0.25,1,4]:
    r=symbest(10,1,'ri',lam); H,f0=antiH(r.x,10,1,'ri',lam)
    print('ri lam',lam,'lng=%.3f c=%.4f J=%.5f'%(r.x[0],r.x[1],r.fun),'antisym eig',np.round(np.linalg.eigvalsh(H),4))
