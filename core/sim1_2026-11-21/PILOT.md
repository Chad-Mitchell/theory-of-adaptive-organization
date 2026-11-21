# T28 pre-lock pilots (not official)

*Saturday 21 November 2026, America/New_York. Seeds `20261122800..20261122819` only. Official candidates `20261122000..20261122015` were not evaluated.*

These numbers informed the locked ladders, the P4 cell, the jump counts, and the \(1.5\) tolerance. They are not official results of T28 and are not scored.

## Seeds

Pilot seeds do not collide with S5, convexity search, T20/T25 named seeds, T27 official or chain blocks, or the reserved official/chain blocks of this test (`sim1_lib.seed_collides`).

## I0 box tightening (before lock)

A first scan of the 20 pilots used \(I_0=10^{U(-1.0,0.0)}\in[0.10,1.00]\). Exact P1–P3 held on 80/80 \(K\)-rows; \(m^\star(W_{\mathrm{LOW}})=0\) and \(m^\star(W_{\mathrm{HIGH}})\ge 1\) on 80/80; \(W_{\mathrm{th}}\) always sat in \((0.02,20)\). At a provisional P4 stake \(w=5\), two of the 20 pilots had joint \(m^\star=0\), which would have made “evolution finds a positive rehearsal count” too weak. At \(w=20\), all 20 pilots had joint \(m^\star\in\{4,\ldots,14\}\).

A closed-form corner probe of that first box found one corner with joint \(m^\star=0\) at \(w=20\): minimum \(e_{\mathrm{base}}\), maximum \(\gamma\), minimum \(\varphi\), maximum \(I_0=1\). The locked box therefore tightens \(I_0\) to \(10^{U(-1.0,-0.3)}\in[0.10,0.50]\). After the tightening:

- Every corner of the locked box has joint \(m^\star\ge 3\) at \(w=20\), and \(m^\star(0.02)=0\) at every \(K\).
- The same 20 pilot seeds, with only the \(I_0\) map changed (the earlier uniforms are identical), again passed every exact P1–P3 clause and the exact-Boltzmann P4 screen at \(\beta=40\), with joint \(m^\star\in\{4,\ldots,14\}\).

4,000 draws from the *untightened* box at \(w=20\) had \(m^\star\ge 3\) (no miss in that sample); they were not used to set a gate, and they are not a substitute for the corner probe.

## Exact gates on the tightened-box pilots (20 worlds, 80 \(K\)-rows)

- P1 monotone in \(w\) and in \(\lambda\): 80/80.
- P2 threshold clauses: 80/80.
- P3 monotone in \(c\): 80/80.
- Joint \(m^\star(w)\) happened to be nondecreasing on these 20 ladders, and CT33 spend/error held 20/20. Joint monotone \(m\) is **not** locked as a gate (substitutes).
- Exact Boltzmann at the P4 cell, \(\beta=40\): unique argmin, marginal mode \(=m^\star\) on 20/20, \(|\mathbb E[m]-m^\star|\) at most \(0.767\) (the locked bar is \(1.5\)).

## Mixing probe (not official)

Five of the first-box pilots, at \(w=20\), \(\beta=40\), 8 chains, 150,000 jumps, 15,000 burn (the locked counts), reused `run_moran_ct`: TV to exact Boltzmann was \(0.025\)–\(0.054\) (bar \(0.20\)); empirical marginal mode equalled \(m^\star\); empirical \(|\bar m-m^\star|\) was at most \(0.752\). Runtime about 4 s per world. After the I0 tightening the P4 landscapes are of the same kind (same \(e_{\mathrm{base}},\gamma,\varphi\); smaller \(I_0\)), and the locked jump counts are left as that probe set them.

A shorter first probe at \(w=5\), \(\beta\in\{8,10,12\}\), 40,000 jumps, was discarded as a P4 design: mass at the exact joint argmin was as low as 5%, two pilots had \(m^\star=0\), and a couple of empirical joint modes missed. That is why the official P4 cell is \(w=20\), \(\beta=40\), and why the official clauses use the *marginal* on \(m\) and a mean tolerance rather than the joint mode alone (neighbor gaps in \(J\) are often \(\sim 10^{-3}\)).

Raw first-scan output: `pilot_explore.py`, `pilot_explore.json`. Those files are a disclosure of the first scan; they are not the official runner and are not hash-locked.
