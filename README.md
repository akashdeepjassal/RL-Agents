# RL Agents: a small Prime Intellect coding task

This repository contains one working [Prime Intellect Verifiers](https://github.com/PrimeIntellect-ai/verifiers) taskset. A coding agent repairs a bug in a Python range-merging function. The agent can inspect and edit a file, run public tests, and submit its change. A fresh Docker container runs additional tests against only the edited file and assigns a binary reward: `1.0` when all tests pass, `0.0` otherwise.

This is a **local evaluation environment**, not an RL training run. It is intentionally small so you can understand the task, verify the scorer, and test a locally served model before expanding to more tasks or training.

## What is in the repository

| Path | Purpose |
| --- | --- |
| `range_repair/taskset.py` | Buggy source, public and held-out tests, task setup, and reward |
| `environments/range_repair_agent/` | Standalone v1 package for the Prime Environments Hub |
| `configs/local-eval.toml` | Docker runtime, agent limits, and evaluation settings |
| `.env.example` | Template for local model settings; the filled `.env` stays untracked |
| `scripts/local.sh` | Loads `.env` and runs the model check, validation, or evaluation |
| `pyproject.toml` and `uv.lock` | Python project and pinned dependencies |
| `results/` | Short, publishable summaries of completed evaluations |

The task uses a known bug in a tiny original fixture. It does not clone an outside codebase. The agent sees `/workspace/ranges.py` and `/workspace/test_public.py` inside its container. The held-out tests are staged only for scoring, after the agent finishes. `isolated-verifier` copies the edited `ranges.py` into a fresh container, then scores it there.

## Prerequisites

1. Git and [uv](https://docs.astral.sh/uv/getting-started/installation/) installed. `uv` can download Python 3.12 during setup.
2. Docker Desktop (macOS/Windows) or Docker Engine (Linux) running. Check with `docker info`.
3. A model server reachable from the machine running this evaluation, with OpenAI-compatible `/v1/models` and `/v1/chat/completions` endpoints **and tool calling**.
4. Enough network access for the first dependency download and Docker's `python:3.11-slim` image pull. Later runs reuse the local caches.

No Prime account or login is required for the local commands below. `push = false` keeps evaluation traces local.

## Setup from a fresh checkout

```bash
git clone https://github.com/akashdeepjassal/RL-Agents.git
cd RL-Agents

# On macOS, start Docker Desktop if it is not already running:
open -a Docker
docker info

# Install this project and the pinned Verifiers version into .venv:
uv sync --python 3.12

# Put your own endpoint, exact model ID, and optional key in the ignored file:
cp .env.example .env
# Edit .env locally before the next command.
chmod 600 .env
```

On Linux, start Docker with your usual service manager instead of `open -a Docker`. Wait until `docker info` succeeds before evaluating.

Set `LOCAL_MODEL_BASE_URL` to your server's `/v1` base URL, `LOCAL_MODEL_ID` to an ID returned by the server, and `LOCAL_MODEL_KEY` only if authentication is required. Keep `.env` on this machine; `.gitignore` excludes it and other `.env.*` files. The endpoint must end in `/v1`, not `/v1/models`.

Check the connection and model catalog without showing your key:

```bash
./scripts/local.sh models
```

## Verify the task without a model

```bash
./scripts/local.sh validate
```

This runs two checks: the untouched buggy code must fail, and the known repair must pass. Both checks should report `valid: 1`. Results are written under `outputs/range-repair--validate--.../`.

## Evaluate the local model

```bash
./scripts/local.sh dry-run
./scripts/local.sh eval
```

The first command checks the configuration. The second gives the agent one attempt on one task. The script passes the endpoint and model from `.env` to Verifiers at run time. It writes `traces.jsonl`, its resolved configuration, and logs under `outputs/isolated-verifier+range-repair--.../`. Look for `"held_out_tests": {"score": 1.0}` in the trace or the final reward in the command output. A score of `0.0` is a valid model result, not a setup failure; inspect the trace to see what the agent did. **The resolved config and trace can contain your endpoint**, so `outputs/` is ignored by Git.

To try several independent attempts, change `num_rollouts` in `configs/local-eval.toml`, then rerun the evaluation. Each run receives a new output directory. Keep the model ID, settings, taskset version, attempt count, and score together when comparing results. One successful attempt is only a smoke test, not evidence of a reliable success rate.

The pinned Verifiers version currently prints a deprecation notice for `vf-eval` in favor of Prime RL's newer `eval` entry point. The commands above are the ones tested with this repository's lockfile.

## Run a task from Prime's Environments Hub

This repository's `range-repair` task is local. To evaluate a public Hub task with the same local model, install the [Prime CLI](https://github.com/PrimeIntellect-ai/prime), find a taskset ID in the [Environments Hub](https://app.primeintellect.ai/dashboard/environments), and install it into the Verifiers environment:

```bash
uv tool install prime
prime login
prime env install <taskset-id>
./scripts/local.sh dry-run --env.taskset.id <taskset-id>
./scripts/local.sh eval --env.taskset.id <taskset-id>
```

Replace `<taskset-id>` with the actual ID shown by Prime. Some Hub tasks need a different harness, Docker image, extra packages, or credentials; check that task's README and override its settings in the evaluation config. The local model server must support the API and tool calls required by the selected harness. `prime login` is for Hub access; the model still runs on the endpoint in your `.env`.

The built-in `bash` harness is the coding agent used and tested here. To try the separate **Prime Agent** harness with this task, use `--env.agent.harness.id prime-agent` on the dry run and evaluation commands. That harness installs its own agent program and has not yet been verified against this local model; its tool and API requirements may differ.

## Publish this environment to Prime's Hub

The standalone package is in `environments/range_repair_agent/`. It includes the task, held-out scorer, and an isolated verifier environment. Its source is a copy of `range_repair/taskset.py`, so update both files when changing the task.

Validate the package and test it with the local model before publishing:

```bash
PYTHONPATH=environments/range_repair_agent uv run vf-validate range-repair-agent --runtime.type docker --no-rich
PYTHONPATH=environments/range_repair_agent ./scripts/local.sh eval --env.id range-repair-agent --env.taskset.id range-repair-agent
uv build environments/range_repair_agent
```

This package is published as [`akashdeepjassal/range-repair-agent@0.1.0`](https://app.primeintellect.ai/dashboard/environments/akashdeepjassal/range-repair-agent). To publish an updated version, bump the version in its `pyproject.toml`, sign in to Prime, and push the package directory, explicitly selecting Verifiers v1:

```bash
prime login
prime env push --path environments/range_repair_agent --runtime v1 --visibility PUBLIC
```

Prime requires a username on your profile before a push. Use `prime env install akashdeepjassal/range-repair-agent@0.1.0` to install the published version. Keep `.env`, raw `outputs/`, build artifacts, and Prime's local metadata out of Git. This is a one-task evaluation example; publishing it does not train the model.

## Submit a local-model evaluation to Prime

The Hub environment and an evaluation are separate records. `prime env push` publishes the task code. The local commands earlier in this README use `push = false` in `configs/local-eval.toml`, so they write traces under `outputs/` but create **no** entry on Prime's Evaluations dashboard. The successful run in `results/2026-10-13-range-repair-agent.md` was local and was not submitted to Prime.

**Keep the model address private before uploading a trace.** The local trace includes the client's base URL. The existing local traces were created with a literal LAN address and must stay local. To submit a new evaluation without putting that address in Prime's trace, use a local hostname that resolves to your model server. If your model machine has no hostname, add a private mapping in this computer's `/etc/hosts` (on macOS, `sudo nano /etc/hosts`):

```text
<your-model-server-LAN-address> rl-model.test
```

Then edit only the ignored `.env`, retaining your current port and model ID. For a server using port 8000, the base URL would be:

```text
LOCAL_MODEL_BASE_URL=http://rl-model.test:8000/v1
```

Do not put the address, key, or filled `.env` in Git, commands pasted into public issues, or result reports. Confirm the hostname resolves and the model is reachable:

```bash
./scripts/local.sh models
prime whoami
```

If `prime whoami` fails, run `prime login` first. Next, make one **unsubmitted** trial run with the hostname and inspect its newest trace:

```bash
PYTHONPATH=environments/range_repair_agent ./scripts/local.sh eval --env.id range-repair-agent --env.taskset.id range-repair-agent

python3 - <<'PY'
from pathlib import Path
import re

traces = list(Path('outputs').glob('range-repair-agent+range-repair-agent--*/traces.jsonl'))
latest = max(traces, key=lambda path: path.stat().st_mtime)
data = latest.read_bytes()
assert not re.search(rb'(?<![0-9])(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?![0-9])', data), 'Trace contains an IP address'
assert not re.search(rb'(?i)(?:sk-[A-Za-z0-9_-]{12,}|ghp_[A-Za-z0-9]{12,}|github_pat_[A-Za-z0-9_]{12,})', data), 'Trace contains a credential-like token'
print('Newest trace passed the basic privacy check:', latest)
PY
```

Review the trace for any other private data before submitting. Now run a **new** evaluation with `--push`; this overrides the repository's `push = false` setting and uploads the run to your private Prime Evaluations tab:

```bash
PYTHONPATH=environments/range_repair_agent ./scripts/local.sh eval --env.id range-repair-agent --env.taskset.id range-repair-agent --push
prime eval list --output json --plain
```

The evaluation output should include a Prime dashboard URL ending in `/dashboard/evaluations/<evaluation-id>`. Confirm the new record appears in `prime eval list`; an evaluation can finish locally even if its upload fails. Use `prime eval get <evaluation-id>` and `prime eval samples <evaluation-id>` to inspect the submitted status and score. The Evaluations page is at [Prime Evaluations](https://app.primeintellect.ai/dashboard/evaluations).

Do not use `prime eval push` on this repository's v1 `outputs/` directories: that separate command expects `metadata.json` and `results.jsonl`, while this project writes `traces.jsonl`. To run a hosted evaluation instead, use `prime eval run ... --hosted` with a model reachable from Prime's runner. A model available only on your LAN will not be reachable from that runner. Hosted evaluations may require billing; the local `--push` path uses your own model server.

## Task and scoring details

- **Issue:** `merge_ranges` incorrectly separates ranges that share an endpoint. For example, `(1, 2)` and `(2, 5)` should become `(1, 5)`.
- **Boundary rule:** Consecutive ranges without a shared endpoint stay separate; `(1, 2)` and `(3, 4)` remain two ranges.
- **Public feedback:** The agent can run `python -m unittest -q test_public` in `/workspace`.
- **Reward:** The edited `/workspace/ranges.py` is the only declared artifact. A fresh Docker container restores it, runs the held-out `unittest` cases, and gives `1.0` only when all pass.
- **Reference solution:** Changing the new-range condition from `start >= previous_end` to `start > previous_end` satisfies the specification. The model never receives this reference solution in its task prompt.

The taskset includes `validate()` so `vf-validate` can prove the reference solution passes and the original source does not. The tests cover touching chains, nested ranges, empty input, separated consecutive ranges, and invalid ranges.

## Publishing and next steps

The `results/` directory contains a concise report suitable for GitHub. Raw `outputs/` are ignored by Git because traces can be large and may include model messages, endpoint URLs, and local machine details. Review any trace before sharing it separately.

To turn this into a larger coding RL environment, add more independently sourced tasks with clear issue statements, pre-fix source, known repairs, and tests that reject plausible wrong fixes. Run model-free validation on each task before evaluation. Training a model requires a separate training setup and access to its weights; connecting an inference endpoint only enables evaluation.
