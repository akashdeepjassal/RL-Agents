# Public Prime evaluation: range repair agent

- **Date:** 13 October 2026 (Asia/Kolkata)
- **Environment:** [`akashdeepjassal/range-repair-agent@0.1.0`](https://app.primeintellect.ai/dashboard/environments/akashdeepjassal/range-repair-agent)
- **Evaluation:** [`ge1divvv3grrjdn1y4tbx1qr`](https://app.primeintellect.ai/dashboard/evaluations/ge1divvv3grrjdn1y4tbx1qr)
- **Model:** `sparky/qwen3.8-flash-next`, served locally through an OpenAI-compatible endpoint
- **Task and attempts:** `touching-ranges-001`, one attempt
- **Result:** `avg_score = 1.0`, `held_out_tests = 1.0`
- **Prime status:** `COMPLETED`, `is_public = true`, `show_on_leaderboard = true`

The model repaired the touching-range bug and passed the held-out tests. This is one successful evaluation attempt, not a measured reliability rate or an RL training run.

The public result was submitted from a privacy-checked, one-sample summary of the completed local trace. The earlier `vf-eval --push` submission is a separate private evaluation. Raw traces and local model settings remain outside Git.

This report records the completed submission. To repeat the workflow with a new attempt, follow the [setup, validation, private upload, and score-only public submission steps](../README.md#submit-a-local-model-evaluation-to-prime). The pinned local run writes `traces.jsonl`; the installed Prime CLI requires `metadata.json` and `results.jsonl` for `prime eval push`. Publishing an evaluation alone does not ensure leaderboard inclusion.

To check the published record:

```bash
prime eval get ge1divvv3grrjdn1y4tbx1qr --output json --plain
prime eval samples ge1divvv3grrjdn1y4tbx1qr --output json --plain
```

Check `status`, `metrics.score`, `is_public`, and `show_on_leaderboard` in the evaluation record, then confirm the one sample and its `reward = 1.0` in the samples response. The published sample's `score` field is null, so use the evaluation metric and sample reward for this result. More independent tasks and repeated attempts remain future work; no RL training was performed.
