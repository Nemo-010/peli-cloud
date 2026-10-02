#!/usr/bin/env python3
"""rank.py - build the usage-ranked catalogue from the derived costs.

Question: for one fixed sandbox shape, what does each surveyed provider cost
over a sandbox's real horizons - an hour, a 10-hour workday, a day, a week,
10 h/day for a month, and the 24/7 month - and how does the field rank at each?

The prices come from data/derived.json (research/tools/derive.mjs, which runs
the battleships engine - see tools/fetch-corpus.sh). This script does no network
and no pricing. It sorts, adds the caveat notes, and writes the tables. A $0
total with no published compute rate is never ranked as free.

Usage: python3 tools/rank.py [--data data/derived.json] [--out data]
Exit 0 ran, 2 could not run.
"""
import json
import os
import re
import sys
import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HORIZONS = ["r1h", "r10h", "d1", "w1", "m10h", "m30"]
LABELS = {
    "r1h": "1 h",
    "r10h": "10 h",
    "d1": "1 day",
    "w1": "1 week",
    "m10h": "10 h/d x30",
    "m30": "24/7 x30",
}
PRIMARY = "m10h"


def arg(name, default):
    if name in sys.argv:
        i = sys.argv.index(name)
        if i + 1 < len(sys.argv):
            return sys.argv[i + 1]
    return default


DATA = os.path.join(ROOT, arg("--data", "data/derived.json"))
OUT = os.path.join(ROOT, arg("--out", "data"))
if not os.path.exists(DATA):
    print(f"missing {DATA}; run research/tools/derive.mjs first", file=sys.stderr)
    sys.exit(2)

D = json.load(open(DATA))
PROVIDERS = D["providers"]
SHAPE = D.get("shape", {})
WORKLOADS = D["workloads"]


def compute_rate_published(p):
    for m in p["facts"].get("modes", []):
        if (m.get("vcpu_h") or 0) > 0 or (m.get("ram_gib_h") or 0) > 0:
            return True
        if m.get("always_on_month_per_instance") is not None:
            return True
        for s in m.get("sizes") or []:
            if (s.get("hour") or 0) > 0 or (s.get("month_cap") or 0) > 0:
                return True
    return False


def chosen_plan(p, wl):
    name = p["cost"][wl].get("plan")
    for pl in p["facts"].get("plans", []):
        if pl["name"] == name:
            return pl
    return None


def plan_floor(p, wl):
    """Prepaid floor on the plan the engine actually chose: a fee that is a
    usage credit, so usage below it is still billed at the fee."""
    pl = chosen_plan(p, wl)
    return pl["fee"] if pl and pl.get("fee") and pl.get("fee_is_credit") else None


def commit_terms(p):
    out = []
    for m in p["facts"].get("modes", []):
        if "commit" in (m.get("flags") or []):
            out.append(m.get("commit_note") or "term commitment")
    return out[:1]


CORRECTIONS = {
    "netcup": "entry row is VPS Lite 1 (6-month min); VPS 500 is $8.51/mo",
    "oracle-cloud": "unverified: all oracle.com returns 403; Always Free A1 covers this shape ($0)",
    "scaleway": "Stardust disk is billed on top of the instance rate",
    "contabo": "visible $4.40 is a 24-month intro, list is $6.60",
    "lizard": "disputed: pricing page sells Small 2 vCPU/4 GiB at $0.009/h; docs fix 4 vCPU",
    "bright-data-browser": "browser product, bandwidth-metered",
    "unikraft-cloud": "flat pool, no per-shape rate",
    "lightning-ai": "free CPU Studio: 4 h/session then paid, one at a time; rest is Drive storage; 403 here",
    "azure-container-apps": "free grant ($5.40) is Consumption vCPU/GiB, not the Dynamic Sessions mode priced",
    "google-cloud-run": "free tier is the Services grant; row is the Instances (Preview) meter",
}


def engine_caveats(p, wl):
    c = p["cost"][wl]
    out = []
    for x in (c.get("caveats") or []):
        low = x.lower()
        if "stock" in low:
            out.append("stock-limited")
        elif "preview" in low or "beta" in low:
            out.append("preview pricing")
        elif "flat pool" in low:
            out.append("flat pool, billed whether used or not")
        elif "monthly cap" in low:
            out.append("price is one month's rent at every horizon")
    return out


def notes_for(p, m10h):
    cv = []
    if p["id"] in CORRECTIONS:
        cv.append(CORRECTIONS[p["id"]])
    for x in (p["cost"][m10h].get("caveats") or []):
        low = x.lower()
        if "machine size" in low:
            cv.append("no machine size published, not shape-comparable")
        elif "price unknown" in low:
            cv.append(x[:70])
    free_note = (p.get("free") or {}).get("note") or ""
    if re.search(r"always[ _-]?free|free allowance|resource allowance", free_note, re.I):
        cv.append("free tier is a resource allowance, not modelled (see card)")
    f = p.get("free") or {}
    if f.get("monthly_credit"):
        cv.append(f"${f['monthly_credit']:g}/mo free credit")
    if plan_floor(p, m10h):
        cv.append(f"${plan_floor(p, m10h):g}/mo minimum, fee is a usage credit")
    ms = p["facts"].get("features", {}).get("max_session_h")
    if ms and ms < 24:
        cv.append(f"session cap {ms:g} h, needs restarts")
    net = p["facts"].get("network") or {}
    if net.get("egress_gib") is None and net.get("egress_free_gib") is None:
        cv.append("egress unpublished")
    cv.extend(engine_caveats(p, m10h))
    seen, uniq = set(), []
    for x in cv:
        x = x.strip()[:90]
        if x and x not in seen:
            seen.add(x)
            uniq.append(x)
    return "; ".join(uniq[:3])


def direct(cost):
    if cost.get("eligible") and isinstance(cost.get("total"), (int, float)):
        return cost["total"]
    return None


def build_rows():
    rows = []
    for p in PROVIDERS:
        costs = {h: direct(p["cost"][h]) for h in HORIZONS}
        any_eligible = any(v is not None for v in costs.values())
        zero_all = any_eligible and all((v or 0) == 0 for v in costs.values())
        unpriced = zero_all and not compute_rate_published(p)
        notes = notes_for(p, PRIMARY)
        if unpriced:
            notes = "unpriced: no published compute rate" + ("; " + notes if notes else "")
        elif costs.get(PRIMARY) == 0:
            notes = ("free at this horizon (" + (p["cost"][PRIMARY].get("plan") or "free plan") + ")" +
                     ("; " + notes if notes else ""))
        if costs.get(PRIMARY) is None and not unpriced:
            why = "; ".join(p["cost"][PRIMARY].get("reasons") or p["cost"]["r1h"].get("reasons") or [])[:80]
            notes = ("not priceable at 10 h/d x30" + (": " + why if why else "") +
                     ("; " + notes if notes else ""))
        rows.append({
            "id": p["id"], "name": p["name"], "url": p["url"],
            "category": p["category"], "isolation": p["isolation"],
            "costs": costs, "eligible": any_eligible, "unpriced": unpriced,
            "mode": p["cost"][PRIMARY].get("mode") or p["cost"]["r1h"].get("mode"),
            "plan": p["cost"][PRIMARY].get("plan"),
            "reasons": p["cost"][PRIMARY].get("reasons") or p["cost"]["r1h"].get("reasons") or [],
            "caveats": p["cost"][PRIMARY].get("caveats") or [],
            "notes": notes,
        })
    return rows


def money(v):
    if v is None:
        return "-"
    if v == 0:
        return "$0"
    if v < 0.01:
        return f"${v:.4f}"
    if v < 1:
        return f"${v:.3f}"
    if v < 100:
        return f"${v:.2f}"
    return f"${v:,.0f}"


def table(rows, with_rank=True):
    head = ["#", "Provider", "Type", "1 h", "10 h", "1 day", "1 week", "10 h/d x30", "24/7 x30", "Notes"] \
        if with_rank else ["Provider", "Type", "1 h", "10 h", "1 day", "1 week", "10 h/d x30", "24/7 x30", "Notes"]
    lines = ["| " + " | ".join(head) + " |", "|" + "|".join(["---"] * len(head)) + "|"]
    for r in rows:
        typ = f"{r['category']}/{r['isolation'] or '-'}"
        cells = [f"[{r['name']}]({r['url']})", typ] + [money(r["costs"][h]) for h in HORIZONS] + [r["notes"]]
        if with_rank:
            cells = [str(r.get("rank", "-"))] + cells
        lines.append("| " + " | ".join(c.replace("|", r"\|") for c in cells) + " |")
    return "\n".join(lines)


def sort_by(rows, h):
    good = [r for r in rows if r["costs"][h] is not None and not r["unpriced"]]
    good.sort(key=lambda r: (r["costs"][h], r["name"].lower()))
    return good


rows = build_rows()
priced = [r for r in rows if any(v is not None for v in r["costs"].values()) and not r["unpriced"]]
unpriced = [r for r in rows if r["unpriced"]]
nofit = [r for r in rows if not r["eligible"]]

# primary ranking: the realistic agent month (10 h/day for 30 days)
primary = sort_by(rows, PRIMARY)
for i, r in enumerate(primary, 1):
    r["rank"] = i
primary_ids = {r["id"] for r in primary}
nofit_primary = [r for r in rows if r["id"] not in primary_ids and not r["unpriced"]]

# JSON: every provider, costs for every horizon, plus ranks
rank_maps = {h: {r["id"]: i for i, r in enumerate(sort_by(rows, h), 1)} for h in HORIZONS}
out = {
    "generated": datetime.date.today().isoformat(),
    "shape": SHAPE,
    "assumptions": {
        "cpu_util": 0.5, "ram_util": 0.5,
        "horizons": {h: {"label": LABELS[h], "minutes": WORKLOADS[h].get("total_minutes", WORKLOADS[h]["minutes"])} for h in HORIZONS},
        "primary": PRIMARY,
        "note": "list prices, free monthly credits applied, one-time credits not subtracted, "
                "required features/product classes not applied (shape ranking)",
    },
    "providers": [],
}
for r in rows:
    out["providers"].append({
        "id": r["id"], "name": r["name"], "url": r["url"],
        "category": r["category"], "isolation": r["isolation"],
        "costs": r["costs"],
        "ranks": {h: rank_maps[h].get(r["id"]) for h in HORIZONS},
        "mode": r["mode"], "plan": r["plan"],
        "eligible": r["eligible"], "unpriced": r["unpriced"],
        "reasons": r["reasons"], "caveats": r["caveats"], "notes": r["notes"],
    })
os.makedirs(OUT, exist_ok=True)
with open(os.path.join(OUT, "usage.json"), "w") as fh:
    json.dump(out, fh, indent=1)

# Markdown
today = datetime.date.today().isoformat()
md = []
md.append("# Usage-ranked provider catalogue\n")
md.append(f"Generated {today} by `tools/rank.py` from `data/derived.json`. "
          f"Every one of the {len(rows)} surveyed providers is here.\n")
md.append(f"**Shape:** {SHAPE.get('vcpu')} vCPU / {SHAPE.get('ram')} GiB RAM / {SHAPE.get('disk')} GiB disk. "
          "**Assumptions:** CPU 50%, RAM 50%, no persistent disk, no egress. "
          "Prices are list prices in USD for the whole horizon. Free *monthly* credits are applied; one-time credits are not. "
          "Each horizon is the cheapest eligible split into sessions of at least 30 minutes; `sessions`/`session_min` per provider and horizon are in `data/derived.json`. "
          "Required features and product classes are **not** applied: this is a shape ranking.\n")
def total_minutes(h):
    w = WORKLOADS[h]
    return w.get("total_minutes", w["minutes"])


md.append("Horizons: " + ", ".join(f"**{LABELS[h]}** = {total_minutes(h) // 60} h" for h in HORIZONS) + ".\n")
md.append(f"Main table is ranked by **{LABELS[PRIMARY]}** (the realistic agent month). "
          "A dash means the shape cannot be priced on that provider/horizon.\n")

md.append("## Every surveyed provider, ranked by the realistic agent month (10 h/day x 30)\n")
all_sorted = primary + sorted([r for r in rows if r["id"] not in primary_ids], key=lambda r: r["name"].lower())
md.append(table(all_sorted))
md.append("")

# sandbox/container providers only - what most of this corpus is about
sb = [r for r in primary if r["category"] == "agent-sandbox"]
md.append("## Sandbox & container providers only (`agent-sandbox` category)\n")
md.append(f"{len(sb)} of the {len(primary)} priceable providers are sandbox products. "
          "Same shape and sort as above; hyperscaler VMs, PaaS and CI runners are excluded here but present in the full table.\n")
for i, r in enumerate(sb, 1):
    r["rank"] = i
md.append(table(sb))
md.append("")

md.append("## All surveyed providers, cheapest first at each horizon\n")
for h in HORIZONS:
    ranked = sort_by(rows, h)
    md.append(f"### {LABELS[h]} — {len(ranked)} priceable, top {min(25, len(ranked))}\n")
    lines = ["| # | Provider | Type | Cost | Notes |", "|---|---|---|---|---|"]
    for i, r in enumerate(ranked[:25], 1):
        lines.append(f"| {i} | [{r['name']}]({r['url']}) | {r['category']}/{r['isolation'] or '-'} | "
                     f"{money(r['costs'][h])} | {r['notes'].replace('|', r'\|')} |")
    md.append("\n".join(lines) + "\n")

md.append("## Could not be priced at the 10 h/day month (or any horizon)\n")
md.append("| Provider | Type | Reason |")
md.append("|---|---|---|")
for r in nofit + unpriced:
    reason = "; ".join(r["reasons"])[:160] if r["reasons"] else (
        "no published compute rate (meter is bandwidth/pool)" if r["unpriced"] else "shape not offered")
    md.append(f"| [{r['name']}]({r['url']}) | {r['category']}/{r['isolation'] or '-'} | {reason} |")
md.append("")

with open(os.path.join(OUT, "usage.md"), "w") as fh:
    fh.write("\n".join(md))

# keep the old names out of the tree
for stale in ["catalog.md", "credits-vs-floor.md"]:
    p = os.path.join(OUT, stale)
    if os.path.exists(p):
        os.remove(p)
for f in os.listdir(os.path.join(OUT, "rankings")) if os.path.isdir(os.path.join(OUT, "rankings")) else []:
    os.remove(os.path.join(OUT, "rankings", f))
if os.path.isdir(os.path.join(OUT, "rankings")):
    os.rmdir(os.path.join(OUT, "rankings"))

print(f"wrote {OUT}/usage.md and {OUT}/usage.json: {len(rows)} providers")
for h in HORIZONS:
    ranked = sort_by(rows, h)
    top = ", ".join(f"{r['name']} {money(r['costs'][h])}" for r in ranked[:3])
    print(f"  {LABELS[h]:>9}: {len(ranked):>3} priceable | {top}")
print(f"  not priceable: {len(nofit)} | unpriced meters: {len(unpriced)}")
