"""Lemma checks for DUEL_MEMO (numerical confirmations of the analytic statements)."""
import numpy as np, duel_core as d
rng = np.random.default_rng(20261123)
phi = d.CENT
def dens_from_q(q):
    z = np.exp(1j*np.outer(phi, np.arange(len(q))))@q
    return np.abs(z)**2/(2*np.pi)

print("L1 Fejer-Riesz: random nonneg trig polys of degree N-1 are |q|^2 (canonical phase densities of N-level pure states)")
for N in [2,3,5,8]:
    worst = 0; tried = 0; got = 0
    while got < 20:
        tried += 1
        a = rng.normal(size=N-1)*0.6/np.arange(1,N); b = rng.normal(size=N-1)*0.6/np.arange(1,N)
        k = np.arange(1,N)
        p = (1 + np.cos(np.outer(phi,k))@a + np.sin(np.outer(phi,k))@b)/(2*np.pi)
        if p.min() < 0: continue
        got += 1
        # Laurent coeffs P_d (d=-(N-1)..N-1) of 2pi p: P_0=1, P_d=(a-ib)/2
        P = np.zeros(2*N-1, complex); P[N-1] = 1
        P[N:] = (a-1j*b)/2; P[:N-1] = ((a+1j*b)/2)[::-1]
        roots = np.roots(P[::-1])               # z^{N-1} * sum_d P_d z^d
        inside = roots[np.abs(roots) < 1]
        if len(inside) != N-1:                   # roots on circle (measure zero)
            inside = sorted(roots, key=abs)[:N-1]
        q = np.poly(inside)[::-1]                # coefficients low->high
        pq = dens_from_q(q); pq *= p.sum()/pq.sum()
        worst = max(worst, np.max(np.abs(pq-p)))
    print(f"  N={N}: 20 random nonneg polys factorized, max |p - |q|^2| = {worst:.2e}")

print("L2 readable-information cap ln N (Nikolskii/Cauchy-Schwarz: max|q|^2 <= N * mean|q|^2)")
for N in [2,3,8,32]:
    r = 0
    for _ in range(200):
        q = rng.normal(size=N)+1j*rng.normal(size=N)
        pd = dens_from_q(q)*2*np.pi; r = max(r, pd.max()/pd.mean())
    R, tl, c = d.best_state(N, 1.0)
    pd = dens_from_q(c.astype(complex)); m = pd*(2*np.pi/d.M)
    Ican = d.info_of_density(m); chi = -np.sum(c**2*np.log(c**2+1e-300))
    print(f"  N={N}: max ratio {r:.4f} <= {N};  sine state: I_canonical={Ican:.4f}, Holevo chi={chi:.4f}, ln N={np.log(N):.4f}")

print("L3 orbitope: shifted Fejer kernels give N perfectly distinguishable states and a partition of unity")
for N in [2,3,5,9]:
    nodes = 2*np.pi*np.arange(N)/N
    def F(x):
        z = np.exp(1j*np.outer(x, np.arange(N))).sum(1); return np.abs(z)**2/N**2
    S = sum(F(phi-n) for n in nodes)
    Mx = np.array([[F(np.array([ni-nj]))[0] for nj in nodes] for ni in nodes])
    print(f"  N={N}: max|sum_i e_i - 1| = {np.max(np.abs(S-1)):.1e}; max|e_i(node_j) - delta_ij| = {np.max(np.abs(Mx-np.eye(N))):.1e}")

print("L4 Markov clock coherence |Im|/|Re| vs cot(pi/N) (Dmitriev-Dynkin 1946; Barato-Seifert 2017; Ohga-Ito-Kolchinsky 2023)")
for N in [3,4,5,6]:
    best = 0
    for _ in range(20000):
        Q = rng.exponential(size=(N,N))**rng.uniform(1,6); np.fill_diagonal(Q,0)
        if rng.random() < 0.5:  # sparse/near-cyclic
            mask = rng.random((N,N)) < 0.4; Q = Q*mask
            for i in range(N): Q[(i+1)%N, i] += rng.exponential()*5
        Q = Q - np.diag(Q.sum(0))
        w = np.linalg.eigvals(Q); w = w[np.abs(w) > 1e-9]
        if len(w): best = max(best, np.max(np.abs(w.imag)/np.abs(w.real)))
    print(f"  N={N}: max sampled ratio {best:.4f}  vs cot(pi/N) = {1/np.tan(np.pi/N):.4f}")

print("L5 mixing finite records: for ANY estimate law, mean over theta of P(|theta - theta_hat| > pi/2) = 1/2")
for _ in range(3):
    N = rng.integers(2, 20); pts = rng.uniform(-np.pi, np.pi, N); w = rng.dirichlet(np.ones(N))
    th = np.linspace(-np.pi, np.pi, 20001)[:-1]
    P = np.array([np.sum(w*(np.abs(d.wrap(t-pts)) > np.pi/2)) for t in th])
    print(f"  N={N}: mean {P.mean():.4f}, max over theta {P.max():.4f}")
for N in [8, 32]:
    r = 2*np.pi/np.sin(2*np.pi/N)
    print(f"  a3 N={N}: tail at t=1,10,100,1000 rev:", [round(d.a_tail_fourier(N, r, t), 4) for t in [1,10,100,1000]])

print("L6 record dimensions: quantum full N^2, orbit span (Toeplitz section) 2N-1")
for N in [2,3,5,8]:
    c = rng.normal(size=N)+1j*rng.normal(size=N); c /= np.linalg.norm(c)
    vecs = []
    for th in rng.uniform(0, 2*np.pi, 6*N):
        psi = c*np.exp(-1j*np.arange(N)*th); rho = np.outer(psi, psi.conj())
        vecs.append(np.concatenate([rho.real.ravel(), rho.imag.ravel()]))
    print(f"  N={N}: rank of generic orbit span = {np.linalg.matrix_rank(np.array(vecs), tol=1e-9)} (2N-1={2*N-1}, N^2={N*N})")

print("L7 (follow-up probe) sphere: SU(2) orbit of a spin coherent state spans all N^2 dims; band-limited count sum_{l<=N-1}(2l+1) = N^2")
from scipy.linalg import expm
for N in [2,3,4,6]:
    j = (N-1)/2; m = j - np.arange(N)
    Jp = np.diag(np.sqrt(j*(j+1)-m[1:]*(m[1:]+1)), 1); Jx = (Jp+Jp.T)/2; Jy = (Jp-Jp.T)/(2j); Jz = np.diag(m)
    psi0 = np.zeros(N, complex); psi0[0] = 1
    vecs = []
    for _ in range(4*N*N):
        a, b, c = rng.uniform(0, 2*np.pi, 3)
        U = expm(-1j*a*Jz)@expm(-1j*b*Jy)@expm(-1j*c*Jz); psi = U@psi0; rho = np.outer(psi, psi.conj())
        vecs.append(np.concatenate([rho.real.ravel(), rho.imag.ravel()]))
    print(f"  N={N}: rank {np.linalg.matrix_rank(np.array(vecs), tol=1e-9)}  N^2={N*N}  band-limited count={sum(2*l+1 for l in range(N))}")
