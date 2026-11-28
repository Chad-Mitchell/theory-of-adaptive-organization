"""Tests for tools/facts.py: generated blocks and the quote check with the frozen-source rule."""
import os
import shutil
import sys
import tempfile

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import facts  # noqa: E402

ROOT = facts.ROOT


def test_real_repo_passes():
    assert facts.check(ROOT) == []


def test_every_block_has_a_generator_and_every_generator_is_used():
    assert facts.used_blocks(ROOT) == set(facts.GENERATORS)


def test_pending_list_equals_the_pending_blocks():
    assert facts.pending_blocks(ROOT) == facts.GEN_PENDING


@pytest.fixture
def tree():
    d = tempfile.mkdtemp()
    for p in ("CORE.md", facts.CLAIM_MAP, "process/LOCKED_BLOBS.txt"):
        os.makedirs(os.path.dirname(os.path.join(d, p)) or d, exist_ok=True)
        shutil.copy(os.path.join(ROOT, p), os.path.join(d, p))
    yield d
    shutil.rmtree(d)


def test_write_then_check_passes_and_a_tally_edit_makes_the_block_stale(tree):
    p = os.path.join(tree, "CORE.md")
    t = open(p, encoding="utf-8").read()
    new, probs = facts.render(tree, "CORE.md", t)
    assert probs == [] and new == t
    cm = os.path.join(tree, facts.CLAIM_MAP)
    s = open(cm, encoding="utf-8").read().replace("| INCONCLUSIVE | 7 |", "| INCONCLUSIVE | 8 |")
    open(cm, "w", encoding="utf-8").write(s)
    new, _ = facts.render(tree, "CORE.md", t)
    assert new != t and "INCONCLUSIVE (8 rows)" in new


def test_unknown_block_and_unmatched_marker_fail(tree):
    _, probs = facts.render(tree, "X.md", "a <!-- gen:nosuch -->1<!-- /gen:nosuch --> b <!-- gen:field -->")
    assert any("unknown gen block" in x for x in probs) and any("unmatched" in x for x in probs)


def _page(d, text, files=None):
    for p, body in (files or {}).items():
        os.makedirs(os.path.dirname(os.path.join(d, p)), exist_ok=True)
        open(os.path.join(d, p), "w", encoding="utf-8").write(body)
    open(os.path.join(d, "P.md"), "w", encoding="utf-8").write(text)
    os.makedirs(os.path.join(d, "process"), exist_ok=True)
    open(os.path.join(d, "process", "LOCKED_BLOBS.txt"), "a").close()
    return facts.quote_fails(d, ["P.md"])


RUN = {"t/x/PREREG.md": "prereg\n", "t/x/RESULTS.md": "We drew 12,093 qualifying draws; 3/8 seeds.\n"}


def test_quote_found_in_a_frozen_run_file_passes():
    d = tempfile.mkdtemp()
    try:
        assert _page(d, "It used 12,093 draws and 3 of 8 seeds (`t/x/RESULTS.md`).\n", RUN) == []
    finally:
        shutil.rmtree(d)


def test_planted_number_fails():
    d = tempfile.mkdtemp()
    try:
        got = _page(d, "It used 12,094 draws (`t/x/RESULTS.md`).\n", RUN)
        assert len(got) == 1 and "not in its cited frozen source" in got[0]
    finally:
        shutil.rmtree(d)


def test_maintained_only_source_fails_and_no_source_fails():
    d = tempfile.mkdtemp()
    try:
        got = _page(d, "Ledger says 30 rows (`m/LEDGER.md`).\n\nAnd 12,093 draws.\n", {"m/LEDGER.md": "30 rows\n"})
        assert any("cites only maintained pages" in x for x in got) and any("cites no source" in x for x in got)
    finally:
        shutil.rmtree(d)


def test_gen_block_math_and_escape_are_not_quotes():
    d = tempfile.mkdtemp()
    try:
        text = ("Field <!-- gen:field -->30 rows<!-- /gen:field -->.\n\nThe exponent \\(1/2\\) holds.\n\n"
                "Section 4 of 9 <!-- q:ok a section number, not a count -->.\n")
        assert _page(d, text) == []
    finally:
        shutil.rmtree(d)


def test_norm_handles_words_commas_and_ratios():
    assert facts.norm("Twelve of 20,000") == "12/20000"
    assert facts.norm("five bars") == "5 bars"


def test_scored_results_definition():
    files = facts.scored_results(ROOT)
    assert "theory/two-route-2026-11-25/RESULTS.md" in files
    assert all(facts.RESULTS_NAME.search(f) for f in files)
    assert "records/tests/EVO1" in facts.scored_folders(ROOT)
