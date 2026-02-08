#!/bin/bash
# woo-exec.sh - Execute WP-CLI commands on WooCommerce site
# Usage: woo-exec.sh <wp-cli-command>
# Example: woo-exec.sh wc order list --format=json

set -euo pipefail

WP_PATH="domains/uniquecollectionbyprincess.com/public_html"

if [ $# -eq 0 ]; then
    echo "Usage: $0 <wp-cli-command>"
    echo "Example: $0 wc order list --format=json"
    exit 1
fi

ssh molybot-woo "wp --path=$WP_PATH --user=1 $*"
