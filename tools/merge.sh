#!/usr/bin/env bash
# merge.sh <PR>: merge only the exact head that passed tools/premerge.sh, with a merge commit, then check the new main.
#   - refuses unless $GTAO_PREMERGE_DIR/<head>.ok exists for the PR's live head (SHA guard);
#   - merges with `gh pr merge --merge --match-head-commit <head>` (a merge commit: locks keep their commits);
#   - runs tools/premerge.sh --sha <new main> and reports its result (a FAIL there is a miss to log with tools/miss.py).
set -uo pipefail
GH="${GTAO_GH:-gh}"
SLUG="${GTAO_REPO_SLUG:-Chad-Mitchell/theory-of-adaptive-organization}"  # gh needs the repository when run outside a clone
OKDIR="${GTAO_PREMERGE_DIR:-$HOME/.gtao-premerge}"
HERE="$(cd "$(dirname "$0")" && pwd)"
PR="${1:-}"
[[ "$PR" =~ ^[0-9]+$ ]] || { echo "usage: tools/merge.sh <PR-number>"; exit 2; }
HEAD="$("$GH" pr view "$PR" -R "$SLUG" --json headRefOid -q .headRefOid)" || { echo "merge: cannot read the head of #$PR"; exit 2; }
if [[ ! -f "$OKDIR/$HEAD.ok" ]]; then
  echo "merge: REFUSED. No premerge pass for the live head $HEAD of #$PR. Run tools/premerge.sh $PR first."; exit 1
fi
NOW="$("$GH" pr view "$PR" -R "$SLUG" --json headRefOid -q .headRefOid)"
if [[ "$NOW" != "$HEAD" ]]; then
  echo "merge: REFUSED. The head moved from $HEAD to $NOW while checking."; exit 1
fi
"$GH" pr merge "$PR" -R "$SLUG" --merge --match-head-commit "$HEAD" || { echo "merge: gh pr merge failed"; exit 1; }
MAIN="$("$GH" api "repos/$SLUG/commits/main" -q .sha)" || { echo "merge: merged; cannot read the new main"; exit 1; }
echo "merge: #$PR merged at head $HEAD; new main $MAIN; re-checking it"
"$HERE/premerge.sh" --sha "$MAIN"
