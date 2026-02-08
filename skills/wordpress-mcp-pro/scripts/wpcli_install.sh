#!/usr/bin/env bash
set -euo pipefail

# Install WP-CLI in a conservative, reversible way.
# - On macOS: uses Homebrew if available.
# - On Linux: downloads wp-cli.phar to /usr/local/bin/wp.

if command -v wp >/dev/null 2>&1; then
  echo "wp-cli already installed: $(wp --version)"
  exit 0
fi

UNAME="$(uname -s | tr '[:upper:]' '[:lower:]')"

if [[ "$UNAME" == "darwin" ]]; then
  if command -v brew >/dev/null 2>&1; then
    brew install wp-cli
    echo "Installed wp-cli via brew: $(wp --version)"
  else
    echo "Homebrew not found. Install brew first or install wp-cli manually." >&2
    exit 1
  fi
else
  TMPDIR="$(mktemp -d)"
  trap 'rm -rf "$TMPDIR"' EXIT

  curl -L -o "$TMPDIR/wp" https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
  php "$TMPDIR/wp" --info >/dev/null

  chmod +x "$TMPDIR/wp"
  sudo mv "$TMPDIR/wp" /usr/local/bin/wp

  echo "Installed wp-cli: $(wp --version)"
fi
