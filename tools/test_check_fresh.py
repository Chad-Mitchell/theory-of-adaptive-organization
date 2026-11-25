#!/usr/bin/env python3
"""Tests for tools/check_fresh.py: no maintained page keeps a live fact by hand (25 November 2026).

Run:  python3 -m pytest -q tools/test_check_fresh.py
"""
from __future__ import annotations

import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import check_fresh as cf  # noqa: E402


def _copy(tmp_path):
    d = tmp_path / "r"
    for p in cf.live_pages(ROOT):
        dst = d / p
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(os.path.join(ROOT, p), dst)
    return d


def _plant(tmp_path, rel, text, append=True):
    d = _copy(tmp_path)
    p = d / rel
    p.write_text((p.read_text(encoding="utf-8") if append else "") + text, encoding="utf-8")
    return cf.check(str(d))


def test_real_tree_passes():
    assert cf.check(ROOT) == []


def test_planted_main_sha_fails(tmp_path):
    # Acceptance: a planted "main is abc1234" line fails.
    fails = _plant(tmp_path, "README.md", "\n\nThis page is current: `main` is `abc1234`.\n")
    assert len(fails) == 1 and "main SHA pointer" in fails[0] and "README.md" in fails[0]


def test_planted_open_pr_list_fails(tmp_path):
    fails = _plant(tmp_path, "OPEN_WORK.md", "\n\nOpen upstream PRs not yet merged: #288 (Lean) and #290.\n")
    assert len(fails) == 1 and "open-PR list" in fails[0]


def test_planted_version_string_fails(tmp_path):
    # Acceptance: an edited version string outside its source fails.
    fails = _plant(tmp_path, "theory/README.md", "\n\nThe core is THEORY v2.9 draft.\n")
    assert len(fails) == 1 and "version string" in fails[0]
    fails = _plant(tmp_path, "ONE_PAGER.md", "\n\nClaim statuses: `measurement/CLAIM_MAP_v2.md` (v2.89).\n")
    assert len(fails) == 1 and "version string" in fails[0]


def test_planted_lean_total_fails(tmp_path):
    # Acceptance: an edited Lean total outside AUDIT.json fails.
    fails = _plant(tmp_path, "formal/lean/README.md", "\n\nLean now machine-checks **1370 declarations**.\n")
    assert len(fails) == 1 and "Lean total" in fails[0]


def test_core_canonical_statement_is_allow_listed():
    line = "`THEORY.md` is the canonical statement (v2.9 draft)."
    assert cf.hand_pointers(line, "CORE.md") == []
    assert cf.hand_pointers(line, "README.md") != []


def test_history_block_is_skipped():
    text = "a\n<!-- history:begin -->\nbatch 1: **757 declarations**\n<!-- history:end -->\nb\n"
    assert cf.hand_pointers(text, "formal/lean/README.md") == []


def test_prose_and_tables_are_not_pointers():
    assert cf.hand_pointers("The word main is feedback in prose.") == []
    assert cf.hand_pointers("domain is deadbeef; remain is deadbeef") == []
    assert cf.hand_pointers("| W14 | Prereg locked beside `main` `2c32ade`. | needs data | file |") == []
    assert len(cf.hand_pointers("current to main deadbeef")) == 1
    assert len(cf.hand_pointers("**As of:** Monday, on `main` `2c32ade` (PR #1).")) == 1


def test_cli_exit_codes(tmp_path, capsys):
    assert cf.main(["check_fresh.py", ROOT]) == 0
    d = _copy(tmp_path)
    (d / "README.md").write_text("`main` is `abc1234`\n", encoding="utf-8")
    assert cf.main(["check_fresh.py", str(d)]) == 1
    assert "RESULT: FAIL" in capsys.readouterr().out
