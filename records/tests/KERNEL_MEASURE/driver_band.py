"""Driver only: in-band (periods >= 21 business days) consistency: split at 126 days; corner check in band."""
import sys, json, numpy as np, csv
sys.path.insert(0, '../../measurement/estimators')
import aqn
r = [x for x in csv.DictReader(open('data/GSPC_ohlc.csv')) if x['date'] <= '2026-10-30']
y = np.log(np.log(np.array([float(x['high']) for x in r]) / np.array([float(x['low']) for x in r])) ** 2 / (4 * np.log(2)))
B = 2 * np.pi / 21
out = {}
for name, band in [('band_T>=21', (0, B)), ('T>126', (0, 2*np.pi/126)), ('T21-126', (2*np.pi/126, B))]:
    f = aqn.whittle_fit(y, band=band)
    out[name] = {k: float(f[k]) for k in ('alpha', 'se_alpha', 'logq', 'se_logq', 'logs2')}
    print(name, out[name])
z = (out['T>126']['alpha'] - out['T21-126']['alpha']) / np.hypot(out['T>126']['se_alpha'], out['T21-126']['se_alpha'])
c = aqn.whittle_corner_fit(y, band=(0, B))
out['inband_z'] = float(z); out['inband_corner'] = {k: float(v) for k, v in c.items() if np.isscalar(v) and not isinstance(v, str)}
print('in-band z', z, 'corner', out['inband_corner'])
json.dump(out, open('driver_band.json', 'w'), indent=1)
