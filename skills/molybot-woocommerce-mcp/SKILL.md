---
name: molybot-woocommerce-mcp
description: Use WooCommerce MCP tools (developer preview) for product and order operations via the /wp-json/woocommerce/mcp endpoint. Use when the user asks to enable/configure WooCommerce MCP, list available MCP tools, or run WooCommerce MCP product/order actions with API-key authentication.
---

# Molybot WooCommerce MCP

Use WooCommerce MCP for tool-based product/order operations.

## Endpoint + auth
- Endpoint: `https://<store>/wp-json/woocommerce/mcp`
- Header: `X-MCP-API-Key: <consumer_key>:<consumer_secret>`
- Feature flag must be enabled: `woocommerce_feature_mcp_integration_enabled = yes`

## Canonical abilities/tools (current preview)
Docs/ability IDs are namespace-style:
- `woocommerce/products-list`
- `woocommerce/products-get`
- `woocommerce/products-create`
- `woocommerce/products-update`
- `woocommerce/products-delete`
- `woocommerce/orders-list`
- `woocommerce/orders-get`
- `woocommerce/orders-create`
- `woocommerce/orders-update`

Runtime `tools/list` names are usually hyphenized:
- `woocommerce-products-list`
- `woocommerce-products-get`
- `woocommerce-products-create`
- `woocommerce-products-update`
- `woocommerce-products-delete`
- `woocommerce-orders-list`
- `woocommerce-orders-get`
- `woocommerce-orders-create`
- `woocommerce-orders-update`

The script auto-normalizes slash names to runtime hyphen names for `tools/call`.

## Script
Primary script:
`/home/ubuntu/clawd/skills/molybot-woocommerce-mcp/scripts/woo_mcp_call.py`

Wrapper:
`/home/ubuntu/clawd/scripts/molybot/woo-mcp-call.sh`

## Quick checks
List MCP tools:
```bash
WOO_MCP_API_KEY='ck_xxx:cs_xxx' \
python3 /home/ubuntu/clawd/skills/molybot-woocommerce-mcp/scripts/woo_mcp_call.py \
  --method tools/list
```

Call a tool (example: products list):
```bash
WOO_MCP_API_KEY='ck_xxx:cs_xxx' \
python3 /home/ubuntu/clawd/skills/molybot-woocommerce-mcp/scripts/woo_mcp_call.py \
  --method tools/call \
  --params '{"name":"woocommerce/products-list","arguments":{"per_page":20}}'
```

## Safety
- Keep API keys in env vars; never hardcode secrets in files.
- For destructive operations (delete, bulk edits), keep two-phase approval.
- Respect Woo permissions (`read`, `write`, `read_write`) and HTTPS requirements.
