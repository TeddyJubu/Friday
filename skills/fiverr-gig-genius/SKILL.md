---
name: fiverr-gig-genius
description: "Create, optimize, and iterate Fiverr gigs end-to-end: offer positioning, keyword/tag research, gig title + description copywriting, package/pricing design, FAQs, buyer requirements, and launch/iteration checklists. Use when asked to create a new Fiverr gig, improve gig ranking/SEO, rewrite gig copy, design packages/upsells, or research market/buyer language (web/Reddit) for Fiverr."
---

# Fiverr Gig Genius

Create high-converting Fiverr gigs by combining (1) clear positioning, (2) keyword/tag coverage, and (3) buyer-focused copy.

## Workflow (use in order)

### 1) Intake (don’t write copy yet)
Collect:
- Service + deliverables (exactly what the buyer receives)
- Target buyer (role, niche, geography)
- Primary outcome (what changes for the buyer)
- Proof (portfolio, numbers, years, brands)
- Constraints (turnaround, revisions, tools, availability)
- Existing gig link (if optimizing)

If info is missing, ask **only the minimum** needed to proceed.

### 2) Market + buyer-language research
Goal: learn what buyers search for and how they describe the problem.

Do:
- Fiverr autocomplete: type the service → capture top suggestions.
- Review top gigs in the category: note title patterns + scope.
- If Reddit research helps, read: `references/reddit-research-playbook.md`.

Output:
- 1 primary keyword phrase
- 3–6 secondary phrases
- 3 common pain points (in buyer words)
- 3 common objections (for FAQ)

### 3) Offer design (make it irresistible *and* specific)
Write a one-sentence offer statement:
- “I help [buyer type] achieve [outcome] by delivering [deliverable] using [method/tools], with [proof/constraint].”

Then define:
- What’s included (bullets)
- What’s excluded (boundaries)
- What success looks like (acceptance criteria)

### 4) Gig SEO: title + tags (coverage without stuffing)
Use official-community distilled guidance:
- Read: `references/fiverr-keywords-and-ranking.md`

Rules:
- Put the strongest keyword in the **title**.
- Keep title human-readable.
- Use **tags** to expand coverage (don’t waste all tags repeating the title).

Deliver:
- 3 title options
- 5 tag options (with rationale: “covers X search intent”)

### 5) Write the gig copy (conversion > clever)
Use the templates in:
- `references/gig-blueprint-templates.md`

Deliver:
- Hook (2–3 lines)
- “What you get” bullets
- Simple 3–5 step process
- Proof + differentiators
- Clear buyer requirements
- CTA (“message me before ordering…”) 

### 6) Packages + pricing strategy
Design Basic/Standard/Premium so each tier adds **scope** or **speed** or **risk reduction**.

Deliver:
- Package names
- Inclusions (bullets)
- Revision policy
- Delivery times
- Optional upsells (“gig extras”) that are easy to fulfill

### 7) FAQs + requirements questionnaire
Write 5–8 FAQs:
- Turn objections into questions.
- Make answers short and policy-safe (no guarantees you can’t control).

Provide a buyer requirements questionnaire (copy/paste).

### 8) QA checklist (before publishing)
Confirm:
- No exaggerated claims (“guaranteed #1 ranking”, etc.)
- Title matches package scope
- Requirements are complete (no hidden dependencies)
- Gallery text is mobile-readable
- Keywords are present naturally (no stuffing)

### 9) Launch + iteration plan
Set expectations:
- Search is personalized; daily swings are normal.
- Avoid constant edits; test changes for ~3–4 weeks.

Iteration loop:
- Track impressions → clicks → inquiries → orders.
- If impressions low: revisit keywords/title/tags.
- If clicks low: improve first image + title clarity.
- If inquiries low: tighten packages + add proof.
- If conversions low: rewrite hook + clarify deliverables.

## Optional automation
- Use `scripts/gig_brief_to_copy.py` to generate a first-pass skeleton from a JSON brief, then refine manually.

Example:
```bash
python3 skills/fiverr-gig-genius/scripts/gig_brief_to_copy.py brief.json
```
