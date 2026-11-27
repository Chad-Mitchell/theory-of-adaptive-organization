"""Tests for tools/movemap.py: the one move map."""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import movemap as mm  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_map_is_one_to_one_and_round_trips():
    assert mm.check_map() == []
    assert len(mm.MOVES) == 19


def test_longest_prefix_wins_both_ways():
    assert mm.forward("reviews/night1/formal/AXIOMS.md") == "theory/axioms/AXIOMS.md"
    assert mm.forward("reviews/night1/OTHER.md") == "records/reviews/night1/OTHER.md"
    assert mm.forward("theory/reviews/x.md") == "records/reviews/theory/x.md"
    assert mm.backward("records/reviews/theory/x.md") == "theory/reviews/x.md"
    assert mm.forward("theory/CORE_x.md") == "theory/CORE_x.md"
    assert mm.forward("tests") == "records/tests"


def test_swarm_rule_is_a_design_and_its_cases_stay_in_the_case_index():
    assert mm.forward("theory/SWARM_RULE_2026-11-23.md") == "theory/swarm/SWARM_RULE.md"
    assert mm.forward("theory/swarm_checks/a.py") == "theory/swarm/checks/a.py"
    assert mm.forward("applications/CANCER_DEFECTION_2026-11-23.md") == "theory/applications/CANCER_DEFECTION_2026-11-23.md"
    assert mm.forward("applications/README.md") == "theory/applications/README.md"


def test_rewrite_touches_root_relative_paths_only():
    t = "see `tests/F1/RESULTS.md`, [x](NOTES/a.md), theory/tests/y, ../tests/z and /workspace/tests/q"
    r = mm.rewrite(t)
    assert "`records/tests/F1/RESULTS.md`" in r and "(records/notes/a.md)" in r
    assert "theory/tests/y" in r and "../tests/z" in r and "/workspace/tests/q" in r
    assert mm.unrewrite(r) == t


def test_rewrite_does_not_round_trip_on_text_that_already_names_a_new_path():
    t = "records/tests/x"  # already new: unrewrite maps it back, by design
    assert mm.unrewrite(mm.rewrite(t)) != t


def test_rewrite_round_trips_on_every_maintained_page():
    from check_consistency import MAINTAINED_DOCS
    for p in MAINTAINED_DOCS:
        fp = os.path.join(ROOT, p)
        if os.path.isfile(fp):
            t = open(fp, encoding="utf-8").read()
            assert mm.unrewrite(mm.rewrite(t)) == t, p


def test_lock_line_resolves_against_the_pre_move_folder():
    c = mm.resolve_lock_line("records/tests/EVO1/PREREG_EVO.sha256", "../../theory/layers_checks/stores.py")
    assert "theory/layers_checks/stores.py" in c
    c = mm.resolve_lock_line("records/tests/LOCK1/PREREG.sha256", "tests/LOCK1/PREREG.md")
    assert "records/tests/LOCK1/PREREG.md" in c


def test_verify_rewrite_cli_passes_on_an_unchanged_file():
    r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "movemap.py"), "--verify-rewrite", "HEAD",
                        "process/LOCKED_BLOBS.txt"], cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stdout
