#!/bin/bash
# woo-product-get.sh - Get product details
# Usage: woo-product-get.sh <product_id>

set -euo pipefail

WP_PATH="domains/uniquecollectionbyprincess.com/public_html"

if [ $# -eq 0 ]; then
    echo "Usage: $0 <product_id>"
    exit 1
fi

PRODUCT_ID="$1"

ssh molybot-woo "wp --path=$WP_PATH --user=1 wc product get $PRODUCT_ID --format=json"
