#!/usr/bin/env python3
"""Perplexity Agentic Research helper (OpenAI Responses-compatible).

Uses Perplexity's OpenAI-compatible Responses API.
- Base URL: https://api.perplexity.ai/v2
- Env: PERPLEXITY_API_KEY

Prints: output_text and (if available) citations from annotations.

Usage:
  python3 perplexity_research.py "question" --model openai/gpt-5-mini
  python3 perplexity_research.py "question" --preset pro-search

"""

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, List, Set

import requests

BASE_URL = "https://api.perplexity.ai/v2"


def extract_citations(resp: Dict[str, Any]) -> List[str]:
    urls: Set[str] = set()

    # Common shapes: output -> message -> content -> annotations -> citation
    output = resp.get("output") or []
    for item in output:
        if item.get("type") != "message":
            continue
        for content in item.get("content") or []:
            for ann in content.get("annotations") or []:
                u = ann.get("url")
                if isinstance(u, str) and u.startswith("http"):
                    urls.add(u)

    # Fallback: regex scan over JSON
    blob = json.dumps(resp)
    for u in re.findall(r"https?://[^\"\s]+", blob):
        if "perplexity.ai" not in u:
            urls.add(u)

    return sorted(urls)


def call_responses(prompt: str, model: str | None, preset: str | None, temperature: float | None = None) -> Dict[str, Any]:
    api_key = os.environ.get("PERPLEXITY_API_KEY")
    if not api_key:
        raise SystemExit("Missing PERPLEXITY_API_KEY env var")

    body: Dict[str, Any] = {
        "input": prompt,
    }
    if preset:
        body["preset"] = preset
    if model:
        body["model"] = model
    if temperature is not None:
        body["temperature"] = temperature

    r = requests.post(
        f"{BASE_URL}/responses",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        data=json.dumps(body),
        timeout=300,
    )
    r.raise_for_status()
    return r.json()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt")
    ap.add_argument("--model", default=None, help="e.g., openai/gpt-5-mini")
    ap.add_argument("--preset", default=None, help="e.g., pro-search")
    ap.add_argument("--temperature", type=float, default=None)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if not args.model and not args.preset:
        # sensible default for research
        args.preset = "pro-search"

    data = call_responses(args.prompt, args.model, args.preset, args.temperature)

    if args.json:
        print(json.dumps(data, indent=2))
        return

    out = data.get("output_text")
    if out:
        print(out)
    else:
        print(json.dumps(data, indent=2))

    cites = extract_citations(data)
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
