"""C4: sigma_pred with the joint (alpha, log q) covariance (c3.json) and the noise-profile total derivative; resulting
sigma_D and verdict under the locked rule's form (reviewer recomputation, not a re-score of the lock)."""
import json, math, numpy as np
c2, c3, c1 = json.load(open('c2.json')), json.load(open('c3.json')), json.load(open('c1.json'))
ga = c2['dW21_dalpha']; gq = (c2['planned_lq+0.2']['mean'] - c2['planned_locked']['mean']) / 0.2
C = np.array(c3['cov_alpha_logq']); g = np.array([ga, gq])
P = c3['profile']; dls = (P['-0.7']['W21_planned'] - P['-1.2']['W21_planned']) / 0.5   # total derivative along profile
out = {'dW_dalpha': ga, 'dW_dlogq': gq, 'dW_dlogs2_partial': (c2['planned_ls+0.2']['mean'] - c2['planned_locked']['mean']) / 0.2,
       'dW_dlogs2_total_profile': dls, 'sigma_pred_diag_alpha_only': abs(ga) * math.sqrt(C[0, 0]),
       'sigma_pred_joint': math.sqrt(g @ C @ g + (dls * 0.1185) ** 2)}
W, sd = c1['W21_block126']['W21'], c1['W21_block126']['sd']
for lab, pred, sp in [('locked_constants', 0.2770, 0.0264), ('reviewer_joint', c2['planned_locked']['mean'], out['sigma_pred_joint']),
                      ('free_noise_consistent', c3['profile']['-30.0']['W21_planned'], out['sigma_pred_joint']),
                      ('fullband_inputs', c3['fullband']['W21_planned'], out['sigma_pred_joint'])]:
    D = W - pred; sD = math.hypot(sd, sp)
    v = 'PASS' if abs(D) + 1.96 * sD <= 0.13 else ('FAIL' if abs(D) - 1.96 * sD > 0.13 else 'INCONCLUSIVE')
    out[lab] = {'pred': pred, 'sigma_pred': sp, 'D': D, 'sigma_D': sD, 'verdict': v, 'decisive_resolution': sD <= 0.0401}
json.dump(out, open('c4.json', 'w'), indent=1); print(json.dumps(out, indent=1))
