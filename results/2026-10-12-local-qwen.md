# Local evaluation: range repair

- **Date:** 12 October 2026 (Asia/Kolkata)
- **Environment source:** `range-repair` taskset version `0.1.0`
- **Taskset:** `range-repair`, one task (`touching-ranges-001`)
- **Harness and runtime:** Verifiers `bash` agent in Docker; `isolated-verifier` scoring in a fresh Docker container
- **Verifiers:** `0.3.2.dev209`, pinned to commit `e2253343056e2ed7507e67af48ebddfa4e3a7b96`
- **Model:** `sparky/qwen3.8-flash-next`, served over an OpenAI-compatible local vLLM chat endpoint
- **Sampling:** temperature `0.0`, max tokens `2048` per call

## Result

| Check | Result |
| --- | ---: |
| Model-free validation: known fix passes | 1/1 |
| Model-free validation: untouched bug fails | 1/1 |
| Agent attempts | 1 |
| Agent attempts passing held-out tests | 1/1 |
| Reward | 1.0 |
| Model turns | 7 |
| Total tokens recorded | 4,373 |

The agent inspected the file, used the edit tool, ran the four public tests, and finished with the public tests passing. The separate verifier restored the edited `ranges.py` and scored all held-out tests as passing. This is a one-attempt smoke test; it does not estimate a stable success rate.

## Reproduce

After following the [setup instructions](../README.md#setup-from-a-fresh-checkout), run:

```bash
./scripts/local.sh validate
./scripts/local.sh eval
```

The completed local run was written to `outputs/isolated-verifier+range-repair--sparky--qwen3.8-flash-next--bash--3d179357/`. Its episode ID was `f5a6f84345584e2885e11e754abcafa7`, and the scorer recorded `held_out_tests: 1.0`. Raw traces stay local under `outputs/` and are excluded from Git; inspect them before publishing because they contain model messages and local configuration details.
