#!/bin/sh
# regressions-anon-vms.sh - do the delivered artifacts actually hold, and do the
# checks FAIL against the tree this commit was built on?
#
# Usage:
#   sh tests/regressions-anon-vms.sh            # check the working tree
#   sh tests/regressions-anon-vms.sh --stash    # check the tree as it was
#                                               # BEFORE these changes
#
# The `--stash` mode is the point: a regression clause that passes against the
# unpatched tree is not testing the patch. It stashes the files this work added
# or changed (tracked or not, hence --include-untracked), restores them, and
# prints its verdict. A clause about a file that did not exist before the change
# CANNOT fail there, so those clauses are counted separately as `new-file` and a
# reader can see that they were not the ones doing the failing.
set -u
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT"

STASH=0
[ "${1:-}" = "--stash" ] && STASH=1

pass=0; fail=0; newfile=0
check() { # name, shell command expected to exit 0
  name="$1"; shift
  if sh -c "$*" >/dev/null 2>&1; then
    if [ "$STASH" = 1 ] && ! new_file_clause "$name"; then
      echo "new-file $name (did not exist before this change; cannot fail here)"
      newfile=$((newfile+1))
    else
      echo "ok   $name"; pass=$((pass+1))
    fi
  else
    echo "FAIL $name"; fail=$((fail+1))
  fi
}

# Clauses whose subject is a file this work CREATED. Stashing the work removes
# the subject, so these can only pass or error, never fail.
new_file_clause() {
  case "$1" in
    guard_anon_vms|at_least_10_ssh_free|anonymous_row|page_in_step_with_json|\
    ssh_relay_note|anon_page_relay_section|anon_manifest|stripper_selftest|\
    stripper_selftest_fails_naive|jsonld_crosscheck_recorded|credit_mover_guard_can_fail) return 0 ;;
    *) return 1 ;;
  esac
}

stash_on()  {
  git stash push --quiet --include-untracked -m regressions-anon-vms -- . 2>/dev/null \
    || { echo "warning: nothing to stash; the clauses below test the working tree" >&2; return 1; }
}
stash_off() { git stash pop --quiet 2>/dev/null || true; }
if [ "$STASH" = 1 ]; then
  stash_on || STASH=2
fi

# 1. The guard on the anonymous/free VM census passes.
check "guard_anon_vms" 'python3 tools/check-anon-vms.py'
# 2. At least ten SSH-capable free-or-anonymous rows (the brief's floor).
check "at_least_10_ssh_free" 'python3 -c "
import json,sys
d=json.load(open(\"data/anonymous-vms.json\"))
n=[r for r in d[\"rows\"] if r[\"ssh\"] and r[\"class\"] in (\"anonymous\",\"free-account\",\"free-tier-card\")]
sys.exit(0 if len(n)>=10 else 1)"'
# 3. An anonymous row exists and needs no account.
check "anonymous_row" 'python3 -c "
import json,sys
d=json.load(open(\"data/anonymous-vms.json\"))
sys.exit(0 if any(r[\"class\"]==\"anonymous\" and not r[\"account_required\"] for r in d[\"rows\"]) else 1)"'
# 4. The rendered page is in step with the JSON it claims to be generated from.
# The page is a pure function of the JSON: re-render it and require the bytes on
# disk to be identical. A `git diff` would also be red for the source JSON, which
# is not the claim being tested.
check "page_in_step_with_json" 'tools/page-in-step.sh'
# 5. The no-credit ranking column exists per provider.
check "usage_json_has_no_credit" 'python3 -c "
import json,sys
d=json.load(open(\"data/usage.json\"))
p=d[\"providers\"][0]
sys.exit(0 if \"costs_no_credit\" in p and \"ranks_no_credit\" in p else 1)"'
# 6. The no-credit ranking is a real re-sort: Kedge falls when its credit is
#    removed. THIS clause is the one that must fail against the pre-change tree;
#    it is kept identical save for its guard, and the selftest proves the guard
#    bites by running the same predicate against a mutated record.
check "credit_mover_kedge" 'python3 tools/check-credit-mover.py'
# 7. ... and the guard for it can fail: the same predicate over a mutated copy
#    of the data, where the no-credit column was never re-sorted, must fail.
check "credit_mover_guard_can_fail" '! python3 tools/check-credit-mover.py --mutate'
# 7. The SSH/relay method is recorded, with the passwd-file mechanism named.
check "ssh_relay_note" 'grep -q -- "-Y" research/verification/ssh-relay-2026-10-02.md && grep -q "Pubkey auth succeeded" research/verification/ssh-relay-2026-10-02.md'
# 8. The anonymous-VM page carries the relay section and the reproduced result.
check "anon_page_relay_section" 'grep -q "dropssh" docs/ANONYMOUS-VMS.md && grep -q "cannot bind a port" docs/ANONYMOUS-VMS.md'
# 9. No credential is committed: no relay token (dropssh's 64-hex pair tokens)
#    appears in a file this commit adds or changes. The source manifest carries
#    SHA-256 digests and third-party HTML carries hashes, so the clause looks
#    only at the files this work writes: the census, the page, the tools, the
#    notes and the guard.
check "no_committed_tokens" '! grep -rnE "[0-9a-f]{64}" data/anonymous-vms.json docs/ANONYMOUS-VMS.md tools/check-anon-vms.py tools/render-anon-vms.py tools/ssh-relay-check.sh research/verification/ssh-relay-2026-10-02.md tests/regressions-anon-vms.sh 2>/dev/null | grep -q .'
# 10. The source manifest for the census is committed and non-empty.
check "anon_manifest" 'test -s sources/anon-2026-10-02/MANIFEST.tsv && grep -q "railway.com/free-vm" sources/anon-2026-10-02/MANIFEST.tsv'
# 11. The claim-stripper's known-answer cases hold, and the naive stripper these
#     cases exist to catch must FAIL them. Both halves are asserted: a self-test
#     that passes either way is not a self-test.
check "stripper_selftest" 'python3 tools/check-strip-selftest.py'
check "stripper_selftest_fails_naive" '! python3 tools/check-strip-selftest.py --naive'
# 12. The upstream crosscheck is committed and records what it found.
check "jsonld_crosscheck_recorded" 'python3 -c "
import json,sys
d=json.load(open(\"data/jsonld-crosscheck.json\"))
sys.exit(0 if d[\"rows_checked\"] and \"misclassified\" in d else 1)"'

[ "$STASH" = 1 ] && stash_off

echo
echo "passed=$pass failed=$fail new_file=$newfile"
if [ "$STASH" != 0 ]; then
  echo "(stash mode: the clauses about pre-existing files are the ones that must FAIL here)"
fi
[ "$fail" = 0 ]
