"""ECOLI-MEM (theory/measured/ecoli): the locked prereg is unchanged and the locked calculation reproduces its verdicts."""
import hashlib, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "theory", "measured", "ecoli")


def test_prereg_hash_matches_lock():
    lock = dict(l.split()[::-1] for l in open(os.path.join(D, "LOCK.txt")) if l.strip())
    h = hashlib.sha256(open(os.path.join(D, "PREREG.md"), "rb").read()).hexdigest()
    assert lock["ecoli/PREREG.md"] == h


def test_locked_calc_reproduces_verdicts(tmp_path):
    out = subprocess.run([sys.executable, os.path.join(D, "ecoli_calc.py")], capture_output=True, text=True, check=True)
    r = json.load(open(os.path.join(D, "results.json")))
    assert r["verdicts"]["A"] == "FAIL" and r["verdicts"]["B"] == "FAIL"
    assert r["verdicts"]["A_label"].startswith("INVALID")
    assert r["verdicts"]["rival_R1_tau_equals_tau_v"]["verdict"] == "FAIL"
    lo, hi = r["arms"]["B"]["tau_range"]
    assert 1.0 < lo < hi < 1.2
    qa = r["arms"]["A"]["check_quartic"]; ra = r["arms"]["A"]["check_riccati"]
    for a, b in zip(sorted(qa), sorted(ra)):
        assert abs(a[0] - b[0]) < 1e-8 and abs(a[1] - b[1]) < 1e-8


def test_coordinates_file():
    m = json.load(open(os.path.join(ROOT, "theory", "measured", "measured.json")))
    y = m["current_map"]["loglat"]
    assert y["lo"] < y["central"] < y["hi"]
    x = m["current_map"]["logR_proxy"]
    assert x["lo"] < x["hi"]
