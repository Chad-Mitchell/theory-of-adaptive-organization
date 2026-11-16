"""Post-run summary of C3: identification of each loss's best EWMA gain (flat minima) -> range of the A->B move.
For each loss, gains whose loss is within 1% (and 0.5%) of the minimum; t_A over that set; A->B ln t_A range
(min over B-set minus max over A-set .. max minus min) and the move at each loss's fitted optimum."""
import json, math, numpy as np
d = json.load(open("c3_telegraph_ewma_loss.json"))
out = {"bayes_dln_tA_lattice_switch_law": round(math.log(0.95 / 0.6641), 4)}
for key, lab in (("mse", "MSE(s=1)"), ("abs", "abs(best s)"), ("sign", "sign01")):
    rng = {}
    for tol in (0.005, 0.01):
        ta = {}
        for P in ("A", "B"):
            c = d[P]["curve"]; L = np.array(c[key]); t = np.array(c["tA"])
            m = L <= L.min() * (1 + tol)
            ta[P] = (t[m].min(), t[m].max())
        rng[f"tol{tol}"] = [round(math.log(ta["B"][0] / ta["A"][1]), 3), round(math.log(ta["B"][1] / ta["A"][0]), 3)]
    out[lab] = {"dln_tA_at_fit": d["dln_tA_A_to_B"][lab], "dln_tA_range_within_tol": rng}
out["kalman_cont_gain_dln_tA"] = round(math.log(d["B"]["tA_at_kalman"] / d["A"]["tA_at_kalman"]), 4)
print(json.dumps(out, indent=1)); json.dump(out, open("c3_flatness.json", "w"), indent=1)
