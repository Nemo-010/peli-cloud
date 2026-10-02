# The relay's forward transport and colo rotation — measured

Technical report, 2026-10-02. Relay `tcp.ssh.relay.ajam.dev`, version
`2026-10-01-r2`. Standalone; every number below is from a fetch or a probe on
that date, and every one is reproducible with the scripts named at the end.

Related: [`SSH-RELAY.md`](SSH-RELAY.md) (the reverse path — SSH *into* a host
that cannot bind a port), [`ANONYMOUS-VMS.md`](ANONYMOUS-VMS.md) (the provider
census this sits beside). Data: `data/relay-colo-egress.json`. Raw captures and
their hashes: `sources/relay-2026-10-02/MANIFEST.tsv`.

## 1. What the service is

A WebSocket ⇄ TCP relay: binary WebSocket frames carry a raw TCP stream in both
directions. It does not implement SSH or any client protocol; it moves bytes to
a TCP target, or between two paired peers. Deployment `default`; outbound TCP
prefers the Workers VPC network binding (egress by Cloudflare Gateway) and falls
back to a direct Worker socket.

Addresses (from the relay's own `llms.txt` and `/`):

| Purpose | Address |
| --- | --- |
| Forward, arbitrary public TCP target | `wss://tcp.ssh.relay.ajam.dev/connect/<host>/<port>` |
| Reverse node | `wss://tcp.ssh.relay.ajam.dev/v1/node/<name>` |
| Reverse operator | `wss://tcp.ssh.relay.ajam.dev/v1/connect/<name>` |
| Reverse status | `https://tcp.ssh.relay.ajam.dev/v1/status/<name>` |
| Self-service pair | `POST https://tcp.ssh.relay.ajam.dev/v1/pair` |
| Self-service forward token | `POST https://tcp.ssh.relay.ajam.dev/v1/mint` |
| Pool ranking | `https://tcp.ssh.relay.ajam.dev/relays.json` |
| Diagnostics | `https://tcp.ssh.relay.ajam.dev/trace` |

## 2. Forward transport

1. `POST /v1/mint` with an empty body returns `{token, expires, scope}`. The
   token has the form `ephm1.<exp>.forward.<mac>` and dies at `expires`, never
   later than 72 h after minting. Expiry is checked when a session is
   established, not per frame.
2. Open a WebSocket to `/connect/<host>/<port>` with the token in
   `X-Relay-Token` (or `?token=`, or the path form `/t/<t>/connect/...`).
3. Binary frames are copied to the target socket in order; target bytes return
   as binary frames. Any TCP protocol works.

Policy reported by `GET /health?detail=1` and echoed in `/trace`:

```
policy.token_required = true
policy.forward_auth_ready = true
policy.allow = "any public target"
policy.max_frame_bytes = 262144
policy.dns_guard = true
policy.road_locked = false
policy.deny_ports = []
```

A `403` with `missing or wrong token` means absent or wrong; a `403` that names
the target is an allow-list denial. `503` on mint means issuance is disabled.

## 3. The colo pool and rotation

`relays.json` lists the pool; `GET /relays.json` ranks it for the caller's edge
colo and target. It accepts `?prefer=`, `?region=`, `?relay=`, `?spread=`,
`?host=` and `?port=`. The four entries:

| host | bucket | placement |
| --- | --- | --- |
| `tcp.ssh.relay.ajam.dev` | — | client-nearest colo (no placement) |
| `tcp-1.ssh.relay.ajam.dev` | `ap` | `aws:ap-south-1` |
| `tcp-2.ssh.relay.ajam.dev` | `eu` | `aws:eu-central-1` |
| `tcp-3.ssh.relay.ajam.dev` | `us` | `aws:us-east-1` |

## 4. Measured: egress per colo

Method: mint one forward token, then for each colo `GET
/trace?egress=1&format=text`. That endpoint dials `api.ipify.org` through the
relay and reports the address the target observed. Run at 2026-10-02T08:16Z
from this host; full result in `data/relay-colo-egress.json`.

| host | bucket | region | observed egress IP | family | total_ms |
| --- | --- | --- | --- | --- | --- |
| `tcp.ssh.relay.ajam.dev` | — | — | `104.28.204.8` | 6 | 87 |
| `tcp-1.ssh.relay.ajam.dev` | ap | `aws:ap-south-1` | `104.28.200.92` | 6 | 242 |
| `tcp-2.ssh.relay.ajam.dev` | eu | `aws:eu-central-1` | `104.28.197.9` | 6 | 206 |
| `tcp-3.ssh.relay.ajam.dev` | us | `aws:us-east-1` | `104.28.196.79` | 6 | 45 |

Four distinct source addresses, all inside Cloudflare's `104.28.196.0/22`. The
target therefore observes the relay's egress, not the caller's address. The
rotation selects which colo carries the session; `total_ms` is dominated by the
path from this host's edge colo to the chosen colo (us-east-1 fastest here at
45 ms, ap-south-1 slowest at 242 ms).

Egress road on every colo was `vpc` (`egress.vpc_binding=true`,
`egress.roads.direct=0`), i.e. the Workers VPC / Cloudflare Gateway road.

## 5. Measured: forward banner check

Method: same token, `GET /trace?target=github.com:22&banner=1&format=text`.
The relay dials the target and returns its first bytes.

```
target.host=github.com
target.port=22
target.ok=true
target.road=vpc
target.dialed=140.82.114.3
target.address_family=4
target.connect_ms=3
target.first_byte_ms=107
target.bytes_seen=17
target.verdict=live
target.banner=SSH-2.0-2097ddd
```

The relay resolved and dialed the public SSH endpoint, and returned the server
banner. This exercises the forward transport end to end without a client
WebSocket: the same dial a `/connect/github.com/22` session performs.

## 6. Limits and session accounting

From the relay's own documentation (`llms-full.txt`), not measured here:

- Idle sessions close after 180000 ms of payload inactivity; transport
  keepalives do not reset that.
- Session caps: 720 min, 64 MiB.
- The 120/minute admission brake applies to unauthenticated forward WebSocket
  attempts and to public `mint`/`pair` calls (keys `mint:` and `pair:`).
  Authenticated sessions and diagnostics do not share that bucket.
- Rotating `MINT_SECRET` invalidates every minted token at once.
- Reverse credentials are operator-issued, except agent-created pairs, which
  mint their own and carry `node_token` / `connect_token` / `stop_token`.

## 7. What this report does not establish

- **Not a stability claim.** `relays.json` and `/trace` are point-in-time; the
  pool ranking is computed for the caller's edge colo and changes with it.
- **Not all four colos under load.** Each colo answered one probe; no
  throughput, concurrency or sustained-session measurement was made.
- **Not the VPC vs direct road difference.** Every probe took the `vpc` road;
  `direct` was not forced with `&path=direct` or observed under failure.
- **Not the forward WebSocket itself.** Section 5 uses `/trace`, which performs
  the same dial server-side; a raw `/connect/<host>/<port>` session from a
  WebSocket client was not driven in this pass. The reverse WebSocket *was*
  driven, and is in `SSH-RELAY.md`.
- **Not IPv4 egress.** Every observed egress was family 6; `?family=4` was not
  forced.
- **Not the caller's own address.** The local host's `request.client_ip` and
  geo fields are deliberately not reproduced; they identify the caller, not the
  relay, and are not part of a report about the relay.

## 8. Reproduce

```sh
sh tools/relay-probe.sh                 # mint, probe 4 colos, banner check -> data/relay-colo-egress.json
sh tools/fetch-relay-sources.sh         # re-fetch the relay docs + traces -> sources/relay-<date>/MANIFEST.tsv
sh tests/regressions-relay-forward.sh   # guard the JSON shape and the colo/egress invariants
```

`relay-probe.sh` mints its token per run and never prints it. Exit 0 requires
all four colos to answer and the banner verdict to be `live`.
