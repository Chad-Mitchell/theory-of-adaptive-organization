"""Estimator dry run on SYNTHETIC truth (no simulator): D_rel(N) = A - B N^(a-1) with known N*, plus noise.
Checks that analyze.py recovers a known slope (-1 and -2) and flags a flat/no-crossing case."""
import json, numpy as np, subprocess
rng = np.random.default_rng(0)
TH = json.load(open('THEORY_PREDICTIONS.json'))
rhos = [0.01, 0.02, 0.04, 0.08, 0.16, 0.32]
lines = []
truth = {'RR': (0.5, -1.0, 4.0), 'AA': (2/3, -2.0, 27.0)}
for arm, (a, e, Pi) in truth.items():
    C = TH['arms'][arm]['Nstar']
    for r, c in zip(rhos, C):
        Ns = [c * 2 ** ((j - 8) / 2) for j in range(17)]
        nst = Pi * r ** e * 1.3   # true N* off theory level by 30% to check levels are not forced
        A = 0.5 * r
        for s in range(16):
            noise = 0.002 * rng.standard_normal(17) + 0.001 * rng.standard_normal()
            rows = [dict(N=N, D_rel=A * (1 - (N / nst) ** (a - 1)) + noise[i], D_rel_ind=A * (1 - (N / nst) ** (a - 1)) + 3 * noise[i]) for i, N in enumerate(Ns)]
            lines.append(json.dumps(dict(arm=arm, cell='rho=%g' % r, seed=s, learner='es', flat_eff=[40.0] * 16, lev_eff=[20.0] * 17, rows=rows)))
open('dryrun_synth.jsonl', 'w').write('\n'.join(lines) + '\n')
out = json.loads(subprocess.run(['python3', 'analyze.py', 'dryrun_synth.jsonl', 'THEORY_PREDICTIONS.json'], capture_output=True, text=True, check=True).stdout)
for arm in truth:
    o = out['primary'][arm]
    print(arm, 'true slope', truth[arm][1], 'e_hat %.3f CI %s valid %s verdict %s' % (o['e_hat'], [round(x, 3) for x in o['e_ci']], o['valid_rhos'], o['verdict']), 'logistic', round(o.get('logistic_slope', np.nan), 3))
    print('   Pi ratio', {k: round(v, 2) for k, v in o['Pi_ratio'].items() if v})
print('contrast', out['contrasts'])
print('findability RR', json.dumps(out['findability']['RR']['perception_noise_logistic']))
