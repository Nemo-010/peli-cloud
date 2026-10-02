#!/bin/sh
# regressions-anon-vms.sh - do the delivered artifacts actually hold, and do the
# checks FAIL against the tree this commit was built on?
#
# Usage:
#   sh tests/regressions-anon-vms.sh            # check the working tree
#   sh tests/regressions-anon-vms.sh --stash    # stash the tracked changes and
#                                               # expect every clause to fail
#
# The `--stash` mode is the point: a regression clause that passes against the
# unpatched tree is not testing the patch. It stashes only TRACKED files, so the
# new untracked tools remain and the checks are exercised on the old data.
set -u
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT"

STASH=0
[ "${1:-}" = "--stash" ] && STASH=1

pass=0; fail=0
check() { # name, shell command expected to exit 0
  name="$1"; shift
  if sh -c "$*" >/dev/null 2>&1; then
    echo "ok   $name"; pass=$((pass+1))
  else
    echo "FAIL $name"; fail=$((fail+1))
  fi
}

stash_on()  { git stash push --quiet -m regressions-anon-vms -- . 2>/dev/null || true; }
stash_off() { git stash pop --quiet 2>/dev/null || true; }
[ "$STASH" = 1 ] && stash_on

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
check "page_in_step_with_json" 'python3 tools/render-anon-vms.py >/dev/null && git diff --quiet -- docs/ANONYMOUS-VMS.md'
# 5. The no-credit ranking column exists per provider.
check "usage_json_has_no_credit" 'python3 -c "
import json,sys
d=json.load(open(\"data/usage.json\"))
p=d[\"providers\"][0]
sys.exit(0 if \"costs_no_credit\" in p and \"ranks_no_credit\" in p else 1)"'
# 6. The no-credit ranking is a real re-sort: Kedge falls when its credit is removed.
check "credit_mover_kedge" 'python3 -c "
import json,sys
d=json.load(open(\"data/usage.json\"))
k=[p for p in d[\"providers\"] if p[\"id\"]==\"kedge\"][0]
sys.exit(0 if k[\"ranks_no_credit\"][\"m10h\"] > k[\"ranks\"][\"m10h\"] else 1)"'
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

[ "$STASH" = 1 ] && stash_off

echo
echo "passed=$pass failed=$fail"
if [ "$STASH" = 1 ]; then
  echo "(stash mode: a low pass count is the expected result)"
fi
[ "$fail" = 0 ]
