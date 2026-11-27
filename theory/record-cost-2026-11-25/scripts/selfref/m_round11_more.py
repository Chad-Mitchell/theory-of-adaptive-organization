# Round 11-M: more parts (affinely regular hexagon, cube) and the leverage diagnostic on max composites.
import sys, os, itertools, time
sys.path.insert(0, os.path.dirname(__file__))
from m_round11_lib import *
from m_round11_lib import _out as out0
S['hexagon']=dict(V=[[1,1,0],[1,0,1],[1,-1,1],[1,-1,0],[1,0,-1],[1,1,-1]],
                  E=[[1,-1,0],[1,1,0],[1,0,-1],[1,0,1],[1,-1,-1],[1,1,1]], u=[1,0,0])
S['cube']=dict(V=[[1]+list(s) for s in itertools.product((1,-1),repeat=3)],
               E=[[1]+[sg if k==i else 0 for k in range(3)] for i in range(3) for sg in (1,-1)], u=[1,0,0,0])
P("=== Round 11-M continued: hexagon and cube parts (m_round11_more.py) ===")
for a,b in [('hexagon','hexagon'),('square','hexagon'),('hexagon','octahedron'),('square','cube'),('cube','octahedron'),('cube','cube')]:
    t0=time.time()
    V=max_tensor_vertices(S[a],S[b])
    st,found,VV,prod,ent,Kl=analyse(f"max {a}x{b}",S[a],S[b],V)
    if ent:
        lp=set(Kl[i][i] for i in prod); le=set(Kl[i][i] for i in ent)
        P(f"   leverage: product min > entangled max: {min(lp)>max(le)} ; {round(time.time()-t0,1)}s")
# (repository copy: prints only; the session copy also appended this output to outputs_m.txt)
