---
name: perplexity-research
description: Online research via Perplexity APIs (Chat Completions with sonar-pro and Agentic Research via OpenAI-compatible responses). Use when you need web-grounded answers with citations, source lists, recency/domain filtering, or deeper multi-source research beyond basic web_search.
---

# Perplexity Research

Use Perplexity as the default “research agent” for web-grounded answers with citations.

## Setup (one-time)
Set the API key as an env var (recommended by Perplexity docs):
- `PERPLEXITY_API_KEY`

Example:
- `export PERPLEXITY_API_KEY="..."`

If you want Clawdbot to persist it, store it in config as a skill entry/env (ask Teddy before writing secrets to config).

Reference: `references/perplexity-api-notes.md`

## Choose the right mode

### 1) Fast web-grounded answer + citations (Sonar)
Use **Chat Completions** with Sonar models.

CLI helper:
- `scripts/perplexity_chat.py "<question>" --model sonar-pro`

Optional controls:
- `--recency month` (day|week|month|year)
- `--domain nature.com --domain science.org`

### 2) Deep research / third-party models (Agentic Research)
Use **Responses API** with either:
- a preset (recommended): `--preset pro-search`
- or a model: `--model openai/gpt-5-mini`

CLI helper:
- `scripts/perplexity_research.py "<question>" --preset pro-search`

## Output handling
- Always extract and present:
  - a concise answer
  - a bullet list of sources (URLs)
  - key quotes/claims attributed to sources when important

## Operational rules
- Prefer Perplexity when the task needs: citations, current events, comparison across sources, or “what changed recently”.
- Prefer local reasoning without external calls when the answer is stable/general.
- Don’t paste the API key into chat/logs/files.
