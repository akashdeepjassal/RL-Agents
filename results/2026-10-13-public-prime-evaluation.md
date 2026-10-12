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

To check the published record:

```bash
prime eval get ge1divvv3grrjdn1y4tbx1qr --output json --plain
```
