# Deep reviews, 2026-10-02

A parallel implementation of the same idea — `talaria0101/peli-cloud`, 0BSD,
created the same day — was read against this one. What was worth taking was
ported; what was wrong was not. Ten adversarial reviews of the result follow.
Each one states the attack, the method, the evidence, and a verdict, so a
reader can reproduce the check rather than trust the paragraph.

## What was read, ported, and refused

**Ported, because it closes a real gap.** The minimum billable unit and
granularity per start (`data/usage.md`, bursty table). A headline $/hour is not
what a short session costs, and an agent that starts a sandbox per tool call
pays the minimum every time; that was invisible in every earlier revision here.
The free-tier census (recurring / one-time / unknown), and the exclusion ledger
that accounts for all 366 cards, including the ones that cannot be priced.

**Rejected.** Talaria vendors the entire third-party `battleships` corpus in
tree under `references/`. That corpus publishes **no licence**, so it cannot be
redistributed, and publishing it under the repo's 0BSD header would put a
licence on somebody else's unlicensed material. This repo fetches the pinned
corpus with `tools/fetch-corpus.sh` and commits none of it; that is the
deliberate difference and it is not negotiable. Talaria's HTML-primary
presentation was also not taken: the markdown + JSON split here is auditable
and diffable, and a machine consumer wants the JSON.

Two of talaria's computed results were independently reproduced here rather
than taken on faith (the census counts differ because the definitions differ;
this repo's are stated in `data/usage.md`).

---

## 1. Is the bursty column honest, or built to make cheap rows look bad?

**Attack.** A 30-minute session on a one-hour minimum is billed as a full
hour. If the bursty profile were chosen to maximise the penalty, the column is
an accusation, not a measurement.

**Method.** `derive.mjs` emits the bursty workload explicitly:
`bursty.b30m = 600 sessions × 30 min = 18000 min = 300 h`, the same demand as
the `m10h` column (`30 × 600 min`). Three controls are then fixed by arithmetic
and cannot be tuned: a per-second provider must be exactly 1.000×, a one-hour
minimum exactly 2.000×, and credit-dependent rows must scale with the billed
hours rather than the delivered hours.

**Evidence.**

| provider | smooth | bursty | ratio | why |
|---|---|---|---|---|
| Agent 37 | 2.5479 | 2.5479 | 1.000× | per-second mode |
| zipbox | 4.110 | 4.110 | 1.000× | per-second mode |
| Hetzner Cloud | 3.120 | 6.240 | 2.000× | 1 h minimum, 600 starts → 600 billed h |
| Civo | 8.9286 | 17.8572 | 2.000× | 1 h minimum |
| Azure Container Apps | 3.600 | 12.600 | 3.500× | 600×0.03 − 5.40 = 12.60 vs 300×0.03 − 5.40 = 3.60; the credit is fixed, so the ratio exceeds 2 |
| Expo | 124.00 | 298.00 | 2.403× | a **$1 per-start fee**, a second mechanism |

**Verdict: holds.** The 2× is arithmetic. The 3.5× is the fixed credit, and the
per-start fee is a third cause, which is why each row's note names its own
mechanism. The profile is deliberately pessimistic (every session shorter than
the minimum), and the table says so; an agent that holds one box past the
minimum pays once. Weakness that remains: for a provider with a minimum
*shorter* than 30 minutes, the penalty is understated, not overstated — the
bound only ever flatters, never punishes.

## 2. Does the cheapest-split ever exceed a plan's published session cap?

**Attack.** The catalogue claims a 10 h day can be served by splitting around
an 8 h cap (two 5 h sessions). If the engine ever priced a single session longer
than the cap without flagging it, the row is fiction.

**Method.** For every m10h-priceable provider, match the chosen plan name to the
plan in `facts.plans` and compare the chosen `session_min / 60` with
`max_session_h`. Independently, the engine's own `planErrs` path rejects a plan
whose cap is exceeded unless `ignorePlanLimits` is set.

**Evidence.** **0 of 179** exceed their plan's session cap. Providers that need
splitting show a shorter `session_min` (300 min = 5 h, 240, 120) and carry the
note "session cap N h, needs restarts". The 30-minute floor (`MIN_SESSION_MIN`)
is what stops a 1 h horizon being gamed as sixty one-minute starts.

**Verdict: holds.**

## 3. Is a monthly credit applied once per month, or once per session?

**Attack.** The bursty run has 600 sessions. If the engine applied the Azure
$5.40 credit per session, the bursty row would be near-free while the smooth
row is not, inverting the finding.

**Method.** Read the engine's credit block (`research/corpus/site/engine.js`,
the `opts.credits` branch) and check every horizon output for three
credit-bearing providers.

**Evidence.** Azure Container Apps: `r1h 0, r10h 0, d1 0, w1 0, m10h 3.60,
m30 16.20`. The credit is `min(monthly_credit, total)`, subtracted **once per
priced horizon**, and the horizon itself is the demand (300 h or 720 h). Google
Cloud Run and Kedge behave the same way (`w1 0.14`, `m10h 4.36`, `m30 17.77`;
`w1 0.98`, `m10h 5.68`, `m30 20.64`).

**Verdict: holds for the six modelled horizons.** Named weakness: a horizon of
exactly one month matches the credit cadence, but a 45-day horizon would need a
second monthly credit and is not modelled. None of the six horizons exceeds 30
days, so nothing published is wrong — but the model is not a general
multi-month one, and the README should not be read as saying it is.

## 4. Ranking ties and run-to-run determinism.

**Attack.** Cheap providers cluster on round numbers; if ties shuffle between
runs, two readers get two tables.

**Method.** Enumerate tied m10h totals; inspect the sort key in `tools/rank.py`.

**Evidence.** Twelve tied totals among the 179, including $6 (2 providers), $15
(3), $20 (3), $49.68 (4), $50.166 (2), $99 (2), $250 (2). `rank.py` sorts on a
stable key and preserves the `derived.json` card order, which is the corpus
order, so the output is deterministic. Ties are adjacent.

**Verdict: holds**, with one honest caveat the README did not state: **the order
*within* a tie is corpus order, not a ranking.** Three providers at $20 are not
"#x, #y, #z" in any meaningful sense.

## 5. Exclusion ledger: is every card accounted for exactly once?

**Attack.** "All 366 accounted for" is exactly the claim that hides a card that
silently vanished.

**Method.** Partition the 366 into (a) any horizon with a positive total,
(b) every horizon zero and no published compute rate, (c) no horizon priceable.
Assert the ids are unique and the three sets sum to 366 with no overlap.

**Evidence.** ids unique = **366**; priced > 0 = **179**; all-zero unpriced =
**2** (`bright-data-browser`, `unikraft-cloud` — a bandwidth meter and a
flat-pool meter, neither with a published compute rate); nofit = **185**;
179 + 2 + 185 = 366. Five `nofit` rows were spot-checked against their cards and
are `nofit` because no mode offers ≥ 2 vCPU **and** ≥ 4 GiB, not because of a
parsing failure.

**Verdict: holds.** The 2 unpriced rows are the only $0 rows excluded; every
other $0 is a credit the catalogue names.

## 6. Currency and arithmetic reproducibility.

**Attack.** A row that cannot be reproduced from the provider's own numbers by
hand is a rumour.

**Method.** Recompute four rows from the corpus card rates.

**Evidence.** PPIO/UCloud: (2 × ¥0.00003 + 4 × ¥0.000015) ¥/s × 3600 × 300 h ×
0.14902 USD/CNY = **$19.313** = the row. IONOS Basic Cube S: card `hour`
0.0147914 × 300 = **$4.4374** = the row. Hetzner CX23: 0.0104 × 300 =
**$3.12** = the row. Civo Standard: 0.0298 × 300 = **$8.9286** = the row.

**Verdict: holds.** The important detail this review establishes: the corpus
stores **USD-normalised** hourly rates, so EUR→USD is baked at capture time,
not applied by `rank.py`. The README's exchange-rate line is provenance, not a
live conversion; `rank.py` does no network and no currency maths. That is why a
rate change never silently moves a row.

## 7. Is the top of the table a free-tier artefact?

**Attack.** Every horizon applies monthly credits, so the cheapest rows may be
cheapest only because of a credit a real account exhausts.

**Method.** Re-rank all 179 by `total_no_credit` and compare.

**Evidence.** **Only 6 of 179** are credit-dependent at m10h: Azure Container
Apps ($3.60 → $9.00), Google Cloud Run ($4.36 → $9.58), Kedge ($5.69 → $10.69),
Freestyle ($21.81 → $40.19), Blacksmith ($33 → $45), Scrapeless ($398.91 →
$399.00). The top four — Lightning AI, Agent 37, Oracle, Hetzner — do **not**
move. Azure falls from #5 to #24 and Google from #7 to #28.

**Verdict: the concern is real for exactly two of the top seven rows, and
overstated for the rest.** Finding 3's wording ("the cheapest rows are cheapest
because they have a free tier") is too broad; the top four are rate-driven.
Amendment: tightened to "two of the top seven" in the README.

## 8. Does the stated mechanism explain each bursty penalty?

**Attack.** A penalty column without a cause is numerology.

**Method.** For all 21 penalised rows, compare the bursty mode to the m10h mode
and read the label emitted for each.

**Evidence.** 19 of 21 stay on the same mode and their labels are `min 1 h`,
`rounds to 1 h`, or `$1 per start`. **2 switch mode:** E2E Networks
(E1 shared-core → C3 compute-intensive — the switch *mitigates*, leaving only
1.05×) and Expo (Android build, medium worker → Workflows linux-medium — the
switch introduces a *different product*, a CI workflow, with a $1 per-start
fee).

**Verdict: holds for 19; the 2 switches are named, not hidden.** Amendment: the
bursty table header now warns that a bursty run may select a different mode of
the same provider, and therefore may not be the same product.

## 9. Is the bursty workload feasible on the caps providers publish?

**Attack.** 600 starts over 30 days is 20 starts/day. A provider that publishes
a 10/day cap would be priced for a workload it cannot run.

**Method.** Scan every plan in every corpus card for `max_starts_per_day`,
`max_starts_per_hour`, `max_starts_per_min`.

**Evidence.** The smallest published caps anywhere in the corpus are **75
starts/day**, **25 starts/hour**, **5 starts/min** — all above the profile's 20
starts/day. No card publishes a cap the bursty run violates. Where a cap is
absent, the engine leaves it unknown rather than assuming a number.

**Verdict: holds.** Named weakness: the engine prices a cap-violating plan
anyway (it picks the "least-bad" plan and reports the limit as a caveat), so if
a future corpus update introduces a 10/day cap, the bursty row would be
silently infeasible. The scan above is the guard, and it should be re-run when
the corpus commit moves; it is cheap enough to keep in the reproduce steps.

## 10. Do the prose counts agree with the generated data?

**Attack.** Hardcoded numbers in a README rot the moment the data changes.

**Method.** Reconcile each count in `README.md` against `data/usage.json`.

**Evidence.** 366 cards ✓; 179 priceable ✓; 187 unpriceable = 185 no-fit + 2
unpriced ✓; 21 bursty-penalised ✓; census 13 recurring / 89 one-time / 71
unknown ✓; 20 reconciled + 2 blocked + 344 carried = 366 ✓ (the 20 are the
provider sections in `research/verification/2026-10-02.md`; Oracle and
Lightning AI are the blocked pair; Gcore is listed there explicitly as *not*
re-verified and is therefore counted in the 344 carried). **One stale number
was found and fixed:** the README's intro still said "thirteen" findings while
there are now fifteen.

**Verdict: holds after the fix.** Weakness that remains and is named here: the
"20 reconciled" count is not anchored to an enumerated list in the README, so a
reader has to count the verification sections. The list above is the anchor;
this paragraph is the only place it exists, which is itself a smell.

---

## What this round changed

- `research/tools/derive.mjs` — a second workload, `b30m` (600 × 30 min), priced
  through the same engine with the same shape, emitted per provider as `burst`.
- `tools/rank.py` — a bursty table, a free-tier census, an exclusion ledger, and
  per-row `min`/`rounds to`/`$per start` notes and `burst`/`burst_x`/`burst_bill`
  in the JSON.
- `data/usage.md` / `data/usage.json` — regenerated; 179 priceable, 21 bursty,
  366 accounted for.
- `README.md` — findings 14 and 15, a bursty row in the per-horizon table, and
  the "thirteen" → "fifteen" fix.

## What remains unverifiable, and is not claimed

- **Oracle and Lightning AI** are blocked from this host entirely (domain-wide
  403), so their rows carry corpus figures. Oracle's Always Free allowance would
  price this shape at $0; Lightning AI's non-zero figure is Drive storage, not
  compute.
- **Lizard**'s pricing page and its docs still disagree about whether this shape
  is the $0.009/h Small mode; the conservative docs reading stands.
- **Gcore**'s per-shape price is not on the marketing page fetched; that row is
  carried.
- **A multi-month credit model** does not exist (review 3), and **the corpus
  stores USD-normalised rates**, so the EUR figure in the verification note is
  historical, not live (review 6).

*We aim to provide the software that shapes the world of tomorrow.*
