"""GRID-DX: committed verdicts, wording, and retained historical arm scores."""
import json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parents[1]
G = ROOT / "theory/measured/grid"

GB_HEADLINE = "NOT A TEST (not qualified; proxy: failed)"
PASS_STATUS = "NOT A TEST (qualification not established; proxy: passed)"
FAIL_STATUS = "NOT A TEST (qualification not established; proxy: failed)"


def test_qualification_verdict_and_wording():
    q = json.loads((G / "qualification_verdict.json").read_text())
    assert q["verdict"] == "NOT QUALIFIED"
    assert q["headline"] == GB_HEADLINE
    assert "law" not in q["headline"].lower()
    assert q["locked_g1_arm_deleted"] is False
    assert q["g3b_used"] is False
    assert q["definition_commit"].startswith("36416d2")
    assert q["definition_commit_main_reachable"].startswith("b311a40")
    assert q["prereg_sha_original"].startswith("5d0c11a")
    assert q["prereg_sha"].startswith("d70c540") or q["prereg_sha"].startswith("5d0c11a")
    assert q["R_go_live_2011_2026"] == 7
    assert q["R_with_cessations_upper"] == 9
    assert q["R_is_informational_not_a_T_red_test"] is True
    assert q["items"]["a_cost_to_fitness_map"] == "not established"
    assert q["items"]["b_population_proxy"] == "failed"
    assert q["items"]["c_resolvable_band"] == "failed"
    assert q["items"]["d_power"] == "failed"
    assert q["items"]["e_redesign_time_same_world"] == "failed"
    # Locked arm scores were not deleted.
    r2 = (G / "RESULTS_GRID2.md").read_text()
    assert "**FAIL on proxy**" in r2
    assert GB_HEADLINE in r2
    assert "not a test of the law" not in r2.lower()
    r3 = (G / "RESULTS_GRID3_4.md").read_text()
    assert "the GRID-2 G1 FAIL replicates" in r3
    assert GB_HEADLINE in r3
    # QUALIFICATION: BSIS sourced; (a) not established; inertia is world change;
    # falling requirement is a design choice; go-live count not a T_red test.
    qual = (G / "QUALIFICATION.md").read_text()
    assert "not established" in qual
    assert "https://www.ofgem.gov.uk/sites/default/files/docs/2015/03/electricity_so_incentives_-_final_proposals_2.pdf" in qual
    assert "https://www.ofgem.gov.uk/sites/default/files/docs/2017/03/final_proposals_for_electricity_system_operator_incentives_from_april_2017.pdf" in qual
    assert "b311a40" in qual
    assert "design choice" in qual
    assert "not a test of 10 T_red" in qual
    assert "229" in qual and "168" in qual
    assert "no blinding for Part A" in qual or "no blinding" in qual.lower()
    # Post-miss gloss is flagged, not used as a fail.
    assert "gloss written after the GRID-2 miss" in qual


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
    assert grids["AU_NEM"]["S_is_lower_bound"] is True
    assert grids["AU_NEM"]["S_sigma_status"] == "MISSING"
    assert grids["IE_NI"]["S_is_lower_bound"] is True
    text = (G / "SELECTION_SCORES.md").read_text()
    assert "MISSING" in text
    assert "lower bound" in text
    assert "S_N rubric ambiguity" in text


def test_rank_test_untested_when_n_lt_5():
    # Locked rule: n < 5 complete (S, d) pairs => UNTESTED. This pass has only GB d1.
    text = (G / "RESULTS_GRIDDX.md").read_text()
    assert "n = 1" in text
    assert "n < 5 ⇒ the test is **UNTESTED**" in text
    assert "d1 = 3" in text
    assert "UNTESTED/INCONCLUSIVE" in text
    assert "1,800 MW" in text or "1800 MW" in text
    assert "ruin slack" in text.lower() or "ruin-slack" in text.lower()
    assert "ROBUSTNESS.md" in text
    assert "cannot test the hypothesis as scored" in text
    assert "competing design lineages" in text
    assert GB_HEADLINE in text
    assert "law" not in text.lower() or "law" in " ".join(
        ln for ln in text.splitlines() if "law" in ln.lower() and "gloss" in ln.lower()
    )  # allow only flagged uses; this file should have none
    assert "law" not in text.lower()


def test_claim_map_retype_and_new_rows():
    cm = (ROOT / "measurement/CLAIM_MAP_v2.md").read_text()

    def status(pid):
        m = re.search(r"^\| " + pid + r" \|.*?\|.*?\|\s*\*\*([^*]+)\*\*", cm, re.M)
        assert m, pid
        return m.group(1)

    assert status("P19") == GB_HEADLINE
    assert status("P21") == GB_HEADLINE
    assert status("P18") == PASS_STATUS
    assert status("P20") == PASS_STATUS
    assert status("H3") == PASS_STATUS
    assert status("P1") == FAIL_STATUS
    assert "Qualification prospect (reviewer judgment, not a result)" in cm
    assert "not a test of the law" not in cm
    assert status("P23") == "DECIDED"
    assert status("P24") == "INCONCLUSIVE"
    assert status("P25") == "OPEN"
    # Historical arm scores remain in the cells.
    assert "G1 (count by degree) FAIL on proxy, by the locked rule" in cm
    assert "Original status, kept as history, not deleted: **PROXY-PASS**" in cm
    assert "not qualified" in cm
    assert "1,800 MW" in cm
    assert "ROBUSTNESS.md" in cm
    assert "UNTESTED/INCONCLUSIVE" in cm
    # Status column does not use the old labels.
    for pid in ("P19", "P21"):
        assert status(pid) != "NOT APPLICABLE"
