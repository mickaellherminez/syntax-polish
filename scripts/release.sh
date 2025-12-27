#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

usage() {
  cat <<'EOF'
Usage:
  bash scripts/release.sh --bump {patch|minor|major}
  bash scripts/release.sh --set X.Y.Z

Ce script :
- met à jour VERSION + workflow/info.plist (clé: version)
- met à jour CHANGELOG.md (ajoute une section TODO)
- génère dist/Syntax-Polish-vX.Y.Z.alfredworkflow
- génère dist/SHA256SUMS.txt

Ensuite, crée un tag Git vX.Y.Z et une GitHub Release manuellement (recommandé).
EOF
}

if [[ $# -lt 2 ]]; then
  usage
  exit 1
fi

if [[ "${1}" == "--bump" ]]; then
  version="$(python3 scripts/bump_version.py --bump "${2}")"
elif [[ "${1}" == "--set" ]]; then
  version="$(python3 scripts/bump_version.py --set "${2}")"
else
  usage
  exit 1
fi

echo "Version: ${version}"

bash scripts/build_workflow.sh

pushd dist >/dev/null
shasum -a 256 *.alfredworkflow > SHA256SUMS.txt
popd >/dev/null

echo "OK: dist/SHA256SUMS.txt"
echo "À faire ensuite :"
echo "  - git commit -am \"chore: release v${version}\""
echo "  - git tag \"v${version}\""
echo "  - GitHub Release v${version} (upload: dist/Syntax-Polish-v${version}.alfredworkflow + dist/SHA256SUMS.txt)"


