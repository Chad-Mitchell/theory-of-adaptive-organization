#!/usr/bin/env bash
# Download SEC companyfacts and submissions bulk zips into raw/, then check hashes.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p raw
UA="${SEC_USER_AGENT:-GTAO research research@example.invalid}"
download() {
  local url="$1" dest="$2"
  echo "GET $url -> $dest"
  curl -L --fail -A "$UA" -o "$dest" "$url"
}
download "https://www.sec.gov/files/companyfacts.zip" raw/companyfacts.zip
download "https://www.sec.gov/files/submissions.zip" raw/submissions.zip
echo "Checking sha256 against raw/*.sha256 (the original run's hashes):"
# The archived hashes may not match a later SEC snapshot. Report both.
(cd raw && sha256sum companyfacts.zip submissions.zip)
echo "Original run:"
cat raw/companyfacts.sha256 raw/submissions.sha256
