# Verification: the relay's forward transport and colo rotation

**Date:** 2026-10-02
**Relay:** `tcp.ssh.relay.ajam.dev`, version `2026-10-01-r2`
**Method:** first-party HTTP against the relay's own endpoints; one forward
token minted per run and never recorded.
**Artefacts:** `data/relay-colo-egress.json` (result), `tools/relay-probe.sh`
(reproduction), `tools/fetch-relay-sources.sh` (documents + hashes),
`sources/relay-2026-10-02/MANIFEST.tsv`.

This note records the raw answers behind `docs/RELAY-FORWARD.md`. The caller's
own `request.client_ip`, city, region, ASN and coordinates are redacted: they
describe this host, not the relay, and a report about the relay does not need
them.

## What was fetched

| id | url | http | bytes | sha256 (first 16) |
| --- | --- | --- | --- | --- |
| llms-txt | `https://tcp.ssh.relay.ajam.dev/llms.txt` | 200 | 3595 | `caadf93f5be7acd6` |
| llms-full | `https://tcp.ssh.relay.ajam.dev/llms-full.txt` | 200 | 15477 | `a82bf7c9841a9b58` |
| relays-json | `https://tcp.ssh.relay.ajam.dev/relays.json` | 200 | 3197 | `ec1a28c3f48b5835` |
| health-detail | `https://tcp.ssh.relay.ajam.dev/health?detail=1` | 200 | 764 | `728ff3720e1622eb` |
| trace-egress | `https://tcp.ssh.relay.ajam.dev/trace?egress=1&format=text` | 200 | 1282 | `32ba754b00f3749c` |
| trace-banner | `https://tcp.ssh.relay.ajam.dev/trace?target=github.com:22&banner=1&format=text` | 200 | 1316 | `180107903c1fa3f2` |

Full hashes and fetch timestamps are in the manifest. `relays.json` and the
`/trace` rows are dynamic (they depend on the caller's edge colo and the
moment); the two `llms` documents are the stable specification.

## Policy (from `/health?detail=1`)

```json
{
  "ok": true,
  "service": "tcp-ssh-relay",
  "version": "2026-10-01-r2",
  "relay": { "name": "default", "edge_colo": "BAQ", "path_config": "auto", "dial": "eager" },
  "egress": { "vpc_binding": true, "roads": { "vpc": 2, "direct": 0, "vpc_failed": 0 } },
  "pool": ["default", "1", "2", "3"],
  "reverse": { "enabled": true },
  "policy": {
    "token_required": true,
    "forward_auth_ready": true,
    "max_frame_bytes": 262144,
    "allow": "any public target",
    "dns_guard": true,
    "road_locked": false,
    "deny_ports": []
  }
}
```

The `allow` field is the plain string `any public target`; the relay requires a
valid forward token but does not restrict the target beyond its DNS guard.

## Egress probe, one colo (excerpt, caller fields redacted)

```
request.host=tcp.ssh.relay.ajam.dev
request.path=/trace
relay.name=default
relay.bucket=null
relay.region=null
relay.version=2026-10-01-r2
relay.path_config=auto
relay.dial=eager
relay.families_supported=auto,4,6
egress.vpc_binding=true
egress.configured=auto
egress.roads.vpc=2
egress.roads.direct=0
egress.roads.vpc_failed=0
egress.roads.vpc_resting=false
pool=[object Object],[object Object],[object Object],[object Object]
named=
auth.token_required=true
auth.allow=any public target
observed_egress.probe=api.ipify.org
observed_egress.road=vpc
observed_egress.dialed=api.ipify.org
observed_egress.address_family=6
observed_egress.observed_ip=104.28.204.8
observed_egress.connect_ms=4
observed_egress.total_ms=94
```

Across the four colos the `observed_ip` values were `104.28.204.8` (default),
`104.28.200.92` (ap), `104.28.197.9` (eu), `104.28.196.79` (us) — four distinct
addresses in `104.28.196.0/22`. This is the rotation, stated exactly: the
*source address observed by the target* changes with the chosen colo. It is not
a change of target and not a second machine; the same relay dials in each case.

## Forward banner probe (excerpt)

```
auth.allow=any public target
target.host=github.com
target.port=22
target.ok=true
target.road=vpc
target.dialed=140.82.114.3
target.dialed_literal=true
target.address_family=4
target.connect_ms=3
target.first_byte_ms=102
target.bytes_seen=17
target.verdict=live
target.banner=SSH-2.0-2097ddd
```

The relay dialed `github.com:22` over the VPC road and returned a 17-byte SSH
banner. Verdict `live`.

## Verdicts

- **Forward transport: confirmed.** `/trace?target=...&banner=1` performs the
  same target dial a `/connect/<host>/<port>` session performs, and it returned
  a live banner. What is *not* confirmed here is a client-driven WebSocket
  session over `/connect`; see the report's limits section.
- **Colo rotation: confirmed, as egress-IP rotation.** Four colos, four
  distinct observed egress IPs, all Cloudflare.
- **Token gating: confirmed.** `auth.token_required=true`; the tokenless probe
  is not shown because it was not needed, and `/trace` target dials require a
  token per the specification.
- **No caller address is recorded.** Redacted by design.

## Reproduce

```sh
sh tools/relay-probe.sh          # -> data/relay-colo-egress.json, exit 0 = 4 colos + live banner
sh tools/fetch-relay-sources.sh  # -> sources/relay-<date>/MANIFEST.tsv
```
