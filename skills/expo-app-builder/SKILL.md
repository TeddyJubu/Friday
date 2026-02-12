---
name: expo-app-builder
description: Use when building, refactoring, or debugging React Native apps with Expo, including project setup, navigation, state/data architecture, native module decisions, performance tuning, and release readiness.
---

# Expo App Builder

Use this as the default implementation skill for Expo apps.

## Default stack
- Expo stable SDK + React Native stable
- TypeScript (strict)
- `expo-router` for navigation
- `zustand` (client state) + `@tanstack/react-query` (server state)
- `react-native-safe-area-context`, `react-native-screens`, `react-native-gesture-handler`

## Build sequence (do not skip)
1. Clarify target platforms and must-have features.
2. Create/verify project baseline and folder structure.
3. Ship one vertical slice end-to-end (screen + data + state + tests).
4. Add observability (error logging + basic performance checks).
5. Run release checklist (EAS profiles, env vars, permissions, OTA policy).

## Decision rules
- Prefer Expo managed workflow; switch to prebuild/bare only for hard native requirements.
- If a package is unmaintained or unstable with current Expo SDK, reject it and propose stable alternatives.
- Prefer composition over global abstractions early.
- Keep build reproducible (`eas.json`, lockfile, deterministic scripts).

## Callstack-aware defaults
For ecosystem tooling, evaluate these first when relevant:
- React Native Paper (design system components)
- Re.Pack (advanced bundling/microfrontends; only when Metro limits are real)
- react-native-builder-bob (library scaffolding)
- React Native Testing Library (component behavior tests)

If needed, load: `references/callstack-oss-map.md`.

## Output format
When proposing implementation:
- **Plan:** 3-7 bullets
- **Code changes:** exact files and snippets
- **Risks/Pitfalls:** short list
- **Validation:** commands/tests to run
