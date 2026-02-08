#!/bin/bash
# woo-mcp-call.sh - Wrapper for WooCommerce MCP JSON-RPC calls
# Usage examples:
#   WOO_MCP_API_KEY='ck_xxx:cs_xxx' woo-mcp-call.sh --method tools/list
#   WOO_MCP_API_KEY='ck:cs' woo-mcp-call.sh --method tools/call --params '{"name":"woocommerce/products-list","arguments":{"per_page":10}}'

set -euo pipefail

SCRIPT="/home/ubuntu/clawd/skills/molybot-woocommerce-mcp/scripts/woo_mcp_call.py"
python3 "$SCRIPT" "$@"
