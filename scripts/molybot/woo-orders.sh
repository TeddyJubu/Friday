#!/bin/bash
# woo-orders.sh - List recent WooCommerce orders
# Usage: woo-orders.sh [--json] [--limit=N]

set -euo pipefail

WP_PATH="domains/uniquecollectionbyprincess.com/public_html"
FORMAT="table"
LIMIT=20

for arg in "$@"; do
    case $arg in
        --json)
            FORMAT="json"
            ;;
        --limit=*)
            LIMIT="${arg#*=}"
            ;;
    esac
done

ssh molybot-woo "wp --path=$WP_PATH --user=1 wc shop_order list --per_page=$LIMIT --format=$FORMAT"
