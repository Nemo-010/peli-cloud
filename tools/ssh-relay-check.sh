#!/bin/sh
# ssh-relay-check.sh - prove a sealed sandbox can be SSH'd into over an
# outbound-only relay, end to end, using dropssh.
#
# Why this exists: the sandbox cannot bind a TCP port (bind(2) INET -> EACCES,
# shown by `sandhome report` as bind=unix) and has no /etc/passwd. dropssh
# carries ssh over an outbound WebSocket and dropbear -Y reads the account from
# a file instead of the system database. This script makes a pair, serves one
# session, connects through the relay and runs a command over that session.
#
# Nothing here is a credential committed to the repository: the pair is minted
# at run time and its tokens are written mode 600 under the work dir and never
# printed. Drop the work dir to rotate them.
#
# Usage: sh tools/ssh-relay-check.sh
# Exit 0 when a real login ran; 1 when any step did not.
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
WORK=${DROPSSH_WORK:-"$ROOT/.dropssh-check"}
DROPSSH_VERSION=v0.2.3
TARBALL="dropssh-x86_64-linux-musl.tar.gz"
URL="https://github.com/talaria0101/dropssh/releases/download/$DROPSSH_VERSION/$TARBALL"
RELAY="${DROPSSH_RELAY:-tcp.ssh.relay.ajam.dev}"

mkdir -p "$WORK"
cd "$WORK"
umask 077

# 1. Fetch the pinned release once. Its own SHA256SUMS is checked against the
#    files it shipped with, so a truncated download fails here and not at login.
if [ ! -x ./dropssh ] || [ ! -x ./dropbear ]; then
  rm -rf unpack && mkdir unpack
  curl -fsSL -o "$TARBALL" "$URL"
  tar -xzf "$TARBALL" -C unpack
  cp unpack/dropssh unpack/dropbear unpack/dropbearkey unpack/fakepwd.so . 2>/dev/null || true
  (cd unpack && sha256sum -c --ignore-missing SHA256SUMS >/dev/null) || { echo "FAIL: release checksum"; exit 1; }
fi

# 2. The passwd entry names THIS uid: dropbear refuses a login whose uid differs
#    from the server's, and a root-only file here logs "wrong user". The home
#    must be owned by the login user, which /tmp is not, so the work dir is not
#    under /tmp.
ME_UID=$(id -u)
ME_GID=$(id -g 2>/dev/null || echo "$ME_UID")
if [ "$ME_UID" = 0 ]; then ME_NAME=root; else
  ME_NAME=$(id -un 2>/dev/null || true)
  case "$ME_NAME" in ''|*[!a-zA-Z0-9._-]*) ME_NAME=user"$ME_UID" ;; esac
fi
ME_HOME=${HOME:-/}
printf '%s:x:%s:%s:test:%s:/bin/sh\n' "$ME_NAME" "$ME_UID" "$ME_GID" "$ME_HOME" > passwd

# 3. Host key in dropbear format, operator key in OpenSSH format. ssh-keygen
#    needs a passwd entry for the client uid; the sandhome fakepwd shim supplies
#    one where /etc/passwd does not exist: the release's own fakepwd.so is
#    preferred (so no sandhome install is needed), the sandhome shim kept as a
#    fallback.
CLIENT_SHIM=""
for s in "$WORK/fakepwd.so" /state/home/.local/share/sandhome/shims/fakepwd.so "$HOME"/.local/share/sandhome/shims/fakepwd.so; do
  [ -r "$s" ] && { CLIENT_SHIM="$s"; break; }
done
rm -f hostkey ak/id ak/id.pub
mkdir -p ak
./dropbearkey -t ed25519 -f hostkey >/dev/null 2>&1
if [ -n "$CLIENT_SHIM" ]; then
  SANDHOME_PASSWD="$WORK/passwd" LD_PRELOAD="$CLIENT_SHIM" \
    ssh-keygen -q -t ed25519 -N '' -f ak/id
else
  ssh-keygen -q -t ed25519 -N '' -f ak/id
fi
cp ak/id.pub ak/authorized_keys
chmod 600 ak/authorized_keys

# 4. A self-service reverse pair. node_token stays here; connect_token is what
#    an operator would be handed. Neither is echoed.
./dropssh pair --relay "$RELAY" > pair.txt 2> pair.err || { echo "FAIL: pair"; cat pair.err; exit 1; }
NAME=$(awk '/^name /{print $2}' pair.txt)
NODE=$(awk '/^node /{print $5}' pair.txt)
CONN=$(awk '/^connect /{print $5}' pair.txt)
[ -n "$NAME" ] && [ -n "$NODE" ] && [ -n "$CONN" ] || { echo "FAIL: pair shape"; exit 1; }

# 5. Serve exactly one session. -Y is the file passwd database; without it the
#    server logs "Login attempt with wrong user".
./dropssh serve --relay "$RELAY" --name "$NAME" --token "$NODE" \
  --server "./dropbear -i -E -F -r $WORK/hostkey -D $WORK/ak -Y $WORK/passwd" \
  --once --retry-budget 3 --json --verbose >serve.out 2>serve.log < /dev/null &
SERVE_PID=$!
sleep 3

# 6. Connect through the relay and run a command on the far side. `timeout`
#    around ssh because a ProxyCommand that never pairs would otherwise wait.
set +e
if [ -n "$CLIENT_SHIM" ]; then
  MARK=$(SANDHOME_PASSWD="$WORK/passwd" LD_PRELOAD="$CLIENT_SHIM" \
    timeout 45 ssh -o "ProxyCommand=$WORK/dropssh connect --relay $RELAY --name $NAME --token $CONN" \
        -i "$WORK/ak/id" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
        -o BatchMode=yes -o ConnectTimeout=20 \
        "$ME_NAME@$NAME" 'printf "MARK:%s:%s" "$(id -u)" "$(uname -s)"' 2>/dev/null)
else
  MARK=$(timeout 45 ssh -o "ProxyCommand=$WORK/dropssh connect --relay $RELAY --name $NAME --token $CONN" \
        -i "$WORK/ak/id" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
        -o BatchMode=yes -o ConnectTimeout=20 \
        "$ME_NAME@$NAME" 'printf "MARK:%s:%s" "$(id -u)" "$(uname -s)"' 2>/dev/null)
fi
RC=$?
set -e
kill "$SERVE_PID" 2>/dev/null || true

echo "relay=$RELAY name=$NAME login=$ME_NAME"
echo "ssh_exit=$RC marker=$MARK"
echo "--- serve.log (tokens redacted) ---"
sed -E 's/[0-9a-f]{64}/<TOK>/g' serve.log 2>/dev/null | tail -8

case "$MARK" in
  "MARK:$ME_UID:"*) echo "PASS: a real ssh login ran over the outbound-only relay"; exit 0 ;;
  *) echo "FAIL: no login over the relay"; exit 1 ;;
esac
