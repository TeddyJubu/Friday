#!/bin/bash
# woo-order-get.sh - Get order details
# Usage: woo-order-get.sh <order_id>

set -euo pipefail

WP_PATH="domains/uniquecollectionbyprincess.com/public_html"

if [ $# -eq 0 ]; then
    echo "Usage: $0 <order_id>"
    exit 1
fi

ORDER_ID="$1"

ssh molybot-woo "wp --path=$WP_PATH --user=1 wc shop_order get $ORDER_ID --format=json"
