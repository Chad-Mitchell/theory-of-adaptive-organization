"""Robustness only (PREREG section 2: pop learner never decides a verdict): pop learner, R-level arms, 8 seeds, main scan."""
import os, json
from multiprocessing import Pool
import run_onset as ro
if __name__ == '__main__':
    os.nice(19)
    done = set()
    if os.path.exists('results_pop.jsonl'):
        for l in open('results_pop.jsonl'): x = json.loads(l); done.add((x['arm'], x['cell'], x['seed']))
    J = [a for a in ro.joblist('pop', 8, 'scan') if a[0] in ('RR', 'RRh') and (a[0], a[1], a[5]) not in done]
    print('jobs', len(J), flush=True)
    with Pool(3) as p, open('results_pop.jsonl', 'a') as f:
        for line in p.imap_unordered(ro.work, J): f.write(line + '\n'); f.flush()
