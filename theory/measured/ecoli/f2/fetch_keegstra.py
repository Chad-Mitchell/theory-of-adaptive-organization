#!/usr/bin/env python3
"""Fetch Keegstra et al. 2017 (eLife 6:e27455, CC BY 4.0) Figure 4 source data and write the per-cell table used by
f2_score.py. Fields used: analysis.NoiseAmplitudeFromPSD (eta_OU), analysis.NoiseTimescale (tau_m, s), and
analysis.NoiseAmplitudeFromTimeSeries for the 89 wild-type (CheRB+) cells. Note: in the .mat file the 89-cell
wild-type set is stored under the key 'RBmin' (the paper reports 89 WT and 33 CheRB- cells; counts identify the sets)."""
import io, os, urllib.request, zipfile
import numpy as np, scipy.io as sio
HERE = os.path.dirname(os.path.abspath(__file__))
URL = "https://cdn.elifesciences.org/articles/27455/elife-27455-fig4-data1-v3.zip"
z = zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(URL, timeout=120).read()))
m = sio.loadmat(io.BytesIO(z.read("FIG4.mat")), squeeze_me=True, struct_as_record=False)["FIG4"].analysis
eo, tm, ets = m.NoiseAmplitudeFromPSD, m.NoiseTimescale, m.NoiseAmplitudeFromTimeSeries.RBmin
assert eo.size == tm.size == ets.size == 89
with open(os.path.join(HERE, "keegstra2017_fig4_percell.csv"), "w") as f:
    f.write("cell,eta_OU,tau_m_s,eta_TS\n")
    for i in range(89): f.write(f"{i},{eo[i]:.6g},{tm[i]:.6g},{ets[i]:.6g}\n")
print("wrote 89 cells")
