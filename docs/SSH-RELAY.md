# Reaching a sealed sandbox over an outbound SSH relay

Detailed report, 2026-10-02. Companion to
[`research/verification/ssh-relay-2026-10-02.md`](../research/verification/ssh-relay-2026-10-02.md)
(the dated first-party note) and [`tools/ssh-relay-check.sh`](../tools/ssh-relay-check.sh)
(the reproduction). Reader-facing summary in
[`ANONYMOUS-VMS.md`](ANONYMOUS-VMS.md).

## What this establishes

A real SSH login ran on this host, over a connection this host could only *dial
out*. The session returned `uid=966`, `uname -s` = `Linux`, and the server
logged `Pubkey auth succeeded`. Nothing here listens on an inbound port,
because nothing here can.

**There were no patches to OpenSSH, `dropbear`, or `dropssh`.** The word
"patch" is the wrong frame; the four things that had to be changed are
*configuration and shims*, each forced by a specific property of this sandbox.
They are listed in full in section 4, because "it works now" without the
failures it went through is not a reusable result.

## 1. The constraint: why a listener is impossible here

`sandhome report` describes this sandbox as `bind=unix`, `passwd=no`. Concretely:

- **No inbound socket.** `bind(2)` on `AF_INET` is refused with `EACCES`. A
  process here cannot open a TCP port, so no `sshd` can wait for a connection
  and no reverse tunnel can accept one. Any transport has to be a connection
  *this side initiates*.
- **No `/etc/passwd`.** `dropbear`/`sshd` resolve the login account through the
  system database; there is none. The same is true of the local `ssh-keygen`
  and `ssh`, which map a uid to a name to start.
- **No `/dev/ptmx`** (recorded on the host line of the verification note), so
  anything that insists on allocating a pty has another problem to solve.

A stock `OpenSSH sshd` in `-i` mode also needs a privilege-separation user and
a chroot directory, neither of which can be created here. So the ordinary
"start sshd and port-forward" answer is ruled out twice over: no bound port,
and no privilege-separation account.

## 2. The shape of the answer

Two ends that both dial *out* to a rendezvous, instead of one end dialing *in*:

```
   sandbox (uid 966)                                operator
   ────────────────                                 ────────
   dropssh serve ──┐                            ┌── dropssh connect
   (node_token)    │   outbound WebSocket       │   (connect_token)
                   └──►  tcp.ssh.relay.ajam.dev ◄┘
                            (pairs the two by name)
   dropbear -i -Y passwd  ◄── SSH bytes ──►  ssh -o ProxyCommand="dropssh connect"
```

- **`dropssh`** carries the SSH stream over an outbound WebSocket. The relay
  pairs a node to an operator by a random name and never needs the node to be
  addressable.
- **`dropbear -i`** is the server. Inetd mode means it serves a single
  connection on stdin/stdout rather than binding a socket — exactly what a
  `bind=unix` host can offer.
- **The operator's `ssh`** runs `dropssh connect` as its `ProxyCommand`, so the
  relay is invisible to the client above it.

Relay: `tcp.ssh.relay.ajam.dev`, version `2026-10-01-r2`, reverse enabled.
Tool: [`dropssh` v0.2.3](https://github.com/talaria0101/dropssh), release
`dropssh-x86_64-linux-musl.tar.gz` (a pinned download, checksum-verified
against the release's own `SHA256SUMS` before use).

## 3. The sequence that works

```sh
# 1. Mint a pair. The node keeps node_token; connect_token goes to the operator.
dropssh pair --relay tcp.ssh.relay.ajam.dev

# 2. Node side: serve exactly one session.
dropssh serve --relay tcp.ssh.relay.ajam.dev --name "$NAME" --token "$NODE_TOKEN" \
  --server "./dropbear -i -E -F -r hostkey -D ak -Y passwd" \
  --once --retry-budget 3

# 3. Operator side: SSH through the relay.
ssh -o 'ProxyCommand=dropssh connect --relay tcp.ssh.relay.ajam.dev \
        --name $NAME --token $CONNECT_TOKEN' \
    -i ak/id user966@"$NAME"
```

`dropbear` flags, in order: `-i` inetd/single-connection mode, `-E` log to
stderr, `-F` stay in the foreground, `-r` the host key, `-D` the
`authorized_keys` directory, `-Y` the **file** passwd database (section 4.1).

## 4. The four things that had to change

Each is a symptom, the diagnosis, and the fix. The fixes are configuration; two
of them are the difference between the shipped tool working and not working on a
static binary. (A fifth, client-side one — section 4.4 — was added when this
check was run on 2026-10-02 and the first script revision failed.)

### 4.1 The passwd database must come from a file (`-Y`), not the system

- **Symptom:** the first login attempt was refused with
  `Login attempt with wrong user root`.
- **Diagnosis:** there is no `/etc/passwd`, so the server has no account to
  authenticate `root` (or anyone) against. `dropssh` ships a `fakepwd.so`
  `LD_PRELOAD` shim for this case — but the `dropbear` in the v0.2.3 tarball is
  a **static-pie musl** binary, and `LD_PRELOAD` is a dynamic-loader mechanism.
  It has no effect on a static executable, so the shipped shim cannot fix the
  shipped server.
- **Fix:** use dropbear's own file-backed passwd database, `-Y FILE`, which
  reads one `passwd(5)` line per login from a file the user controls. With
  `-Y ./passwd`, the same login reached `Pubkey auth succeeded`.
- **Why it matters beyond this host:** the shim-vs-`-Y` distinction is the whole
  reason this row is not "just use the bundled preload". On a glibc `dropbear`
  the shim works; on the musl static one it silently does nothing, and `-Y` is
  the only passwd path.

### 4.2 The passwd line must name this host's uid

- **Symptom:** even with `-Y ./passwd`, the first file named `root:0:0` and the
  login was still refused — the server serves as **uid 966**, and `dropbear`
  refuses a login whose uid differs from the serving process's.
- **Fix:** write the line as `966:x:966:965:...:` — the login name, uid and gid
  must match the process that `dropssh serve` started. This is the same
  constraint `dropssh` documents in its own `tests/passwd-file-test.sh`.
- **Also:** the passwd entry's home directory must be owned by the login user,
  or the session's `$HOME` breaks.

### 4.3 The server's paths must not sit under a world-writable directory

- **Symptom:** with the work directory under `/tmp`, `dropbear` refused to
  start serving:
  `/tmp must be owned by user or root, and not writable by group or others`.
- **Diagnosis:** `/tmp` is mode `1777`. `dropbear` refuses to trust a host key,
  an `authorized_keys` directory, or a passwd file that a third party could
  replace between the time it reads them and the time it uses them.
- **Fix:** put the host key, the `-D` authorized-keys directory, and the passwd
  file under a directory this user owns and can execute — here the repository's
  own `.dropssh-check/` work dir. Not under `/tmp`, not under a shared path.

### 4.4 Client-side: OpenSSH still needs a passwd entry

- **Symptom:** on a host with no `/etc/passwd`, the local `ssh-keygen` and `ssh`
  cannot map the local uid to a name and fail before the relay is ever reached:
  `No user exists for uid 966` (OpenSSH exit 255).
- **Diagnosis:** unlike the static server `dropbear`, the **client** OpenSSH is
  dynamically linked, so an `LD_PRELOAD` shim *can* interpose it.
- **Fix:** load the release's own `fakepwd.so` (shipped in the same tarball)
  with `LD_PRELOAD=<fakepwd.so>` and `SANDHOME_PASSWD=<workdir>/passwd` for the
  `ssh-keygen` and `ssh` invocations. This is the one place a preload shim is
  the correct tool, and it is deliberately the client, not the server.
- **The first version of the check script missed this.** It only looked for a
  *sandhome-installed* shim (`~/.local/share/sandhome/shims/fakepwd.so`) and
  skipped the client shim entirely when sandhome was absent — which it is on
  this host — so the check died at `No user exists for uid 966` with exit 255.
  The shipped shim lives in the release tarball and exposes the same interface
  (`SANDHOME_PASSWD`), so the fix is to prefer it; the sandhome path stays as a
  fallback. This is the **fifth** thing that had to change, found by running the
  check rather than reading it.

## 5. Credentials and the trust model

`dropssh pair` calls the relay's self-service rendezvous (`POST /v1/pair`) and
returns a random **128-bit name**, a `node_token`, a `connect_token`, and a
`stop_token`, all expiring within **72 hours**. The relay's own documentation
states the model plainly: **the relay authenticates tokens, not people**, and
the connect token has to reach the operator over a channel the operator trusts
(trust-on-first-use).

That makes both tokens bearer credentials, so:

- **No token is committed to this repository.** The check script mints a fresh
  pair on every run, writes `pair.txt` mode `600` inside the work directory,
  and never echoes the tokens; `serve.log` is printed with 64-hex runs replaced
  by `<TOK>` before it is shown.
- The only key material that is generated is a *public* operator key
  (`ak/id` / `ak/authorized_keys`), which stays in the work directory.
- The work directory (`.dropssh-check/`) is gitignored, so dropping it rotates
  the tokens.

## 6. Operational guards

These are not correctness fixes; they stop the check from hanging or leaving a
node behind:

- `--once` on `dropssh serve` serves exactly one session.
- `--retry-budget 3` bounds the relay reconnect loop.
- `timeout 45` wraps the client `ssh`, because a `ProxyCommand` whose pair never
  completes would otherwise wait forever.
- The script kills the serve process after the attempt, so nothing is left
  listening or dialing.
- `umask 077` for the whole work directory; `chmod 600` on `authorized_keys`.

## 7. Measured result

Two runs on 2026-10-02, both `sh tools/ssh-relay-check.sh` and a compound
remote shell. First, the check itself:

```
relay=tcp.ssh.relay.ajam.dev name=p-99e03c... login=966
ssh_exit=0 marker=MARK:966:Linux
dropssh: registered with tcp.ssh.relay.ajam.dev as p-99e03c... (path /v1/node/...)
dropssh: relay hello: maxFrameBytes=65536 maxSessions=64
dropssh: operator opened session 4f606bce (ready sent)
[451] Child connection from unix:0
[451] Pubkey auth succeeded for '966' with ssh-ed25519 key SHA256:eYhfcUTt... from unix:0
[451] Exit (966) from <unix:0>: Exited normally
PASS: a real ssh login ran over the outbound-only relay
```

Second, a single session running a compound command, to show it is a shell and
not one `printf`. Everything below came back over the relay:

```
whoami=966
id=uid=966 gid=965 groups=965
kernel=Linux 7.2.2-artix1-1.1 x86_64
home=/state/home
cwd=/state/home
repo=LICENSE NOTICE README.md data docs research sources tests tools
hostname=sandbox
```

The server logged `Pubkey auth succeeded for '966' with ssh-ed25519 key ...` and
`Exit (966) ...: Exited normally` on both. `ssh_exit=0` both times. The remote
side ran `id`, `uname -srm`, expanded `$HOME`/`pwd`, listed the repository, and
read the kernel hostname — over a connection this host only ever dialed out of.
The bearer name and tokens are redacted here and are not committed.

## 8. What this does not establish

- **Not privacy and not durability.** The pair is a bearer credential for at
  most 72 h; anyone who reads the name and tokens can open a session, and the
  relay sees the plaintext SSH stream it carries.
- **Not a listener.** The check serves one session and exits; it does not leave
  a node dialing or a port open, and it proves nothing about running a
  long-lived node.
- **Only the reverse node path was driven from this host.** The relay's forward
  path (`--mint`) and the public gateways it fronts (for example
  `ssh railway.new`) were not exercised here.
- **The three failure modes above are the ones this host produced.** A
  different sandbox — one with a dynamic `dropbear`, a writable-by-user `/tmp`,
  or a real `/etc/passwd` — would fail differently, and possibly not at all.

## 9. Reproduce

```sh
sh tools/ssh-relay-check.sh
```

It downloads the pinned release and verifies its checksum, generates a host key
and an operator key, writes a passwd entry for the current uid, serves one
session, and connects through the relay with
`ssh -o ProxyCommand="dropssh connect ..."`. **Exit 0 means a real login ran.**
It does not need `sandhome`; where the client cannot map the local uid, it loads
the `sandhome` `fakepwd.so` shim if one is present.
