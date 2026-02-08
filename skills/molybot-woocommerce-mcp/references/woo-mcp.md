# WooCommerce MCP reference (developer preview)

## Enable feature flag

Programmatic:
```php
add_filter( 'woocommerce_features', function( $features ) {
  $features['mcp_integration'] = true;
  return $features;
});
```

CLI:
```bash
wp option update woocommerce_feature_mcp_integration_enabled yes
```

## Endpoint + auth
- Endpoint: `https://yourstore.com/wp-json/woocommerce/mcp`
- Header: `X-MCP-API-Key: <consumer_key>:<consumer_secret>`
- HTTPS required by default (`woocommerce_mcp_allow_insecure_transport` only for local dev)

## Built-in abilities (preview)
From WooCommerce AbilitiesRestBridge:
- `woocommerce/products-list`
- `woocommerce/products-get`
- `woocommerce/products-create`
- `woocommerce/products-update`
- `woocommerce/products-delete`
- `woocommerce/orders-list`
- `woocommerce/orders-get`
- `woocommerce/orders-create`
- `woocommerce/orders-update`

## Permission mapping
Based on Woo API key permission:
- `read` → GET/HEAD
- `write` → POST/PUT/PATCH/DELETE
- `read_write` → all

## Notes
- Developer preview: contracts may change.
- Order/customer data can include PII; apply least privilege and key rotation.
