# Round 11-M: exact checks of the two lemmas used in the leverage proof (orthogonal coordinates: square, octahedron, cube).
import sys, os, itertools
sys.path.insert(0, os.path.dirname(__file__))
from m_round11_lib import *
from m_round11_lib import _out as out0
S['cube']=dict(V=[[1]+list(s) for s in itertools.product((1,-1),repeat=3)],
               E=[[1]+[sg if k==i else 0 for k in range(3)] for i in range(3) for sg in (1,-1)], u=[1,0,0,0])
P("=== Round 11-M continued: lemma checks (m_round11_lemma.py) ===")
for a,b in [('square','square'),('square','octahedron'),('octahedron','octahedron'),('square','cube'),('cube','octahedron'),('cube','cube')]:
    A,B=S[a],S[b]; dA,dB=len(A['u']),len(B['u'])
    RA2=sum(x*x for x in A['V'][0][1:]); RB2=sum(x*x for x in B['V'][0][1:])
    nA2=sum(x*x for x in A['E'][0][1:]); nB2=sum(x*x for x in B['E'][0][1:])
    V=max_tensor_vertices(A,B)
    Ps=set(tuple(F(t) for t in kron(x,y)) for x in A['V'] for y in B['V'])
    maxC=F(0); viol=0; pure_marg_ent=0
    for v in V:
        W=[[v[i*dB+j] for j in range(dB)] for i in range(dA)]
        C2=sum(W[i][j]**2 for i in range(1,dA) for j in range(1,dB)); maxC=max(maxC,C2)
        a_=[W[i][0] for i in range(dA)]; b_=[W[0][j] for j in range(dB)]
        if tuple(v) not in Ps and (a_ in [list(map(F,x)) for x in A['V']] or b_ in [list(map(F,x)) for x in B['V']]): pure_marg_ent+=1
    P(f"{a}x{b}: R_A^2|n_A|^2={RA2*nA2} (d_A-1={dA-1}), R_B^2|n_B|^2={RB2*nB2} (d_B-1={dB-1}); max ||C||_F^2 over max-composite vertices = {maxC} vs R_A^2 R_B^2 = {RA2*RB2}; entangled vertices with a pure marginal: {pure_marg_ent}")
# (repository copy: prints only; the session copy also appended this output to outputs_m.txt)
