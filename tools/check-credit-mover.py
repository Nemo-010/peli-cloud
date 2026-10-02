#!/usr/bin/env python3
"""check-credit-mover.py - does removing a free monthly credit move the ranking?

The claim: `data/usage.json`'s `costs_no_credit` / `ranks_no_credit` are a real
re-sort and not a copy of the credit-adjusted numbers, demonstrated by a
provider whose published rank falls once its credit is taken away.

Kedge is that provider: a $5/month credit covers its short horizons entirely, so
it is `$0` at 1 h, 10 h, 1 day and 1 week and rank 10 at the agent month, and
rank 31 without the credit, at $10.68. Because of that credit it is the clearest
case in the table, and a mutation of its record is what proves this check can
fail rather than merely agree.

Usage:
  python3 tools/check-credit-mover.py            # the committed data
  python3 tools/check-credit-mover.py --mutate   # a copy with the credit removed
                                                 # from the no-credit column; the
                                                 # check must FAIL on it
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "usage.json")
HORIZON = "m10h"
MOVERS = ("kedge", "google-cloud-run", "azure-container-apps")


def load():
    d = json.load(open(DATA))
    if "--mutate" not in sys.argv:
        return d
    # The mutation: make the no-credit column identical to the credited one for
    # the movers, which is exactly the "it was never a re-sort" defect.
    for p in d["providers"]:
        if p["id"] in MOVERS:
            p["costs_no_credit"] = dict(p["costs"])
            p["ranks_no_credit"] = dict(p["ranks"])
    return d


d = load()
by_id = {p["id"]: p for p in d["providers"]}
problems = []

for pid in MOVERS:
    p = by_id.get(pid)
    if p is None:
        problems.append(f"{pid}: not in data/usage.json")
        continue
    cn = p.get("costs_no_credit", {}).get(HORIZON)
    cc = p.get("costs", {}).get(HORIZON)
    rn = p.get("ranks_no_credit", {}).get(HORIZON)
    rc = p.get("ranks", {}).get(HORIZON)
    print(f"{pid:24s} with={cc} no_credit={cn} rank_with={rc} rank_no_credit={rn}")
    if cn is None or cc is None or rn is None or rc is None:
        problems.append(f"{pid}: missing a cost or rank at {HORIZON}")
        continue
    if cn <= cc:
        problems.append(f"{pid}: removing the credit did not raise the cost "
                        f"({cn} <= {cc})")
    if rn <= rc:
        problems.append(f"{pid}: removing the credit did not lower the rank "
                        f"({rn} <= {rc})")

if problems:
    print("FAIL credit_mover")
    for x in problems:
        print(" -", x)
    sys.exit(1)
print("ok credit_mover")
sys.exit(0)
