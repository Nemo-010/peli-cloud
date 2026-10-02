#!/usr/bin/env python3
"""check-anon-vms.py - guard the anonymous/free VM list.

Question: does data/anonymous-vms.json contain at least 10 free-or-anonymous
machines that answer SSH, and does every row carry the source and the caveat
this repository requires before a number is published?

Exit 0 when every clause holds, 1 when one does not (and say which).
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "anonymous-vms.json")
FREE_CLASSES = {"anonymous", "free-account", "free-tier-card"}
MIN_SSH = 10
MIN_ROWS = 20

problems = []
d = json.load(open(DATA))
rows = d["rows"]

# 1. The list is not a two-row list.
if len(rows) < MIN_ROWS:
    problems.append(f"only {len(rows)} rows; the brief asks for an enumerable list and this guard wants >= {MIN_ROWS}")

seen = set()
for r in rows:
    rid = r.get("id", "<no id>")
    if rid in seen:
        problems.append(f"{rid}: duplicate id")
    seen.add(rid)
    # 2. Every row must be re-derivable: a source, a quote, a verification note.
    for field in ("id", "name", "class", "source", "quote", "verification", "caveats"):
        if not r.get(field):
            problems.append(f"{rid}: missing {field}")
    if r.get("class") not in FREE_CLASSES | {"dead", "changed", "free-not-a-vm"}:
        problems.append(f"{rid}: unknown class {r.get('class')!r}")
    if r.get("ssh") not in (True, False):
        problems.append(f"{rid}: ssh must be true or false")
    if not isinstance(r.get("account_required"), bool) or not isinstance(r.get("card_required"), bool):
        problems.append(f"{rid}: account_required/card_required must be booleans")

# 3. The point of the brief: at least ten free-or-anonymous SSH machines.
ssh_capable = [
    r for r in rows
    if r.get("class") in FREE_CLASSES and r.get("ssh") is True
]
if len(ssh_capable) < MIN_SSH:
    problems.append(f"only {len(ssh_capable)} free/anon rows with ssh=true; the brief asks for >= {MIN_SSH}")
# 4. And at least one genuinely anonymous (no account at all) row.
anonymous = [r for r in rows if r.get("class") == "anonymous"]
if not anonymous:
    problems.append("no row is class=anonymous; the brief names anonymous VMs explicitly")

print(f"rows={len(rows)} ssh_capable_free_or_anon={len(ssh_capable)} anonymous={len(anonymous)}")
if problems:
    print("FAIL anon_vms_guard")
    for p in problems:
        print(" -", p)
    sys.exit(1)
print("ok anon_vms_guard")
sys.exit(0)
