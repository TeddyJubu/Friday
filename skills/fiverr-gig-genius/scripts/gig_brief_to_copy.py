#!/usr/bin/env python3
"""Generate a Fiverr gig copy skeleton from a structured brief.

Usage:
  python3 gig_brief_to_copy.py brief.json

Input JSON fields (suggested):
  service, target_buyer, outcome, deliverables[], tools[], proof[], turnaround,
  revisions_basic, revisions_standard, revisions_premium,
  packages[{name, price_hint, includes[]}]

This is intentionally a skeleton generator; refine manually.
"""

import json
import sys


def get(d, k, default=""):
    v = d.get(k, default)
    return v if v is not None else default


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 gig_brief_to_copy.py brief.json", file=sys.stderr)
        return 2

    path = sys.argv[1]
    with open(path, "r", encoding="utf-8") as f:
        brief = json.load(f)

    service = get(brief, "service")
    target = get(brief, "target_buyer")
    outcome = get(brief, "outcome")
    deliverables = brief.get("deliverables", []) or []
    tools = brief.get("tools", []) or []
    proof = brief.get("proof", []) or []
    turnaround = get(brief, "turnaround")

    title = f"I will {service} for {target} to {outcome}".strip()

    print("=== TITLE (draft) ===")
    print(title)
    print()

    print("=== TAG IDEAS (draft) ===")
    print("- [primary keyword]")
    print("- [adjacent keyword]")
    print("- [tool/platform]")
    print("- [industry/niche]")
    print("- [outcome term]")
    print()

    print("=== DESCRIPTION (skeleton) ===")
    print(f"If you’re a {target} and you want {outcome}, you’re in the right place.")
    if turnaround:
        print(f"I can typically deliver within {turnaround} (depending on scope).")
    print()

    print("What you get:")
    for d in deliverables:
        print(f"- {d}")
    if tools:
        print("\nTools/platforms:")
        for t in tools:
            print(f"- {t}")
    if proof:
        print("\nWhy me:")
        for p in proof:
            print(f"- {p}")

    print("\nHow it works:")
    print("1) You answer a short questionnaire")
    print("2) I confirm scope + timeline")
    print("3) First delivery")
    print("4) Revisions (per package)")
    print("5) Final handoff")

    print("\nBuyer requirements (copy/paste):")
    print("1. Goal for this project:")
    print("2. Target audience:")
    print("3. Assets/links:")
    print("4. Examples you like:")
    print("5. Deadline:")

    packages = brief.get("packages") or []
    if packages:
        print("\n=== PACKAGES (draft) ===")
        for pkg in packages:
            print(f"- {pkg.get('name','Package')}: {pkg.get('price_hint','')}".strip())
            for inc in pkg.get("includes", []) or []:
                print(f"  - {inc}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
