# Range Repair Agent

A one-task coding environment for Prime Intellect Verifiers v1. The agent edits a buggy Python `merge_ranges` function. It can inspect the source and run public tests. The final edited file is copied into a fresh container, where held-out tests assign a binary reward: `1.0` if all pass, `0.0` otherwise.

The task ID is `touching-ranges-001`. The fixture, tests, and reward are included in this package; no external dataset, repository, or API key is required by the environment. A Docker or Prime container runtime and a model endpoint are required to evaluate it. This is a small evaluation example, not a complete RL training dataset.

## Local validation

From the repository root, with `uv`, Python 3.11+, and Docker running:

```bash
uv sync --python 3.12
PYTHONPATH=environments/range_repair_agent uv run vf-validate range-repair-agent --runtime.type docker --no-rich
```

Validation checks that the untouched buggy code fails and the known fix passes. Both checks should report `valid: 1`.

## Evaluate with a local model

Copy `.env.example` to the ignored `.env` in the repository root and set its model URL, exact model ID, and optional key. Then run:

```bash
PYTHONPATH=environments/range_repair_agent ./scripts/local.sh eval --env.id range-repair-agent --env.taskset.id range-repair-agent
```

The repository's `configs/local-eval.toml` selects Docker, the bash coding harness, and one rollout. The overrides select this package's isolated verifier environment and taskset. Outputs remain under the ignored `outputs/` directory and can contain private endpoint details; do not publish raw traces or resolved configs. A score of zero is a valid model result, so inspect the trace before treating it as a setup failure.

## Hub package

Build the standalone package before publishing:

```bash
uv build environments/range_repair_agent
```

After validating and signing in with the Prime CLI, publish this directory as a v1 environment:

```bash
prime env push --path environments/range_repair_agent --runtime v1
```

The package contains the full taskset and its isolated verifier environment. Use the exact Hub owner and version returned by the push command when reproducing a Hub evaluation.
