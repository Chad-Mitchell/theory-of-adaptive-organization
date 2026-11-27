"""J: round 7. Sharp-fixed-point condition (SFP): every reversible transformation of the state space fixes at least one
pure state (a definite self-consistent pattern persists under ANY law). Also the persistent-bit version (fixes a
perfectly distinguishable pair). Sample each group; report the fraction of elements that fix a pure state."""
import numpy as np, itertools
from scipy.stats import special_ortho_group, ortho_group, unitary_group
rng=np.random.default_rng(3); n=3000
def frac(gen,test): return np.mean([test(gen()) for _ in range(n)])
has1=lambda R: np.min(np.abs(np.linalg.eigvals(R)-1))<1e-8
pm1=lambda R: np.min(np.minimum(np.abs(np.linalg.eigvals(R)-1),np.abs(np.linalg.eigvals(R)+1)))<1e-8
def realev(R):  # real QM d: pure state |v><v| fixed iff Ov = +-v for real v
    w,V=np.linalg.eig(R); return any(abs(abs(x)-1)<1e-8 and abs(x.imag)<1e-8 for x in w)
rows=[]
# classical simplex n=3,4 (S_n): fixed vertex
for k in (2,3,4):
    perms=list(itertools.permutations(range(k))); rows.append((f"classical simplex, {k} outcomes (S_{k})",np.mean([any(p[i]==i for i in range(k)) for p in perms]),"finite"))
# square D4 acting on 4 vertices: rotations r^0..r^3, reflections: 2 through vertices (diagonals) fix 2 vertices, 2 through edge midpoints fix none
rows.append(("square / gbit (D4)",3/8,"finite"))
rows.append(("disk / rebit (SO(2))",frac(lambda: special_ortho_group.rvs(2,random_state=rng),has1),"S^1, chi=0"))
rows.append(("ball with full O(3) (incl. inversion)",frac(lambda: ortho_group.rvs(3,random_state=rng),has1),"S^2 but inversion has no fixed point"))
rows.append(("qubit ball (SO(3)=PU(2))",frac(lambda: special_ortho_group.rvs(3,random_state=rng),has1),"S^2, chi=2"))
rows.append(("4-ball (SO(4)) spin factor",frac(lambda: special_ortho_group.rvs(4,random_state=rng),has1),"S^3, chi=0"))
rows.append(("5-ball (SO(5)) = quaternionic qubit",frac(lambda: special_ortho_group.rvs(5,random_state=rng),has1),"S^4, chi=2"))
for d in (2,3,4):
    rows.append((f"real QM d={d} (O({d}) on RP^{d-1})",frac(lambda: ortho_group.rvs(d,random_state=rng),realev),f"chi(RP^{d-1})={1 if (d-1)%2==0 else 0}"))
for d in (2,3):
    rows.append((f"complex QM d={d} (U({d}) on CP^{d-1})",1.0 if all(True for _ in range(1)) else 0,f"chi={d}: every unitary has an eigenvector"))
print(f"{'state space (reversible group)':42s} fraction of sampled group elements fixing a pure state   note")
for name,f,note in rows: print(f"  {name:42s} {f:6.3f}   {note}")
print("SFP holds iff fraction = 1 for EVERY element (sampling shows generic behaviour; exact statements in NOTE R7).")
# persistent bit: for SO(3) every rotation fixes the two axis poles = an orthogonal (antipodal) pair
R=special_ortho_group.rvs(3,random_state=rng); w,V=np.linalg.eig(R); v=np.real(V[:,np.argmin(abs(w-1))])
print("qubit ball: random rotation fixes poles +v and -v (a perfectly distinguishable pair):",np.allclose(R@v,v),np.allclose(R@(-v),-v))
