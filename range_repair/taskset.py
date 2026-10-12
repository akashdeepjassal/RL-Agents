"""One small file-editing task with deterministic tests."""

import verifiers.v1 as vf


BUGGY_SOURCE = '''\
"""Merge overlapping closed integer ranges or ranges sharing an endpoint."""


def merge_ranges(ranges):
    """Return sorted, non-overlapping (start, end) pairs."""
    merged = []
    for start, end in sorted(ranges):
        if start > end:
            raise ValueError("range start must not exceed end")
        if not merged or start >= merged[-1][1]:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)
    return [tuple(pair) for pair in merged]
'''

KNOWN_FIX = BUGGY_SOURCE.replace("start >= merged[-1][1]", "start > merged[-1][1]")

PUBLIC_TESTS = '''\
import unittest
from ranges import merge_ranges


class PublicTests(unittest.TestCase):
    def test_overlap(self):
        self.assertEqual(merge_ranges([(1, 4), (3, 6)]), [(1, 6)])

    def test_gap(self):
        self.assertEqual(merge_ranges([(1, 2), (4, 5)]), [(1, 2), (4, 5)])

    def test_consecutive_but_separate(self):
        self.assertEqual(merge_ranges([(1, 2), (3, 5)]), [(1, 2), (3, 5)])

    def test_touching(self):
        self.assertEqual(merge_ranges([(1, 2), (2, 5)]), [(1, 5)])


if __name__ == "__main__":
    unittest.main()
'''

HELD_OUT_TESTS = '''\
import unittest
from ranges import merge_ranges


class HeldOutTests(unittest.TestCase):
    def test_touching_chain_out_of_order(self):
        self.assertEqual(merge_ranges([(5, 7), (1, 3), (3, 5)]), [(1, 7)])

    def test_nested_range(self):
        self.assertEqual(merge_ranges([(1, 9), (2, 3)]), [(1, 9)])

    def test_disjoint_singletons_and_empty(self):
        self.assertEqual(merge_ranges([]), [])
        self.assertEqual(merge_ranges([(4, 4), (-2, -2)]), [(-2, -2), (4, 4)])

    def test_consecutive_ranges_stay_separate(self):
        self.assertEqual(merge_ranges([(-1, 0), (1, 2)]), [(-1, 0), (1, 2)])

    def test_invalid_range(self):
        with self.assertRaises(ValueError):
            merge_ranges([(9, 2)])


if __name__ == "__main__":
    unittest.main()
'''


class RangeRepairTask(vf.Task[vf.TaskData]):
    NEEDS_CONTAINER = True

    async def setup(self, trace: vf.Trace, runtime: vf.Runtime) -> None:
        await runtime.run(["mkdir", "-p", "/workspace"], {})
        await runtime.write("/workspace/ranges.py", BUGGY_SOURCE.encode())
        await runtime.write("/workspace/test_public.py", PUBLIC_TESTS.encode())

    async def stage_verifier(self, trace: vf.Trace, runtime: vf.Runtime) -> None:
        await runtime.write("/workspace/test_held_out.py", HELD_OUT_TESTS.encode())

    async def validate(self, runtime: vf.Runtime) -> bool:
        await runtime.write("/workspace/ranges.py", KNOWN_FIX.encode())
        await runtime.write("/workspace/test_held_out.py", HELD_OUT_TESTS.encode())
        result = await runtime.run(
            ["python", "-m", "unittest", "-q", "test_held_out"],
            {"PYTHONPATH": "/workspace"},
        )
        return result.exit_code == 0

    @vf.reward
    async def held_out_tests(self, trace: vf.Trace, runtime: vf.Runtime) -> float:
        await runtime.write("/workspace/test_held_out.py", HELD_OUT_TESTS.encode())
        result = await runtime.run(
            ["python", "-m", "unittest", "-q", "test_held_out"],
            {"PYTHONPATH": "/workspace"},
        )
        return float(result.exit_code == 0)


class RangeRepairTaskset(vf.Taskset[RangeRepairTask, vf.TasksetConfig]):
    def load(self) -> list[RangeRepairTask]:
        return [
            RangeRepairTask(
                vf.TaskData(
                    id="touching-ranges-001",
                    name="Merge touching ranges",
                    workdir="/workspace",
                    prompt=(
                        "Fix the bug in /workspace/ranges.py. merge_ranges should combine "
                        "closed integer ranges that overlap or share an endpoint. "
                        "Consecutive ranges without a shared endpoint stay separate: "
                        "(1, 2) and (3, 4) must remain two ranges. Preserve the existing API and "
                        "ValueError for invalid ranges. Run python -m unittest -q "
                        "test_public before finishing."
                    ),
                    network_allow=[],
                    artifacts=[vf.Artifact(source="/workspace/ranges.py")],
                )
            )
        ]
