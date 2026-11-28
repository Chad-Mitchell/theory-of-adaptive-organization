"""KERNEL-MEASURE locked decision code (design 2). Constants fixed from driver-only measurement and simulation
(driver_band.json, power2/H0_0*.json); nothing here was computed from the VIX kernel.
Run after lock:  python3 decide.py run   (writes results.json)."""
import sys, json, csv, numpy as np
W21_PRED = 0.2770          # sim pseudo-true of the binned-projection survival at age 21 (H0, r = 0, 100 reps; alpha 1.2587)
DW_DALPHA = -0.601         # (0.2232 - 0.3434)/0.2 from H0 sims at alpha +/- 0.1
SIG_PRED = 0.0264          # sqrt((0.601*0.0429)^2 + (0.035*0.1009)^2 + (0.038*0.1185)^2): alpha, log q, log s2 SEs
DELTA = 0.13               # equivalence margin on W21
SIG_MAX = DELTA / 3.24     # = 0.0401: realized resolution needed for P(PASS | true) >= 0.8 (MV8/MV10 realized check)
RIVALS = {'R1_alpha2_EWMA': 0.000, 'R2_flat_1_5_22': 0.012, 'R3_matching_survival_alpha_minus_1': 0.725}
Z = 1.96

def rule(W21, W21_sd, pred=W21_PRED, sig_pred=SIG_PRED):
    D = W21 - pred; sD = float(np.hypot(W21_sd, sig_pred))
    lo, hi = W21 - Z * W21_sd, W21 + Z * W21_sd
    rivals_excluded = all(not (lo <= v <= hi) for v in RIVALS.values())
    if abs(D) + Z * sD <= DELTA and rivals_excluded:
        verdict = 'PASS'
    elif abs(D) - Z * sD > DELTA:
        verdict = 'FAIL'
    else:
        verdict = 'INCONCLUSIVE'
    low_resolution = sD > SIG_MAX            # label only: PASS is unreachable when sD > DELTA/1.96; decisive-lock condition
    return {'D': float(D), 'sigma_D': sD, 'CI_D': [float(D - Z * sD), float(D + Z * sD)], 'W21_CI': [float(lo), float(hi)],
            'rivals_excluded': rivals_excluded, 'low_resolution': bool(low_resolution), 'verdict': verdict}

def load():
    import klib
    r = [x for x in csv.DictReader(open('data/GSPC_ohlc.csv')) if x['date'] <= '2026-10-30']
    y = np.log(np.log(np.array([float(x['high']) for x in r]) / np.array([float(x['low']) for x in r])) ** 2 / (4 * np.log(2)))
    v = {x['observation_date']: x['VIXCLS'] for x in csv.DictReader(open('data/VIXCLS.csv'))}
    z = np.array([2 * np.log(float(v[x['date']])) if v.get(x['date'], '') not in ('', '.') else np.nan for x in r])
    return y, z

if __name__ == '__main__' and sys.argv[1:] == ['run']:
    import klib
    y, z = load()
    out = {'n_driver': int(len(y)), 'n_vix_missing': int(np.isnan(z).sum())}
    m = klib.fit_bins(z, y, nboot=999, seed=20261128)
    out['primary'] = {**m, **rule(m['W21'], m['W21_sd'])}
    # sensitivities (reported, not decisive)
    W_free = W21_PRED + DW_DALPHA * (1.1902 - 1.2587)
    out['sens_free_noise_alpha'] = {'W21_pred': W_free, **rule(m['W21'], m['W21_sd'], W_free, abs(DW_DALPHA) * 0.0980)}
    klib.BLOCK = 252
    m2 = klib.fit_bins(z, y, nboot=999, seed=20261129)
    out['sens_block252'] = {**m2, **rule(m2['W21'], m2['W21_sd'])}
    klib.BLOCK = 126
    out['descriptive_design1_family_s'] = klib.fit(z, y, nboot=499, seed=20261130)
    out['descriptive_raw_alpha_over_2'] = 1.2587 / 2
    json.dump(out, open('results.json', 'w'), indent=1)
    print(json.dumps(out, indent=1))
