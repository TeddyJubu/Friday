---
name: wordpress-mcp-pro
description: Manage WordPress sites and connect AI agents to WordPress via MCP (Model Context Protocol). Use for WordPress setup/admin tasks (plugins/themes/core updates, backups, WP-CLI operations), and for configuring WordPress MCP access for AI clients (WordPress.com MCP server, self-hosted MCP adapter/plugin, client config snippets, auth/risk reduction).
---

# WordPress MCP Pro

Enable reliable WordPress operations (via WP-CLI) and set up **WordPress MCP** so MCP-enabled AI clients can safely read/write WordPress content and settings.

## Quick decision: what are we connecting?

1) **WordPress.com site** → use the built-in MCP server URL (OAuth in client).
- Read: `references/wordpress-mcp.md` (WordPress.com route)

2) **Self-hosted WordPress (WordPress.org)** → install an MCP plugin/adapter, then connect via HTTP or a local proxy.
- Read: `references/wordpress-mcp.md` (self-hosted routes)

## Task A — WordPress ops (fast + safe)

### A1) Install WP-CLI (if needed)
- Run: `scripts/wpcli_install.sh`

### A2) Baseline site health check
Use WP-CLI to gather a quick snapshot before changing anything:
- `wp --info`
- `wp core version`
- `wp plugin list`
- `wp theme list`
- `wp core verify-checksums`

If you need a command cookbook, read: `references/wp-cli.md`.

### A3) Update workflow (risk-reduced)
1) Export DB backup: `wp db export backup.sql`
2) Check core updates: `wp core check-update`
3) Update plugins (one-by-one if risk is high): `wp plugin update <slug>`
4) Update themes: `wp theme update --all`
5) Re-check: `wp plugin list --update=available`

## Task B — Set up MCP for WordPress

### B1) WordPress.com MCP
Use the server URL:
- `https://public-api.wordpress.com/wpcom/v2/mcp/v1`

Then follow your client’s “add MCP server/connector” flow.
Details + role restrictions: `references/wordpress-mcp.md`.

### B2) Self-hosted WordPress MCP (recommended path)
1) Install the official MCP adapter/plugin (canonical project).
2) Decide connection mode:
   - **Direct HTTP MCP** (if your client supports it)
   - **Local proxy (stdio)** using a Node bridge (often easiest)
3) Create least-privilege credentials/tokens for the agent.

Exact config patterns and security checklist: `references/wordpress-mcp.md`.

## Operating principles (don’t skip)
- Prefer **least privilege** (roles/tokens) and **short-lived tokens**.
- Avoid “do everything as admin” unless absolutely required.
- Log/observe changes so you can audit what the agent did.
- For risky operations (updates, deletes, migrations): backup first, change one thing at a time.
