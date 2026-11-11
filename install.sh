#!/usr/bin/env bash
set -euo pipefail

TARGET="${CODEX_HOME:-$HOME/.codex}/skills/pedaily-financing-weekly"
mkdir -p "$(dirname "$TARGET")"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

if command -v curl >/dev/null 2>&1; then
  curl -fsSL "https://github.com/zhichunyang/pedaily-financing-weekly/archive/refs/heads/main.tar.gz" -o "$TMP_DIR/skill.tar.gz"
else
  echo "curl is required" >&2
  exit 1
fi

tar -xzf "$TMP_DIR/skill.tar.gz" -C "$TMP_DIR"
rm -rf "$TARGET"
cp -R "$TMP_DIR/pedaily-financing-weekly-main/pedaily-financing-weekly" "$TARGET"
echo "Installed to: $TARGET"
