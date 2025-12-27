#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$ROOT_DIR"

# Construit l'artefact pour GitHub Releases (versionné)
mkdir -p dist

VERSION="$(cat VERSION | tr -d '[:space:]')"
if [[ -z "${VERSION}" ]]; then
  echo "ERROR: VERSION est vide." >&2
  exit 1
fi

OUT_FILE="dist/Syntax-Polish-v${VERSION}.alfredworkflow"
rm -f "$OUT_FILE"

(cd workflow && zip -qr "../$OUT_FILE" .)

echo "OK: $OUT_FILE"


