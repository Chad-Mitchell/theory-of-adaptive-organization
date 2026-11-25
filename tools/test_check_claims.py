#!/usr/bin/env python3
"""Mutation tests for tools/check_claims.py.

The clean tree must pass. Each planted error must be reported.
"""
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import check_claims as cc  # noqa: E402


def copy_tree():
    import tempfile
    dest = tempfile.mkdtemp()
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in {".git", "__pycache__"}]
        for name in filenames:
            if not name.endswith((".md", ".py", ".json")):
                continue
            src = os.path.join(dirpath, name)
            rel = os.path.relpath(src, ROOT)
            out = os.path.join(dest, rel)
            os.makedirs(os.path.dirname(out), exist_ok=True)
            shutil.copy(src, out)
    return dest


def fails_of(root):
    return "\n".join(cc.check(root))


def test_clean_tree_passes():
    assert cc.check(ROOT) == []


def test_proved_to_open_mismatch(tmp_path=None):
    root = copy_tree()
    try:
        path = os.path.join(root, "measurement/CLAIM_MAP_v2.md")
        text = open(path, encoding="utf-8").read()
        old = "| T61 | proved-in-model |"
        assert old in text
        open(path, "w", encoding="utf-8").write(text.replace(old, "| T61 | open |", 1))
        got = fails_of(root)
        assert "mismatch" in got, got
    finally:
        shutil.rmtree(root)


def test_unsupported_front_page_claim():
    root = copy_tree()
    try:
        path = os.path.join(root, "README.md")
        with open(path, "a", encoding="utf-8") as fh:
            fh.write("\n\nT99 is PROVED in the model.\n")
        got = fails_of(root)
        assert "unmanaged" in got, got
    finally:
        shutil.rmtree(root)


def test_deleted_source_row():
    root = copy_tree()
    try:
        path = os.path.join(root, "measurement/CLAIM_MAP_v2.md")
        text = open(path, encoding="utf-8").read()
        old = "| THEORY.md:41 |"
        assert old in text
        open(path, "w", encoding="utf-8").write(text.replace(old, "| missing/NO_SUCH.md:1 |", 1))
        got = fails_of(root)
        assert "source missing" in got, got
    finally:
        shutil.rmtree(root)


def test_wrong_review_path():
    root = copy_tree()
    try:
        path = os.path.join(root, "measurement/CLAIM_MAP_v2.md")
        text = open(path, encoding="utf-8").read()
        old = "`reviews/coadaptation_2026-11-21/REVIEW.md`"
        assert old in text
        open(path, "w", encoding="utf-8").write(
            text.replace(old, "`reviews/no-such-review-2026.md`", 1)
        )
        got = fails_of(root)
        assert "review path missing" in got, got
    finally:
        shutil.rmtree(root)


def test_whole_physics_lean_claim():
    root = copy_tree()
    try:
        path = os.path.join(root, "README.md")
        with open(path, "a", encoding="utf-8") as fh:
            fh.write("\n\nThe whole physical theorem is formalized in Lean.\n")
        got = fails_of(root)
        assert "lean overclaim" in got, got
    finally:
        shutil.rmtree(root)


def test_changed_hypothesis_sentence():
    root = copy_tree()
    try:
        path = os.path.join(root, "README.md")
        text = open(path, encoding="utf-8").read()
        assert cc.HYPOTHESIS in text
        changed = cc.HYPOTHESIS.replace("minimize", "maximizes")
        open(path, "w", encoding="utf-8").write(text.replace(cc.HYPOTHESIS, changed, 1))
        got = fails_of(root)
        assert "hypothesis sentence" in got, got
    finally:
        shutil.rmtree(root)


def test_invalid_edge():
    root = copy_tree()
    try:
        path = os.path.join(root, "measurement/CLAIM_MAP_v2.md")
        text = open(path, encoding="utf-8").read()
        old = "CX2:open"
        assert old in text
        open(path, "w", encoding="utf-8").write(text.replace(old, "NO_SUCH_EDGE:bogus", 1))
        got = fails_of(root)
        assert "edge" in got, got
    finally:
        shutil.rmtree(root)


if __name__ == "__main__":
    test_clean_tree_passes()
    test_proved_to_open_mismatch()
    test_unsupported_front_page_claim()
    test_deleted_source_row()
    test_wrong_review_path()
    test_whole_physics_lean_claim()
    test_changed_hypothesis_sentence()
    test_invalid_edge()
    print("RESULT: PASS")


# ---------------------------------------------------------------- views (--write), 25 November 2026
def _edit(root, rel, old, new):
    path = os.path.join(root, rel)
    text = open(path, encoding="utf-8").read()
    assert old in text, (rel, old)
    open(path, "w", encoding="utf-8").write(text.replace(old, new, 1))


def test_hand_edited_view_fails_and_write_restores():
    # Acceptance: a hand-edited claim view fails, and --write restores it.
    root = copy_tree()
    try:
        text = open(os.path.join(root, "README.md"), encoding="utf-8").read()
        view = text[text.index(cc.VIEW_BEGIN):text.index(cc.VIEW_END)]
        line = next(l for l in view.splitlines() if l.startswith("T61 |"))
        _edit(root, "README.md", line, line.replace("proved-in-model", "known"))
        assert "view stale README.md" in fails_of(root)
        assert cc.write_views(root) == ["README.md"]
        assert cc.check(root) == []
        assert open(os.path.join(root, "README.md"), encoding="utf-8").read() == text
    finally:
        shutil.rmtree(root)


def test_view_on_a_page_without_one_fails():
    root = copy_tree()
    try:
        text = open(os.path.join(root, "README.md"), encoding="utf-8").read()
        view = text[text.index(cc.VIEW_BEGIN):text.index(cc.VIEW_END) + len(cc.VIEW_END)]
        with open(os.path.join(root, "ONE_PAGER.md"), "a", encoding="utf-8") as fh:
            fh.write("\n" + view + "\n")
        assert "ONE_PAGER.md carries a claims view" in fails_of(root)
    finally:
        shutil.rmtree(root)


# ---------------------------------------------------------------- direction
def test_data_one_given_a_rank_fails():
    # Acceptance: DATA-ONE given a rank fails.
    root = copy_tree()
    try:
        text = open(os.path.join(root, "OPEN_WORK.md"), encoding="utf-8").read()
        row = next(l for l in text.splitlines() if l.startswith("| DATA-ONE | parked |"))
        _edit(root, "OPEN_WORK.md", row, row.replace("| DATA-ONE | parked |", "| DATA-ONE | 7 |", 1))
        assert "DATA-ONE is parked work" in fails_of(root)
    finally:
        shutil.rmtree(root)


def test_in_parallel_real_system_line_fails():
    # Acceptance: an "In parallel" real-system line, or a rank for RS-SCREEN outside section 9, fails.
    for rel, line in [("theory/PHYSICS_CHAIN_2026-11-23.md", "3. **In parallel (Level 2):** qualify one real system.\n"),
                      ("README.md", "Next after BICAUSAL: RS-SCREEN.\n"),
                      ("theory/README.md", "Real-system work runs in parallel with the physics chain.\n")]:
        root = copy_tree()
        try:
            with open(os.path.join(root, rel), "a", encoding="utf-8") as fh:
                fh.write("\n" + line)
            got = fails_of(root)
            assert "orders real-system work outside OPEN_WORK.md section 9" in got and rel in got, (rel, got)
        finally:
            shutil.rmtree(root)


def test_parked_mention_outside_section_9_passes():
    root = copy_tree()
    try:
        with open(os.path.join(root, "README.md"), "a", encoding="utf-8") as fh:
            fh.write("\nDATA-ONE is parked; the next step is not chosen here.\n")
        assert cc.check(root) == []
    finally:
        shutil.rmtree(root)


def test_parked_row_without_restart_or_decider_fails():
    root = copy_tree()
    try:
        text = open(os.path.join(root, "OPEN_WORK.md"), encoding="utf-8").read()
        row = next(l for l in text.splitlines() if l.startswith("| RS-SCREEN | parked |"))
        _edit(root, "OPEN_WORK.md", row, row.replace("Restart:", "Later:"))
        assert "parked row RS-SCREEN needs" in fails_of(root)
    finally:
        shutil.rmtree(root)


# ---------------------------------------------------------------- summaries
def test_whole_theory_summary_fails():
    # Acceptance: a whole-theory summary with no row cite fails.
    for s in ["Overall the theory is looking promising after this week.",
              "This result shows the theory works.",
              "GTAO is confirmed by the swarm data."]:
        assert cc.summary_fails(s, ROOT), s


def test_exact_status_cite_passes_and_wrong_status_fails():
    # Acceptance: an exact-status cite passes.
    assert cc.summary_fails("T61 is proved-in-model in its named classes, so the heat bound holds there.", ROOT) == []
    assert cc.summary_fails("T61 (PROVED (in-model)) holds for a passive plant.", ROOT) == []
    got = cc.summary_fails("T61 holds in general.", ROOT)
    assert got and "T61 is proved-in-model" in got[0]
    assert cc.summary_fails("The theory's reach grows with this result.", ROOT)
    assert cc.summary_fails("The theory's reach: T61 is proved-in-model in its classes.", ROOT) == []


def test_row_by_row_table_quotes_and_plain_mentions_pass():
    table = "| Row | Result | Rival |\n|---|---|---|\n| T61 | holds in class | Landauer-only |\n"
    assert cc.summary_fails(table, ROOT) == []
    assert cc.summary_fails("> the theory works\n", ROOT) == []
    assert cc.summary_fails("A reviewer wrote \"the theory works\" and we did not adopt it.", ROOT) == []
    assert cc.summary_fails("See T61 and T63 for the classes.", ROOT) == []
