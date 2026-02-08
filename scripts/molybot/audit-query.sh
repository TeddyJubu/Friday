#!/bin/bash
# audit-query.sh - Query structured audit log
# Usage: audit-query.sh [--last=N] [--action=X] [--requester=X] [--failed]

set -euo pipefail

AUDIT_FILE="/home/ubuntu/clawd/memory/molybot-audit.jsonl"

if [ ! -f "$AUDIT_FILE" ]; then
    echo "No audit log found at $AUDIT_FILE"
    exit 1
fi

LAST=10
ACTION_FILTER=""
REQ_FILTER=""
FAILED_ONLY=false

for arg in "$@"; do
    case $arg in
        --last=*)
            LAST="${arg#*=}"
            ;;
        --action=*)
            ACTION_FILTER="${arg#*=}"
            ;;
        --requester=*)
            REQ_FILTER="${arg#*=}"
            ;;
        --failed)
            FAILED_ONLY=true
            ;;
    esac
done

# Build jq filter
JQ_FILTER="."

if [ -n "$ACTION_FILTER" ]; then
    JQ_FILTER="$JQ_FILTER | select(.action | contains(\"$ACTION_FILTER\"))"
fi

if [ -n "$REQ_FILTER" ]; then
    JQ_FILTER="$JQ_FILTER | select(.req | contains(\"$REQ_FILTER\"))"
fi

if [ "$FAILED_ONLY" = true ]; then
    JQ_FILTER="$JQ_FILTER | select(.ok == false)"
fi

tail -n "$LAST" "$AUDIT_FILE" | jq -c "$JQ_FILTER" 2>/dev/null || tail -n "$LAST" "$AUDIT_FILE"
