#!/bin/sh
# Fetch the first-party pages cited in research/verification, so the quotes
# there can be re-checked. Raw HTML is not committed (third-party material);
# this script and MANIFEST.tsv are. Usage: sh tools/fetch-sources.sh [dir]
set -eu
DEST="${1:-sources/$(date +%F)}"
mkdir -p "$DEST"
fetch() {
  id="$1"; url="$2"
  code=$(curl -sL --max-time 60 \
    -A "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36" \
    -w "%{http_code}" -o "$DEST/$id.html" "$url")
  printf '%s\t%s\t%s\t%s\t%s\n' "$id" "$url" "$code" "$(wc -c < "$DEST/$id.html")" "$(sha256sum "$DEST/$id.html" | cut -d' ' -f1)"
}
{
  printf 'id\turl\thttp\tbytes\tsha256\n'
  fetch scaleway           "https://www.scaleway.com/en/pricing/virtual-instances/"
  fetch netcup             "https://www.netcup.com/en/server/vps"
  fetch netcup-vps-lite    "https://www.netcup.com/en/server/vps-lite"
  fetch agent-37           "https://www.agent37.com/pricing"
  fetch hetzner-cloud      "https://www.hetzner.com/cloud/"
  fetch contabo            "https://contabo.com/en-us/pricing/"
  fetch boat               "https://docs.boat.dev/pricing"
  fetch lizard             "https://lizard.build/pricing"
  fetch freestyle          "https://www.freestyle.sh/pricing"
  fetch zipbox             "https://zipbox.ai/pricing"
  fetch upstash-box        "https://upstash.com/pricing/box"
  fetch upcloud            "https://upcloud.com/pricing/"
  fetch oracle-cloud       "https://www.oracle.com/cloud/compute/pricing/"
} > "$DEST/MANIFEST.tsv"
echo "wrote $DEST/MANIFEST.tsv"
cat "$DEST/MANIFEST.tsv"
