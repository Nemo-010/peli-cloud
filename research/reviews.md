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
catalogue's own `interp` list starts at Oracle Cloud $21.39 where battleships'
`interp` preset starts at Agent 37 $22, because the preset also requires
`code-interpreter` / `sandbox-api` product classes and Oracle is a plain VM.

**Two more routes with the same shape:** `required` features and product
`classes` are **not** applied here at all. A row in `agent-box` means "cheapest
machine of this shape", not "can run Docker / a browser / a sandbox API". The
per-row `features` object carries the flags so a consumer can filter. This is
the largest known-weak claim in the repository and it is stated on the front page.

Also reached: `site/check.js` in the corpus (`PM.priceCard`, same strict path)
and the published `/data/rankings/<preset>.json`, which are `priceSoft` output.
No other caller.

## 2. Guard mutation — can the `meter` classifier actually fail?

The rule under test: a `$0` total is **free-tier only if a nonzero compute rate
is published**, otherwise **unpriced** (bandwidth/flat-pool meters must not rank
as free) and only a positive total is **paid**.

Planted three mutants into a copy of `data/derived.json` and re-ran
`tools/rank.py`:

| mutant | setup | got |
| --- | --- | --- |
| `mutant-unpriced` | total 0, all `vcpu_h`/`ram_gib_h`/size `hour` zeroed | `unpriced` |
| `mutant-free` | total 0, `vcpu_h=0.01`, `ram_gib_h=0.001` | `free-tier` |
| `mutant-paid` | total 25 | `paid` |

All three landed in the intended bucket, and `mutant-paid` appeared in the
ranked table at $25.00. The guard can fail: before this rule existed, Bright
Data and Unikraft sat at rank 1 of every list at `$0.00`. With it, they are in
`unpriced`, and the shipped top of `nano-box` is Scaleway Stardust at $0.498.

The guard's own limit, stated so it is not mistaken for stronger than it is: it
tests *published compute rate*, not *realisable free tier*. A provider that
publishes a rate but is free for the shape (a credit, a free allowance) is
`free-tier`, and its row carries the limits as caveats rather than a score.

## 3. Claim audit — which sentence is not backed by an artefact?

| claim | artefact | status |
| --- | --- | --- |
| 367 providers, 4 workloads | `data/derived.json` header, `tools/rank.py` output | backed |
| Scaleway Stardust is €0.0006/h, absent from the card | `research/verification/2026-10-02.md`, MANIFEST sha256 | backed |
| boat's effective floor is $20/mo | verification quote + engine total | backed |
| free credits move rows (e.g. Freestyle $39.48→$21.10) | `data/credits-vs-floor.md` | backed |
| netcup is #1 for agent-box | `data/rankings/agent-box.md` | backed, but the number is **disputed** 7–11% low |
| "search was attempted and failed" | the negative-result paragraph; no artefact committed | **claim, not artefact** — reproducible only by retrying the same URLs |
| "217–227 providers fit no workload" | `data/rankings/*.json` `ineligible_count` | backed |

**Known-weak claims, before any recommendation:**

1. The 366 battleships cards are treated as one source, not re-verified
   individually. 12 were re-checked; the other 354 are `index`-grade.
2. `priceCard` strictness plus no `required`-feature pass means the ranking is
   a shape ranking, not a fit ranking (see pass 1).
3. netcup's price is disputed and stated as a lower bound.
4. Oracle Cloud is unverified (403) and its Always-Free ARM tier sits outside
   the paid ranking entirely.
5. The workload shapes are chosen here, not by the operator; a different shape
   reorders the list, which is why four are published.

**Assume more claims remain wrong.** The first four the next pass should
attack: the exact netcup reconciliation, Oracle's current E4 and free-tier
values, whether Lizard's runtime honours Small, and whether any other provider
hides an entry tier the way Scaleway hid Stardust.
