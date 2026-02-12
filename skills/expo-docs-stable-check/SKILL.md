---
name: expo-docs-stable-check
description: Use when you need to verify that React Native/Expo guidance is up to date for the latest stable versions before making architecture, dependency, or implementation decisions.
---

# Expo Docs Stable Check

Use this skill before major technical decisions.

## Goal
Ground implementation on the latest stable docs, not stale memory.

## Required checks
1. Resolve latest stable versions:
   - `npm view expo version`
   - `npm view react-native version`
2. Verify docs against stable channels:
   - Expo docs (`docs.expo.dev`) for SDK/features/workflows
   - React Native docs (`reactnative.dev`) for APIs/architecture
3. Verify high-impact dependencies against compatibility notes/changelogs.

## Workflow
1. Capture current stable versions and date.
2. Check whether planned approach depends on deprecated, experimental, or removed APIs.
3. Flag version-sensitive guidance and write a compatibility note in output.

## Output format
- **Stable baseline:** Expo X / RN Y (date checked)
- **Confirmed valid:** bullets with source URLs
- **Potentially outdated:** bullets with what changed
- **Action:** proceed / adjust plan

## Red flags
- Any recommendation that references an older major SDK/API without migration notes.
- Tutorials that conflict with official docs for current stable versions.
- Community snippets that require unsupported native patches for Expo managed apps.
