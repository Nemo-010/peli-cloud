#!/usr/bin/env python3
"""check-relay-egress.py - guard the relay colo/egress measurement.

Asserts the invariants the report relies on, so a mutated or stale
data/relay-colo-egress.json fails here instead of being read as fact:

  - exactly four colos, each with an egress IP
  - every egress IP inside Cloudflare's 104.28.0.0/16
  - the four egress IPs are distinct (the rotation claim)
  - the forward probe is live and returned an SSH banner
  - the relay policy still says a forward token is required

Usage: python3 tools/check-relay-egress.py [data/relay-colo-egress.json]
Exit 0 = all invariants hold, 1 = at least one failed (printed).
"""
import ipaddress
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "data", "relay-colo-egress.json")

fails = []


def check(ok, msg):
    if not ok:
        fails.append(msg)


try:
    d = json.load(open(PATH))
except Exception as e:  # noqa: BLE001
    print(f"FAIL cannot read {PATH}: {e}")
    sys.exit(1)

colos = d.get("colos", [])
check(len(colos) == 4, f"expected 4 colos, got {len(colos)}")

ips = []
for c in colos:
    ip = c.get("egress_ip")
    check(bool(ip), f"{c.get('host')}: no egress_ip")
    if ip:
        ips.append(ip)
        try:
            check(ipaddress.ip_address(ip) in ipaddress.ip_network("104.28.0.0/16"),
                  f"{c.get('host')}: egress {ip} outside 104.28.0.0/16")
        except ValueError:
            check(False, f"{c.get('host')}: egress {ip} not an IP")

check(len(set(ips)) == len(ips), f"egress IPs not distinct: {ips}")

f = d.get("forward_probe", {})
check(f.get("verdict") == "live", f"forward verdict {f.get('verdict')!r} != 'live'")
check(str(f.get("banner", "")).startswith("SSH-2.0"), f"banner {f.get('banner')!r} not SSH-2.0")

check(d.get("policy", {}).get("token_required") is True, "policy.token_required is not true")

if fails:
    for m in fails:
        print("FAIL", m)
    sys.exit(1)
print(f"ok: {len(colos)} colos, distinct egress in 104.28/16, forward live, token required")
