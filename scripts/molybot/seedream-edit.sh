#!/bin/bash
# seedream-edit.sh - Convenience wrapper for Molybot Seedream 4.5 image editing
# Usage examples:
#   seedream-edit.sh --source image.jpg --instruction "Change dress color" --dress-color red
#   seedream-edit.sh --source image.jpg --design-reference ref.jpg --instruction "Use this design"

set -euo pipefail

SCRIPT="/home/ubuntu/clawd/skills/molybot-seedream-edit/scripts/seedream_edit.py"

python3 "$SCRIPT" "$@"
