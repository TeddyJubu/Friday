#!/usr/bin/env python3
"""Perplexity Chat Completions helper (OpenAI-compatible).

Uses Perplexity's OpenAI-compatible chat completions API with Sonar models.
- Base URL: https://api.perplexity.ai/v2
- Env: PERPLEXITY_API_KEY

Prints: answer text + citations (if present)

Usage:
  python3 perplexity_chat.py "your question" --model sonar-pro --recency month

"""

import argparse
import json
import os
import sys
from typing import Any, Dict, List

import requests

BASE_URL = "https://api.perplexity.ai/v2"


def call_chat(prompt: str, model: str, recency: str | None = None, domains: List[str] | None = None, temperature: float | None = None) -> Dict[str, Any]:
    api_key = os.environ.get("PERPLEXITY_API_KEY")
    if not api_key:
        raise SystemExit("Missing PERPLEXITY_API_KEY env var")

    body: Dict[str, Any] = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
    }
    # Perplexity-specific parameters (OpenAI-compatible via extra fields)
    if recency:
        body["search_recency_filter"] = recency
    if domains:
        body["search_domain_filter"] = domains
    if temperature is not None:
        body["temperature"] = temperature

    r = requests.post(
        f"{BASE_URL}/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        data=json.dumps(body),
        timeout=120,
    )
    r.raise_for_status()
    return r.json()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt")
    ap.add_argument("--model", default="sonar-pro")
    ap.add_argument("--recency", default=None, help="day|week|month|year (as supported)")
    ap.add_argument("--domain", action="append", default=None, help="repeat for multiple")
    ap.add_argument("--temperature", type=float, default=None)
    ap.add_argument("--json", action="store_true", help="print full JSON")
    args = ap.parse_args()

    data = call_chat(args.prompt, args.model, args.recency, args.domain, args.temperature)

    if args.json:
        print(json.dumps(data, indent=2))
        return

    # OpenAI-style
    text = None
    try:
        text = data["choices"][0]["message"]["content"]
    except Exception:
        pass
    if text:
        print(text)
    else:
        print(json.dumps(data, indent=2))

    cites = data.get("citations")
    if cites:
        print("\nSOURCES:")
        for u in cites:
            print(f"- {u}")


if __name__ == "__main__":
    try:
        main()
    except requests.HTTPError as e:
        sys.stderr.write(f"HTTP error: {e}\n")
        sys.stderr.write(getattr(e.response, "text", "") + "\n")
        raise
