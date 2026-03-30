#!/usr/bin/env bash
set -euo pipefail

TARGET_HOME="${CLAUDE_HOME:-$HOME/Library/Application Support/Claude}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_SKILL="${SCRIPT_DIR}/skill/txt2epub"
TARGET_ROOT="${TARGET_HOME}/skills"
TARGET_SKILL="${TARGET_ROOT}/txt2epub"

mkdir -p "${TARGET_ROOT}"
rm -rf "${TARGET_SKILL}"
cp -R "${SOURCE_SKILL}" "${TARGET_SKILL}"
echo "Installed txt2epub to ${TARGET_SKILL}"
