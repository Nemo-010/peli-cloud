#!/bin/sh
# regressions-relay-forward.sh - do the relay-forward artefacts hold, and does
# the guard FAIL when the data is mutated?
#
# Usage:
#   sh tests/regressions-relay-forward.sh           # check the working tree
#   sh tests/regressions-relay-forward.sh --stash   # check the tree BEFORE the
#                                                   # relay-forward changes
#
# The mutant clauses are the point: a guard that cannot fail is not a guard.
# tools/check-relay-egress.py is run against the committed JSON (must pass) and
# against two mutated copies (must fail).
set -u
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT"

STASH=0
[ "${1:-}" = "--stash" ] && STASH=1
pass=0; fail=0; newfile=0; expected=0
EXPECTED_STASH_FAIL=gitignore_excludes_raw

check() { # name, shell command expected to exit 0
  name="$1"; shift
  if sh -c "$*" >/dev/null 2>&1; then
    if [ "$STASH" = 1 ] && new_file_clause "$name"; then
      echo "new-file $name (did not exist before this change; cannot fail here)"; newfile=$((newfile+1))
    else
      echo "ok   $name"; pass=$((pass+1))
    fi
  elif [ "$STASH" = 1 ] && new_file_clause "$name"; then
    echo "new-file $name (subject removed by the stash; cannot fail here)"; newfile=$((newfile+1))
  elif [ "$STASH" = 1 ] && [ "$name" = "$EXPECTED_STASH_FAIL" ]; then
    echo "expected-fail $name (pre-fix tree lacks the rule; proves the clause tests the change)"; expected=$((expected+1))
  else
    echo "FAIL $name"; fail=$((fail+1))
  fi
}

check_not() { # name, shell command expected to exit non-zero
  name="$1"; shift
  if sh -c "$*" >/dev/null 2>&1; then
    echo "FAIL $name (command unexpectedly succeeded)"; fail=$((fail+1))
  else
    echo "ok   $name"; pass=$((pass+1))
  fi
}

# Clauses whose subject is a file this work created: stashing removes it, so
# they cannot fail in --stash mode and are counted separately.
new_file_clause() {
  case "$1" in
    guard_passes_on_committed|guard_rejects_duplicate_ip|guard_rejects_out_of_block|\
    report_exists|verification_note_exists|probe_parses|fetch_parses|manifest_committed|\
    report_names_four_colos) return 0 ;;
    *) return 1 ;;
  esac
}

stash_on()  {
  git stash push --quiet --include-untracked -m regressions-relay-forward -- . 2>/dev/null \
    || { echo "warning: nothing to stash; clauses test the working tree" >&2; return 1; }
}
stash_off() { git stash pop --quiet 2>/dev/null || true; }
if [ "$STASH" = 1 ]; then
  stash_on || STASH=2
fi

# 1. The guard passes on the committed measurement.
check guard_passes_on_committed 'python3 tools/check-relay-egress.py data/relay-colo-egress.json'

# 2-3. Mutants: the guard must reject them. If either passes, the guard is inert.
if [ -s data/relay-colo-egress.json ]; then
  MUT=$(mktemp)
  python3 - "$MUT" <<'PY'
import json, sys
d = json.load(open("data/relay-colo-egress.json"))
d["colos"][1]["egress_ip"] = d["colos"][0]["egress_ip"]   # duplicate
json.dump(d, open(sys.argv[1], "w"))
PY
  check_not guard_rejects_duplicate_ip "python3 tools/check-relay-egress.py $MUT"
  python3 - "$MUT" <<'PY'
import json, sys
d = json.load(open("data/relay-colo-egress.json"))
d["colos"][0]["egress_ip"] = "203.0.113.7"                 # out of block
json.dump(d, open(sys.argv[1], "w"))
PY
  check_not guard_rejects_out_of_block "python3 tools/check-relay-egress.py $MUT"
  rm -f "$MUT"
else
  echo "new-file guard_rejects_duplicate_ip (subject removed by the stash)"; newfile=$((newfile+1))
  echo "new-file guard_rejects_out_of_block (subject removed by the stash)"; newfile=$((newfile+1))
fi

# 4-9. Tree clauses.
check report_exists        'test -s docs/RELAY-FORWARD.md'
check verification_note_exists 'test -s research/verification/relay-forward-2026-10-02.md'
check probe_parses         'sh -n tools/relay-probe.sh'
check fetch_parses         'sh -n tools/fetch-relay-sources.sh'
check manifest_committed   'test -s sources/relay-2026-10-02/MANIFEST.tsv'
check report_names_four_colos 'grep -q "tcp-3.ssh.relay.ajam.dev" docs/RELAY-FORWARD.md'

# 10. The raw captures are excluded, because they carry the caller's address.
# This clause fails against the pre-fix tree: the rule was added by this work.
check gitignore_excludes_raw 'grep -q "sources/\*\*/\*.raw" .gitignore'

# 11. No credential is committed: no 64-hex token in the files this work writes.
check no_committed_tokens '! grep -rnE "[0-9a-f]{64}" docs/RELAY-FORWARD.md research/verification/relay-forward-2026-10-02.md tools/relay-probe.sh tools/fetch-relay-sources.sh tools/check-relay-egress.py tests/regressions-relay-forward.sh 2>/dev/null | grep -q .'

[ "$STASH" = 1 ] && stash_off

echo
echo "passed=$pass failed=$fail new_file=$newfile expected_fail=$expected"
if [ "$STASH" = 1 ]; then
  echo "(stash mode: $EXPECTED_STASH_FAIL is expected to fail against the pre-fix tree)"
fi
[ "$fail" = 0 ]
