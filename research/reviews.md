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
| "search was attempted and failed" | the negative-result paragraph; no artefact committed | **claim, not artefact** — reproducible only by retrying the same URLs |
| "187 of 366 cannot be priced at the 2 vCPU/4 GiB shape" | `data/usage.json` `eligible` flags | backed |

**Known-weak claims, before any recommendation:**

1. The 366 battleships cards are treated as one source, not re-verified
   individually. 12 were re-checked; the other 354 are `index`-grade.
2. `priceCard` strictness plus no `required`-feature pass means the ranking is
   a shape ranking, not a fit ranking (see pass 1).
3. netcup's price is disputed and stated as a lower bound.
4. Oracle Cloud is unverified (403) and its Always-Free ARM tier sits outside
   the paid ranking entirely.
5. The shape and the six horizons are chosen here, not by the operator; a
   different shape or horizon reorders the list, which is why six are published.
6. **Each horizon is priced as the cheapest eligible split into sessions of at
   least 30 minutes** (`sessions` and `session_min` per horizon are recorded in
   `data/derived.json`). For a provider whose cheapest plan needs one
   uninterrupted run, this understates the cost; for a provider with a session
   cap it is the only way it can serve the horizon at all. Both readings are
   shown, because the note says when restarts are needed.
7. **The netcup reconciliation was wrong in revision 1 and is now corrected.**
   Revision 1 compared the card to a Lite plan it was not on and reported a gap
   running the wrong way. The real gap is 2–10 % low on the Lite line, and the
   entry row the catalogue publishes is *VPS Lite 1 G12.5s* (6-month minimum),
   not the VPS 500 G12.5 ("No preference Europe", $8.51 on a 1-month term)
   that the same page shows first. See `research/verification/2026-10-02.md`.
8. **A monthly cap is silently applied at the long horizons.** For netcup the
   engine clamps the total to one monthly rent and emits the caveat "monthly cap
   reached"; the 1 h column is the same number. That is deliberate for a VPS,
   but it means the 1 h and 10 h cells are the *monthly* price, not an hourly
   tariff. Rows that do this carry the caveat in `data/derived.json`.

**Assume more claims remain wrong.** The next pass should attack: Oracle's
current E4 and Always-Free values, whether Lizard's runtime honours Small,
whether any provider hides an entry tier the way revision 1 wrongly believed
Scaleway did, and the white-label Tailscale duplicate (see the findings).
