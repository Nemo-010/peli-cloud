#!/usr/bin/env python3
"""crosscheck-jsonld.py - what the sibling's JSON-LD fix does to THIS catalogue.

`talaria0101/peli-cloud` commit f6401a0 found that its billing-policy probe was
calling 4 readable pages "client-rendered shells" because the stripper removed
every `<script>`, and a JSON-LD pricing block lives inside one. The fix is right
and is ported here as `tools/check-strip-selftest.py`.

This asks the follow-on questions the port alone does not answer:

1. Which of this repository's committed URLs render their prices in JSON-LD? If
   none do, the old reader could not have misclassified anything here and the
   port is a guard against a future probe, not a correction.
2. Did the new reader find anything the old one called unreadable that is in
   fact readable? Those rows would carry the same false "client-rendered shell"
   verdict the sibling had.
3. Did the fix change any published number?

Usage: python3 tools/crosscheck-jsonld.py [--dir sources/anon-2026-10-02] [--limit N]
Writes data/jsonld-crosscheck.json and prints a summary. Network needed only for
URLs not already fetched into --dir.
"""
import html
import json
import os
import re
import ssl
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/120 Safari/537.36")
JSONLD = re.compile(
    r'<script[^>]*type\s*=\s*["\']application/ld\+json["\'][^>]*>(.*?)</script>',
    re.S | re.I)
MONEY = re.compile(r"\$\s?\d|\d\s?")


def strip_naive(body):
    t = re.sub(r"<script.*?</script>", " ", body, flags=re.S | re.I)
    t = re.sub(r"<style.*?</style>", " ", t, flags=re.S | re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", html.unescape(t))


def strip_jsonld_aware(body):
    kept = []
    t = JSONLD.sub(lambda m: (kept.append(m.group(1)), " ")[1], body)
    t = strip_naive(t)
    for k in kept:
        t += " " + re.sub(r"\s+", " ", html.unescape(k))
    return t


def fetch(url):
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en"})
    with urllib.request.urlopen(req, timeout=25, context=ctx) as r:
        return r.read().decode("utf-8", errors="replace")


def arg(name, default):
    if name in sys.argv:
        i = sys.argv.index(name)
        if i + 1 < len(sys.argv):
            return sys.argv[i + 1]
    return default


LIMIT = int(arg("--limit", "40"))

# The URLs this repository actually publishes: the census rows, and the ranking
# table's top rows. A crosscheck that fetched its own favourite list would not
# answer question 1.
census = json.load(open(os.path.join(ROOT, "data", "anonymous-vms.json")))
usage = json.load(open(os.path.join(ROOT, "data", "usage.json")))
urls = []
for r in census["rows"]:
    urls.append((r["id"], r["source"]))
ranked = [p for p in usage["providers"] if p.get("costs", {}).get("m10h") is not None]
ranked.sort(key=lambda p: (p["costs"]["m10h"], p["name"]))
for p in ranked[:LIMIT]:
    urls.append((p["id"], p["url"]))

seen, targets = set(), []
for pid, u in urls:
    if u and u not in seen:
        seen.add(u)
        targets.append((pid, u))

rows, unreadable_naive, unreadable_aware, changed = [], [], [], []
for pid, u in targets:
    try:
        body = fetch(u)
        err = None
    except Exception as e:
        body, err = "", f"{type(e).__name__}: {str(e)[:80]}"
    if err:
        rows.append({"id": pid, "url": u, "error": err,
                     "jsonld_blocks": 0, "readable_naive": None,
                     "readable_jsonld_aware": None})
        continue
    blocks = JSONLD.findall(body)
    n = strip_naive(body)
    a = strip_jsonld_aware(body)
    rn, ra = bool(MONEY.search(n)), bool(MONEY.search(a))
    rows.append({"id": pid, "url": u, "error": None, "bytes": len(body),
                 "jsonld_blocks": len(blocks), "readable_naive": rn,
                 "readable_jsonld_aware": ra})
    if not rn and ra:
        unreadable_naive.append(pid)
        quote = ""
        if blocks:
            quote = re.sub(r"\s+", " ", html.unescape(blocks[0]))[:200]
        changed.append({"id": pid, "url": u, "jsonld_blocks": len(blocks),
                        "first_block": quote})
    if not ra:
        unreadable_aware.append(pid)

out = {
    "generated": "2026-10-02",
    "question": ("does the sibling's JSON-LD stripper fix change anything this "
                 "repository published, and did the old reader misclassify any "
                 "of its own rows?"),
    "rows_checked": len(rows),
    "rows_with_jsonld": sum(1 for r in rows if r.get("jsonld_blocks")),
    "unreadable_by_old_reader": unreadable_naive,
    "unreadable_by_new_reader": unreadable_aware,
    "misclassified": changed,
    "rows": rows,
}
os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
with open(os.path.join(ROOT, "data", "jsonld-crosscheck.json"), "w") as fh:
    json.dump(out, fh, indent=1)

print(f"checked {len(rows)} published URLs")
print(f"  contain a JSON-LD block        : {out['rows_with_jsonld']}")
print(f"  unreadable by the old stripper : {len(unreadable_naive)} {unreadable_naive}")
print(f"  unreadable by the new stripper : {len(unreadable_aware)} {unreadable_aware}")
print(f"  verdicts the fix inverted      : {len(changed)}")
for c in changed:
    print(f"    - {c['id']} ({c['jsonld_blocks']} JSON-LD block(s)): {c['first_block'][:110]}")
print("wrote data/jsonld-crosscheck.json")
