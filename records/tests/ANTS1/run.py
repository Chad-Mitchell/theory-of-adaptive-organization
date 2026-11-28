import numpy as np, sys, os, pickle, time, itertools
from multiprocessing import Pool
from world import generate, WORLDS, SIGMA_OBS, T, M
from score import score
from ants import run_shared, run_private, ARM_CODE, COS, SIN
EGRID = np.exp(np.linspace(np.log(3e-4), np.log(1.0), 19)); EGRID[-1] = 1.0
NS = [1, 2, 4, 8, 16, 32, 64, 128, 256]
ARMS = ["IND", "FOL", "LOCK", "PRIV"]
NSEED = int(os.environ.get("NSEED", 24))
MODE_STEPS = np.arange(0, T, 10)


def job(args):
    arm, w, dr, si, N, seed = args
    x, _ = generate(w, dr, seed)
    so = SIGMA_OBS[si]
    res = np.zeros((len(EGRID), 4))
    rs = 7919 * seed + 104729 * N + 13 * dr + si + 1
    for k, e in enumerate(EGRID):
        if arm == "PRIV":
            na = min(N, 8)
            mm, mo = run_private(x, na, e, so, rs, COS, SIN)
            sc = np.array([score(x, mm[a]) + score(x, mo[a], MODE_STEPS) for a in range(na)]).mean(0)
            res[k] = [sc[0], sc[2], sc[1], sc[3]]
        else:
            mm, mo = run_shared(ARM_CODE[arm], x, N, e, so, rs, COS, SIN)
            a1, c1 = score(x, mm); a2, c2 = score(x, mo, MODE_STEPS)
            res[k] = [a1, a2, c1, c2]
    return args, res   # columns: MSE_mean, MSE_mode, CAP_mean, CAP_mode


if __name__ == "__main__":
    arms = sys.argv[1].split(",") if len(sys.argv) > 1 else ARMS
    worlds = sys.argv[2].split(",") if len(sys.argv) > 2 else WORLDS
    out = sys.argv[3] if len(sys.argv) > 3 else "results.pkl"
    jobs = [(a, w, dr, si, N, s) for a in arms for w in worlds for dr in range(3) for si in range(2)
            for N in NS for s in range(NSEED)]
    jobs.sort(key=lambda j: -j[4])  # big N first for load balance
    R = {}
    t0 = time.time()
    with Pool(int(os.environ.get("NPROC", 6))) as p:
        for i, (a, r) in enumerate(p.imap_unordered(job, jobs, chunksize=1)):
            R[a] = r
            if i % 200 == 0:
                print(f"{i}/{len(jobs)} {time.time()-t0:.0f}s", flush=True)
                pickle.dump(R, open(out, "wb"))
    pickle.dump(R, open(out, "wb"))
    print("done", time.time() - t0)
