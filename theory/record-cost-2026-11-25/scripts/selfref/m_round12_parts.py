"""Round 12-M (Conjecture C beyond (star)): part state spaces as facet effects (1, n) with n.r >= -1,
in invariant Euclidean coordinates with circumradius 1, and vertex enumeration of max(A,B) with pycddlib (float).
Shared by m_round12_diamond.py, m_round12_disk_check.py and m_round12_platonic_slice.py."""
import itertools, math
import numpy as np
import cdd

def polygon(n):
    c = math.cos(math.pi / n)
    return [np.array([1.0, -math.cos((2*k+1)*math.pi/n)/c, -math.sin((2*k+1)*math.pi/n)/c]) for k in range(n)]

def cube(d):   # vertices (+-1)^d/sqrt(d); facets x_i <= 1/sqrt(d)
    return [np.array([1.0]+[(-s*math.sqrt(d) if j == i else 0.0) for j in range(d)]) for i in range(d) for s in (1, -1)]

def cross(d):  # vertices +-e_i; facets sum s_i x_i <= 1
    return [np.array([1.0]+[-s for s in sg]) for sg in itertools.product((1, -1), repeat=d)]

PHI = (1 + 5**.5) / 2
def _pts(base):
    S = set()
    for b in base:
        for c in (b, (b[1], b[2], b[0]), (b[2], b[0], b[1])):
            for s in itertools.product((1, -1), repeat=3):
                S.add(tuple(s[i]*c[i] for i in range(3)))
    V = np.array(sorted(S), float)
    return V / np.linalg.norm(V[0])
ICO = _pts([(0, 1, PHI)]); DOD = _pts([(1, 1, 1), (0, 1/PHI, PHI)]); CUBOCT = _pts([(1, 1, 0)])

def effects_from_vertices(V):
    m = cdd.matrix_from_array([[1.0]+list(v) for v in V], rep_type=cdd.RepType.GENERATOR)
    H = np.array(cdd.copy_inequalities(cdd.polyhedron_from_matrix(m)).array)
    return [h/h[0] for h in H]

PARTS = {'P%d' % n: (lambda n=n: polygon(n)) for n in range(3, 13)}
PARTS.update({'sq': lambda: cube(2), 'cube3': lambda: cube(3), 'oct3': lambda: cross(3),
              'I': lambda: effects_from_vertices(ICO), 'D': lambda: effects_from_vertices(DOD),
              'CO': lambda: effects_from_vertices(CUBOCT)})

def max_vertices(na, nb):
    """Extreme points of max(A,B) as arrays X (dA x dB) with X[0,0] = 1, a = X[1:,0], b = X[0,1:], C = X[1:,1:]."""
    EA, EB = PARTS[na](), PARTS[nb]()
    dA, dB = len(EA[0]), len(EB[0])
    rows = [[0.0]+list(np.kron(e, f)) for e in EA for f in EB]
    u = np.zeros(dA*dB); u[0] = 1
    mat = cdd.matrix_from_array(rows+[[-1.0]+list(u)], rep_type=cdd.RepType.INEQUALITY, lin_set={len(rows)})
    V = np.array(cdd.copy_generators(cdd.polyhedron_from_matrix(mat)).array)[:, 1:]
    return V.reshape(-1, dA, dB)
