---
name: molybot-seedream-edit
description: Edit fashion/product photos with AIMLAPI Seedream 4.5 for Molybot. Use when the user asks to change dress color, transfer dress design from a reference image, keep the same model identity, or produce studio-quality product photos from an existing image.
---

# Molybot Seedream 4.5 Image Editing

Require environment variable: `AIMLAPI_API_KEY` (or `AIMLAPI_KEY`).

Use script:
`/home/ubuntu/clawd/skills/molybot-seedream-edit/scripts/seedream_edit.py`

## Workflow

1. Collect required inputs:
   - Source image (URL or local path)
   - Requested change (Bangla or English)
2. Collect optional inputs when relevant:
   - Target dress color
   - Reference design image (for design transfer)
3. If request is unclear, ask short follow-up questions in simple Bangla.
4. Run Seedream edit script.
5. Return the edited image path and URL.

## Command templates

Color change only:

```bash
python3 /home/ubuntu/clawd/skills/molybot-seedream-edit/scripts/seedream_edit.py \
  --source "/path/or/url/to/source.jpg" \
  --instruction "Change only the dress color and keep model exactly the same." \
  --dress-color "emerald green"
```

Color + design transfer from reference:

```bash
python3 /home/ubuntu/clawd/skills/molybot-seedream-edit/scripts/seedream_edit.py \
  --source "/path/or/url/to/source.jpg" \
  --design-reference "/path/or/url/to/design-reference.jpg" \
  --instruction "Use the reference design for the dress while preserving the same model and pose." \
  --dress-color "royal blue"
```

Optional deterministic seed:

```bash
--seed 123456
```

## Quality constraints

Always enforce:
- Preserve the same person/model identity exactly.
- Preserve body shape, face, pose, camera framing, and background.
- Edit dress attributes only (color/design) unless user asks otherwise.
- Produce studio-quality, photorealistic e-commerce output.
