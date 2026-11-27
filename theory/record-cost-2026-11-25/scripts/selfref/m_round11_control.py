# Round 11-M positive control: two-qubit stabilizer polytope (octahedron parts, NOT inside the max tensor product,
# i.e. restricted local reads). The detector must find an entangling automorphism here (CNOT).
import sys, os, itertools
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from m_round11_lib import *
from m_round11_lib import _out as out0
I=np.eye(2); X=np.array([[0,1],[1,0]]); Y=np.array([[0,-1j],[1j,0]]); Z=np.diag([1,-1]); Pa=[I,X,Y,Z]
Hd=np.array([[1,1],[1,-1]])/np.sqrt(2); Sg=np.diag([1,1j]); CN=np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
gens=[np.kron(Hd,I),np.kron(I,Hd),np.kron(Sg,I),np.kron(I,Sg),CN]
v=np.zeros(4,complex); v[0]=1; seen={}; fr=[v]
def key(v):
    i=np.argmax(np.abs(v)>1e-9); w=v*np.conj(v[i])/abs(v[i]); return tuple(np.round(w,6))
seen[key(v)]=v
while fr:
    nf=[]
    for s in fr:
        for g in gens:
            w=g@s; k=key(w)
            if k not in seen: seen[k]=w; nf.append(w)
    fr=nf
V=[]
for s in seen.values():
    rho=np.outer(s,s.conj())
    V.append([F(int(round(np.real(np.trace(np.kron(Pa[i],Pa[j])@rho))))) for i in range(4) for j in range(4)])
P("=== Round 11-M continued: positive control (m_round11_control.py) ===")
st,found,VV,prod,ent,Kl=analyse("CONTROL 2-qubit stabilizer polytope (octahedron parts, restricted reads)",S['octahedron'],S['octahedron'],V)
# (repository copy: prints only; the session copy also appended this output to outputs_m.txt)
