#!/usr/bin/env python3
"""Seedream 4.5 image edit helper for Molybot.

Uses AIMLAPI endpoint: POST https://api.aimlapi.com/v1/images/generations
Model default: bytedance/seedream-4-5

Inputs can be HTTP(S) URLs, data URLs, or local files.
Local files are encoded as data URLs automatically.
"""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import pathlib
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

API_URL = "https://api.aimlapi.com/v1/images/generations"
DEFAULT_MODEL = "bytedance/seedream-4-5"


def is_url(value: str) -> bool:
    return value.startswith("http://") or value.startswith("https://")


def is_data_url(value: str) -> bool:
    return value.startswith("data:")


def to_image_url(value: str) -> str:
    """Return URL/base64 data-url accepted by AIMLAPI image_urls."""
    if is_url(value) or is_data_url(value):
        return value

    path = pathlib.Path(value).expanduser().resolve()
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"Image file not found: {value}")

    mime, _ = mimetypes.guess_type(str(path))
    if not mime:
        mime = "image/jpeg"

    data = path.read_bytes()
    encoded = base64.b64encode(data).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def build_prompt(instruction: str, dress_color: str | None, has_reference: bool) -> str:
    parts: list[str] = [
        "Edit a real fashion product photo with strict identity preservation.",
        "Keep the same model/person exactly the same: face, body shape, skin tone, hair, pose, camera angle, framing, background, and garment fit.",
        "Do NOT change the model identity or body proportions.",
    ]

    if dress_color:
        parts.append(f"Change only the dress color to: {dress_color}.")

    if has_reference:
        parts.append(
            "Use the second image only as a dress-design reference. Transfer dress design details while preserving the original model identity and fit."
        )

    if instruction:
        parts.append(f"Extra edit request: {instruction.strip()}")

    parts.extend(
        [
            "Improve to studio-quality product photography: clean lighting, realistic fabric texture, sharp garment details, natural skin rendering.",
            "Output must look photorealistic and e-commerce ready.",
        ]
    )

    return "\n".join(parts)


def extract_output_url(payload: dict[str, Any]) -> str | None:
    for key in ("data", "images"):
        value = payload.get(key)
        if isinstance(value, list) and value:
            first = value[0]
            if isinstance(first, dict) and isinstance(first.get("url"), str):
                return first["url"]
            if isinstance(first, str):
                return first
    return None


def download_file(url: str, destination: pathlib.Path, timeout: int = 180) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(
        url,
        method="GET",
        headers={"User-Agent": "Mozilla/5.0 (OpenClaw Seedream Client)"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = resp.read()
    destination.write_bytes(data)


def main() -> int:
    parser = argparse.ArgumentParser(description="Edit fashion images with Seedream 4.5 via AIMLAPI")
    parser.add_argument("--source", required=True, help="Source image URL or local path")
    parser.add_argument(
        "--instruction",
        required=True,
        help="Requested edit details (e.g. change dress color, style notes)",
    )
    parser.add_argument("--dress-color", help="Target dress color (optional)")
    parser.add_argument(
        "--design-reference",
        help="Reference design image URL/local path (optional)",
    )
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Model id (default: {DEFAULT_MODEL})")
    parser.add_argument("--image-size", help="Optional output size (provider enum/string)")
    parser.add_argument("--seed", type=int, help="Optional deterministic seed")
    parser.add_argument(
        "--sync-mode",
        action="store_true",
        help="If set, waits for ready image payload when provider supports it",
    )
    parser.add_argument(
        "--out",
        help="Optional output file path. If omitted, writes into tmp/seedream-edits/",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=240,
        help="HTTP timeout seconds (default: 240)",
    )

    args = parser.parse_args()

    api_key = os.getenv("AIMLAPI_API_KEY") or os.getenv("AIMLAPI_KEY")
    if not api_key:
        print(
            json.dumps(
                {
                    "status": "error",
                    "error": "Missing AIMLAPI key. Set AIMLAPI_API_KEY (or AIMLAPI_KEY).",
                },
                ensure_ascii=False,
            )
        )
        return 2

    try:
        source_image = to_image_url(args.source)
        image_urls = [source_image]
        has_reference = bool(args.design_reference)
        if has_reference:
            image_urls.append(to_image_url(args.design_reference))
    except Exception as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False))
        return 2

    prompt = build_prompt(args.instruction, args.dress_color, has_reference)

    request_payload: dict[str, Any] = {
        "model": args.model,
        "prompt": prompt,
        "image_urls": image_urls,
        "response_format": "url",
        "watermark": False,
    }

    if args.image_size:
        request_payload["image_size"] = args.image_size
    if args.seed is not None:
        request_payload["seed"] = args.seed
    if args.sync_mode:
        request_payload["sync_mode"] = True

    body = json.dumps(request_payload).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (OpenClaw Seedream Client)",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=args.timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            response_json = json.loads(raw)
    except urllib.error.HTTPError as exc:
        err_body = exc.read().decode("utf-8", errors="replace") if exc.fp else ""
        print(
            json.dumps(
                {
                    "status": "error",
                    "error": f"HTTP {exc.code}",
                    "details": err_body,
                },
                ensure_ascii=False,
            )
        )
        return 1
    except urllib.error.URLError as exc:
        print(json.dumps({"status": "error", "error": f"Network error: {exc}"}, ensure_ascii=False))
        return 1
    except json.JSONDecodeError as exc:
        print(json.dumps({"status": "error", "error": f"Invalid JSON response: {exc}"}, ensure_ascii=False))
        return 1

    output_url = extract_output_url(response_json)
    if not output_url:
        print(
            json.dumps(
                {
                    "status": "error",
                    "error": "No output URL found in response",
                    "response": response_json,
                },
                ensure_ascii=False,
            )
        )
        return 1

    if args.out:
        out_path = pathlib.Path(args.out).expanduser().resolve()
    else:
        ts = time.strftime("%Y%m%d-%H%M%S")
        out_path = pathlib.Path("/home/ubuntu/clawd/tmp/seedream-edits") / f"seedream-edit-{ts}.jpg"

    try:
        download_file(output_url, out_path, timeout=max(60, args.timeout))
    except Exception as exc:
        print(
            json.dumps(
                {
                    "status": "error",
                    "error": f"Image download failed: {exc}",
                    "output_url": output_url,
                },
                ensure_ascii=False,
            )
        )
        return 1

    result = {
        "status": "ok",
        "model": args.model,
        "output_url": output_url,
        "output_path": str(out_path),
        "used_reference": has_reference,
    }
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
