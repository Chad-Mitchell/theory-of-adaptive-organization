"""Round 12-M: the two one-sided disk inequalities (i) ||C||^2 <= 2 + |b|^2 - 2|a|^2, (ii) ||C||^2 <= 2 + |a|^2 - 2|b|^2
on every extreme point of max(P_n, P_m) (P_n inscribed in the unit circle, so max(P_n,P_m) lies inside max(D,D)). Prints only."""
from m_round12_parts import max_vertices
for na, nb in [('P4','P4'),('P5','P5'),('P6','P6'),('P7','P7'),('P8','P8'),('P5','P6'),('P3','P7'),('P5','P8')]:
    X = max_vertices(na, nb); a = X[:, 1:, 0]; b = X[:, 0, 1:]; C = X[:, 1:, 1:]
    A2 = (a**2).sum(1); B2 = (b**2).sum(1); C2 = (C**2).sum((1, 2))
    s1 = (C2-(2+B2-2*A2)).max(); s2 = (C2-(2+A2-2*B2)).max()
    print(f"max({na},{nb}): {len(X)} pts; max slack (i) {s1:+.6f}, (ii) {s2:+.6f}  ({'OK' if max(s1, s2) <= 1e-9 else 'VIOLATED'})")
