"""Tests for tools/premerge.sh and tools/merge.sh with a local repository and a stand-in for gh (no network)."""
import os
import shutil
import stat
import subprocess
import tempfile

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
PRE, MERGE = os.path.join(HERE, "premerge.sh"), os.path.join(HERE, "merge.sh")


def run(cmd, env):
    return subprocess.run(cmd, env=env, capture_output=True, text=True)


@pytest.fixture
def world():
    d = tempfile.mkdtemp()
    repo = os.path.join(d, "repo")
    os.makedirs(repo)
    g = lambda *a: subprocess.run(["git", *a], cwd=repo, check=True, capture_output=True, text=True).stdout.strip()
    g("init", "-q", "-b", "main")
    open(os.path.join(repo, "a.txt"), "w").write("a\n")
    g("add", "a.txt")
    g("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "a")
    sha = g("rev-parse", "HEAD")
    log = os.path.join(d, "gh.log")
    gh = os.path.join(d, "gh")
    # stand-in gh: `pr view` prints the head in d/head (or a body); `pr merge` and `api` are logged.
    open(gh, "w").write("""#!/usr/bin/env bash
echo "$*" >> %s
case "$1 $2" in
  "pr view") if [[ "$*" == *body* ]]; then echo body; else cat %s/head; fi;;
  "pr merge") exit 0;;
  "api "*) echo "$HEAD_MAIN";;
esac
""" % (log, d))
    os.chmod(gh, os.stat(gh).st_mode | stat.S_IEXEC)
    open(os.path.join(d, "head"), "w").write(sha + "\n")
    env = dict(os.environ, GTAO_REPO_URL=repo, GTAO_PREMERGE_DIR=os.path.join(d, "ok"), GTAO_GH=gh,
               GTAO_PREMERGE_CHECKS="true\ntest -f a.txt", HEAD_MAIN=sha)
    yield dict(d=d, sha=sha, env=env, log=log)
    shutil.rmtree(d)


def test_pass_writes_ok_for_the_exact_sha_and_removes_the_clone(world):
    before = set(os.listdir("/tmp"))
    r = run([PRE, "7"], world["env"])
    assert r.returncode == 0, r.stdout + r.stderr
    assert os.path.isfile(os.path.join(world["d"], "ok", world["sha"] + ".ok"))
    assert not [x for x in set(os.listdir("/tmp")) - before if x.startswith("gtao-premerge.")]


@pytest.mark.parametrize("checks", ["true\nfalse", "echo 'RESULT: PARTIAL'"])
def test_a_fail_or_partial_writes_nothing(world, checks):
    r = run([PRE, "7"], dict(world["env"], GTAO_PREMERGE_CHECKS=checks))
    assert r.returncode == 1 and "RESULT: FAIL" in r.stdout
    assert not os.path.exists(os.path.join(world["d"], "ok"))


def test_merge_refuses_without_a_pass(world):
    r = run([MERGE, "7"], world["env"])
    assert r.returncode == 1 and "REFUSED" in r.stdout
    assert "pr merge" not in open(world["log"]).read()


def test_merge_refuses_when_the_head_moved_after_the_pass(world):
    assert run([PRE, "7"], world["env"]).returncode == 0
    open(os.path.join(world["d"], "head"), "w").write("f" * 40 + "\n")
    r = run([MERGE, "7"], world["env"])
    assert r.returncode == 1 and "REFUSED" in r.stdout
    assert "pr merge" not in open(world["log"]).read()


def test_merge_uses_a_merge_commit_at_the_checked_head_then_rechecks_main(world):
    assert run([PRE, "7"], world["env"]).returncode == 0
    r = run([MERGE, "7"], world["env"])
    assert r.returncode == 0, r.stdout + r.stderr
    log = open(world["log"]).read()
    assert "pr merge 7 -R Chad-Mitchell/theory-of-adaptive-organization --merge --match-head-commit %s" % world["sha"] in log
    assert "--squash" not in log and "--rebase" not in log
    assert "premerge: RESULT: PASS" in r.stdout


def test_runs_outside_a_clone(world):
    r = subprocess.run([PRE, "7"], env=world["env"], capture_output=True, text=True, cwd="/")
    assert r.returncode == 0, r.stdout + r.stderr
    assert " -R Chad-Mitchell/theory-of-adaptive-organization" in open(world["log"]).read()


def test_the_list_comes_from_the_commit_being_checked(world):
    d = world["d"]
    repo = os.path.join(d, "repo")
    g = lambda *a: subprocess.run(["git", *a], cwd=repo, check=True, capture_output=True, text=True).stdout.strip()
    os.makedirs(os.path.join(repo, "tools"))
    open(os.path.join(repo, "tools", "premerge_checks.txt"), "w").write("# list\ntest -f a.txt\nfalse $PRARGS\n")
    g("add", ".")
    g("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "list")
    open(os.path.join(d, "head"), "w").write(g("rev-parse", "HEAD") + "\n")
    env = {k: v for k, v in world["env"].items() if k != "GTAO_PREMERGE_CHECKS"}
    r = run([PRE, "7"], env)
    assert r.returncode == 1, r.stdout
    assert "test -f a.txt" in r.stdout and "PASS" in r.stdout
    assert "false --pr 7 --body-file" in r.stdout


def test_scripts_never_rebase_squash_or_force():
    for p in (PRE, MERGE):
        t = open(p).read()
        assert "--force" not in t and "--squash" not in t and "--rebase" not in t and "git rebase" not in t


def test_merge_refuses_a_cut_ok_file(world):
    assert run([PRE, "7"], world["env"]).returncode == 0
    ok = os.path.join(world["d"], "ok", world["sha"] + ".ok")
    assert run([MERGE, "7"], world["env"]).returncode == 0    # the whole file is accepted
    lines = open(ok).read().splitlines()
    for cut in (lines[:4], lines[:5]):                        # header only, or one check of two
        open(ok, "w").write("\n".join(cut) + "\n")
        r = run([MERGE, "7"], world["env"])
        assert r.returncode == 1 and "not a complete premerge pass" in r.stdout
    open(ok, "w").write("")
    assert run([MERGE, "7"], world["env"]).returncode == 1
