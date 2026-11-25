#!/usr/bin/env python3
"""Tests for tools/check_open_work.py (run: python3 -m pytest -q tools/test_check_open_work.py)."""
import json, os, shutil, sys, tempfile, textwrap

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import check_open_work as cow


def _copy_repo_slice(dest):
    q = os.path.join("history", "2026-11-20_queue")
    os.makedirs(os.path.join(dest, q, "queue"))
    os.makedirs(os.path.join(dest, "tools"))
    shutil.copy(os.path.join(ROOT, "OPEN_WORK.md"), dest)
    shutil.copy(os.path.join(ROOT, q, "QUEUE.md"), os.path.join(dest, q))
    shutil.copy(os.path.join(ROOT, q, "queue", "items.json"), os.path.join(dest, q, "queue"))


def test_repo_open_work_lists_every_not_done_id():
    missing, item_nd, queue_nd = cow.check(ROOT)
    assert missing == []
    assert len(item_nd) == 62
    assert "N52-N53-SWEEP" in queue_nd
    assert "CAUSAL-OVER-RESPONSE" in queue_nd
    assert "MV9-DECISION" in queue_nd


def test_dropping_an_id_from_open_work_fails():
    dest = tempfile.mkdtemp(prefix="openwork-")
    try:
        _copy_repo_slice(dest)
        path = os.path.join(dest, "OPEN_WORK.md")
        text = open(path, encoding="utf-8").read()
        # Remove only the whole-token occurrences of an unledgered ID.
        ident = "N52-N53-SWEEP"
        assert cow.token_present(text, ident)
        text = text.replace(ident, "DROPPED-ID")
        open(path, "w", encoding="utf-8").write(text)
        missing, _, _ = cow.check(dest)
        assert ident in missing
    finally:
        shutil.rmtree(dest)


def test_sense_cell_is_not_satisfied_by_longer_ids():
    # T10's SENSE-CELL-MATCHED must not count as SENSE-CELL (review 118 S3).
    text = "T10 is `SENSE-CELL-MATCHED` and `SENSE-CELL-EFFORT` only.\n"
    assert not cow.token_present(text, "SENSE-CELL")
    assert cow.token_present(text + " Also `SENSE-CELL` itself.\n", "SENSE-CELL")


def test_items_json_done_status_is_excluded():
    items = [
        {"id": "KEEP-ME", "status": None},
        {"id": "ALREADY-DONE", "status": "DONE"},
    ]
    assert cow.items_not_done(items) == ["KEEP-ME"]
