#!/bin/sh
# Fetch the third-party corpus this repository cites, at the pinned commit.
#
# The battleships project (ariana-dot-dev/battleships) publishes no licence,
# so its cards and pricing engine are deliberately NOT committed here. This
# script reconstructs them locally so every derived number can be re-computed.
#
# Usage: sh tools/fetch-corpus.sh [dest]
set -eu
COMMIT="${BATTLESHIPS_COMMIT:-f6a71ab09fefa68e355ef47c52315e099f99c921}"
DEST="${1:-research/corpus}"
if [ -e "$DEST" ]; then
  echo "$DEST already exists; remove it to re-fetch" >&2
  exit 2
fi
git clone --quiet https://github.com/ariana-dot-dev/battleships.git "$DEST"
git -C "$DEST" checkout --quiet "$COMMIT"
echo "corpus at $DEST"
echo "commit: $(git -C "$DEST" rev-parse --short=12 HEAD)"
echo "cards:  $(find "$DEST/research/cards" -name '*.json' | wc -l)"
