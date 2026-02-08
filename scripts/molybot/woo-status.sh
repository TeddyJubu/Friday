#!/bin/bash
# woo-status.sh - Quick health check for Molybot
# Usage: woo-status.sh

set -euo pipefail

WP_PATH="domains/uniquecollectionbyprincess.com/public_html"
AUDIT_FILE="/home/ubuntu/clawd/memory/molybot-audit-$(date +%Y-%m).md"

echo "=== Molybot Status Check ==="
echo ""

# SSH connectivity
echo -n "SSH Connection: "
if ssh -o ConnectTimeout=5 molybot-woo "echo OK" 2>/dev/null; then
    echo ""
else
    echo "FAILED"
    exit 1
fi

# WP-CLI version
echo -n "WP-CLI Version: "
ssh molybot-woo "wp --path=$WP_PATH --version"

# WordPress version
echo -n "WordPress Version: "
ssh molybot-woo "wp --path=$WP_PATH core version"

# WooCommerce version
echo -n "WooCommerce Version: "
ssh molybot-woo "wp --path=$WP_PATH plugin get woocommerce --field=version 2>/dev/null || echo 'Unknown'"

# Recent orders count
echo -n "Orders (last 24h): "
ssh molybot-woo "wp --path=$WP_PATH wc order list --after=$(date -d '24 hours ago' -Iseconds 2>/dev/null || date -v-1d +%Y-%m-%dT%H:%M:%S) --format=count 2>/dev/null || echo 'N/A'"

# Last audit entry
echo ""
echo "Last Audit Entry:"
if [ -f "$AUDIT_FILE" ]; then
    tail -1 "$AUDIT_FILE"
else
    echo "No audit file for this month"
fi

echo ""
echo "=== Status Check Complete ==="
