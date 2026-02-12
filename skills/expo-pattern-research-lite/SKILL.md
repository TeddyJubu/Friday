---
name: expo-pattern-research-lite
description: Use when solving unfamiliar Expo/React Native problems and you need fast, low-cost online research to find current techniques, real-world pitfalls, and practical implementation patterns.
---

# Expo Pattern Research (Lite)

Use this skill to research cheaply before deep implementation.

## Objective
Find what practitioners are doing *now* and avoid known traps.

## Cost-first strategy
- Start with lightweight search + fetch (`web_search`, `web_fetch`).
- Prefer official docs, issue threads, release notes, and high-signal blog posts.
- Escalate to deeper research only if evidence conflicts or remains unclear.

## Research loop
1. Define the exact problem in one sentence.
2. Run focused queries (problem + Expo SDK + platform).
3. Extract:
   - 2-4 common solution patterns
   - 3-6 pitfalls (version mismatch, platform quirks, perf regressions, build issues)
   - compatibility constraints for latest stable Expo/RN
4. Cross-check against official docs and mark confidence.

## Query templates
- `"<problem>" Expo SDK <latest> iOS Android`
- `"<problem>" react native <latest> issue`
- `site:github.com <library> expo compatibility`
- `site:docs.expo.dev <feature>`

## Output format
- **What works now:** ranked patterns
- **Pitfalls to avoid:** concise bullets
- **Decision recommendation:** best path + fallback
- **References:** URLs only (5-10 max)

## Stop conditions
- If only anecdotal sources exist, explicitly mark low confidence.
- If guidance conflicts with stable docs, prefer docs and flag community advice as risky.
