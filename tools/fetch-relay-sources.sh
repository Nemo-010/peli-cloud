#!/bin/sh
# fetch-relay-sources.sh - re-fetch the tcp.ssh.relay.ajam.dev documents this
# report cites, and write a manifest of url / http status / bytes / sha256.
#
# The relay's own documents are first-party to the relay, not to this
# repository, so raw copies are not committed; this script and the manifest
# are. Re-run it to check a hash or to see what changed.
#
# The two /trace rows are token-gated: the script mints a forward token
# (POST /v1/mint), uses it, and never prints it.
#
# Usage: sh tools/fetch-relay-sources.sh [dir]
set -eu

DEST="${1:-sources/relay-$(date +%F)}"
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
BASE="https://tcp.ssh.relay.ajam.dev"
mkdir -p "$DEST"
TOK=$(curl -sS --max-time 30 -X POST "$BASE/v1/mint" \
        -H "content-type: application/json" -d '{}' \
      | python3 -c 'import sys,json;print(json.load(sys.stdin).get("token",""))')
[ -n "$TOK" ] || { echo "could not mint a token" >&2; exit 1; }

row() { # id, url, token? ("tok" to send it)
  id="$1"; url="$2"; use="$3"
  if [ "$use" = tok ]; then
    code=$(curl -sL --max-time 40 -A "$UA" -H "X-Relay-Token: $TOK" -w "%{http_code}" -o "$DEST/$id.raw" "$url")
  else
    code=$(curl -sL --max-time 40 -A "$UA" -w "%{http_code}" -o "$DEST/$id.raw" "$url")
  fi
  printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$id" "$url" "$code" "$(wc -c < "$DEST/$id.raw")" \
    "$(sha256sum "$DEST/$id.raw" | cut -d' ' -f1)" "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}

{
  printf 'id\turl\thttp\tbytes\tsha256\tfetched\n'
  row llms-txt      "$BASE/llms.txt"      ""
  row llms-full     "$BASE/llms-full.txt" ""
  row relays-json   "$BASE/relays.json"   ""
  row health-detail "$BASE/health?detail=1" ""
  row trace-egress  "$BASE/trace?egress=1&format=text" tok
  row trace-banner  "$BASE/trace?target=github.com:22&banner=1&format=text" tok
} > "$DEST/MANIFEST.tsv"
echo "wrote $DEST/MANIFEST.tsv"
cat "$DEST/MANIFEST.tsv"
