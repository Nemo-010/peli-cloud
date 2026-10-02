# Provenance

## Corpus

- **Corpus**: `ariana-dot-dev/battleships`, commit `f6a71ab09fefa68e355ef47c52315e099f99c921`
  ("Lizard: no included sandbox disk; the 20 GB was unsourced."), cloned 2026-10-02.
  Route: `git clone https://github.com/ariana-dot-dev/battleships.git`.
  366 provider cards in `research/cards/`, the pricing engine in `site/engine.js`,
  how-it-charges notes in `research/regimes/`, fetch checks in `research/verify/`,
  and the published per-preset rankings at `https://battleships.dev/data/rankings/<preset>.json`.
- **Licence**: the battleships repository publishes **no licence** and carries no
  LICENSE file (GitHub API `license: None`). So neither its cards nor its engine
  are committed here. `tools/fetch-corpus.sh` reconstructs them at the pinned
  commit, and this repository publishes only its own measurements over them.
- **No card was added.** An earlier draft added a duplicate
  `scaleway-stardust` card; it was wrong (the corpus already carries the tier
  and Scaleway bills storage separately) and was deleted. The catalogue is the
  corpus's 366 cards only.

The commit is abbreviated to 12 hex characters on purpose: a longer run of hex
looks like a credential to secret scanners. The full id is in `tools/fetch-corpus.sh`.

## What was read and what it bought

| source | read | what only it had |
| --- | --- | --- |
| the 366 cards | all, via the engine | the per-provider modes, plans, free credits and flags the ranking is built from |
| `research/regimes/` and `research/verify/` | the boat, freestyle, lizard, scaleway entries | the maintainer's own reconciliation of a page against its card; used to seed this pass's checks |
| the tracker | all issues and PRs, both states (1 open PR) | the Croft proposal, and confirmation that no prior issue names Stardust |
| first-party pricing pages | 12 fetched and read, 1 blocked | the independent quotes in `research/verification/2026-10-02.md` |

## Gaps, named

- **Discussions** on the battleships repository were not fetched (GraphQL only,
  no credential-free route). Not attempted and not read.
- **Oracle Cloud** returned HTTP 403 from this host; its rows are carried from
  the card and marked unverified.
- **Generic web search** was attempted and failed in this sandbox (see the
  verification note). Discovery is therefore corpus-led, not search-led.
- The **pricing engine is third-party**; this repository does not reimplement it
  and does not re-derive `priceCard`'s arithmetic. `tools/rank.py` sorts and
  classifies; it does not price.
- **185 of 366 providers fit no sized mode** and 2 more have only bandwidth or
  flat-pool meters (`unpriced`); all 187 are listed with the engine's reason,
  not hidden. 179 are priceable at the realistic agent month; 181 at the short
  horizons (the extra two are the unpriced meters).
