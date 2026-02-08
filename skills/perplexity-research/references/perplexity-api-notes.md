# Perplexity API notes (quick reference)

Source docs (official):
- Overview: https://docs.perplexity.ai/docs/getting-started/overview
- Quickstart: https://docs.perplexity.ai/docs/getting-started/quickstart
- OpenAI compatibility: https://docs.perplexity.ai/docs/grounded-llm/openai-compatibility

## Base URL
Per Perplexity OpenAI-compat docs, use:
- `https://api.perplexity.ai/v2`

## Auth
- `Authorization: Bearer <PERPLEXITY_API_KEY>`

Env var recommended by docs:
- `PERPLEXITY_API_KEY` (official)

## Main modes

### Chat Completions (Sonar, grounded answers + citations)
- Endpoint style: OpenAI `chat.completions.create`
- Example model: `sonar-pro`

### Agentic Research (OpenAI Responses-compatible)
- Endpoint style: OpenAI `responses.create`
- Example model: `openai/gpt-5-mini`
- Supports `preset` (e.g., `pro-search`) via `extra_body` / direct param.

## Perplexity-specific search controls (chat completions)
Examples shown in docs:
- `search_domain_filter`: ["nature.com", "science.org"]
- `search_recency_filter`: "month"

## Output citations
- Chat completions responses include `citations: [url...]`.
- Agentic research responses include `output_text` plus annotations/citations depending on model/preset.
