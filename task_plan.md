# Task Plan: Import marketingskills into Friday

## Goal
Add the skills from https://github.com/coreyhaines31/marketingskills into Friday’s local workspace so they can be used like other skills, with minimal risk (no secrets committed), and then commit + push the change to https://github.com/TeddyJubu/Friday.git.

## Current Phase
Phase 1

## Phases

### Phase 1: Requirements & Discovery
- [x] Understand user intent
- [x] Identify constraints and requirements
- [x] Document findings in findings.md
- **Status:** complete

### Phase 2: Planning & Structure
- [x] Decide where to place imported skills (top-level `/home/ubuntu/clawd/skills/<skill-name>/`)
- [x] Determine what files are needed for Clawdbot skill loading (SKILL.md etc.)
- [x] Document decisions
- **Status:** complete

### Phase 3: Implementation
- [x] Fetch upstream repo (temporary vendor clone)
- [x] Copy 25 skills into `/home/ubuntu/clawd/skills/`
- **Status:** complete

### Phase 4: Testing & Verification
- [x] Verify skills exist in `skills/` and include SKILL.md
- [ ] Sanity-check one or two skills are usable in conversation
- **Status:** complete

### Phase 5: Delivery
- [x] Summarize what was added + how to use
- [x] Commit + push
- **Status:** complete

## Key Questions
1. What is the structure of `coreyhaines31/marketingskills` and how should it map into Clawdbot skills?
2. Does it contain one skill or many, and do they already have SKILL.md files?
3. How do we expose them: as one big skill, or multiple separate skills?

## Decisions Made
| Decision | Rationale |
|----------|-----------|
| Use vendor import into `skills/marketingskills/` | Keeps external content isolated and easy to update/remove |

## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|
| planning-with-files init script failed (CRLF) | 1 | Created planning files manually from templates |

## Notes
- After this major change: commit + push to `TeddyJubu/Friday`.
- Do not commit secrets; `.gitignore` already excludes `memory/` and `keys/`.
