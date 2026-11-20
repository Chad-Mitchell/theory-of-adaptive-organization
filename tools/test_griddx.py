"""GRID-DX: committed verdicts follow the locked prereg rules (no raw grid series in git)."""
import json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parents[1]
G = ROOT / "theory/measured/grid"


def test_qualification_verdict_and_wording():
    q = json.loads((G / "qualification_verdict.json").read_text())
    assert q["verdict"] == "NOT QUALIFIED"
    assert q["headline"] == (
        "NOT APPLICABLE (system not qualified): a diagnosis of a patient, not a test of the law"
    )
    assert q["locked_g1_arm_deleted"] is False
    assert q["g3b_used"] is False
    assert q["definition_commit"].startswith("36416d2")
    assert q["prereg_sha"].startswith("5d0c11a")
    assert q["R_go_live_2011_2026"] == 7
    assert q["R_with_cessations_upper"] == 9
    assert all(v == "failed" for v in q["items"].values())
    # Locked arm scores were not deleted.
    r2 = (G / "RESULTS_GRID2.md").read_text()
    assert "**FAIL on proxy**" in r2
    assert "NOT APPLICABLE (system not qualified)" in r2
    r3 = (G / "RESULTS_GRID3_4.md").read_text()
    assert "the GRID-2 G1 FAIL replicates" in r3
    assert "NOT APPLICABLE (system not qualified)" in r3


def test_selection_scores_in_range_and_sum():
    s = json.loads((G / "selection_scores.json").read_text())
    assert s["pass"] == 1
    assert s["window"] == ["2011-01-01", "2026-11-20"]
    grids = s["grids"]
    assert grids["Hawaii"]["status"] == "UNTESTED"
    want = {"GB": 5, "ERCOT": 4, "AU_NEM": 1, "IE_NI": 1, "Nordic": 1, "Continental_Europe": 1}
    for name, total in want.items():
        g = grids[name]
        assert g["status"] == "scored"
        for k in ("S_sigma", "S_N", "S_red", "S_ruin"):
            assert g[k] in (0, 1, 2)
        assert g["S"] == g["S_sigma"] + g["S_N"] + g["S_red"] + g["S_ruin"] == total


def test_rank_test_untested_when_n_lt_5():
    # Locked rule: n < 5 complete (S, d) pairs => UNTESTED. This pass has only GB d1.
    text = (G / "RESULTS_GRIDDX.md").read_text()
    assert "n = 1" in text
    assert "n < 5 ⇒ the test is **UNTESTED**" in text
    assert "d1 = 3" in text


def test_claim_map_retype_and_new_rows():
    cm = (ROOT / "measurement/CLAIM_MAP_v2.md").read_text()
    def status(pid):
        m = re.search(r"^\| " + pid + r" \|.*?\|.*?\|\s*\*\*([^*]+)\*\*", cm, re.M)
        assert m, pid
        return m.group(1)
    assert status("P19") == "NOT APPLICABLE"
    assert status("P21") == "NOT APPLICABLE"
    assert status("P23") == "DECIDED"
    assert status("P24") == "INCONCLUSIVE"
    assert status("P25") == "OPEN"
    # Historical arm scores remain in the cells.
    assert "G1 (count by degree) FAIL on proxy, by the locked rule" in cm
