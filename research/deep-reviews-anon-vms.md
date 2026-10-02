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
