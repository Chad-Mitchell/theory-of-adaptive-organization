#!/usr/bin/env bash
# Fetch the Valiev et al. 2018 minimal frame (Zenodo 1297925) into data/.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p data
# Recorded source: https://zenodo.org/records/1297925
# Direct file URL pattern on Zenodo (dataset_minimal_Jan_2018.zip):
URL="${VALIEV_ZIP_URL:-https://zenodo.org/records/1297925/files/dataset_minimal_Jan_2018.zip?download=1}"
echo "Downloading $URL"
curl -L --fail -o data/valiev_min.zip "$URL"
unzip -l data/valiev_min.zip
echo "Extract the package_urls.csv member into data/package_urls.csv (name inside the zip may vary; inspect the listing)."
