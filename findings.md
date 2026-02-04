# Findings & Decisions

## Requirements
- Import the skills/content from `https://github.com/coreyhaines31/marketingskills` into Friday.
- Skills must be available in the Clawdbot workspace under `/home/ubuntu/clawd/skills` (or referenced by that).
- After major changes, commit + push to `https://github.com/TeddyJubu/Friday.git`.

## Research Findings
- `coreyhaines31/marketingskills` already contains **25 Clawdbot-style skills** under `skills/<skill-name>/SKILL.md`.
- Imported skills include: seo-audit, programmatic-seo, copywriting, paid-ads, pricing-strategy, schema-markup, etc.
- These skills can be copied directly into `/home/ubuntu/clawd/skills/<skill-name>/` (no gateway config change needed).

## Technical Decisions
| Decision | Rationale |
|----------|-----------|
| Vendor the repo into `skills/marketingskills/` | Keeps upstream content separated; easier updates |

## Issues Encountered
| Issue | Resolution |
|-------|------------|
| planning-with-files init script has CRLF/compat issue | Manually created task_plan.md/findings.md/progress.md |

## Resources
- Source repo: https://github.com/coreyhaines31/marketingskills
- Local imported skill dirs: `/home/ubuntu/clawd/skills/<skill-name>/`
- Friday repo remote: https://github.com/TeddyJubu/Friday.git

## Visual/Browser Findings
- (none)
