"""KERNEL-MEASURE (pick 28): regime-first measurement of the DRIVER only (no tracker/VIX data used).
Driver proxy: x_t = log Parkinson daily variance of the S&P 500, (ln H/L)^2/(4 ln 2), business days as steps."""
import sys, json, numpy as np, csv
sys.path.insert(0, '../../measurement/estimators')
import aqn
r = list(csv.DictReader(open('data/GSPC_ohlc.csv')))
r = [x for x in r if x['date'] <= '2026-10-30']
h = np.array([float(x['high']) for x in r]); l = np.array([float(x['low']) for x in r])
pv = np.log(h / l) ** 2 / (4 * np.log(2))
ok = pv > 0
y = np.log(pv[ok])
print('n', len(y), 'dropped zero-range days', int((~ok).sum()), r[0]['date'], r[-1]['date'])
out = {'n': int(len(y)), 'dates': [r[0]['date'], r[-1]['date']]}
for name, band in [('full', None), ('low_T>20d', (0, 2*np.pi/20)), ('high_T<=20d', (2*np.pi/20, np.pi))]:
    f = aqn.whittle_fit(y, band=band)
    print(name, {k: (round(v, 4) if isinstance(v, float) else v) for k, v in f.items() if k in ('alpha','se_alpha','logq','logs2','se_logs2')})
    out[name] = {k: float(v) for k, v in f.items() if isinstance(v, (float, int, np.floating))}
c = aqn.whittle_corner_fit(y)
print('corner', {k: (round(float(v), 4) if np.isscalar(v) else v) for k, v in c.items() if np.isscalar(v)})
out['corner'] = {k: float(v) for k, v in c.items() if np.isscalar(v) and not isinstance(v, str)}
print('DFA', aqn.dfa_alpha(y))
json.dump(out, open('driver_spectrum.json', 'w'), indent=1)
