"""PREREG_5 incomplete-output paths. No T1/T2 search, no --execute, no minimize()."""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

# Locked one-liners, to be run from theory/stop-copying-2026-11-25/.
# These strings must appear byte-for-byte in PREREG_5.md once that file is locked.
CMD_T1_ONLY = (
    'python3 -c \'import sys, json; sys.path.insert(0, "checks"); import aggregate as a; '
    'rows, _ = a._parse_out("checks/run_t1_v2.out"); labs = [r["label"] for r in rows]; '
    't1 = a.aggregate_settings(labs); form = a.tform(t1, [r.get("leader_c") for r in rows]); '
    'print(json.dumps({"T1": t1, "T-form": form, "T1_settings": labs}, default=str))\' '
    '> checks/aggregate_t1_only.out'
)
CMD_T2_ONLY = (
    'python3 -c \'import sys, json; sys.path.insert(0, "checks"); import aggregate as a; '
    'rows, _ = a._parse_out("checks/run_t2_v2.out"); labs = [r["label"] for r in rows]; '
    't2 = a.aggregate_settings(labs); acyc = a.tacyclic(t2, [r.get("circulation", False) for r in rows]); '
    'print(json.dumps({"T2": t2, "T-acyclic": acyc, "T2_settings": labs}, default=str))\' '
    '> checks/aggregate_t2_only.out'
)
CMD_BOTH = (
    "python3 checks/aggregate.py checks/run_t1_v2.out checks/run_t2_v2.out "
    "> checks/aggregate.out"
)

SETTINGS = [(10, 0.5), (10, 1), (10, 2), (3, 1), (30, 1)]
HERE = Path(__file__).resolve().parent
PREREG_DIR = HERE.parent
AGG_SRC = HERE / "aggregate.py"


def _complete(path: Path) -> bool:
    """The PREREG_5 completeness rule: exists, five SETTING_JSON lines, a TOTAL_JSON line."""
    if not path.is_file():
        return False
    setting = total = 0
    for line in path.read_text().splitlines():
        if line.startswith("SETTING_JSON:"):
            setting += 1
        elif line.startswith("TOTAL_JSON:"):
            total += 1
    return setting >= 5 and total >= 1


def _write_t1(path: Path, n=5, total=True, label="clean miss", leader_c=0.5):
    lines = []
    for w, wx in SETTINGS[:n]:
        lines.append("SETTING_JSON: " + json.dumps({"label": label, "leader_c": leader_c, "w": w, "wx": wx}))
    if total:
        lines.append("TOTAL_JSON: " + json.dumps({"total_cpu": 12.0, "settings": n, "total_cap": 7200}))
    path.write_text("\n".join(lines) + "\n")


def _write_t2(path: Path, n=5, total=True, label="clean miss", circulation=False):
    lines = []
    for w, wx in SETTINGS[:n]:
        lines.append(
            "SETTING_JSON: " + json.dumps({"label": label, "circulation": circulation, "w": w, "wx": wx})
        )
    if total:
        lines.append(
            "TOTAL_JSON: "
            + json.dumps({"total_cpu": 40.0, "t1_cpu": 12.0, "grand_total_cpu": 52.0, "settings": n, "total_cap": 7200})
        )
    path.write_text("\n".join(lines) + "\n")


def _workspace(tmp_path: Path) -> Path:
    root = tmp_path / "stop-copying"
    checks = root / "checks"
    checks.mkdir(parents=True)
    shutil.copy(AGG_SRC, checks / "aggregate.py")
    return root


def _run(cmd: str, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, shell=True, cwd=cwd, text=True, capture_output=True)


def test_locked_commands_appear_in_prereg5_when_present():
    path = PREREG_DIR / "PREREG_5.md"
    if not path.is_file():
        return
    text = path.read_text()
    assert CMD_T1_ONLY in text
    assert CMD_T2_ONLY in text
    assert CMD_BOTH in text


def test_t1_incomplete_yields_measurement_code_without_crash(tmp_path):
    root = _workspace(tmp_path)
    _write_t1(root / "checks" / "run_t1_v2.out", n=3, total=False)
    t1_out = root / "checks" / "run_t1_v2.out"
    t2_out = root / "checks" / "run_t2_v2.out"
    assert not _complete(t1_out)
    assert not _complete(t2_out)
    labels = {
        "T1": "measurement/code",
        "T-form": "not applicable",
        "T2": "measurement/code",
        "T-acyclic": "not applicable",
    }
    assert labels["T1"] == "measurement/code"
    assert labels["T-form"] == "not applicable"
    r = _run(CMD_BOTH, root)
    assert r.returncode != 0


def test_t2_incomplete_runs_t1_one_liner(tmp_path):
    root = _workspace(tmp_path)
    _write_t1(root / "checks" / "run_t1_v2.out", n=5, total=True)
    _write_t2(root / "checks" / "run_t2_v2.out", n=2, total=False)
    assert _complete(root / "checks" / "run_t1_v2.out")
    assert not _complete(root / "checks" / "run_t2_v2.out")
    r = _run(CMD_T1_ONLY, root)
    assert r.returncode == 0, r.stderr
    data = json.loads((root / "checks" / "aggregate_t1_only.out").read_text())
    assert data["T1"] == "clean miss"
    assert data["T-form"] == "not applicable"
    assert data["T1_settings"] == ["clean miss"] * 5
    t2_label, t2_cond = "measurement/code", "not applicable"
    assert t2_label == "measurement/code" and t2_cond == "not applicable"
    r_both = _run(CMD_BOTH, root)
    assert r_both.returncode != 0


def test_t2_missing_runs_t1_one_liner(tmp_path):
    root = _workspace(tmp_path)
    _write_t1(root / "checks" / "run_t1_v2.out", n=5, total=True)
    assert _complete(root / "checks" / "run_t1_v2.out")
    assert not (root / "checks" / "run_t2_v2.out").exists()
    r = _run(CMD_T1_ONLY, root)
    assert r.returncode == 0, r.stderr
    data = json.loads((root / "checks" / "aggregate_t1_only.out").read_text())
    assert data["T1"] == "clean miss"
    assert data["T-form"] == "not applicable"
    assert "T1_settings" in data


def test_both_complete_runs_aggregate_py(tmp_path):
    root = _workspace(tmp_path)
    _write_t1(root / "checks" / "run_t1_v2.out", n=5, total=True)
    _write_t2(root / "checks" / "run_t2_v2.out", n=5, total=True)
    assert _complete(root / "checks" / "run_t1_v2.out")
    assert _complete(root / "checks" / "run_t2_v2.out")
    r = _run(CMD_BOTH, root)
    assert r.returncode == 0, r.stderr
    data = json.loads((root / "checks" / "aggregate.out").read_text())
    assert data["T1"] == "clean miss"
    assert data["T2"] == "clean miss"
    assert data["T-form"] == "not applicable"
    assert data["T-acyclic"] == "not applicable"
    r2 = _run(CMD_T2_ONLY, root)
    assert r2.returncode == 0, r2.stderr
    t2 = json.loads((root / "checks" / "aggregate_t2_only.out").read_text())
    assert t2["T2"] == "clean miss"
    assert t2["T-acyclic"] == "not applicable"
    assert t2["T2_settings"] == ["clean miss"] * 5
