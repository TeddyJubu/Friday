#!/bin/bash
# woo-products.sh - List WooCommerce products
# Usage: woo-products.sh [--json] [--limit=N]

set -euo pipefail

WP_PATH="domains/uniquecollectionbyprincess.com/public_html"
FORMAT="table"
LIMIT=50

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

ssh molybot-woo "wp --path=$WP_PATH --user=1 wc product list --per_page=$LIMIT --format=$FORMAT"
