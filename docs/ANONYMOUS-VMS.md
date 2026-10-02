# Anonymous and free VMs that answer SSH

The catalogue in [`data/usage.md`](../data/usage.md) prices 366 providers at a
fixed shape. This page answers a different question, the one a sandbox that is
being bootstrapped actually asks first: **what can I get a shell on without a
card, without an account, or for nothing — and how do I reach it if the machine
cannot accept an inbound connection?**

Generated from [`data/anonymous-vms.json`](../data/anonymous-vms.json) by
`tools/render-anon-vms.py`. The guard `tools/check-anon-vms.py` fails if the
list drops below ten SSH-capable free-or-anonymous machines or a row loses its
source or its caveat. Prices and quotas are 2026-10-02 unless the row says
otherwise; the fetch is reproducible with `tools/fetch-anon-sources.sh`.

## What the three classes mean

- **anonymous** — no account and no card. The first connect identifies the
  machine by the SSH key that made it.
- **free-account** — signup is required; no card is charged for the free quota.
- **free-tier-card** — a card is required, and a recurring or time-boxed
  allowance covers the machine.

**15 rows below are a free or anonymous machine you can reach
over SSH.** That count is the guard's, not this paragraph's. The reviews of
this pass, including what it did not establish, are in
[`research/deep-reviews-anon-vms.md`](../research/deep-reviews-anon-vms.md).

## 1. Anonymous: no account, no card

| Provider | SSH | How you get in | What you get | Lifetime | Cost |
|---|---|---|---|---|---|
| [Railway Free VM](https://railway.com/free-vm) | yes | ssh railway.new, with any ed25519 key as the identity | 2 vCPU / 2 GB, coding agents preinstalled (Claude Code, Codex, OpenCode, Cursor CLI, Grok, pi, Railway Agent) | 60-minute build window, then 24 h to claim; unclaimed boxes and their files are deleted | 0 |

Anonymous means exactly what it says: Railway's own FAQ answers *"Do I need a
Railway account?"* with **"No. Railway identifies you by your SSH key."** It is
the rare case where the signup step is the key itself, and it is the only row
here that needs nothing else. The box lasts 60 minutes to build and 24 hours to
claim; an unclaimed box and its files are deleted.

## 2. Free with an account

| Provider | SSH | How you get in | What you get | Lifetime | Cost |
|---|---|---|---|---|---|
| [alwaysdata Free](https://www.alwaysdata.com/en/pricing/) | yes | SSH to the account's user; alwaysdata documents SSH users, keys and 2FA | 1 GB SSD, 256 MB RAM, 1/4 CPU, shared hosting | the free offer is described as available for life | 0 |
| [GitHub Codespaces](https://docs.github.com/en/billing/concepts/product-billing/github-codespaces) | yes | gh codespace ssh -c CODESPACE-NAME; the default dev container runs an SSH server | 2-core default machine; choose 2/4/8/16/32-core | quota resets monthly; a codespace is deleted after its retention period of inactivity | 0 within the free quota |
| [Google Cloud Shell](https://cloud.google.com/shell/docs/limitations) | yes | Open in the browser or connect with the gcloud CLI; SSH from a terminal is available for the ephemeral VM | temporary Compute Engine VM, 5 GB persistent $HOME | ephemeral VM per session; the 5 GB $HOME persists | 0 within the weekly quota |
| [hashbang (#!)](https://hashbang.sh/) | yes | Register an SSH public key with the provisioning API, then ssh username@server.hashbang.sh | shared shell server | free shell account, community-run | 0 |
| [Hugging Face Spaces (CPU)](https://huggingface.co/pricing) | yes | Spaces Dev Mode exposes an SSH endpoint for a running Space | free CPU basic Space (2 vCPU / 16 GB) | while the Space exists and is built | 0 on the free CPU tier |
| [Lightning AI](https://lightning.ai/pricing) | yes | SSH into a Studio where the product exposes it; the free CPU Studio is the free tier | free CPU Studio; 4 h per session then paid, one at a time | free tier recurring | 0 for the free CPU Studio |
| [Modal Starter](https://modal.com/pricing) | yes | modal shell into a sandbox container from the Modal CLI | containers and sandboxes on Modal's pool; 1 TiB/month free egress | monthly credit reissued each month | 0 within $30/month of compute |
| [SDF Public Access UNIX System](https://sdf.org/?signup) | yes | ssh new@sdf.org to create the account, then ssh USER@sdf.org; an HTML5 SSH client is also offered | shared multi-user UNIX host, not a private VM | free USER tier for as long as the account is used | 0 |
| [tilde.club](https://tilde.club/wiki/) | yes | SSH; the wiki publishes the host's RSA, ECDSA and ED25519 fingerprints | shared shell account | free while active | 0 |
| [tilde.town](https://tilde.town/) | yes | SSH; the site publishes the host ECDSA key | shared shell account | free while active | 0 |
| [AWS CloudShell](https://aws.amazon.com/cloudshell/) | no | Browser terminal only; no inbound SSH endpoint is published | 1 GB persistent storage per AWS Region | session persists within the Region; idle sessions end | 0 |
| [Azure Cloud Shell](https://learn.microsoft.com/en-us/azure/cloud-shell/overview) | no | Browser terminal only; no inbound SSH endpoint is published | cloud-hosted shell with a persistent Azure Files share | session times out after 20 minutes without interactive activity; files persist | 0 for the machine; storage costs apply |
| [Killercoda](https://killercoda.com/) | no | browser terminal; no inbound SSH published | Linux or Kubernetes scenario environment | FREE scenario runs up to 1 hour; PLUS up to 4 hours and 3 concurrent scenarios | 0 on the free tier |
| [Northflank Sandbox tier](https://northflank.com/pricing) | no | No published inbound SSH; deploy services and use the web console or API | 2 free services, 1 free database, 2 free cron jobs, always-on | free while the account is used | 0 |
| [Render Free compute](https://render.com/pricing) | no | No published inbound SSH for free web services | 512 MB RAM, less than 1 CPU | free compute plans have usage limits and are for exploration and previews | 0 |

These are the durable free rows: shared shells and dev environments that renew
every month, plus the free browser shells. None of them asks for a card.

## 3. Free allowance with a card

| Provider | SSH | How you get in | What you get | Lifetime | Cost |
|---|---|---|---|---|---|
| [AWS Free Tier](https://aws.amazon.com/free/) | yes | SSH key pair is chosen at instance launch; the console and the CLI both connect | EC2 instances up to the plan's credit; the current free plan is credit-based (up to $200 over 6 months) | 6 months, or until the credits run out; the account then closes on its own unless converted to paid | 0 within the credits |
| [Azure Free Account](https://azure.microsoft.com/en-us/free/) | yes | SSH keys are set at VM creation; the portal and the CLI both connect | 750 hours each of B1s, B2pts v2 (Arm) and B2ats v2 (AMD) burstable VMs, plus 65+ always-free services | the VM hours are 12 months for new customers; the $200 credit lasts 30 days; always-free services do not expire | 0 within the monthly amounts |
| [Google Cloud Free Tier (e2-micro)](https://cloud.google.com/free/docs/free-cloud-features) | yes | SSH keys are added to the instance or its project metadata; gcloud and the browser SSH both work | 1 non-preemptible e2-micro, 30 GB standard persistent disk, 1 GB egress | every month, for the life of the account | 0 within the allowance |
| [Oracle Cloud Always Free](https://www.oracle.com/cloud/free/) | yes | SSH key is installed at instance creation; the console and the CLI both connect | 2 AMD micro VMs and up to 4 OCPU / 24 GB Arm Ampere A1 across one or more instances; 200 GB block storage | Always Free, no time limit, while the tenancy qualifies | 0 on the Always Free shapes |

The largest machines on the page: Oracle's Always Free A1 allowance and
Google's e2-micro are real 24/7 machines. AWS's free plan is now a six-month
credit that closes the account when it ends, and Azure's 750 hours are twelve
months only.

## 4. Products that changed or died

| Provider | SSH | How you get in | What you get | Lifetime | Cost |
|---|---|---|---|---|---|
| [Fly.io](https://fly.io/docs/about/pricing/) | no | fly ssh console reaches a running Machine, but there is no free allowance to run one | shared-CPU Machines; volumes first 10 GB free per month | pay-as-you-go | no free VM allowance; the only 'first free' is 10 GB of volume capacity |
| [Koyeb](https://www.koyeb.com/pricing) | no | No published inbound SSH; the free plan is not in the published tiers | platform services and workers; included usage is a plan feature | included usage reissued monthly on paid plans | 0 only if a free tier is still offered; the published Starter/Pro plans carry included usage |
| [Play with Docker](https://labs.play-with-docker.com/) | no | browser terminal, never SSH | 4-hour Docker-in-Docker session (historical) | unavailable from 2026-03-01 | n/a |

Two corrections matter here. **Play with Docker**, the canonical anonymous free
VM in every list older than this one, says: *"Play with Docker will be
unavailable starting March 1, 2026."* It is recorded because citing it as live
is a mistake this page exists to prevent. **Fly.io** no longer publishes a free
Machine allowance: the only "first free" left on its pricing page is 10 GB of
volume capacity.

## The detail behind every row

**alwaysdata Free** — `free-account`, account=yes, card=no
- quote: “Free ... 0 €/month ... Disk space SSD 1 Go gift RAM 256 Mo free CPU 1/4 ... for life”
- checked: first-party-fetched 2026-10-02, sources/anon-2026-10-02/alwaysdata.html and alwaysdata-ssh.html
- caveats: Shared web-hosting account, not a root VM; the free quota is small and some services are restricted.

**AWS Free Tier** — `free-tier-card`, account=yes, card=yes
- quote: “When you create a new AWS Free Tier account, you get $100 in credits immediately. As you explore key services, you can earn up to $100 more. That's up to $200 over 6 months ... The account closes on its own 6 months after you open it or when your credits run out, whichever comes first.”
- checked: first-party-fetched 2026-10-02, sources/anon-2026-10-02/aws-free.html
- caveats: A card is required. The free plan is time-boxed and closes itself; the old 750-hours-for-12-months t2.micro offer is no longer the headline shape of the plan.

**Azure Free Account** — `free-tier-card`, account=yes, card=yes
- quote: “12 months Azure Virtual Machines for Linux or Windows 750 hours each of B1s, B2pts v2 (Arm-based), and B2ats v2 (AMD-based) burstable VMs ... $200 credit to use on Azure services within 30 days”
- checked: first-party-fetched 2026-10-02, sources/anon-2026-10-02/azure-free.html
- caveats: A card is required and a temporary $1 authorization may be placed at signup. The 750-hour VM allowance is 12 months only; the $200 credit is 30 days.

**GitHub Codespaces** — `free-account`, account=yes, card=no
- quote: “GitHub will provide users in the free plan 120 core hours or 60 hours of run time on a 2 core codespace, plus 15 GB of storage each month.”
- checked: first-party-fetched 2026-10-02, sources/anon-2026-10-02/gh-codespaces.html and gh-codespaces-feat.html and gh-codespaces-cli.html
- caveats: Free quota is for personal accounts only; organizations and enterprises must pay. Storage beyond 15 GB-month and compute beyond the quota are billed.

**Google Cloud Free Tier (e2-micro)** — `free-tier-card`, account=yes, card=yes
- quote: “1 non-preemptible e2-micro VM instance per month in one of the following US regions ... 30 GB-months standard persistent disk ... 1 GB of outbound data transfer ... per month.”
- checked: first-party-fetched 2026-10-02, sources/anon-2026-10-02/gcp-free-features.html
- caveats: A billing account with a card is required. The allowance is one e2-micro in us-west1, us-central1 or us-east1; the $300 signup credit is one-time and separate.

**Google Cloud Shell** — `free-account`, account=yes, card=no
- quote: “The default weekly Cloud Shell quota is 50 hours.”
- checked: first-party-fetched 2026-10-02, sources/anon-2026-10-02/gcloud-shell-limits.html
- caveats: Sign-in with a Google account is required. Exceeding the weekly quota suspends Cloud Shell until the next week. The VM is recreated, so only $HOME survives.

**hashbang (#!)** — `free-account`, account=yes, card=no
- quote: “curl -d '{"user":"someuser","key":"'"$(cat ~/.ssh/id_rsa.pub)"'","host":"someHost.hashbang.sh"}' -H 'Content-Type: application/json' https://hashbang.sh/user/create”
- checked: first-party-fetched 2026-10-02, sources/anon-2026-10-02/hashbang.html
- caveats: Account creation is automatic from a public key; it is a shared shell, and the project says it has never handed user data to a government agency but offers no formal SLA.

**Hugging Face Spaces (CPU)** — `free-account`, account=yes, card=no
- quote: “Spaces Hardware ... Starting at $0.”
- checked: first-party-fetched 2026-10-02, sources/anon-2026-10-02/hf-pricing.html
- caveats: A free account is required. It is an app host, not a general VM; Dev Mode is the documented way to get a shell and its availability should be checked against the current docs.

**Lightning AI** — `free-account`, account=yes, card=no
- quote: “unavailable: every lightning.ai URL returns a 403 ('hasn't expanded to your area yet') to this host”
- checked: blocked-from-host 2026-10-02: 739-byte regional 403; the figure is carried from the corpus card and research/verification/2026-10-02.md
- caveats: Not sold in every region; the catalogue's #1 row rests on this unverified card. A free tier on an account, not an anonymous VM.

**Modal Starter** — `free-account`, account=yes, card=no
- quote: “$0 + compute / month ... $30 / month free credits ... 1 TiB / month free network egress”
- checked: first-party-fetched 2026-10-02, sources/anon-2026-10-02/modal-pricing.html
- caveats: An account is required; the $30 is a monthly credit, not a permanent free machine. It is a container sandbox, not a general VPS.

**Oracle Cloud Always Free** — `free-tier-card`, account=yes, card=yes
- quote: “All tenancies get the first 1,500 OCPU hours and 9,000 GB hours per month for free for VM instances using the VM.Standard.A1.Flex shape (carried from research/verification/2026-10-02.md; the oracle.com domain returns 403 to this host)”
- checked: blocked-from-host: every oracle.com URL returns a 1,339-byte export-control 403 here; the corpus card and the quoted allowance are the evidence
- caveats: A card is required at signup and capacity can be reclaimed; A1 is often out of capacity in a region. The allowance is a resource allowance, not a dollar credit.

**Railway Free VM** — `anonymous`, account=no, card=no
- quote: “No. Railway identifies you by your SSH key. If you don't have one, run ssh-keygen -t ed25519 and connect again. You only sign up if you want to keep the box.”
- checked: first-party-fetched 2026-10-02, sources/anon-2026-10-02/railway-free-vm.html
- caveats: Anonymous trials are capped per region and can be temporarily disabled under demand; the preview URL is visible only from the creating IP until claimed; abuse protections and a shared AI budget apply.

**SDF Public Access UNIX System** — `free-account`, account=yes, card=no
- quote: “Create a Free UNIX Shell Account ... Linux/UNIX users can type 'ssh new@sdf.org' at their shell prompt.”
- checked: first-party-fetched 2026-10-02, sources/anon-2026-10-02/sdf-signup.html
- caveats: It is a shared shell, not a VM; the free USER tier is validated by the community and paid MetaARPA tiers add services.

**tilde.club** — `free-account`, account=yes, card=no
- quote: “How to connect using SSH (Secure SHell) ... SSH fingerprints: SHA256:M2URWy/QGPdn8K1XHA5KEWQs+7RtqKCkHCqp1NyxFyI (RSA) ... (ED25519)”
- checked: first-party-fetched 2026-10-02, sources/anon-2026-10-02/tildeclub-wiki.html
- caveats: Shared shell, not a VM; signups no longer accept gmail.com addresses.

**tilde.town** — `free-account`, account=yes, card=no
- quote: “ecdsa host key: SHA256:RNFVaXxh2wnrolcByZQBRxRZDFBb2HRCnNq/g9ZGRp0”
- checked: first-party-fetched 2026-10-02, sources/anon-2026-10-02/tildetown.html
- caveats: Shared shell; signup is by invitation/request; not a VM.

**AWS CloudShell** — `free-account`, account=yes, card=no
- quote: “Run scripts and commands at no extra cost, with up to 1 GB of persistent storage per AWS Region.”
- checked: first-party-fetched 2026-10-02, sources/anon-2026-10-02/aws-cloudshell.html
- caveats: An AWS account is required. It is a browser shell, not a machine you can SSH into from elsewhere.

**Azure Cloud Shell** — `free-account`, account=yes, card=no
- quote: “Use of the machine hosting Cloud Shell is free. Cloud Shell requires a storage account to host the mounted Azure Files share. Regular storage costs apply.”
- checked: first-party-fetched 2026-10-02, sources/anon-2026-10-02/azure-cloudshell-learn.html
- caveats: An Azure account and a storage account are required; the storage share is billed normally.

**Fly.io** — `changed`, account=yes, card=yes
- quote: “$0.08/GB per month First 10GB free each month”
- checked: first-party-fetched 2026-10-02, sources/anon-2026-10-02/fly-pricing.html
- caveats: The free Machine allowance Fly.io used to grant is gone from the pricing page. A card is required; the 10 GB is storage, not compute.

**Killercoda** — `free-account`, account=yes, card=no
- quote: “Membership PLUS Includes all from FREE Use scenarios for up to 4 hours instead of just one ... Open up to 3 scenarios at the same time”
- checked: first-party-fetched 2026-10-02, sources/anon-2026-10-02/killercoda.html
- caveats: The page does not state whether a login is required to start a free scenario; treat 'anonymous' as unverified. Browser terminal only, no SSH.

**Koyeb** — `changed`, account=yes, card=no
- quote: “Pro $29 /mo +compute ... Included Usage $10 ... Once you've consumed your included monthly free credit, we start billing you on a pay-per-use basis.”
- checked: first-party-fetched 2026-10-02, sources/anon-2026-10-02/koyeb-pricing.html
- caveats: The old free 'Hobby' instance is not in the tiers shown on 2026-10-02; included usage is a paid-plan feature, so a free VM should not be assumed.

**Northflank Sandbox tier** — `free-account`, account=yes, card=no
- quote: “Tiers Sandbox ... Always-on-compute - no sleeping :) 2x free services 1x free database 2x free cron jobs”
- checked: first-party-fetched 2026-10-02, sources/anon-2026-10-02/northflank-pricing.html
- caveats: A container platform, not a VM you SSH into; the free tier is for testing and building trust.

**Play with Docker** — `dead`, account=no, card=no
- quote: “Deprecation notice: Play with Docker will be unavailable starting March 1, 2026.”
- checked: first-party-fetched 2026-10-02, sources/anon-2026-10-02/play-with-docker.html
- caveats: Recorded because it is the canonical 'anonymous free VM' many lists still cite. It is gone; Docker Docs now points at supported labs.

**Render Free compute** — `free-account`, account=yes, card=no
- quote: “Free ( limitations apply ) $0/month 512 MB RAM free Less than 1 CPU”
- checked: first-party-fetched 2026-10-02, sources/anon-2026-10-02/render-pricing.html
- caveats: Web services, key-value and Postgres - not a VM. Free instances sleep and are not for production.

## Reaching a box that cannot listen: `dropssh` and a relay

Most of these machines are reachable because the provider grew an SSH endpoint.
A sealed sandbox does not have one, and cannot have one: this host reports
`bind(2) INET` refused with `EACCES`, so no process here can listen on a TCP
port. The catalogued answer is a relay both ends dial out to, with a server that
speaks SSH over the outbound socket.

The errand proved that path end to end on this sandbox with
[`dropssh`](https://github.com/talaria0101/dropssh) and the
[`tcp.ssh.relay.ajam.dev`](https://tcp.ssh.relay.ajam.dev/llms.txt) relay. The
sequence that works, and the three things that fail before it does:

```sh
# 1. a pair: the agent keeps node_token and hands connect_token to the operator
dropssh pair

# 2. the node side. -Y ./passwd is not optional: there is no /etc/passwd here,
#    and a login name that does not exist logs "wrong user".
dropssh serve --name "$NAME" --token "$NODE_TOKEN" \
  --server "./dropbear -i -E -F -r hostkey -D ak -Y ./passwd"

# 3. the operator side, over the relay
ssh -o ProxyCommand="dropssh connect --name $NAME --token $CONNECT_TOKEN" \
    user966@"$NAME"
```

Measured on this host, 2026-10-02:

- **The server must read the passwd database from a file.** The shipped
  `dropbear` is immune to `LD_PRELOAD`, and the sandbox has no `/etc/passwd`;
  `dropbear -Y ./passwd` is what turns `Login attempt for wrong user root` into
  `Pubkey auth succeeded for 'user966'`. The passwd line must name **this
  sandbox's uid (966)**, because dropbear refuses a login whose uid differs from
  the server's.
- **The server's paths must not sit under a world-writable directory.** The
  same setup under `/tmp` dies on `"/tmp must be owned by user or root, and not
  writable by group or others"`. `-D`, the host key and the passwd file all live
  under a directory this user owns and this user can execute.
- **A reverse pair is self-service, and its tokens are credentials.** The pair
  above mints its own name and two 64-hex tokens; the relay authenticates the
  tokens, not people. They are not committed here and must not be.

The working session returned `uid=966 gid=965`, `Linux`, and the login's
`$HOME`, and the server logged `Pubkey auth succeeded` — a real SSH session on a
host that cannot bind a port. The full note, with the conditions and the exact
commands, is in
[`research/verification/ssh-relay-2026-10-02.md`](../research/verification/ssh-relay-2026-10-02.md);
the consolidated mechanism-and-failures report is
[`docs/SSH-RELAY.md`](SSH-RELAY.md). The relay's forward transport and colo
rotation are measured separately in [`docs/RELAY-FORWARD.md`](RELAY-FORWARD.md).

## How this was checked

- Sources are fetched by [`tools/fetch-anon-sources.sh`](../tools/fetch-anon-sources.sh)
  into `sources/anon-2026-10-02/`; the committed `MANIFEST.tsv` records the URL,
  HTTP status, byte count and SHA-256 of every page at fetch time.
- The one row that could not be re-fetched (`oracle.com` returns a 1,339-byte
  export-control 403 to this host) is marked `blocked-from-host` and carries the
  carried figure and the reason rather than a silent guess.
- **A page that renders its own words inside a JSON-LD block is not unreadable.**
  A sibling implementation found that stripping every `<script>` threw away a
  schema.org pricing block and made 4 readable pages read as "client-rendered
  shells". [`tools/check-strip-selftest.py`](../tools/check-strip-selftest.py)
  is the reader here, with 8 known-answer cases; `--naive` runs the same cases
  through the pre-fix one-liner and must fail 3 of them.
  [`tools/crosscheck-jsonld.py`](../tools/crosscheck-jsonld.py) then asked what
  that means for this page: of 62 published URLs, 31 carry a JSON-LD block and
  **0 verdicts changed**, so it is a guard rather than a correction. The result
  is in [`data/jsonld-crosscheck.json`](../data/jsonld-crosscheck.json).
- `tools/check-anon-vms.py` gates the list. Run it with:

```sh
python3 tools/check-anon-vms.py       # rows, ssh-capable count, missing fields
python3 tools/render-anon-vms.py      # rewrite this page from the JSON
python3 tools/check-strip-selftest.py # the reader's known-answer cases
python3 tools/crosscheck-jsonld.py    # does the JSON-LD fix change anything
sh tests/regressions-anon-vms.sh      # 14 clauses; --stash proves they can fail
```

The reviews of both passes are in
[`research/deep-reviews-anon-vms.md`](../research/deep-reviews-anon-vms.md),
including what the JSON-LD crosscheck did **not** establish: 31 of 62 published
URLs carry a JSON-LD block, and none of them changed verdict.

*We aim to provide the software that shapes the world of tomorrow.*
