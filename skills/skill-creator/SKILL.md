---
name: skill-creator
description: Create or update AgentSkills. Use when designing, structuring, testing, or packaging skills; also use when improving skill discoverability, trigger descriptions, and reliability under pressure scenarios.
---

# Skill Creator

This skill provides guidance for creating effective skills.

## Core Principles

### Concise is Key
Only add context Codex does not already know. Keep SKILL.md lean and move heavy reference to separate files.

### Set Appropriate Degrees of Freedom
- High freedom: text heuristics for variable tasks
- Medium freedom: pseudocode/scripts with params
- Low freedom: strict sequence for fragile operations

### Progressive Disclosure
1. Frontmatter metadata (always loaded)
2. SKILL.md body (loaded on trigger)
3. Bundled resources (loaded only when needed)

## Anatomy of a Skill

```
skill-name/
├── SKILL.md (required)
└── optional resources
    ├── scripts/
    ├── references/
    └── assets/
```

Only create files that directly support execution. Avoid extra docs like README/CHANGELOG unless explicitly required.

## Frontmatter Rules (Critical)

Use only:
- `name`
- `description`

`description` is primarily for triggering. Write it to describe **when to use** the skill (not workflow internals), with concrete symptoms/contexts.

Good style:
- Starts with “Use when…”
- Includes trigger keywords users actually say
- Mentions symptoms/errors where relevant
- Stays concise and third-person

## Skill Creation Process

1. Understand concrete user examples
2. Plan reusable resources (scripts/references/assets)
3. Initialize skill (if new)
4. Implement resources + SKILL.md
5. Package and validate
6. Iterate from real usage

### Naming
Use lowercase letters, digits, hyphens; keep under 64 chars.

## Test-Driven Skill Development (Added)

Treat skill writing like TDD for documentation:

### RED
Run pressure scenarios **without** the skill and capture failures/rationalizations.

### GREEN
Write the minimal skill that addresses those observed failures.

### REFACTOR
Retest, identify new loopholes, add explicit counters, repeat.

### Iron Law
No skill (or major edit) without a failing baseline test first.

For discipline-oriented skills, explicitly block common rationalizations (e.g., “just this once”, “too simple to test”).

## Packaging

```bash
scripts/package_skill.py <path/to/skill-folder>
```

Packaging validates structure/frontmatter and emits `.skill` if valid.

## Quality Checklist

- Description is trigger-focused (“Use when…”) and not a workflow summary
- Keywords cover user phrasing, symptoms, and relevant tools
- SKILL.md stays concise; heavy details moved to references
- Examples are few but high-quality and runnable
- For strict-behavior skills: include red flags and rationalization countermeasures
- Skill tested on realistic scenarios before deployment

## Optional Resources Guidance

- `scripts/`: deterministic or repeated logic
- `references/`: large docs loaded on demand
- `assets/`: templates/static files used in outputs

Keep references one hop from SKILL.md (avoid deep nesting).
