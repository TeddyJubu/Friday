---
name: agent-browser
description: Use the agent-browser CLI (vercel-labs/agent-browser) for headless browser automation when the built-in browser tool is unavailable or blocked. Supports open/navigate, snapshot (accessibility tree refs), click/fill/type/press, get text/html/value/url/title, screenshots, and PDF. Use for logging into web apps, administering dashboards (e.g., WordPress wp-admin), and automating browser flows via CLI.
---

# agent-browser (headless browser)

Use `agent-browser` as the default browser automation path in this environment.

## Quick start workflow (recommended)
1) Open the page:
- `agent-browser open <url>`

2) Get a ref-based accessibility tree:
- `agent-browser snapshot`

3) Act using refs from snapshot (preferred):
- `agent-browser click @e2`
- `agent-browser fill @e3 "text"`
- `agent-browser press Enter`

4) Verify:
- `agent-browser get url`
- `agent-browser get title`
- `agent-browser get text @eX`

5) Capture evidence:
- `agent-browser screenshot /tmp/page.png` (add `--full` if needed)

6) Close:
- `agent-browser close`

## Practical patterns

### Login flows
- Prefer `fill` (clears first) for inputs.
- Use `press Tab` to move between fields when selectors are annoying.
- After submit, always `get url` + `screenshot` to confirm success.

### WordPress wp-admin
- Open `/wp-admin/`
- Snapshot → find Username/Password fields → fill → click Log In
- After login: verify by `get url` contains `/wp-admin/` and take a screenshot.

### If selectors/refs are unstable
- Try role-based find via `agent-browser find role ...` (see upstream docs)
- Or fallback to CSS selectors for unique IDs (e.g. `#user_login`).

## Setup / troubleshooting
- If Chromium won’t launch on Linux, run:
  - `agent-browser install --with-deps`
- If it complains about missing browsers, run:
  - `agent-browser install`

## Safety
- Don’t paste credentials into logs or files.
- Prefer temporary accounts; revoke/delete access after the task.
