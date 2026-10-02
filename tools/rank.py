#!/usr/bin/env python3
"""rank.py - re-run the catalogue from the derived data.

Question this answers: for a fixed agent workload, which providers can run it
at all, and what is the monthly list bill once recurring free credits and
subscription floors are applied - cheapest first?

The input, data/derived.json, is produced by research/tools/derive.mjs from the
third-party battleships corpus plus research/cards-extra. This script does no
network and no pricing: it sorts, applies the caveat rules below, and writes
the tables. Every number it prints is traceable to a card field or to the
engine's own total.

Usage: python3 tools/rank.py [--data data/derived.json] [--out data]
Exit 0 ran, 2 could not run.
"""
import json
import os
import sys
import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


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
FREE_CREDIT_NOTE = {}


def compute_rate_published(p):
    """True when at least one mode publishes a nonzero compute figure. A $0
    total with no such figure is an unpriced meter (bandwidth, flat pool),
    not a free sandbox."""
    for m in p["facts"].get("modes", []):
        if (m.get("vcpu_h") or 0) > 0 or (m.get("ram_gib_h") or 0) > 0:
            return True
        if m.get("always_on_month_per_instance") is not None:
            return True
        for s in m.get("sizes") or []:
            if (s.get("hour") or 0) > 0 or (s.get("month_cap") or 0) > 0:
                return True
    return False


def classify(p, c):
    """paid | free-tier | unpriced | ineligible."""
    if not c.get("eligible"):
        return "ineligible"
    total = c.get("total")
    if total is None:
        return "unpriced"
    if total > 0:
        return "paid"
    if compute_rate_published(p):
        return "free-tier"
    return "unpriced"


def plan_floor(p):
    """Cheapest self-serve plan fee that is a usage credit: cash you must put
    in each month before usage counts. None when no such plan is published."""
    fees = [pl["fee"] for pl in p["facts"].get("plans", [])
            if pl.get("fee") and pl.get("fee_is_credit")]
    return min(fees) if fees else None


def subscription(p):
    """A recurring plan fee that is NOT a usage credit (a surcharge)."""
    fees = [pl["fee"] for pl in p["facts"].get("plans", [])
            if pl.get("fee") and not pl.get("fee_is_credit")]
    return min(fees) if fees else None


def commit_terms(p):
    out = []
    for m in p["facts"].get("modes", []):
        if "commit" in (m.get("flags") or []):
            out.append(m.get("commit_note") or "term commitment")
        note = (m.get("commit_note") or "")
        if any(w in note.lower() for w in ["month term", "month prepaid", "prepaid", "annual", "commit", "reservation"]):
            out.append(note)
    seen, uniq = set(), []
    for x in out:
        if x not in seen:
            seen.add(x)
            uniq.append(x)
    return uniq[:2]


def caveat_list(p, c):
    cv = list(c.get("caveats") or [])
    f = p.get("free") or {}
    mc = f.get("monthly_credit")
    ot = f.get("one_time_credit")
    if mc:
        cv.append(f"${mc:g}/mo free credit applied")
    if ot:
        cv.append(f"${ot:g} one-time credit")
    fl = plan_floor(p)
    if fl:
        cv.append(f"${fl:g}/mo prepaid minimum (fee is a usage credit)")
    sub = subscription(p)
    if sub:
        cv.append(f"${sub:g}/mo subscription fee")
    net = p["facts"].get("network") or {}
    if net.get("egress_gib") is None and net.get("egress_free_gib") is None:
        cv.append("egress price not published")
    if net.get("ipv4_month"):
        cv.append(f"IPv4 ${net['ipv4_month']:.2f}/mo extra")
    for t in commit_terms(p):
        cv.append(t)
    # dedupe, keep order
    seen, uniq = set(), []
    for x in cv:
        if x not in seen:
            seen.add(x)
            uniq.append(x)
    return uniq


def row_for(p, wl, rank=None):
    c = p["cost"][wl]
    facts = p["facts"]
    return {
        "rank": rank,
        "id": p["id"],
        "name": p["name"],
        "url": p["url"],
        "category": p["category"],
        "isolation": p["isolation"],
        "monthly_usd": c.get("total"),
        "monthly_no_credit_usd": c.get("total_no_credit"),
        "monthly_floor_usd": plan_floor(p),
        "free_monthly_credit_usd": (p.get("free") or {}).get("monthly_credit"),
        "one_time_credit_usd": (p.get("free") or {}).get("one_time_credit"),
        "mode": c.get("mode"),
        "plan": c.get("plan"),
        "eligible": bool(c.get("eligible")),
        "meter": classify(p, c),
        "features": {k: v for k, v in (p["facts"].get("features") or {}).items()
                     if k in ("persistent_disk", "docker_inside", "browser", "desktop", "ssh", "root",
                              "gpu", "arm64", "pause_resume", "open_source", "self_host", "byoc")},
        "reasons": c.get("reasons") or [],
        "caveats": caveat_list(p, c),
    }


def rank_workload(wl):
    rows = [row_for(p, wl) for p in PROVIDERS]
    paid = [r for r in rows if r["meter"] == "paid" and isinstance(r["monthly_usd"], (int, float))]
    elig = sorted(paid, key=lambda r: (r["monthly_usd"], r["name"].lower()))
    for i, r in enumerate(elig, 1):
        r["rank"] = i
    free = sorted([r for r in rows if r["meter"] == "free-tier"], key=lambda r: r["name"].lower())
    unpriced = sorted([r for r in rows if r["meter"] == "unpriced"], key=lambda r: r["name"].lower())
    inelig = sorted([r for r in rows if r["meter"] == "ineligible"], key=lambda r: r["name"].lower())
    return elig, free, unpriced, inelig


def esc(s):
    return str(s).replace("|", r"\|").replace("\n", " ").strip()


def money(v):
    if v is None:
        return "-"
    return f"${v:,.2f}" if v >= 1 else f"${v:.3f}"


def md_table(rows, limit=None):
    lines = ["| # | Provider | $/mo | $/mo no credit | Prepaid min | Free credit | Plan / mode | Caveats |",
             "|---|---|---|---|---|---|---|---|"]
    for r in (rows if limit is None else rows[:limit]):
        lines.append("| {rank} | [{name}]({url}) | {m} | {mn} | {fl} | {fc} | {mode} | {cv} |".format(
            rank=r["rank"], name=esc(r["name"]), url=r["url"],
            m=money(r["monthly_usd"]), mn=money(r["monthly_no_credit_usd"]),
            fl=money(r["monthly_floor_usd"]),
            fc=money(r["free_monthly_credit_usd"]),
            mode=esc((r["plan"] or "") + " / " + (r["mode"] or ""))[:70],
            cv=esc("; ".join(r["caveats"]))[:120]))
    return "\n".join(lines)


os.makedirs(os.path.join(OUT, "rankings"), exist_ok=True)
today = datetime.date.today().isoformat()
summary = ["# Catalogue", "",
           f"Generated {today} by `tools/rank.py` from `data/derived.json`.",
           "All prices are monthly list prices in USD for the fixed workloads below. "
           "`$ /mo no credit` is the same bill with recurring free credits removed. "
           "`Prepaid min` is cash the provider makes you put in before usage counts.", ""]

for wl, wdef in D["workloads"].items():
    elig, free, unpriced, inelig = rank_workload(wl)
    doc = {"workload": wl, "description": wdef["description"], "workload_spec": wdef["w"],
           "generated": today, "paid_count": len(elig), "free_tier_count": len(free),
           "unpriced_count": len(unpriced), "ineligible_count": len(inelig),
           "rows": elig, "free_tier": free, "unpriced": unpriced, "ineligible": inelig}
    with open(os.path.join(OUT, "rankings", f"{wl}.json"), "w") as fh:
        json.dump(doc, fh, indent=1)
    with open(os.path.join(OUT, "rankings", f"{wl}.md"), "w") as fh:
        fh.write(f"# {wl}\n\n{wdef['description']}\n\n")
        fh.write(f"{len(elig)} priced providers of {len(elig) + len(free) + len(unpriced) + len(inelig)}. Sorted cheapest first.\n\n")
        fh.write(md_table(elig))
        if free:
            fh.write("\n\n## Free tiers (no usage rate for this shape; published limits decide)\n\n")
            fh.write(md_table(free))
        if unpriced:
            fh.write("\n\n## Unpriced (billed on a meter this workload does not fix)\n\n")
            for r in unpriced:
                fh.write(f"- [{r['name']}]({r['url']}): {'; '.join(r['caveats'])[:200]}\n")
        fh.write("\n\n## Did not fit\n\n")
        for r in inelig:
            fh.write(f"- {r['name']}: {'; '.join(r['reasons'])[:180]}\n")
    summary += [f"## {wl}", "", wdef["description"], "",
                f"{len(elig)} priced providers fit. Top 40, cheapest first:", "",
                md_table(elig, limit=40), "",
                f"Full table: [rankings/{wl}.md](rankings/{wl}.md)", ""]

with open(os.path.join(OUT, "catalog.md"), "w") as fh:
    fh.write("\n".join(summary))

# effective-cost view: credit-adjusted vs not, for the primary workload
wl = "agent-box"
elig, _, _, _ = rank_workload(wl)
with open(os.path.join(OUT, "credits-vs-floor.md"), "w") as fh:
    fh.write("# Where the credits and the minimums land (agent-box)\n\n")
    fh.write("Providers whose credit-adjusted bill differs from the list bill, and providers with a prepaid minimum.\n\n")
    fh.write("| Provider | $/mo | $/mo no credit | Prepaid min | Free credit/mo | One-time |\n|---|---|---|---|---|---|\n")
    interesting = [r for r in elig if (r["monthly_no_credit_usd"] or 0) - (r["monthly_usd"] or 0) > 0.01
                   or r["monthly_floor_usd"] or (r["one_time_credit_usd"] or 0) > 0]
    for r in sorted(interesting, key=lambda x: x["monthly_usd"]):
        fh.write("| {name} | {m} | {mn} | {fl} | {fc} | {ot} |\n".format(
            name=esc(r["name"]), m=money(r["monthly_usd"]), mn=money(r["monthly_no_credit_usd"]),
            fl=money(r["monthly_floor_usd"]), fc=money(r["free_monthly_credit_usd"]),
            ot=money(r["one_time_credit_usd"])))

print(f"wrote {OUT}/catalog.md and {OUT}/rankings/*")
for wl in D["workloads"]:
    elig, free, unpriced, inelig = rank_workload(wl)
    print(f"  {wl}: {len(elig)} priced / {len(free)} free-tier / {len(unpriced)} unpriced / {len(inelig)} no-fit")
    for r in elig[:5]:
        print(f"    {r['rank']}. {r['name']:<32} {money(r['monthly_usd'])}")
