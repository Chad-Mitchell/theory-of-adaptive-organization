"""Runs theory/shannon_checks/shannon_checks.py (converse, achievability, duality, Farrell on input cost)."""
import importlib.util
import os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load_checks():
    path = os.path.join(ROOT, "theory", "shannon_checks", "shannon_checks.py")
    spec = importlib.util.spec_from_file_location("shannon_checks", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_shannon_checks_all_pass():
    r = subprocess.run(
        [sys.executable, os.path.join(ROOT, "theory", "shannon_checks", "shannon_checks.py")],
        capture_output=True, text=True, timeout=300,
    )
    assert r.returncode == 0, r.stdout + r.stderr
    assert "ALL PASS" in r.stdout


def test_memoryless_counterexample_undercuts_old_floor_and_sits_above_corrected():
    sc = _load_checks()
    a, Q, k, s2 = 0.9, 1.0, 2, 0.2
    h, kappa, c, w = 1.0, 0.1, 0.1, 1.0
    J, I, r, P, D = sc.memoryless_cost(a, Q, k, kappa, c, w, s2)
    J_old, _ = sc.retracted_floor_with_layer_charge(a, Q, k, h, kappa, c, w)
    J_new, _ = sc.floor_cost(a, Q, k, kappa, c, w)
    assert abs(P - 0.193) < 5e-4
    assert abs(I - 1.654) < 5e-4
    assert abs(r - 0.950) < 5e-4
    assert abs(D - 1.936) < 5e-4
    assert abs(J - 2.197) < 5e-4
    assert abs(J_old - 3.187) < 5e-4
    assert J < J_old
    assert J_new <= J + 1e-9


def test_farrell_input_cost_identity():
    sc = _load_checks()
    a, Q, k = 0.9, 1.0, 2
    kappa, c, w, h = 0.1, 0.1, 10.0, 0.1
    I, r0, P = sc.kalman_resources(a, Q, 0.05)
    I_w = I + 1.0
    r = 1.5 * r0
    D = sc.lead_loss(a, Q, P, k)
    J_act = h + kappa * I_w + c * r + w * D
    theta = max(sc.I_min(a, Q, P) / I_w, sc.R_seq(a, Q, P) / r)
    Jf_retracted, _ = sc.retracted_floor_with_layer_charge(a, Q, k, h, kappa, c, w)
    J_tech = h + theta * (kappa * I_w + c * r) + w * D
    # Retracted identity on J fails.
    assert abs(theta * (Jf_retracted / J_tech) - (Jf_retracted / J_act)) > 0.2
    C_act = kappa * I_w + c * r
    C_min = kappa * sc.I_min(a, Q, P) + c * sc.R_seq(a, Q, P)
    eta_C = C_min / C_act
    eta_A = eta_C / theta
    assert abs(eta_C - theta * eta_A) < 1e-12
    assert abs(C_act - 0.5680) < 5e-4
    assert abs(C_min - 0.3892) < 5e-4
    assert abs(eta_A - 0.9818) < 5e-4
    assert abs(eta_C - 0.6852) < 5e-4
