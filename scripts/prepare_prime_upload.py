"""Export score-only Prime upload files from a Verifiers trace."""

import argparse
import json
from collections import Counter
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("trace", type=Path, help="Explicit path to one traces.jsonl")
    parser.add_argument("destination", type=Path, help="New directory under ignored outputs/")
    parser.add_argument("--model", required=True, help="Public model ID, not an endpoint URL")
    args = parser.parse_args()

    if args.trace.name != "traces.jsonl" or not args.trace.is_file():
        parser.error("pass an existing traces.jsonl file")
    if args.destination.resolve().is_relative_to(Path("outputs").resolve()) is False:
        parser.error("destination must be under the ignored outputs/ directory")
    if args.destination.exists():
        parser.error("destination already exists; choose a new directory")
    if "://" in args.model:
        parser.error("--model must be a model ID, not a URL")

    samples = []
    for line in args.trace.read_text().splitlines():
        if not line.strip():
            continue
        episode = json.loads(line)
        traces = episode["traces"]
        if len(traces) != 1 or not episode["ok"] or not traces[0]["ok"]:
            parser.error("expected exactly one successful trace per episode")
        reward = float(traces[0]["rewards"]["held_out_tests"]["score"])
        if not 0.0 <= reward <= 1.0:
            parser.error("held-out reward must be between 0 and 1")
        samples.append({
            "example_id": episode["task"]["data"]["id"],
            "trace_id": episode["id"],
            "reward": reward,
            "score": reward,
            "held_out_tests": reward,
        })
    if not samples:
        parser.error("trace file contains no episodes")
    counts = Counter(sample["example_id"] for sample in samples)
    if len(set(counts.values())) != 1:
        parser.error("each task must have the same number of attempts")

    average = sum(sample["score"] for sample in samples) / len(samples)
    metadata = {
        "env_id": "akashdeepjassal/range-repair-agent",
        "model": args.model,
        "framework": "verifiers",
        "num_examples": len(counts),
        "rollouts_per_example": next(iter(counts.values())),
        "avg_score": average,
        "avg_reward": average,
        "avg_held_out_tests": average,
    }
    args.destination.mkdir(parents=True)
    (args.destination / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    (args.destination / "results.jsonl").write_text(
        "".join(json.dumps(sample) + "\n" for sample in samples)
    )
    print(f"Prepared {len(samples)} score-only sample(s) in {args.destination}")


if __name__ == "__main__":
    main()
