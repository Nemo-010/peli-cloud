#!/bin/sh
# page-in-step.sh - is docs/ANONYMOUS-VMS.md exactly what the JSON renders to?
#
# The page is a pure function of data/anonymous-vms.json. Render it into a
# scratch directory and compare bytes with the committed page. A `git diff`
# would also go red when the JSON itself is dirty, which is not the claim being
# tested; a byte comparison against a fresh render is.
#
# Usage: sh tools/page-in-step.sh
set -eu
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
PAGE="$ROOT/docs/ANONYMOUS-VMS.md"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

ANON_VMS_OUT="$TMP/ANONYMOUS-VMS.md" python3 "$ROOT/tools/render-anon-vms.py" >/dev/null

if cmp -s "$TMP/ANONYMOUS-VMS.md" "$PAGE"; then
  echo "page is in step with data/anonymous-vms.json"
  exit 0
fi
echo "page DIFFERS from a fresh render of the JSON" >&2
diff -u "$PAGE" "$TMP/ANONYMOUS-VMS.md" | head -40 >&2
exit 1
