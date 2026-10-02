# Deep reviews: the anonymous/free VM census, the no-credit ranking, and the relay

Scope of this pass, 2026-10-02, against the changes that added
`docs/ANONYMOUS-VMS.md`, `data/anonymous-vms.json`, the no-credit columns in
`data/usage.json`, `tools/ssh-relay-check.sh` and the notes in
`research/verification/ssh-relay-2026-10-02.md`.

Each review below is written to be falsifiable: it states what it attacked, what
it found, and what changed as a result. Where nothing changed, that is stated
too, and why.

## R1 — "Anonymous" is a claim about identity, and a search hit is not evidence

**Attacked:** every row classed `anonymous` or `free-account`.

**Finding:** the first keyword sweep over candidate pages matched the word
"ssh" in page footers and navigation, and "free" in marketing copy. If those
had been promoted to rows, the page would have claimed free SSH machines that
do not exist. The census now records, per row, whether an account is required
and whether a card is required, and the classes are defined in the page before
any table appears.

**What changed:** `data/anonymous-vms.json` carries `account_required` and
`card_required` as booleans per row, and `tools/check-anon-vms.py` fails if they
are missing or if the `class` is not one of the defined values. The page renders
the classes rather than describing them loosely.

## R2 — The "at least 10" instruction could be satisfied by padding

**Attacked:** the count that answers the brief. The risk is that rows are ranked
SSH-capable on inference (for example, "it is a container, so you could open a
shell") rather than on the provider's own words.

**Finding:** several rows genuinely do not publish an SSH path: AWS CloudShell,
Azure Cloud Shell, Render, Northflank. Others do: Codespaces documents
`gh codespace ssh`; SDF documents `ssh new@sdf.org`; tilde.club publishes host
key fingerprints; Oracle and Google both install SSH keys at instance creation.
The split is now explicit, and only `ssh: true` rows count toward the floor.

**What changed:** the page sorts SSH-capable rows first and prints the guard's
own count (`15` on 2026-10-02) instead of a typed sentence; the guard recomputes
it from the JSON.

## R3 — A provider that changed or died must not read as live

**Attacked:** the rows a reader is most likely to be misled by, because every
older list repeats them.

**Finding:** two are wrong in the opposite direction from padding. Play with
Docker's own page carries a deprecation notice — "unavailable starting March 1,
2026" — and Fly.io's pricing page no longer carries a free Machine allowance at
all; the only "first free" left there is 10 GB of volume capacity. Both would
have been ranked by a keyword sweep.

**What changed:** a `changed`/`dead` class with its own table, so the corrections
are visible instead of being silently dropped, and a paragraph naming both.

## R4 — The census quotes could not be re-checked

**Attacked:** every quote in the page. A quote with no fetch behind it is a
fabricated measurement.

**Finding:** the first draft of the page had quotes in prose only. Nothing in the
tree recorded the URL, the HTTP status, the byte count or the time.

**What changed:** `tools/fetch-anon-sources.sh` fetches every cited page and
writes `sources/anon-2026-10-02/MANIFEST.tsv` with `http`, `bytes` and `sha256`
per row. Two rows returned a 403 from this host (oracle.com: 1,339-byte
export-control page; lightning.ai: 739-byte regional page), and both rows say
`blocked-from-host` with the carried figure and the reason rather than a guess.
This is the same treatment the main catalogue gives Oracle.

## R5 — The no-credit column could have been a cosmetic duplicate

**Attacked:** the new `costs_no_credit` / `ranks_no_credit` output. If the
underlying engine had no pre-credit figure, the column would repeat the
credit-adjusted number and claim to be a re-sort.

**Finding:** `data/derived.json` already carries `total_no_credit` (1,084
horizon entries across 366 providers), so the column is a genuine re-sort. Kedge
demonstrates it: `$5.68` at 10 h/d x30 with its `$5` credit and `$10.68`
without, moving from rank 10 to rank 31. A first render had the wrong column
header (`Rank w/ credit` printed the no-credit sort), caught by reading the
generated table against the JSON rather than trusting the code path.

**What changed:** `rank.py` builds a second ordering from `total_no_credit`, adds
`costs_no_credit` and `ranks_no_credit` per provider, and renders a section
with the five rows the credit moves most. A regression clause asserts Kedge's
rank falls in the no-credit ordering, and it fails against the pre-fix tree.

## R6 — The SSH proof could have been a claim with no artefact

**Attacked:** the relay section. "It works here" is not evidence unless a reader
can re-run it.

**Finding:** the working sequence took three attempts, and each failure is a
distinct mechanism worth recording: a static-pie musl `dropbear` cannot be
`LD_PRELOAD`-ed with `fakepwd.so`, so `-Y FILE` is the only passwd path; the
passwd line must name the sandbox uid (966) because dropbear refuses a login
whose uid differs from the server's; and the same setup under `/tmp` dies on
`"/tmp must be owned by user or root, and not writable by group or others"`.

**What changed:** `tools/ssh-relay-check.sh` reproduces the whole path from
nothing but the network — fetch the pinned release, verify its `SHA256SUMS`,
generate keys, write the passwd entry, serve one session, connect through the
relay and run `id -u`. It exits 0 only when a real login ran, and it mints a
fresh pair each run so no token is ever committed. The note records the three
failures, not just the success.

## R7 — The relay check could leave a node dialing, or a token in the tree

**Attacked:** the side effects of R6.

**Finding:** a `--once` node that never pairs waits forever, which is how the
first version of the script hung. Separately, `dropssh pair` writes two 64-hex
bearers into the work dir, and a careless commit would publish them.

**What changed:** the script passes `--retry-budget 3`, wraps `ssh` in `timeout`,
and kills the node after the attempt. The work dir (`.dropssh-check/`) is
`gitignore`d, tokens are written mode `600` and never echoed, and a regression
clause fails if any 64-hex string appears in the files this work adds.

## R8 — The rendered page and the JSON could drift apart

**Attacked:** the generated page. A generator that is not re-run leaves the
prose contradicting the data.

**Finding:** this is exactly the defect the honest sibling repo
(`talaria0101/peli-cloud`) records about its own README citing an uncommitted
`data/derived.json`. The fix here is the same as this repository already uses
for `tools/rank.py`: the JSON is committed and the page is a pure function of
it.

**What changed:** `tools/render-anon-vms.py` is deterministic, and a regression
clause re-renders the page and fails if it differs (`git diff --quiet` after a
render). The page links the JSON it comes from at the top.

## R9 — The guard could pass on an empty or malformed file

**Attacked:** `tools/check-anon-vms.py` itself.

**Finding:** the first version only counted rows, so a census with 10 rows and
no sources would pass. It also accepted a row with any `class` string.

**What changed:** the guard now checks the row floor, the duplicate ids, the
required fields (`source`, `quote`, `verification`, `caveats`), the class enum,
the boolean types, the SSH floor and the presence of at least one genuinely
anonymous row. It prints its computed counts before its verdict, so a reader can
see what it measured.

## R10 — The claim "this host cannot listen" could be stale

**Attacked:** the premise of the whole relay section. If `bind(2)` worked here,
the dropssh path would be unnecessary and the section would be misleading.

**Finding:** it is measured, not assumed. `sandhome doctor` reports
`bind(2) INET on loopback  refused with EACCES` and `bind(2) AF_UNIX  bound a
unix socket`, and `sandhome report` reports `bind=unix`. The sealed-sandbox
skill records the same refinement, so the claim is consistent with the
repository's own guidance rather than invented here.

**What changed:** nothing in the code; the page states the measured values and
cites the command that produces them, so a reader on a different host can tell
whether the section applies to them.

## What this pass did not establish

- **Whether any of these free tiers will still exist next year.** The census is
  a snapshot from 2026-10-02 with a re-fetchable manifest; two of the rows
  (Play with Docker, Fly.io's allowance) are in it precisely because they
  changed under a reader's feet.
- **That the relay is private or durable.** The pair is a bearer credential
  with a 72 h ceiling, and the relay's own documentation says so. Nothing here
  asserts otherwise.
- **That the anonymous Railway box is reachable from every network.** The
  anonymous cap is per region and the trial can be disabled under demand; only
  the provider's own words are quoted.
- **That the "free-account" rows are anonymous.** They are not, and the class
  names say so; 14 of the 15 SSH-capable rows ask for an account.

---

# Second pass, 2026-10-02: consuming the sibling's next commit (f6401a0)

`talaria0101/peli-cloud` moved again while this work was in progress. Its new
commit is a defect report against its own instrument, not new pricing:

> **The stripper was calling 4 readable pages "client-rendered shells"** —
> aptible's 713 KB pricing page carries a JSON-LD block *inside a `<script>`
> tag* holding the very billing sentences the probe looks for, including
> "Starting at $499/month". Stripping every script discarded it, the page looked
> empty, and the verdict became "no price rendered in the HTML (client-side)".
> Re-checking all 26 shell verdicts: **4 were mislabelled, 22 are genuinely
> client-rendered.**

The reviews below are this pass's response: what was ported, what was not, and
what the port turned out to mean for this repository.

## R11 — The lesson, not the fix, is what transfers

**Attacked:** the assumption that the sibling's change is a patch to copy.

**Finding:** this repository has no billing-posture probe. It has never fetched
183 pages looking for idle-billing sentences, so it had no `strip_markup()` and
no verdict to correct. Its `data/usage.json` carries no `shell` verdicts, and 0
of its 62 checked published URLs would have been flipped by the fix (measured,
not assumed — R14). Copying the diff would have added a function nothing calls.

**What changed:** the *class* of defect was ported instead of the code: a
reader that turns HTML into text, and a known-answer self-test that fails if the
reader drops published data. `tools/check-strip-selftest.py` — 8 cases, 3 of
which fail against the naive one-liner the sibling shipped.

## R12 — A self-test that passes either way is not a self-test

**Attacked:** the ported self-test itself.

**Finding:** the sibling's commit records that reverting the stripper makes its
self-test fail on the JSON-LD case, and its mutation harness counts "17 of 17
caught". That is the right shape, and a port that only shipped the passing half
would be strictly weaker than the thing it came from — a checker whose failure
has never been observed.

**What changed:** `--naive` mode runs the *same* cases through the pre-fix
one-liner and exits non-zero. A regression clause asserts both halves
(`stripper_selftest` and `stripper_selftest_fails_naive`), so the passing half
cannot outlive the failing half. The mutation is checked into the test file
rather than being a claim in a commit message.

## R13 — An existing clause was passing for the wrong reason

**Attacked:** `credit_mover_kedge`, added in the first pass of this work. It
read `data/usage.json` through a shell-quoted `python3 -c`.

**Finding:** the clause worked on the fixed tree and failed against the
pre-fix tree, which is exactly what was claimed of it — so nothing here is
wrong. The defect is in the *mechanism*: the check was never observed failing
against a tree that merely had bad **data**, only against a tree where the field
was absent. A copy of the credited numbers into the no-credit column would have
passed it. That is the same "it was never a re-sort" failure the clause exists
to catch.

**What changed:** the clause is now `tools/check-credit-mover.py`, which checks
three providers (Kedge, Google Cloud Run, Azure Container Apps) rather than one
and has a `--mutate` mode that writes the credited numbers into the no-credit
column. Against the mutation the check fails, naming all six violated
assertions. The regression suite asserts both directions
(`credit_mover_kedge` and `credit_mover_guard_can_fail`).

## R14 — Did the old reader misclassify anything here? (measured)

**Attacked:** the possibility that this repository is carrying the same false
"unreadable page" verdict, which is the whole reason the sibling's commit
matters.

**Finding:** `tools/crosscheck-jsonld.py` fetched **62 URLs this repository
publishes** (every census row plus the 40 cheapest ranked rows) and ran both
readers over each. **31 of the 62 contain a JSON-LD block** — the format is
pervasive, so the class of defect was live here even though the symptom was not.
**0 verdicts changed**: every one of those pages is also readable without the
JSON-LD. One page, `killercoda`, is unreadable by both readers and stays
recorded as such, which is the honest answer.

So the port is a **guard against a future probe, not a correction to a published
row**, and that is stated rather than implied. The result is committed as
`data/jsonld-crosscheck.json` with the per-URL evidence.

## R15 — The stash mode was not doing what its own comment claimed

**Attacked:** `tests/regressions-anon-vms.sh --stash`, the mode that has to
demonstrate the clauses can fail.

**Finding:** after the first pass was committed, the mode stashed nothing —
`git stash push` without `--include-untracked` leaves untracked files, and a
dirty tree leaves nothing to stash — so `--stash` reported a full pass while
printing "(a low pass count is the expected result)", which was false. A mode
that reports success when it tested nothing is worse than no mode: it would have
been the artefact someone trusted.

**What changed:** the mode now stashes tracked *and* untracked files, warns and
degrades explicitly when there is nothing to stash, and separates clauses whose
subject is a file this work created (`new-file`, which can never fail against
the pre-change tree) from clauses over pre-existing files (which must fail
there). The run above shows **3 failed, 2 new-file** against the pre-change
tree, and names which are which — so a reader can tell that the failing clauses
bind.

## R16 — The upstream commit message is evidence, and its numbers are close to constants

**Attacked:** the choice to quote the sibling's defects instead of measuring
them here.

**Finding:** the sibling's commit is a first-party defect report about its own
instrument, dated the same day, with the mechanism and the corrected count
("4 were mislabelled this way and 22 are genuinely client-rendered"). It is
reproducible by its own self-test. What it is **not** is verifiable from here:
this host cannot re-run 183 fetches through their probe in one pass, and the 4
pages are not named individually in the diff.

**What changed:** nothing, deliberately. The sibling's commit is cited as a
*different repository's measurement*, the same treatment this catalogue already
gives a corpus card. The claim this repository makes is only about its own 62
measured URLs, which is why R14 exists.

## What this second pass did not establish

- **That 31 JSON-LD-bearing pages is a property of the market** rather than of
  the 62 URLs sampled. The sample is every census URL plus the 40 cheapest
  ranked rows, which is what this repository publishes first, not a random draw.
- **That a future probe would have hit the defect.** 0 of 62 would have been
  flipped; the port is insurance, and calling it a correction would overstate it.
- **That the sibling's 4 mislabelled pages are the only ones it has.** Its own
  message says the check was re-run over 26 shell verdicts; the unreadable set
  beyond that is not re-derived here.
- **That the stripper's JSON-LD handling is complete.** A page that renders its
  prices only inside a framework payload (for example a Next.js flight
  script) is still unreadable by this reader, and `killercoda` is left recorded
  that way rather than papered over.

## R17 — The "page is in step" clause was checking the wrong thing

**Attacked:** `page_in_step_with_json`, which exists so the generated page cannot
drift from the JSON.

**Finding:** it ran `render` and then `git diff --quiet -- docs/ANONYMOUS-VMS.md`.
That is red whenever the *source JSON* is dirty, even though the page is
correct, and it says nothing about whether the page matches a fresh render — it
compares the page to its last commit, not to its generator. It passed in the
first pass by accident of ordering: the page had been rendered immediately
before, so there was nothing to differ from. Rendered after a JSON edit without
a re-render, it would have reported the page as out of step for the wrong
reason, and after a re-render it would have reported *in step* even if the
renderer was invoked with the wrong output path.

**What changed:** `tools/page-in-step.sh` renders into a scratch directory (the
renderer now honours `ANON_VMS_OUT`) and compares bytes with the committed page.
Both mutations are demonstrated: a stray line appended to the page fails it, and
an edited `cost_usd` in the JSON fails it with the exact `diff -u`. Nothing here
changed a published number; the check that guards the page is what improved.
