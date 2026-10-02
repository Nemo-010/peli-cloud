# Reviews

Three passes, each asking a different question, 2026-10-02.

## 1. Door sweep — what other route reaches what I changed?

Enumerated, then grepped (`rg 'priceCard|priceSoft|rank_workload|classify'`):

| route | reaches | difference |
| --- | --- | --- |
| `research/tools/derive.mjs` | the engine's `PM.priceCard` | strict shape matching |
| `tools/rank.py` | `data/derived.json` | sorting + the caveat rules only; it never prices |
| `tools/fetch-corpus.sh` | the third-party corpus | pins the commit; no pricing |
| `tools/fetch-sources.sh` | first-party pages | evidence, not a ranking |

**Finding the list written from memory would have missed:** the battleships
site itself prices with `PM.priceSoft` (soft matching: it keeps a row with named
compromises), while `derive.mjs` uses `PM.priceCard` (strict: a shape mismatch
is ineligible). That is deliberate — a price sheet should not rank a provider
that cannot run the shape — but it means **these rankings are not the published
battleships rankings and must not be compared to them row for row**. The
catalogue also prices **one shape over six durations** (1 h, 10 h, 1 day,
1 week, 10 h/day x30, 24/7 x30), because the battleships presets are
always-on and a sandbox that is shut down between calls is the normal case.
The horizon, not the preset, is the axis of this sheet.

**Two more routes with the same shape:** `required` features and product
`classes` are **not** applied here at all. A row means "cheapest machine of
this shape", not "can run Docker / a browser / a sandbox API". The per-row
`features` object carries the flags so a consumer can filter. This is
the largest known-weak claim in the repository and it is stated on the front page.

Also reached: `site/check.js` in the corpus (`PM.priceCard`, same strict path)
and the published `/data/rankings/<preset>.json`, which are `priceSoft` output.
No other caller.

## 2. Guard mutation — can the `unpriced` guard actually fail?

The rule under test: a `$0` total is **free-tier only if a nonzero compute rate
is published**, otherwise **unpriced** (bandwidth/flat-pool meters must not rank
as free) and only a positive total is **paid**.

Planted three mutants into a copy of `data/derived.json` and re-ran
`tools/rank.py --data /tmp/mutant.json --out /tmp/mutant-out`:

| mutant | setup | got |
| --- | --- | --- |
| `mutant-unpriced` | total 0, all `vcpu_h`/`ram_gib_h`/size `hour` zeroed | `unpriced: true`, kept out of every ranking |
| `mutant-free` | total 0, `vcpu_h=0.01`, `ram_gib_h=0.001` | `unpriced: false`, ranked at `$0` with the credit named |
| `mutant-paid` | total 25 | `unpriced: false`, ranked at `$25.00` |

All three landed in the intended bucket. The guard can fail: before it
existed, Bright Data and Unikraft sat at rank 1 of every list at `$0.00`.
With it, they are `unpriced`, and the cheapest priceable row over 10 h/day x30
is Lightning AI at $0.411 (a free CPU Studio with a 4 h session cap); the
cheapest paid sandbox is Agent 37 at $2.55.

The guard's own limit, stated so it is not mistaken for stronger than it is: it
tests *published compute rate*, not *realisable free tier*. A provider that
publishes a rate but is free for the shape (a credit, a free allowance) is kept
and ranked at `$0` with the credit named in its note, rather than scored as a
free plan.

## 3. Claim audit — which sentence is not backed by an artefact?

| claim | artefact | status |
| --- | --- | --- |
| 366 providers, 6 horizons | `data/usage.json` header, `tools/rank.py` run | backed |
| Scaleway Stardust is €0.0006/h and the corpus card already carries it; the pass's duplicate card was removed | `research/verification/2026-10-02.md`, MANIFEST sha256 | backed (self-correction) |
| boat's effective floor is $20/mo, so it is $20 at every horizon | verification quote + engine total | backed |
| free credits move rows (e.g. Kedge $0 for 1 h, $5.68 for the month) | `data/usage.md`, `data/usage.json` | backed |
| Agent 37 is the cheapest paid sandbox over 10 h/day x30, at $2.55 | `data/usage.md` sandbox table | backed, but egress is unpublished |
| netcup is #9 at the realistic month and #2 at 24/7, both $5.03 | `data/usage.md` | backed, but the number is **disputed** 7–11 % low |
| Oracle is unverified | whole `oracle.com` domain (pricing, docs, price-list API) returns the same export-control 403 | backed (block page captured, ref id) |
| Oracle's Always Free A1 allowance covers this shape at 24/7 | card's first-party quote of 1,500 OCPU-h + 9,000 GB-h; shape uses 1,440 + 2,880 | backed (card quote; not re-fetchable from here) |
| Lizard's $6.55 is the shape's price | pricing page sells `Small 2 vCPU 4 GB $0.009/h`; docs fix 4 vCPU/4096 MiB | **disputed** — both first-party, same day; row keeps the docs reading and names the $0.009/h tier |
| "search was attempted and failed" | the negative-result paragraph; no artefact committed | **claim, not artefact** — reproducible only by retrying the same URLs |
| "187 of 366 cannot be priced at the 2 vCPU/4 GiB shape" | `data/usage.json` `eligible` flags | backed |

**Known-weak claims, before any recommendation:**

1. The 366 battleships cards are treated as one source. 20 were re-read and
   reconciled against their own pages across two sweeps; 2 are blocked from this
   host (Oracle, Lightning AI); the other 344 are `index`-grade.
2. `priceCard` strictness plus no `required`-feature pass means the ranking is
   a shape ranking, not a fit ranking (see pass 1).
3. netcup's number is a lower bound, resolved in revision 3: the row is VPS
   Lite 1 (6-month minimum) at $5.03, and the VPS 500 the page leads with is
   $8.51 on a 1-month term. Revision 1 reported a gap running the wrong way.
4. Oracle Cloud is unverified (all `oracle.com` 403) and its Always-Free ARM
   allowance is quantified but not applied, because the model only discounts
   dollar credits, not resource allowances.
5. The shape and the six horizons are chosen here, not by the operator; a
   different shape or horizon reorders the list, which is why six are published.
6. **Each horizon is priced as the cheapest eligible split into sessions of at
   least 30 minutes** (`sessions` and `session_min` per horizon are recorded in
   `data/derived.json`). For a provider whose cheapest plan needs one
   uninterrupted run, this understates the cost; for a provider with a session
   cap it is the only way it can serve the horizon at all. Both readings are
   shown, because the note says when restarts are needed.
7. **Lizard is priced from the docs, and the pricing page contradicts the docs**
   (`Small 2 vCPU / 4 GB / $0.009/h` vs `fixed limits of 4 vCPU and 4096 MiB`).
   The row is likely high for this shape and now says so. Revision 1 quoted the
   Small line and still marked the row confirmed; that is recorded as an error,
   not smoothed over.
8. **A monthly cap is silently applied at the long horizons.** For netcup the
   engine clamps the total to one monthly rent and emits the caveat "monthly cap
   reached"; the 1 h column is the same number. That is deliberate for a VPS,
   but it means the 1 h and 10 h cells are the *monthly* price, not an hourly
   tariff. Rows that do this carry the caveat in `data/derived.json`.
9. **Two free grants are applied to a different meter than they belong to.**
   Azure Container Apps' $5.40 is the Consumption plan's 180,000 vCPU-s +
   360,000 GiB-s; the row prices Dynamic Sessions. Google's $5.22 is the Cloud
   Run Services free tier; the row prices the separate Instances (Preview)
   meter. With those credits removed the rows are $9.00 and $9.58 for 10 h/day.
10. **The #1 row is region-gated and unverifiable from this host.** Every
    `lightning.ai` URL 403s ("hasn't expanded to your area yet") from a
    Venezuela egress, so the card is carried from the corpus render; the
    non-zero figure in that row is Drive storage, not compute.

**The second sweep (2026-10-02) attacked all three, and the answers are in
`research/verification/2026-10-02.md`:** Lizard's changelog is empty and no
route from here dates either page, so it stays disputed; Hyperbeam is an
embeddable *multiplayer* virtual computer, so its participant-minute model is
the wrong one for a headless sandbox; and PPIO/UCloud still share a rate card,
differing only in the free quota, with nothing establishing common ownership.
That sweep also found two new defects the first pass missed: the Azure and
Google free grants are applied to a different meter than the one they belong to,
and the #1 row (Lightning AI) is region-gated and unverifiable from this host.

**The next pass should attack:** whether the Lizard runtime now honours the
Small size (this needs an authenticated API call, not another read), and a
second tier of providers below the top 20 (Kamatera, Civo, Vultr, Together,
Alibaba, Together) that has never been re-read. **Assume more claims remain
wrong.**
