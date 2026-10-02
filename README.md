# peli-cloud

A cheapest-first catalogue of cloud sandbox, VM and agent-runtime providers,
priced for fixed agent workloads, with the up-front minimums and the recurring
free credits left visible instead of folded into one number.

0BSD. Data is facts measured from provider pages; see `NOTICE`.

Neuwork would call this a Neucom Info job: gather the Electrosphere's public
price cards, bill one workload the way each provider bills it, and rank.
No simulation, no Nemo — just the invoices.

---

## What this does NOT establish, read this before the rankings

- **It is a shape ranking, not a fit ranking.** Every row means "cheapest
  machine of this shape". It does **not** apply required features: a row may be
  a plain VM where the workload implies a sandbox API, Docker, or a browser.
  Per-row `features` are in the JSON so you can filter. This is the largest
  known-weak claim here.
- **It uses the engine's strict path (`priceCard`), not the soft one
  (`priceSoft`)** that battleships.dev's own page uses. A provider that can only
  run the shape with a named compromise is listed under "Did not fit", not
  ranked. These numbers are therefore **not** the battleships rankings and must
  not be compared row for row.
- **354 of 367 providers were not re-verified by hand.** 12 provider pages were
  re-fetched and reconciled (`research/verification/2026-10-02.md`); the other
  354 carry the corpus's figure at its captured commit and are `index`-grade.
- **Generic web search failed in this sandbox** (DuckDuckGo and Bing are
  JavaScript-gated). Discovery is corpus-led, not search-led.
- **A `$0` row is never treated as free.** A zero total with no published
  compute rate is classed `unpriced` and kept out of the ranking (Bright Data,
  Unikraft). Genuine free tiers are listed separately.
- **Assume more claims are wrong than the five listed at the end.**

## Conditions

- One host, 2026-10-02, reading provider pages over HTTPS. Prices are public
  list prices on that day; USD unless stated. EUR→USD at 1.1378 (ECB
  2026-09-28), the rate the corpus uses.
- 367 provider cards: 366 from `ariana-dot-dev/battleships` at commit
  `f6a71ab09fefa68e355ef47c52315e099f99c921`, plus one added here
  (`scaleway-stardust`).
- 4 fixed workloads: `nano-box`, `agent-box`, `devbox`, `interp`. They are
  declared in `research/tools/derive.mjs` and repeated in each ranking file.

## The headline: one always-on agent box

2 vCPU / 4 GiB / 20 GiB, 24/7, 100 GiB egress. 143 priced providers, sorted
cheapest first. Full table: [`data/rankings/agent-box.md`](data/rankings/agent-box.md).

| # | Provider | $/mo | $/mo no credit | Prepaid min | Free credit | Caveats |
|---|---|---|---|---|---|---|
| 1 | netcup VPS | $5.03 | $5.03 | - | - | disputed: page says ~$5.60; 6–24 month term |
| 2 | Agent 37 | $6.20 | $6.20 | - | - | egress not published |
| 3 | Hetzner Cloud | $6.49 | $6.49 | - | - | IPv4 $0.60/mo |
| 4 | Contabo | $6.60 | $6.60 | - | - | 24-month intro rate advertised |
| 5 | Oracle Cloud | $7.51 | $7.51 | - | - | $300 one-time; unverified |
| 6 | Kedge | $10.00 | $15.00 | - | $5.00 | public preview |
| 7 | Upstash Box | $10.00 | $10.00 | - | - | flat pool billed whether used or not |
| 8 | zipbox | $10.00 | $10.00 | - | $25 one-time | egress not published |
| 9 | IONOS Cloud | $10.80 | $10.80 | - | - | IPv4 $5.69/mo |
| 10 | UpCloud | $14.00 | $14.00 | - | - | |
| 11 | Gcore Cloud | $14.12 | $14.12 | - | - | disk price unknown |
| 12 | Alibaba Cloud ECS Intl | $14.50 | $14.50 | - | $90 one-time | prepaid terms |
| 13 | shellbox | $14.60 | $14.60 | - | - | egress not published |
| 14 | Hostinger VPS | $14.99 | $14.99 | - | - | 24 months paid up front |
| 15 | exe.dev | $15.00 | $15.00 | $15.00 | - | flat pool; invite-only |
| 16 | Lizard | $15.94 | $15.94 | - | $10 one-time | Medium only (runtime fixes 4 vCPU) |
| 17 | Azure Container Apps | $16.50 | $21.90 | - | $5.40 | size per session not published |
| 18 | OVHcloud | $18.69 | $18.69 | - | $200 one-time | 12/36-month commits |

`boat.dev` sits at **$20.00** here, not at its metered $13.14, because the $20
plan fee is a usage credit and the bill cannot fall below it. On a much smaller
shape it is worse: the effective floor is still $20.

## The floor of the market: one tiny box

1 vCPU / 1 GiB / 10 GiB, 24/7. [`data/rankings/nano-box.md`](data/rankings/nano-box.md).

| # | Provider | $/mo | Note |
|---|---|---|---|
| 1 | Scaleway Stardust | **$0.498** | added this pass; absent from the corpus card |
| 2 | netcup VPS | $1.54 | pico, 12-month term |
| 3 | Scaleway Instances | $1.58 | |
| 4 | Maritime | $2.00 | +$20/mo subscription |
| 5 | UpCloud | $3.50 | |

## Where the credits and the minimums land

[`data/credits-vs-floor.md`](data/credits-vs-floor.md) has the full view.
Examples for `agent-box`:

- **Free monthly credits** that move a row: Kedge $15.00→$10.00,
  Azure Container Apps $21.90→$16.50, Google Cloud Run $35.19→$29.97,
  Freestyle $97.79→$79.41. On the `nano-box` shape Freestyle is
  $39.48→$21.10 and Google Cloud Run $8.86→$3.64.
- **Prepaid minimums** that set a floor below which usage cannot fall:
  boat.dev $20, Freestyle $50, exe.dev $15, Prized $10, Fly.io $5, Railway $5.
- **One-time credits** (not monthly) are listed but never subtracted: on the
  `agent-box` shape the notable ones are Oracle $300, Civo $250, KakaoCloud
  $221, IBM $200, OVHcloud $200, Azure $200, Kamatera $100, Alibaba $90.

## Findings

1. **Scaleway Stardust was missing from the corpus.** Its card starts at DEV1-S
   (~€0.0102/h); STARDUST1-S is €0.0006/h, about 17× cheaper, and becomes the
   cheapest full VM in the catalogue. Added, verified, quoted.
2. **boat's cheap headline is a $20/month floor**, exactly as the operator
   warned. Confirmed from the provider's own pricing page.
3. **netcup's number is disputed.** The page is 7–11% above the corpus card.
   Rank unchanged; the figure is a lower bound.
4. **Free tiers distort a naive sort.** Bright Data and Unikraft produced a
   `$0.00` total from an unpriced meter; Oracle's Always-Free ARM tier is
   real but sits outside the paid ranking. The classifier now keeps both out
   of the list and names them.
5. **The tracker proposed Croft** (open PR #1): flat $24/$99 plans, no published
   shape. Recorded and excluded, not ranked.

## Negative results

- **Web search is not usable here.** DuckDuckGo lite/html and Bing returned
  JavaScript shells; discovery could not use them.
- **Oracle's pricing page returns 403.** No independent Oracle number; the row
  stays unverified.
- **`$0` ranking was a dead end that had to be reverted.** Before the `meter`
  classifier, Bright Data and Unikraft ranked #1 on every list. The fix is the
  mutation-tested `classify()` in `tools/rank.py`; see `research/reviews.md`.

## Reproduce

```sh
sh tools/fetch-corpus.sh                 # pin the third-party corpus locally
sh tools/fetch-sources.sh                # re-fetch the 13 first-party pages
node research/tools/derive.mjs --corpus research/corpus --out data/derived.json
python3 tools/rank.py                    # writes data/catalog.md and data/rankings/*
```

`derive.mjs` needs Node ≥ 18. `rank.py` is pure Python 3 and does no network.
The corpus and engine are third-party and are not committed; the fetch script
reconstructs them at the pinned commit.

## Provenance and licence

- Corpus, commit, route, and the gaps: [`research/provenance.md`](research/provenance.md).
- Independent checks and quotes: [`research/verification/2026-10-02.md`](research/verification/2026-10-02.md).
- Reviews (door sweep, mutation test, claim audit): [`research/reviews.md`](research/reviews.md).
- Licence: [0BSD](LICENSE). The provider pages and the battleships corpus are
  not relicensed here; see [`NOTICE`](NOTICE).

## Route the reader by budget

| you have | read |
|---|---|
| two minutes | this page's headline table and the five findings |
| ten minutes | "What this does NOT establish", then the five findings |
| to implement from it | `data/rankings/*.json` (per-row features + caveats), then `tools/rank.py` |
| a reason to distrust it | `research/verification/2026-10-02.md`, then `research/reviews.md` |

*We aim to provide the software that shapes the world of tomorrow.*
