#!/bin/sh
# Usage: sh output/schluesseldienste-deutschland/03-cache/check-batch.sh 007
cd "$(dirname "$0")/../../.." || exit 2
B="output/schluesseldienste-deutschland"
python3 scripts/merge_enriched.py "$B/02-listings-clean.csv" --attributes "$B/03-attributes.json" \
  --patterns "$B/03-attributes.json" --evidence "$B/03-cache/evidence" --enriched "$B/03-cache/enriched" \
  --out "$B/03-listings-enriched.csv" --only "$B/03-cache/enriched/batch-$1.json" --slugs "$B/03-cache/batches/batch-$1.slugs.json"
