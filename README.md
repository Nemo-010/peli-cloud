# peli-cloud

A cheapest-first catalogue of **366** cloud sandbox, container and agent-runtime
providers, priced for a **fixed sandbox shape over real usage horizons** — an
hour, a 10-hour workday, a day, a week, 10 h/day for a month, and the 24/7
month — instead of pretending every sandbox lives forever.

0BSD. Data is facts measured from provider pages; see `NOTICE`.

Full tables: [`data/usage.md`](data/usage.md) (human) and
[`data/usage.json`](data/usage.json) (machine). Every provider is in both.

---

## What this does NOT establish, read this before the rankings

- **It is a shape ranking, not a fit ranking.** Every row means "cheapest
  machine of this shape". Required features (Docker, browser, a sandbox API)
  and product classes are **not** applied. Per-row `features` are in the JSON.
- **The shape is one choice:** 2 vCPU / 4 GiB / a 20 GiB disk, CPU and RAM at
  50 %, persistent-disk billing off, no egress. Disk, egress, IPv4 and seats
  are excluded (many providers would add them). A different shape reorders
  the list.
- **Each horizon is the cheapest eligible split into sessions**, each at least
  30 minutes (a 10 h day may be one 10 h session or two 5 h sessions, whichever
  the provider bills cheaper). This is how a sandbox is actually used — stopped
  between calls — and it is why a provider with an 8 h session cap still
  appears; its note says restarts are needed. One uninterrupted run is not
  what the price is for.
- **It uses the engine's strict `priceCard`, not the site's `priceSoft`.** It is
  not the battleships ranking and must not be compared row for row.
- **354 of 366 providers were not re-verified by hand.** 12 provider pages were
  re-fetched and reconciled (`research/verification/2026-10-02.md`); the rest
  carry the corpus figure at its captured commit.
- **A `$0` row is only a genuine free tier/credit.** A zero with no published
  compute rate is `unpriced` and kept out of the ranking (Bright Data,
  Unikraft). Free tiers are shown with the credit that produces them, and a
  free-tier product leads the list (Lightning AI) because the engine prices it
  honestly; its 4 h session cap is in the note.
- **Recurring free *allowances* are not modelled, only dollar credits.** The
  engine applies `monthly_credit` and `one_time_credit`; a resource allowance
  (so many OCPU-hours or GB-hours a month) is carried as a note and prices at
  list. This matters most for **Oracle**, whose Always Free Ampere A1 allowance
  (1,500 OCPU-h + 9,000 GB-h/month) covers this whole shape **including 24/7**,
  so a qualifying account pays **$0** against the $7.41 shown. GCP, AWS and
  Azure free tiers are too small for a 4 GiB shape and do not change a row.
  Details in `research/verification/2026-10-02.md`.
- **Assume more claims are wrong than the eleven listed at the end.**

## Conditions

- One host, 2026-10-02, reading provider pages over HTTPS. Prices are public
  list prices that day; USD unless stated. EUR→USD at 1.1378 (ECB 2026-09-28).
- 366 provider cards from `ariana-dot-dev/battleships` at commit
  `f6a71ab09fefa68e355ef47c52315e099f99c921`. No cards added.
- Free *monthly* credits are applied; one-time credits are not. Subscription
  floors stay visible.

## Horizon key

| column | means | hours |
|---|---|---|
| 1 h | one hour | 1 |
| 10 h | one agent workday | 10 |
| 1 day | 24 hours | 24 |
| 1 week | 7 days | 168 |
| 10 h/d x30 | 10 h/day for 30 days — the realistic agent month | 300 |
| 24/7 x30 | always on for 30 days | 720 |

Each cell is the cheapest eligible way to deliver those hours as sessions of
at least 30 minutes each, with free *monthly* credits applied and one-time
credits not.

## Sandbox & container providers only

Most of this corpus is sandbox products; the field looks different once the
hyperscaler VMs are out. Ranked by **10 h/d x30**. Full list in
[`data/usage.md`](data/usage.md).

| # | Provider | Type | 1 h | 10 h | 1 day | 1 week | 10 h/d x30 | 24/7 x30 | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 1 | [Agent 37](https://www.agent37.com/pricing) | agent-sandbox/gvisor | $0.0085 | $0.085 | $0.204 | $1.43 | **$2.55** | $6.12 | egress unpublished |
| 2 | [zipbox](https://zipbox.ai/pricing) | agent-sandbox/firecracker | $0.014 | $0.137 | $0.329 | $2.30 | **$4.11** | $9.86 | egress unpublished |
| 3 | [Kedge](https://kedge.dev/docs/billing) | agent-sandbox/vm | $0 | $0 | $0 | $0.984 | **$5.68** | $20.64 | $5/mo free credit |
| 4 | [shellbox](https://shellbox.dev/) | agent-sandbox/firecracker | $0.020 | $0.200 | $0.480 | $3.36 | **$6.00** | $14.40 | egress unpublished |
| 5 | [Lizard](https://lizard.build/pricing) | agent-sandbox/container | $0.022 | $0.218 | $0.524 | $3.67 | **$6.55** | $15.72 | disputed: pricing page sells Small 2 vCPU/4 GiB at $0.009/h; docs fix 4 vCPU |
| 6 | [Upstash Box](https://upstash.com/pricing/box) | agent-sandbox/container | $0.103 | $1.03 | $2.47 | $8.46 | **$8.82** | $9.97 | egress unpublished; flat pool, billed whether used or not |
| 7 | [Together Code Sandbox](https://www.together.ai/pricing) | agent-sandbox/firecracker | $0.030 | $0.300 | $0.720 | $5.04 | **$9.00** | $21.60 | no machine size published, not shape-comparable; egress unpublished |
| 8 | [Sail Research (Sailboxes)](https://docs.sailresearch.com/pricing) | agent-sandbox/firecracker | $0 | $0 | $0 | $5.09 | **$13.01** | $38.21 | $5/mo free credit; egress unpublished |
| 9 | [tama](https://tama.computer/) | agent-sandbox/vm | $0.045 | $0.454 | $1.09 | $7.63 | **$13.62** | $32.70 | egress unpublished |
| 10 | [Coasty](https://coasty.ai/pricing) | agent-sandbox/vm | $0.050 | $0.500 | $1.20 | $8.40 | **$15.00** | $30.00 | no machine size published, not shape-comparable; disk beyond 0 GiB: price unknown; egress unpublished |
| 11 | [Mosaic Sandbox](https://sandbox.mosaicos.com/) | agent-sandbox/firecracker | $0.050 | $0.500 | $1.20 | $8.40 | **$15.00** | $36.00 | egress unpublished |
| 12 | [machine0](https://machine0.io/) | agent-sandbox/vm | $0.052 | $0.520 | $1.25 | $8.74 | **$15.60** | $37.44 |  |
| 13 | [Runtime (withruntime.com)](https://withruntime.com/pricing) | agent-sandbox/firecracker | $0.055 | $0.550 | $1.32 | $9.24 | **$16.50** | $39.60 |  |
| 14 | [Railway](https://railway.com/pricing) | agent-sandbox/vm | $5.00 | $5.00 | $5.00 | $9.34 | **$16.68** | $40.02 | disk beyond 0 GiB: price unknown; $5/mo minimum, fee is a usage credit |
| 15 | [Alibaba Cloud Agent Sandbox / FC / AgentRun](https://help.aliyun.com/zh/agent-sandbox/product-overview/billing-overview) | agent-sandbox/- | $0.056 | $0.562 | $1.35 | $9.44 | **$16.86** | $40.46 | egress unpublished |
| 16 | [Celesto Cloud](https://celesto.ai/pricing) | agent-sandbox/vm | $0.060 | $0.600 | $1.44 | $10.08 | **$18.00** | $43.20 | egress unpublished |
| 17 | [Sandbox0](https://sandbox0.ai/pricing) | agent-sandbox/gvisor | $0.060 | $0.606 | $1.45 | $10.17 | **$18.16** | $43.59 |  |
| 18 | [UCloud Agent Sandbox](https://astraflow.ucloud.cn/docs/agent-sandbox) | agent-sandbox/firecracker | $0.064 | $0.644 | $1.54 | $10.82 | **$19.31** | $46.35 | disk beyond 10 GiB: price unknown; egress unpublished |
| 19 | [PPIO Agent Sandbox](https://ppio.com/docs/sandbox/pricing.md) | agent-sandbox/firecracker | $0.064 | $0.644 | $1.54 | $10.82 | **$19.31** | $46.35 | session cap 1 h, needs restarts; egress unpublished |
| 20 | [Volcano Engine AgentKit / veFaaS sandbox](https://docs.volcengine.com/docs/agentkit/Billing_items?lang=zh) | agent-sandbox/vm | $0.065 | $0.653 | $1.57 | $10.98 | **$19.60** | $47.05 |  |
| 21 | [boat.dev](https://docs.boat.dev/pricing) | agent-sandbox/vm | $20.00 | $20.00 | $20.00 | $20.00 | **$20.00** | $20.00 | disk beyond 12 GiB: price unknown; $20/mo minimum, fee is a usage credit |

`boat.dev` is the clearest case for this whole exercise: **$20 for an hour and
$20 for a month**, because the plan fee is a usage credit. Ranked hourly it is
last; ranked on the realistic month it is mid-field. A 24/7-only list picks one
of those and hides the other.

## Every provider, ranked by the realistic agent month

Top 16 of 179 priceable. **All 366 rows** — every provider surveyed, including
 the 187 that cannot be priced at this shape (185 that fit no sized mode,
 plus 2 unpriced bandwidth/flat-pool meters), each with its reason — are in
[`data/usage.md`](data/usage.md).

| # | Provider | Type | 1 h | 10 h | 1 day | 1 week | 10 h/d x30 | 24/7 x30 | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 1 | [Lightning AI](https://lightning.ai/pricing) | dev-env/vm | $0.0014 | $0.014 | $0.033 | $0.230 | **$0.411** | $0.986 | free CPU Studio stack: 4 h/session then it converts to paid; one at a time; egress unpublished; flat pool, billed whether used or not |
| 2 | [Agent 37](https://www.agent37.com/pricing) | agent-sandbox/gvisor | $0.0085 | $0.085 | $0.204 | $1.43 | **$2.55** | $6.12 | egress unpublished |
| 3 | [Oracle Cloud Infrastructure](https://www.oracle.com/cloud/compute/pricing/) | hyperscaler/vm | $0.010 | $0.103 | $0.247 | $1.73 | **$3.09** | $7.41 | unverified: all oracle.com returns 403; Always Free A1 covers this shape ($0) |
| 4 | [Hetzner Cloud](https://docs.hetzner.com/general/infrastructure-and-availability/price-adjustment/) | hyperscaler/vm | $0.010 | $0.104 | $0.250 | $1.75 | **$3.12** | $6.49 |  |
| 5 | [Azure Container Apps (Consumption, Dedicated, Dynamic Sessions)](https://azure.microsoft.com/en-us/pricing/details/container-apps/) | hyperscaler/vm | $0 | $0 | $0 | $0 | **$3.60** | $16.20 | no machine size published, not shape-comparable; disk beyond 4 GiB: price unknown; $5.4/mo free credit |
| 6 | [zipbox](https://zipbox.ai/pricing) | agent-sandbox/firecracker | $0.014 | $0.137 | $0.329 | $2.30 | **$4.11** | $9.86 | egress unpublished |
| 7 | [Google Cloud Run](https://cloud.google.com/run/pricing) | hyperscaler/gvisor | $0 | $0 | $0 | $0.144 | **$4.36** | $17.77 | $5.22/mo free credit |
| 8 | [IONOS Cloud](https://docs.ionos.com/cloud/support/general-information/price-list/ionos-cloud-eur-en) | hyperscaler/vm | $0.015 | $0.148 | $0.355 | $2.48 | **$4.44** | $10.65 |  |
| 9 | [netcup VPS](https://www.netcup.com/en/server/vps) | hyperscaler/vm | $5.03 | $5.03 | $5.03 | $5.03 | **$5.03** | $5.03 | entry row is VPS Lite 1 (6-month min); VPS 500 is $8.51/mo; price is one month's rent at every horizon |
| 10 | [Kedge](https://kedge.dev/docs/billing) | agent-sandbox/vm | $0 | $0 | $0 | $0.984 | **$5.68** | $20.64 | $5/mo free credit |
| 11 | [Gcore Cloud / Functions / GPU](https://gcore.com/cloud/virtual-machines) | hyperscaler/vm | $0.019 | $0.193 | $0.464 | $3.25 | **$5.80** | $13.92 | disk beyond 0 GiB: price unknown |
| 12 | [Browser Use Cloud](https://browser-use.com/pricing) | browser/- | $0.020 | $0.200 | $0.480 | $3.36 | **$6.00** | $14.40 | no machine size published, not shape-comparable; disk beyond 0 GiB: price unknown; session cap 4 h, needs restarts |
| 13 | [shellbox](https://shellbox.dev/) | agent-sandbox/firecracker | $0.020 | $0.200 | $0.480 | $3.36 | **$6.00** | $14.40 | egress unpublished |
| 14 | [UpCloud](https://upcloud.com/pricing/) | hyperscaler/vm | $0.021 | $0.209 | $0.500 | $3.50 | **$6.25** | $14.00 |  |
| 15 | [Lizard](https://lizard.build/pricing) | agent-sandbox/container | $0.022 | $0.218 | $0.524 | $3.67 | **$6.55** | $15.72 | disputed: pricing page sells Small 2 vCPU/4 GiB at $0.009/h; docs fix 4 vCPU |
| 16 | [Contabo](https://contabo.com/en-us/pricing/) | hyperscaler/vm | $6.60 | $6.60 | $6.60 | $6.60 | **$6.60** | $6.60 | visible $4.40 is a 24-month intro, list is $6.60; price is one month's rent at every horizon |

## Cheapest at each horizon (all providers)

Standouts where the horizon changes the winner — see
[`data/usage.md`](data/usage.md) for the top 25 at each.

| horizon | cheapest | runners-up |
|---|---|---|
| 1 h | Amika $0, Anchor Browser $0, Azure $0 | Blacksmith $0, Buddy Sandboxes $0, Agent 37 $0.0085 |
| 10 h | Amika $0, Anchor Browser $0, Azure $0 | Blacksmith $0, Buildkite $0, Agent 37 $0.085 |
| 1 day | Anchor Browser $0, Azure $0, Blacksmith $0 | CircleCI $0, Freestyle $0, Agent 37 $0.204 |
| 1 week | Azure $0, InsForge $0.038 | Google Cloud Run $0.144, Lightning AI $0.230, Hyperbeam $0.560 |
| 10 h/d x30 | Lightning AI $0.411, Agent 37 $2.55 | Oracle $3.09, Hetzner $3.12, Azure $3.60 |
| 24/7 x30 | Lightning AI $0.986, netcup $5.03 | Agent 37 $6.12, Hetzner $6.49, Contabo $6.60 |

## Findings

1. **Horizon changes the ranking, which is the point.** Lightning AI is first
   at the month horizons ($0.411) because its free CPU Studio is a real free
   tier and the engine prices it that way; netcup costs $5.03 whether you run
   an hour or a month (a monthly VPS, so the 1 h cell is a month's rent — the
   note now says so); Agent 37 is the cheapest paid sandbox at 10 h/day ($2.55)
   and second at 24/7 ($6.12); boat.dev is $20 at every horizon because of its
   floor.
2. **The operator's named edge cases are all covered.** lizard.build and
   freestyle.sh rank directly. Scaleway's Stardust tier is in the corpus card at
   €0.0006/h; at this 2 vCPU/4 GiB shape the engine selects Scaleway's larger
   `shared-development` instance, which is why the Scaleway row is not the
   Stardust price. An earlier draft wrongly called Stardust missing, added a
   duplicate card and briefly ranked it first; it was caught in review and
   removed (`commit 767fa59`).
3. **Free tiers dominate the short end, and one leads the month.** Azure,
   Google Cloud Run, Blacksmith, Kedge, InsForge, Sail, Amika and Freestyle are
   $0 or near-$0 for short use because a free monthly credit or allowance
   covers it. Lightning AI leads the realistic month on a free CPU Studio with
   a 4 h session cap (restart between sessions). That is real, and every row
   says which credit or product produces it.

   It is also the main caveat on the top of the table: the cheapest rows are
   cheapest *because they have a free tier*, not because their paid rate is
   low. Kedge is $5.68 with its $5 credit and $10.68 without it; Azure is $3.60
   with its $5.40 credit and $9.00 without it. `data/derived.json` carries
   `total_no_credit` per provider and horizon for exactly this question; the
   published tables use the credit-applied figure because that is what a new
   account actually pays first.
4. **Fixed pools look cheap hourly and expensive monthly.** Upstash Box is
   $0.103/h but $9.97 for 24/7 (a fixed $8/box). Read the whole row, not the
   first number.
5. **netcup's entry row was wrong, and is now named.** The $5.03 is *VPS Lite 1
   G12.5s* on a 6-month minimum, not the VPS 500 G12.5 the page lists first for
   "No preference Europe" ($8.51/mo on a 1-month term, $7.33 on 12 months,
   both before the $0.57 IPv4). Revision 1 compared the card to the wrong Lite
   plan and called a 7–11 % gap the wrong way round; the real card gap is 2–10 %
   low and closes as the term shortens. If you want the VPS 500 the page shows
   first, the honest 24/7 column is **$8.51**, which drops netcup below Hetzner.
   See `research/verification/2026-10-02.md`.
6. **Two cards sell an identical rate card.** PPIO and UCloud Agent Sandbox quote
   the same figures line-for-line — ￥0.00003/s per vCPU, ￥0.000015/GiB/s of
   memory, ￥0.0005/GB/h of storage — with the same 512 MiB memory steps and the
   same limits. They are separate cards in the corpus with separate domains
   (`ppio.com`, `astraflow.ucloud.cn`), so both are ranked, as two adjacent rows
   at $19.31 each. Recorded as a duplicate candidate, not silently merged.
7. **Hyperbeam's weekly $0.56 is not a rate.** Its `HD participant-hour` size
   is $0.42/h with **10,000 free participant-minutes a month** ($70 of the base
   rate), so every horizon shorter than a week prices at $0 and the week shows
   $0.56. The card's own regime notes come first in `data/derived.json` under
   `caveats` ("machine size per session not published") and its regime file
   warns the size is not a 4 vCPU / 8 GiB equivalent. A row that says $0 for
   an hour and $0.56 for a week, with no machine size, is not comparable to a
   priced sandbox; it carries the caveat rather than being dropped.
8. **A monthly cap shows up as a flat row.** netcup and Contabo are the same
   number in every column because the engine clamps to one month's rent; that is
   right for a VPS and the note says "price is one month's rent at every
   horizon". It is also why they cannot compete in the 1 h column at all, which
   is a statement about their product model, not a missing price.
9. **The tracker proposed Croft** (open PR #1): flat $24/$99 plans, no published
   shape. Recorded, not rankable.
10. **Oracle's paid row is not what a qualifying account pays.** Its Always Free
   Ampere A1 allowance is 1,500 OCPU-hours + 9,000 GiB-hours a month, and this
   shape uses 1,440 + 2,880 even running 24/7 — so the 24/7 row is **$0** for an
   account that qualifies, against the $7.41 the table shows. The allowance is
   scoped to A1 only, capacity can be reclaimed, and the engine prices resource
   allowances as list, so the table keeps the paid number and says so. This is
   the largest single understatement in the catalogue.
11. **Lizard is probably the one row that is too high.** Its pricing page sells
   *Small (2 vCPU / 4 GB) at $0.009/h* — this comparison shape exactly — while
   its sandbox docs say `Create options do not change these limits` (4 vCPU /
   4096 MiB). Both pages are live first-party pages fetched today, and they also
   disagree on Medium's RAM (pricing says 8 GB, docs say 4096 MiB). The table
   keeps the conservative docs reading at $6.55 for 10 h/day; if Small is real
   the row is **$2.70**, second only to Agent 37. Revision 1 called this row
   "confirmed" while quoting the Small line in the same breath — that was a
   lazy confirmation, and it is corrected in `research/verification/2026-10-02.md`.

## Negative results

- **Generic web search is unusable here.** DuckDuckGo lite/html and Bing return
  JavaScript shells; discovery is corpus-led, which is a limit, not coverage.
- **Oracle is blocked at the domain, not the page.** Every `oracle.com` URL,
  `docs.oracle.com`, and the `apexapps` price-list API return the same
  1,339-byte **export-control 403** from this host. Its row is unverified, and
  its Always Free A1 allowance (which would price this shape at $0) is not
  modelled.
- **netcup's number is a lower bound, with the mechanism now known**: the
  comparison shape is $8.51/mo on a 1-month term. `research/reviews.md` pass 4.

## Reproduce

```sh
sh tools/fetch-corpus.sh                 # pin the third-party corpus locally
sh tools/fetch-sources.sh                # re-fetch the 13 first-party pages
node research/tools/derive.mjs --corpus research/corpus --out data/derived.json
python3 tools/rank.py                    # writes data/usage.md and data/usage.json
```

`derive.mjs` needs Node ≥ 18. `rank.py` is pure Python 3 and does no network.

## Provenance and licence

- Corpus, commit, route, gaps: [`research/provenance.md`](research/provenance.md).
- Independent checks and quotes: [`research/verification/2026-10-02.md`](research/verification/2026-10-02.md).
- Reviews (door sweep, mutation test, claim audit): [`research/reviews.md`](research/reviews.md).
- Licence: [0BSD](LICENSE). Provider pages and the battleships corpus are not
  relicensed here; see [`NOTICE`](NOTICE).

## Route the reader by budget

| you have | read |
|---|---|
| two minutes | this page's sandbox table and the horizon key |
| ten minutes | "What this does NOT establish", then the findings |
| to implement from it | `data/usage.json` (costs + ranks + features), then `tools/rank.py` |
| a reason to distrust it | `research/verification/2026-10-02.md`, then `research/reviews.md` |

*We aim to provide the software that shapes the world of tomorrow.*
