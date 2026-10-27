#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."
mode="${1:-}"
shift || true

case "$mode" in
  validate)
    exec uv run vf-validate range-repair --runtime.type docker --no-rich "$@"
    ;;
  models|dry-run|eval)
    if [[ ! -f .env ]]; then
      echo "Create .env from .env.example and fill in your local model settings." >&2
      exit 1
    fi
    set -a
    # This local file is user-controlled and ignored by Git.
    source ./.env
    set +a
    : "${LOCAL_MODEL_BASE_URL:?Set LOCAL_MODEL_BASE_URL in .env}"
    if [[ "$mode" == models ]]; then
      if [[ -n "${LOCAL_MODEL_KEY:-}" ]]; then
        exec curl -fsS -H "Authorization: Bearer $LOCAL_MODEL_KEY" "$LOCAL_MODEL_BASE_URL/models"
      fi
      exec curl -fsS "$LOCAL_MODEL_BASE_URL/models"
    fi
    : "${LOCAL_MODEL_ID:?Set LOCAL_MODEL_ID in .env}"
    options=( @ configs/local-eval.toml --client.base-url "$LOCAL_MODEL_BASE_URL" --model "$LOCAL_MODEL_ID" )
    if [[ "$mode" == dry-run ]]; then
      exec uv run vf-eval "${options[@]}" --dry-run "$@"
    fi
    exec uv run vf-eval "${options[@]}" --no-rich "$@"
    ;;
  *)
    echo "Usage: scripts/local.sh {models|validate|dry-run|eval} [extra vf-eval options]" >&2
    exit 2
    ;;
esac
