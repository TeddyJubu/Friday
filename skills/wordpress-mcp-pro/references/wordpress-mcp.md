# WordPress MCP (Model Context Protocol) reference

## Choose your MCP route

### A) WordPress.com (built-in MCP server)
- Server URL: `https://public-api.wordpress.com/wpcom/v2/mcp/v1`
- Auth: OAuth in the client (browser-based)
- Requirements: WordPress.com account + paid plan + MCP enabled on the account

Typical clients:
- Claude Desktop: add a custom connector with the URL above.
- ChatGPT: create an MCP app (Developer Mode) using the same URL.
- VS Code / Cursor: add MCP server using the same URL.

### B) Self-hosted WordPress (WordPress.org)
Recommended: use the official **mcp-adapter** project (canonical).
- Repo: https://github.com/WordPress/mcp-adapter
- Concept: exposes WordPress “Abilities API” as MCP tools/resources/prompts.

Legacy/archived option: `Automattic/wordpress-mcp` (use mainly for historical reference)
- Repo: https://github.com/Automattic/wordpress-mcp

## Self-hosted: common connection patterns

### 1) HTTP (direct) to WordPress MCP endpoint
When the plugin exposes an HTTP/streamable MCP endpoint, clients that support HTTP MCP servers can connect directly.

Example (VS Code-style config pattern):
- URL: `https://YOUR_SITE/wp-json/.../streamable`
- Header: `Authorization: Bearer <JWT>` (if using JWT)

(Exact endpoint path depends on the plugin/version; confirm in the plugin docs you installed.)

### 2) Proxy/bridge using `mcp-wordpress-remote` (Node)
Common when your MCP client expects stdio, or you want a local process to handle auth.

Example Claude Desktop config pattern:
```json
{
  "mcpServers": {
    "wordpress-mcp": {
      "command": "npx",
      "args": ["-y", "@automattic/mcp-wordpress-remote@latest"],
      "env": {
        "WP_API_URL": "https://your-site.com/",
        "JWT_TOKEN": "<your-jwt-token>"
      }
    }
  }
}
```

## Security / risk-reduction checklist
- Prefer least-privilege WordPress users/roles for the tasks you want the agent to do.
- Use short-lived JWT tokens where possible.
- Log actions (server-side) so you can audit changes.
- Avoid giving “administrator” unless absolutely required.
- Don’t expose MCP endpoints publicly without auth + TLS.

## Troubleshooting quick hits
- 401/403: role/permissions too low, token expired, wrong header name, wrong endpoint path.
- Tool list empty: Abilities API not active, MCP adapter not registered, or transport disabled.
- CORS/client issues: prefer proxy/stdio mode if the client is finicky.
