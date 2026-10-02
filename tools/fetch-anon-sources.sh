#!/bin/sh
# Fetch the first-party pages cited in docs/ANONYMOUS-VMS.md, at one moment,
# so every quote there can be re-checked. Raw HTML is not committed
# (third-party material); this script and the MANIFEST.tsv it writes are.
#
# Usage: sh tools/fetch-anon-sources.sh [dir]
set -eu
DEST="${1:-sources/anon-$(date +%F)}"
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
  # anonymous, no account
  fetch railway-free-vm        "https://railway.com/free-vm"
  # free with an account, SSH-capable
  fetch gh-codespaces          "https://docs.github.com/en/billing/concepts/product-billing/github-codespaces"
  fetch gh-codespaces-feat     "https://github.com/features/codespaces"
  fetch gh-codespaces-cli      "https://docs.github.com/en/codespaces/developing-in-a-codespace/using-github-codespaces-with-github-cli"
  fetch gcloud-shell-limits    "https://cloud.google.com/shell/docs/limitations"
  fetch aws-cloudshell         "https://aws.amazon.com/cloudshell/"
  fetch azure-cloudshell-learn "https://learn.microsoft.com/en-us/azure/cloud-shell/overview"
  fetch sdf-home               "https://sdf.org/"
  fetch sdf-signup             "https://sdf.org/?signup"
  fetch hashbang               "https://hashbang.sh/"
  fetch tildeclub-wiki         "https://tilde.club/wiki/"
  fetch tildetown              "https://tilde.town/"
  fetch alwaysdata             "https://www.alwaysdata.com/en/pricing/"
  fetch alwaysdata-ssh         "https://help.alwaysdata.com/en/docs/web-hosting/remote-access/ssh/"
  # free tier with a card
  fetch gcp-free-features      "https://cloud.google.com/free/docs/free-cloud-features"
  fetch aws-free               "https://aws.amazon.com/free/"
  fetch azure-free             "https://azure.microsoft.com/en-us/free/"
  fetch oracle-free            "https://www.oracle.com/cloud/free/"
  # free compute that is not an SSH machine, and products that changed or died
  fetch play-with-docker       "https://labs.play-with-docker.com/"
  fetch killercoda             "https://killercoda.com/"
  fetch fly-pricing            "https://fly.io/docs/about/pricing/"
  fetch koyeb-pricing          "https://www.koyeb.com/pricing"
  fetch render-pricing         "https://render.com/pricing"
  fetch northflank-pricing     "https://northflank.com/pricing"
  fetch modal-pricing          "https://modal.com/pricing"
  fetch hf-pricing             "https://huggingface.co/pricing"
  fetch lightning-pricing      "https://lightning.ai/pricing"
} > "$DEST/MANIFEST.tsv"
echo "wrote $DEST/MANIFEST.tsv"
cat "$DEST/MANIFEST.tsv"
