#!/bin/bash
# audit-log.sh - Append structured audit entry (JSON Lines format)
# Usage: audit-log.sh <requester> <site> <action> <command> <ok|fail> [duration_ms]
# Example: audit-log.sh "+8801714469527" "uniquecollection" "order.list" "wc order list" "ok" 1234

set -euo pipefail

AUDIT_DIR="/home/ubuntu/clawd/memory"
AUDIT_FILE="$AUDIT_DIR/molybot-audit.jsonl"

REQUESTER="${1:-unknown}"
SITE="${2:-unknown}"
ACTION="${3:-unknown}"
CMD="${4:-}"
STATUS="${5:-ok}"
DURATION="${6:-0}"

TS=$(date +%s)
ISO_TS=$(date -Iseconds)

# Create JSON entry
JSON=$(cat <<EOF
{"ts":$TS,"iso":"$ISO_TS","req":"$REQUESTER","site":"$SITE","action":"$ACTION","cmd":"$CMD","ok":$([ "$STATUS" = "ok" ] && echo "true" || echo "false"),"dur_ms":$DURATION}
EOF
)

echo "$JSON" >> "$AUDIT_FILE"
echo "Logged: $ACTION ($STATUS)"
