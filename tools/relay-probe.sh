#!/bin/sh
# relay-probe.sh - measure the tcp.ssh.relay.ajam.dev forward transport and
# its colo pool, and write the result as JSON.
#
# What it does, in order:
#   1. mint a self-service forward token (POST /v1/mint); the value is never
#      printed and lives only in this process
#   2. for each colo in the pool, GET /trace?egress=1&format=text and read the
#      relay identity and the egress IP an external probe observed
#   3. run one forward banner check against a fixed public target (github.com:22)
#   4. assemble data/relay-colo-egress.json and print a table
#
# It needs curl and python3 only. Nothing here is committed as a credential:
# the token is minted per run and dies at its expiry (<=72h).
#
# Usage: sh tools/relay-probe.sh [out.json]
# Exit 0 on a complete probe; 1 if any colo or the banner check did not answer.
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
OUT=${1:-"$ROOT/data/relay-colo-egress.json"}
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
BASE=tcp.ssh.relay.ajam.dev
DOMAIN=ssh.relay.ajam.dev
COLOS="$BASE tcp-1.$DOMAIN tcp-2.$DOMAIN tcp-3.$DOMAIN"
BANNER_TARGET=github.com:22

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

TOK=$(curl -sS --max-time 30 -X POST "https://$BASE/v1/mint" \
        -H "content-type: application/json" -d '{}' \
      | python3 -c 'import sys,json;print(json.load(sys.stdin).get("token",""))')
[ -n "$TOK" ] || { echo "FAIL: could not mint a forward token" >&2; exit 1; }
echo "minted forward token (${#TOK} chars, not printed)"

n=0
for h in $COLOS; do
  n=$((n+1))
  curl -sL --max-time 40 -A "$UA" -H "X-Relay-Token: $TOK" \
    "https://$h/trace?egress=1&format=text" > "$TMP/colo$n.txt" 2>/dev/null || true
  [ -s "$TMP/colo$n.txt" ] || { echo "FAIL: no answer from $h" >&2; exit 1; }
done

curl -sL --max-time 40 -A "$UA" -H "X-Relay-Token: $TOK" \
  "https://$BASE/trace?target=$BANNER_TARGET&banner=1&format=text" > "$TMP/banner.txt" 2>/dev/null || true
[ -s "$TMP/banner.txt" ] || { echo "FAIL: no answer for the banner probe" >&2; exit 1; }

python3 - "$OUT" "$TMP" "$BASE" "$BANNER_TARGET" $COLOS <<'PY'
import json, os, sys, datetime
out, tmp, base, target = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
hosts = sys.argv[5:]

def kv(path):
    d = {}
    for line in open(path, encoding="utf-8", errors="replace"):
        if "=" in line:
            k, _, v = line.strip().partition("=")
            d[k] = v
    return d

colos = []
for i, h in enumerate(hosts, 1):
    d = kv(os.path.join(tmp, "colo%d.txt" % i))
    colos.append({
        "host": h,
        "relay_name": d.get("relay.name"),
        "bucket": d.get("relay.bucket"),
        "region": d.get("relay.region"),
        "egress_ip": d.get("observed_egress.observed_ip"),
        "address_family": d.get("observed_egress.address_family"),
        "egress_road": d.get("observed_egress.road"),
        "connect_ms": int(d.get("observed_egress.connect_ms", 0) or 0),
        "total_ms": int(d.get("observed_egress.total_ms", 0) or 0),
        "allow": d.get("auth.allow"),
        "relay_version": d.get("relay.version"),
    })

b = kv(os.path.join(tmp, "banner.txt"))
forward = {
    "target": target,
    "ok": b.get("target.ok") == "true",
    "verdict": b.get("target.verdict"),
    "dialed": b.get("target.dialed"),
    "address_family": b.get("target.address_family"),
    "road": b.get("target.road"),
    "connect_ms": int(b.get("target.connect_ms", 0) or 0),
    "first_byte_ms": int(b.get("target.first_byte_ms", 0) or 0),
    "bytes_seen": int(b.get("target.bytes_seen", 0) or 0),
    "banner": b.get("target.banner"),
}

doc = {
    "generated": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "relay_base": base,
    "relay_version": colos[0]["relay_version"] if colos else None,
    "policy": {
        "token_required": True,
        "allow": colos[0]["allow"] if colos else None,
        "max_frame_bytes": 262144,
        "dns_guard": True,
        "deny_ports": [],
    },
    "colos": colos,
    "forward_probe": forward,
}
os.makedirs(os.path.dirname(out), exist_ok=True)
json.dump(doc, open(out, "w"), indent=1)
print("wrote", out)
PY

python3 - "$OUT" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
print("%-30s %-8s %-18s %-16s %-8s %s" % ("host", "bucket", "region", "egress_ip", "family", "total_ms"))
for c in d["colos"]:
    print("%-30s %-8s %-18s %-16s %-8s %s" % (
        c["host"], c["bucket"], c["region"], c["egress_ip"], c["address_family"], c["total_ms"]))
f = d["forward_probe"]
print("\nforward %s -> ok=%s verdict=%s dialed=%s banner=%s" % (
    f["target"], f["ok"], f["verdict"], f["dialed"], f["banner"]))
PY

# completeness: every colo answered, and the banner check is live
python3 - "$OUT" <<'PY' || exit 1
import json, sys
d = json.load(open(sys.argv[1]))
assert len(d["colos"]) == 4, "expected 4 colos"
assert all(c["egress_ip"] for c in d["colos"]), "a colo had no egress ip"
assert d["forward_probe"]["verdict"] == "live", "banner probe not live"
PY
echo "PASS: 4 colos measured, forward banner live"
