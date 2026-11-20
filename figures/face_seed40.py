"""Review 26's three-scale world (seed 40): greedy and greedy + pairwise look-ahead both miss the cheapest store set.
   nice -n 19 python3 figures/face_seed40.py      (about 3 min; writes face_seed40.json; checked in tools/test_face_map.py)
World from gtao-review26/review_work/d_greedy_partial.jsonl (seed 40), reproduced with the guarded optimizer (face_hybrid.best_fast, 12 starts,
every optimum confirmed by the Lyapunov mse()).  Cost = n*h_l*k_local + h_c*k_shared + n*w_u*E, with h_l = 1."""
import os, sys, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import face_hybrid as fh
W = dict(a=[1.0, 0.005027537976562518, 2.7395275135039827e-05], v=[0.14677341438335517, 0.08139373286450213, 0.7718328527521426],
         rho=[0.18059359059116353, 0.5564010436740665, 0.11885206520719416], N=0.31919888320688583, n=8, lead=4.982001746750192,
         wu=3987.6678490368113, hl=1.0, hc=1.0233055364466324, max_local=3, max_shared=3)

def cost(kl, kc, E): return W['n'] * W['hl'] * kl + W['hc'] * kc + W['n'] * W['wu'] * E

if __name__ == '__main__':
    a, v, rho = (np.array(W[k]) for k in ('a', 'v', 'rho')); D = {}
    for kl in range(4):
        for kc in range(4):
            if kl + kc == 0: E, bl, bc = float(v.sum()), [], []
            else:
                E, x = fh.best_fast(a, v, W['N'], W['n'], rho, W['lead'], kl, kc, starts=12, seed=1)
                bl, bc = fh._rates(x[:kl]).tolist(), fh._rates(x[kl:]).tolist()
            D[f'{kl},{kc}'] = dict(E=float(E), cost=float(cost(kl, kc, E)), bl=bl, bc=bc); print(kl, kc, round(D[f'{kl},{kc}']['cost'], 3), flush=True)
    C = {tuple(map(int, k.split(','))): d['cost'] for k, d in D.items()}
    exact = min(C, key=C.get)
    def walk(pair):
        cur = (0, 0); path = [cur]
        while True:
            nb = [(cur[0] + 1, cur[1]), (cur[0], cur[1] + 1)]
            if pair: nb += [(cur[0] + 2, cur[1]), (cur[0], cur[1] + 2), (cur[0] + 1, cur[1] + 1)]
            nb = [d for d in nb if d in C]
            single = [d for d in nb[:2] if C[d] < C[cur]]
            if single: cur = min(single, key=C.get)
            elif pair and [d for d in nb[2:] if C[d] < C[cur]]: cur = min([d for d in nb[2:] if C[d] < C[cur]], key=C.get)
            else: return cur, path
            path.append(cur)
    g, gp = walk(False); p, pp = walk(True)
    out = dict(world=W, designs=D, exact=list(exact), greedy=list(g), greedy_path=[list(x) for x in gp], lookahead=list(p),
               regret_greedy=C[g] / C[exact] - 1, regret_lookahead=C[p] / C[exact] - 1)
    json.dump(out, open(os.path.join(HERE, 'face_seed40.json'), 'w'), indent=1)
    print('exact', exact, 'greedy', g, gp, 'look-ahead', p, 'regret', out['regret_greedy'])
