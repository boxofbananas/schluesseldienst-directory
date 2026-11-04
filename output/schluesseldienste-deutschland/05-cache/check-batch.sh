#!/bin/sh
# Usage: sh output/schluesseldienste-deutschland/05-cache/check-batch.sh 07
cd "$(dirname "$0")/../../.." || exit 2
B="output/schluesseldienste-deutschland"
python3 scripts/check_city_copy.py --copy "$B/05-cache/city-copy" --batches "$B/05-cache/city-batches" \
  --facts "$B/05-fact-sheet.md" --niche "Schlüsseldienste" --only "batch-$1"
