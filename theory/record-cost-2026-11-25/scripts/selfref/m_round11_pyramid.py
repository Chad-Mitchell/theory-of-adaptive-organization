# Round 11-M: reducible non-classical part (Al-Safi-Richens "squashed g-trit" = square pyramid) in max composites.
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from m_round11_lib import *
from m_round11_lib import _out as out0
S['pyramid']=dict(V=[[1,1,1,0],[1,1,-1,0],[1,-1,1,0],[1,-1,-1,0],[1,0,0,1]],
                  E=[[0,0,0,1],[1,-1,0,-1],[1,1,0,-1],[1,0,-1,-1],[1,0,1,-1]], u=[1,0,0,0])
P("=== Round 11-M continued: reducible part (m_round11_pyramid.py) ===")
for a,b in [('pyramid','square'),('pyramid','pyramid'),('pyramid','octahedron')]:
    V=max_tensor_vertices(S[a],S[b]); analyse(f"max {a}x{b}",S[a],S[b],V)
# (repository copy: prints only; the session copy also appended this output to outputs_m.txt)
