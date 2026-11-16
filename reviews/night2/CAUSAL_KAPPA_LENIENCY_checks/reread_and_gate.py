#!/usr/bin/env python3
"""(a) Report-only re-reading of the locked causal-form results under the mirror PASS rule (labels NOT changed).
(b) Gate identity: under mirror PASS, P(PASS|true) = Phi((1-k)SNR - z) and P(FAIL|b=0) = Phi(k SNR - z); for 0<k<=1/2 the
binding leg is FAIL, so MV10's minimal gate |b|S >= (z+z_pi) sigma / k is unchanged. Compared with tools/power_gate.py."""
import json, subprocess, os
from statistics import NormalDist
N = NormalDist(); Phi, zq = N.cdf, N.inv_cdf
R = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
z = 1.96
def verdicts(D, sig, pred, k):
    hi, lo = D + z * sig, D - z * sig
    fail = hi < k * pred
    return {"D": D, "sigma": sig, "pred": pred, "kill_line": round(k * pred, 4), "lo": round(lo, 4), "hi": round(hi, 4),
            "share": round(D / pred, 3), "share_ci": [round(lo / pred, 3), round(hi / pred, 3)],
            "current_rule": "FAIL" if fail else ("PASS" if lo > 0 else "INCONCLUSIVE"),
            "mirror_rule": "FAIL" if fail else ("PASS" if lo > k * pred else "INCONCLUSIVE")}
a = json.load(open(f"{R}/tests/LAB_AKLMT_TAU/results.json"))
cni = json.load(open(f"{R}/reviews/night2/CAUSAL_NULL_INVARIANCE/test_result.json"))
out = {"LAB_AKLMT_TAU primary (Exp 1)": verdicts(a["primary"]["D"], a["primary"]["sigma_boot"], a["primary"]["b_opt"], 0.5),
       "LAB_AKLMT_TAU R3 (Exp 3, report-only)": verdicts(a["R3_exp3"]["D"], a["R3_exp3"]["sigma"], a["R3_exp3"]["b_opt"], 0.5)}
out["CAUSAL_NULL_INVARIANCE locked test (raw keys)"] = {k: v for k, v in cni.items() if not isinstance(v, (list, dict))}
gate = []
for k in (0.25, 0.5):
    for snr in (2.80 / k, 2.80 / k * 0.9):
        mine = {"kappa": k, "snr": round(snr, 3), "P_pass_mirror": round(Phi((1 - k) * snr - z), 4),
                "P_pass_direction": round(Phi(snr - z), 4), "P_fail_null": round(Phi(k * snr - z), 4)}
        pg = json.loads(subprocess.run(["python3", f"{R}/tools/power_gate.py", "contrast", "--sigma", "1", "--effect", str(snr),
                                        "--fail-kappa", str(k), "--sims", "20000"], capture_output=True, text=True).stdout)
        mine["power_gate_met"] = pg.get("gate_met", pg.get("met"))
        mine["mirror_gate_met"] = min(mine["P_pass_mirror"], mine["P_fail_null"]) >= 0.8 - 1e-3
        gate.append(mine)
out["gate"] = gate
print(json.dumps(out, indent=1)); json.dump(out, open(__file__.replace(".py", ".json"), "w"), indent=1)
