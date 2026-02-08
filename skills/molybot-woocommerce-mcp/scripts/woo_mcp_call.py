#!/usr/bin/env python3
"""Call WooCommerce MCP endpoint via JSON-RPC over HTTP.

Features:
- Handles MCP session lifecycle automatically (initialize + initialized notification)
- Adds required Mcp-Session-Id header for calls
- Optionally normalizes tool names from slash-form to runtime hyphen-form

Auth header required by Woo transport:
X-MCP-API-Key: <consumer_key>:<consumer_secret>
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any

DEFAULT_ENDPOINT = "https://uniquecollectionbyprincess.com/wp-json/woocommerce/mcp"
DEFAULT_PROTOCOL_VERSION = "2025-06-18"


def parse_params(raw: str | None) -> dict[str, Any]:
    if not raw:
        return {}
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid --params JSON: {exc}") from exc
    if not isinstance(parsed, dict):
        raise ValueError("--params must be a JSON object")
    return parsed


def build_api_key(args: argparse.Namespace) -> str | None:
    if args.api_key:
        return args.api_key

    env_key = os.getenv("WOO_MCP_API_KEY") or os.getenv("MCP_API_KEY")
    if env_key:
        return env_key

    ck = args.consumer_key or os.getenv("WOO_MCP_CONSUMER_KEY")
    cs = args.consumer_secret or os.getenv("WOO_MCP_CONSUMER_SECRET")
    if ck and cs:
        return f"{ck}:{cs}"

    return None


def send_json_rpc(
    endpoint: str,
    api_key: str,
    payload: dict[str, Any],
    timeout: int,
    session_id: str | None = None,
) -> tuple[dict[str, Any], dict[str, str]]:
    headers = {
        "Content-Type": "application/json",
        "X-MCP-API-Key": api_key,
    }
    if session_id:
        headers["Mcp-Session-Id"] = session_id

    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(endpoint, data=body, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            if raw.strip():
                parsed = json.loads(raw)
            else:
                parsed = {"jsonrpc": "2.0", "result": None}
            return parsed, dict(resp.headers.items())
    except urllib.error.HTTPError as exc:
        err_body = exc.read().decode("utf-8", errors="replace") if exc.fp else ""
        try:
            parsed = json.loads(err_body)
        except json.JSONDecodeError:
            parsed = {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32000,
                    "message": f"HTTP {exc.code}",
                    "data": err_body,
                },
            }
        return parsed, dict(exc.headers.items())


def delete_session(endpoint: str, api_key: str, session_id: str, timeout: int) -> None:
    headers = {
        "X-MCP-API-Key": api_key,
        "Mcp-Session-Id": session_id,
    }
    req = urllib.request.Request(endpoint, headers=headers, method="DELETE")
    try:
        with urllib.request.urlopen(req, timeout=timeout):
            return
    except Exception:
        return


def normalize_tool_name(name: str) -> str:
    # Woo docs may show slash IDs (woocommerce/products-list),
    # runtime tool names are typically hyphenized (woocommerce-products-list).
    if "/" in name:
        return name.replace("/", "-")
    return name


def main() -> int:
    parser = argparse.ArgumentParser(description="Call WooCommerce MCP endpoint")
    parser.add_argument("--endpoint", default=DEFAULT_ENDPOINT, help="MCP endpoint URL")
    parser.add_argument("--method", required=True, help="JSON-RPC method (e.g. tools/list, tools/call)")
    parser.add_argument("--params", help="JSON object for method params")
    parser.add_argument("--request-id", type=int, default=2, help="JSON-RPC request id (integer recommended)")
    parser.add_argument("--timeout", type=int, default=60, help="HTTP timeout seconds")
    parser.add_argument("--protocol-version", default=DEFAULT_PROTOCOL_VERSION, help="MCP protocol version for initialize")
    parser.add_argument("--no-normalize-tool-name", action="store_true", help="Disable slash->hyphen normalization for tools/call params.name")
    parser.add_argument("--keep-session", action="store_true", help="Keep MCP session open (skip DELETE)")

    # Auth inputs
    parser.add_argument("--api-key", help="Full X-MCP-API-Key value (ck_xxx:cs_xxx)")
    parser.add_argument("--consumer-key", help="Woo consumer key (ck_xxx)")
    parser.add_argument("--consumer-secret", help="Woo consumer secret (cs_xxx)")

    args = parser.parse_args()

    api_key = build_api_key(args)
    if not api_key:
        print(
            json.dumps(
                {
                    "status": "error",
                    "error": "Missing credentials. Set --api-key or WOO_MCP_API_KEY, or provide consumer key/secret.",
                },
                ensure_ascii=False,
            )
        )
        return 2

    try:
        params = parse_params(args.params)
    except ValueError as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False))
        return 2

    # Normalize tool names for convenience
    if args.method == "tools/call" and not args.no_normalize_tool_name:
        name = params.get("name")
        if isinstance(name, str):
            params["name"] = normalize_tool_name(name)

    # 1) initialize session
    init_payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": args.protocol_version,
            "capabilities": {},
            "clientInfo": {"name": "molybot-woo-mcp-call", "version": "1.0"},
        },
    }

    init_response, init_headers = send_json_rpc(
        args.endpoint,
        api_key,
        init_payload,
        timeout=args.timeout,
    )

    session_id = init_headers.get("Mcp-Session-Id") or init_headers.get("mcp-session-id")
    if not session_id:
        print(
            json.dumps(
                {
                    "status": "error",
                    "error": "Failed to obtain MCP session id",
                    "initialize": init_response,
                },
                ensure_ascii=False,
            )
        )
        return 1

    # 2) send initialized notification (best effort)
    notif_payload = {
        "jsonrpc": "2.0",
        "method": "notifications/initialized",
        "params": {},
    }
    send_json_rpc(args.endpoint, api_key, notif_payload, timeout=args.timeout, session_id=session_id)

    # 3) call requested method
    request_payload = {
        "jsonrpc": "2.0",
        "id": args.request_id,
        "method": args.method,
        "params": params,
    }

    response, _headers = send_json_rpc(
        args.endpoint,
        api_key,
        request_payload,
        timeout=args.timeout,
        session_id=session_id,
    )

    if not args.keep_session:
        delete_session(args.endpoint, api_key, session_id, timeout=max(10, args.timeout // 2))

    output = {
        "status": "ok" if "error" not in response else "error",
        "session_id": session_id,
        "request": request_payload,
        "response": response,
    }
    print(json.dumps(output, ensure_ascii=False))
    return 0 if output["status"] == "ok" else 1


if __name__ == "__main__":
    sys.exit(main())
