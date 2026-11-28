#!/usr/bin/env bash
# premerge.sh: every check, on a fresh clone, at one exact commit. The one pre-merge command (process/PROCESS.md
# section 5, R2). Writes $GTAO_PREMERGE_DIR/<sha>.ok only when every step exits 0 and none says PARTIAL;
# tools/merge.sh refuses to merge a head without that file.
#
#   tools/premerge.sh <PR-number>        the PR's live head (gh pr view), its body for the summary checks
#   tools/premerge.sh --sha <SHA>        any commit reachable from the remote (for example the new main after a merge)
#
# Environment: GTAO_REPO_URL (default: the GitHub repository), GTAO_PREMERGE_DIR (default ~/.gtao-premerge),
# GTAO_GH (default gh), GTAO_REPO_SLUG (default Chad-Mitchell/theory-of-adaptive-organization), GTAO_PREMERGE_CHECKS (a newline-separated list of commands; replaces the default list,
# for tests only), GTAO_PREMERGE_LOCK (default /tmp/gtao-premerge.lock). The clone is deleted on exit.
set -uo pipefail
REPO_URL="${GTAO_REPO_URL:-https://github.com/Chad-Mitchell/theory-of-adaptive-organization.git}"
OKDIR="${GTAO_PREMERGE_DIR:-$HOME/.gtao-premerge}"
GH="${GTAO_GH:-gh}"
SLUG="${GTAO_REPO_SLUG:-Chad-Mitchell/theory-of-adaptive-organization}"  # gh needs the repository when run outside a clone
PR=""; SHA=""
case "${1:-}" in
  --sha) SHA="${2:?--sha needs a commit}";;
  ''|-h|--help) sed -n 2,12p "$0"; exit 2;;
  *) PR="$1"; [[ "$PR" =~ ^[0-9]+$ ]] || { echo "premerge: PR must be a number"; exit 2; };;
esac
# One premerge at a time: a run that was interrupted but not killed, plus a resume that started another, piled up
# until the box load made correct trees time out. The lock file names its holder ("pid N key K"). A new run for the
# same PR first stops that holder (the whole process tree), then takes the lock; behind a run for another PR it
# stops with exit 3 and does not queue.
LOCK="${GTAO_PREMERGE_LOCK:-/tmp/gtao-premerge.lock}"; KEY="${PR:-$SHA}"
exec 9>>"$LOCK"
if ! flock -n 9; then
  read -r _ HOLDER _ HKEY < <(tail -n 1 "$LOCK"); HOLDER="${HOLDER//[^0-9]/}"
  if [[ -n "$HOLDER" && "$HKEY" == "$KEY" ]] && tr '\0' ' ' < "/proc/$HOLDER/cmdline" 2>/dev/null | grep -q premerge.sh; then
    killtree() { local c; for c in $(pgrep -P "$1"); do killtree "$c"; done; kill "$1" 2>/dev/null; }
    echo "premerge: stopping the stale premerge of $KEY (pid $HOLDER)"; killtree "$HOLDER"
  fi
  flock -w 15 9 || { echo "premerge: RESULT: REFUSED, another premerge holds $LOCK ($(tail -n 1 "$LOCK"))"; exit 3; }
fi
echo "pid $$ key $KEY" > "$LOCK"
WORK="$(mktemp -d /tmp/gtao-premerge.XXXXXX)"
trap 'rm -rf "$WORK"' EXIT
if [[ -n "$PR" ]]; then
  SHA="$("$GH" pr view "$PR" -R "$SLUG" --json headRefOid -q .headRefOid)" || { echo "premerge: cannot read the head of #$PR"; exit 2; }
  "$GH" pr view "$PR" -R "$SLUG" --json body -q .body > "$WORK/body.md" || exit 2
fi
[[ "$SHA" =~ ^[0-9a-f]{7,40}$ ]] || { echo "premerge: bad commit '$SHA'"; exit 2; }
git clone -q "$REPO_URL" "$WORK/repo" || exit 2
cd "$WORK/repo" || exit 2
if [[ -n "$PR" ]]; then git fetch -q origin "pull/$PR/head" 2>/dev/null || true; fi
git checkout -q --detach "$SHA" 2>/dev/null || { git fetch -q origin "$SHA" && git checkout -q --detach "$SHA"; } || {
  echo "premerge: $SHA not found"; exit 2; }
SHA="$(git rev-parse HEAD)"
echo "premerge: $SHA${PR:+ (#$PR)} on a fresh clone"
if [[ -n "${GTAO_PREMERGE_CHECKS:-}" ]]; then
  mapfile -t CHECKS <<< "$GTAO_PREMERGE_CHECKS"
else
  PRARGS=""; [[ -n "$PR" ]] && PRARGS="--pr $PR --body-file $WORK/body.md"
  [[ -f tools/premerge_checks.txt ]] || { echo "premerge: $SHA has no tools/premerge_checks.txt"; exit 2; }
  CHECKS=()
  while IFS= read -r line; do
    [[ -z "${line// }" || "$line" == \#* ]] && continue
    CHECKS+=("${line//\$PRARGS/$PRARGS}")
  done < tools/premerge_checks.txt
fi
FAILED=0; LOG="$WORK/log.txt"; : > "$LOG"
for c in "${CHECKS[@]}"; do
  [[ -z "$c" ]] && continue
  out="$(nice -n 19 bash -c "$c" 2>&1)"; rc=$?
  status=PASS
  if (( rc != 0 )); then status="FAIL (exit $rc)"; FAILED=1
  elif grep -q "RESULT: PARTIAL" <<< "$out"; then status="FAIL (PARTIAL)"; FAILED=1; fi
  printf '%-90s %s\n' "$c" "$status" | tee -a "$LOG"
  if [[ "$status" != PASS ]]; then tail -n 25 <<< "$out" | sed 's/^/    /'; fi
done
if (( FAILED )); then
  echo "premerge: RESULT: FAIL at $SHA (no .ok written)"; exit 1
fi
mkdir -p "$OKDIR"
# Complete or absent: write beside the target and rename only now that every check has passed, with the count of checks
# in the header so merge.sh can tell a whole file from a cut one.
{ echo "sha $SHA"; echo "pr ${PR:-none}"; echo "date $(date -Iseconds)"; echo "checks $(wc -l < "$LOG" | tr -d ' ')"; cat "$LOG"; } > "$OKDIR/.$SHA.tmp" \
  && mv "$OKDIR/.$SHA.tmp" "$OKDIR/$SHA.ok"
echo "premerge: RESULT: PASS at $SHA; wrote $OKDIR/$SHA.ok"
