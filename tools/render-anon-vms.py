#!/usr/bin/env python3
"""render-anon-vms.py - render docs/ANONYMOUS-VMS.md from data/anonymous-vms.json.

The JSON is the source of truth; the prose is fixed. Nothing in the table is
typed here, so the list and the guard cannot drift apart.
Usage: python3 tools/render-anon-vms.py
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "anonymous-vms.json")
# The output path is overridable so a check can render into a scratch directory
# and compare bytes, without rewriting the committed page.
OUT = os.environ.get("ANON_VMS_OUT") or os.path.join(ROOT, "docs", "ANONYMOUS-VMS.md")

d = json.load(open(DATA))
rows = d["rows"]


def group(name):
    return [r for r in rows if r["class"] == name]


def rank_key(r):
    return (0 if r["ssh"] else 1, r["name"].lower())


def table(rs, cols=("Provider", "SSH", "How you get in", "What you get", "Lifetime", "Cost")):
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for r in sorted(rs, key=rank_key):
        link = f"[{r['name']}]({r['source']})"
        ssh = "yes" if r["ssh"] else "no"
        out.append("| " + " | ".join([
            link, ssh, r["ssh_how"], r["resources"], r["lifetime"], r["cost_usd"],
        ]) + " |")
    return "\n".join(out)


def details(rs):
    out = []
    for r in sorted(rs, key=rank_key):
        out.append(f"**{r['name']}** — `{r['class']}`, "
                   f"account={'yes' if r['account_required'] else 'no'}, "
                   f"card={'yes' if r['card_required'] else 'no'}")
        out.append(f"- quote: \u201c{r['quote']}\u201d")
        out.append(f"- checked: {r['verification']}")
        out.append(f"- caveats: {r['caveats']}")
        out.append("")
    return "\n".join(out)


free_anon = [r for r in rows if r["class"] in ("anonymous", "free-account", "free-tier-card")]
ssh_capable = [r for r in free_anon if r["ssh"]]
not_a_vm = [r for r in rows if r["class"] == "free-not-a-vm"]
changed = [r for r in rows if r["class"] in ("changed", "dead")]
md = f"""# Anonymous and free VMs that answer SSH

The catalogue in [`data/usage.md`](../data/usage.md) prices {366} providers at a
fixed shape. This page answers a different question, the one a sandbox that is
being bootstrapped actually asks first: **what can I get a shell on without a
card, without an account, or for nothing — and how do I reach it if the machine
cannot accept an inbound connection?**

Generated from [`data/anonymous-vms.json`](../data/anonymous-vms.json) by
`tools/render-anon-vms.py`. The guard `tools/check-anon-vms.py` fails if the
list drops below ten SSH-capable free-or-anonymous machines or a row loses its
source or its caveat. Prices and quotas are 2026-10-02 unless the row says
otherwise; the fetch is reproducible with `tools/fetch-anon-sources.sh`.

## What the three classes mean

- **anonymous** — no account and no card. The first connect identifies the
  machine by the SSH key that made it.
- **free-account** — signup is required; no card is charged for the free quota.
- **free-tier-card** — a card is required, and a recurring or time-boxed
  allowance covers the machine.

**{len(ssh_capable)} rows below are a free or anonymous machine you can reach
over SSH.** That count is the guard's, not this paragraph's. The reviews of
this pass, including what it did not establish, are in
[`research/deep-reviews-anon-vms.md`](../research/deep-reviews-anon-vms.md).

## 1. Anonymous: no account, no card

{table(group("anonymous"))}

Anonymous means exactly what it says: Railway's own FAQ answers *"Do I need a
Railway account?"* with **"No. Railway identifies you by your SSH key."** It is
the rare case where the signup step is the key itself, and it is the only row
here that needs nothing else. The box lasts 60 minutes to build and 24 hours to
claim; an unclaimed box and its files are deleted.

## 2. Free with an account

{table(group("free-account"))}

These are the durable free rows: shared shells and dev environments that renew
every month, plus the free browser shells. None of them asks for a card.

## 3. Free allowance with a card

{table(group("free-tier-card"))}

The largest machines on the page: Oracle's Always Free A1 allowance and
Google's e2-micro are real 24/7 machines. AWS's free plan is now a six-month
credit that closes the account when it ends, and Azure's 750 hours are twelve
months only.

## 4. Products that changed or died

{table(not_a_vm + changed)}

Two corrections matter here. **Play with Docker**, the canonical anonymous free
VM in every list older than this one, says: *"Play with Docker will be
unavailable starting March 1, 2026."* It is recorded because citing it as live
is a mistake this page exists to prevent. **Fly.io** no longer publishes a free
Machine allowance: the only "first free" left on its pricing page is 10 GB of
volume capacity.

## The detail behind every row

{details(rows)}
## Reaching a box that cannot listen: `dropssh` and a relay

Most of these machines are reachable because the provider grew an SSH endpoint.
A sealed sandbox does not have one, and cannot have one: this host reports
`bind(2) INET` refused with `EACCES`, so no process here can listen on a TCP
port. The catalogued answer is a relay both ends dial out to, with a server that
speaks SSH over the outbound socket.

The errand proved that path end to end on this sandbox with
[`dropssh`](https://github.com/talaria0101/dropssh) and the
[`tcp.ssh.relay.ajam.dev`](https://tcp.ssh.relay.ajam.dev/llms.txt) relay. The
sequence that works, and the three things that fail before it does:

```sh
# 1. a pair: the agent keeps node_token and hands connect_token to the operator
dropssh pair

# 2. the node side. -Y ./passwd is not optional: there is no /etc/passwd here,
#    and a login name that does not exist logs "wrong user".
dropssh serve --name "$NAME" --token "$NODE_TOKEN" \\
  --server "./dropbear -i -E -F -r hostkey -D ak -Y ./passwd"

# 3. the operator side, over the relay
ssh -o ProxyCommand="dropssh connect --name $NAME --token $CONNECT_TOKEN" \\
    user966@"$NAME"
```

Measured on this host, 2026-10-02:

- **The server must read the passwd database from a file.** The shipped
  `dropbear` is immune to `LD_PRELOAD`, and the sandbox has no `/etc/passwd`;
  `dropbear -Y ./passwd` is what turns `Login attempt for wrong user root` into
  `Pubkey auth succeeded for 'user966'`. The passwd line must name **this
  sandbox's uid (966)**, because dropbear refuses a login whose uid differs from
  the server's.
- **The server's paths must not sit under a world-writable directory.** The
  same setup under `/tmp` dies on `"/tmp must be owned by user or root, and not
  writable by group or others"`. `-D`, the host key and the passwd file all live
  under a directory this user owns and this user can execute.
- **A reverse pair is self-service, and its tokens are credentials.** The pair
  above mints its own name and two 64-hex tokens; the relay authenticates the
  tokens, not people. They are not committed here and must not be.

The working session returned `uid=966 gid=965`, `Linux`, and the login's
`$HOME`, and the server logged `Pubkey auth succeeded` — a real SSH session on a
host that cannot bind a port. The full note, with the conditions and the exact
commands, is in
[`research/verification/ssh-relay-2026-10-02.md`](../research/verification/ssh-relay-2026-10-02.md).

## How this was checked

- Sources are fetched by [`tools/fetch-anon-sources.sh`](../tools/fetch-anon-sources.sh)
  into `sources/anon-2026-10-02/`; the committed `MANIFEST.tsv` records the URL,
  HTTP status, byte count and SHA-256 of every page at fetch time.
- The one row that could not be re-fetched (`oracle.com` returns a 1,339-byte
  export-control 403 to this host) is marked `blocked-from-host` and carries the
  carried figure and the reason rather than a silent guess.
- **A page that renders its own words inside a JSON-LD block is not unreadable.**
  A sibling implementation found that stripping every `<script>` threw away a
  schema.org pricing block and made 4 readable pages read as "client-rendered
  shells". [`tools/check-strip-selftest.py`](../tools/check-strip-selftest.py)
  is the reader here, with 8 known-answer cases; `--naive` runs the same cases
  through the pre-fix one-liner and must fail 3 of them.
  [`tools/crosscheck-jsonld.py`](../tools/crosscheck-jsonld.py) then asked what
  that means for this page: of 62 published URLs, 31 carry a JSON-LD block and
  **0 verdicts changed**, so it is a guard rather than a correction. The result
  is in [`data/jsonld-crosscheck.json`](../data/jsonld-crosscheck.json).
- `tools/check-anon-vms.py` gates the list. Run it with:

```sh
python3 tools/check-anon-vms.py       # rows, ssh-capable count, missing fields
python3 tools/render-anon-vms.py      # rewrite this page from the JSON
python3 tools/check-strip-selftest.py # the reader's known-answer cases
python3 tools/crosscheck-jsonld.py    # does the JSON-LD fix change anything
sh tests/regressions-anon-vms.sh      # 14 clauses; --stash proves they can fail
```

The reviews of both passes are in
[`research/deep-reviews-anon-vms.md`](../research/deep-reviews-anon-vms.md),
including what the JSON-LD crosscheck did **not** establish: 31 of 62 published
URLs carry a JSON-LD block, and none of them changed verdict.

*We aim to provide the software that shapes the world of tomorrow.*
"""

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w") as f:
    f.write(md)
print(f"wrote {OUT}: {len(rows)} rows, {len(ssh_capable)} ssh-capable free/anon")
sys.exit(0)
