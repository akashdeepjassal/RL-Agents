# Range Repair Agent: package validation and local evaluation

- **Environment:** `range-repair-agent` version `0.1.0` (Verifiers v1)
- **Prime Hub:** [`akashdeepjassal/range-repair-agent@0.1.0`](https://app.primeintellect.ai/dashboard/environments/akashdeepjassal/range-repair-agent)
- **Task:** `touching-ranges-001`, one coding task
- **Model:** `sparky/qwen3.8-flash-next`, served through the private local endpoint in `.env`
- **Harness and runtime:** `bash` agent in Docker; scoring in a fresh Docker container
- **Attempts:** one
- **Reward:** `held_out_tests = 1.0` (successful repair)
- **Validation:** gold and untouched checks both valid (`1/1` each)

Commands run from the repository root:

```bash
PYTHONPATH=environments/range_repair_agent uv run vf-validate range-repair-agent --runtime.type docker --no-rich
PYTHONPATH=environments/range_repair_agent ./scripts/local.sh dry-run --env.id range-repair-agent --env.taskset.id range-repair-agent
PYTHONPATH=environments/range_repair_agent ./scripts/local.sh eval --env.id range-repair-agent --env.taskset.id range-repair-agent
uv build environments/range_repair_agent
```

The generated wheel was also installed in a separate temporary environment, where both the taskset and environment classes loaded. Raw traces, logs, and resolved configurations remain under ignored `outputs/`; they can contain private connection details and are not part of this report. This is one successful local evaluation, not an RL training run or a reliability estimate.

The package was pushed to the Prime Hub as a public Verifiers v1 environment. The Hub reports version `0.1.0`, and its archive contains only `README.md`, `pyproject.toml`, and `range_repair_agent.py`.
