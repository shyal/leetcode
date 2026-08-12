"""The judge only ever learns about a peek, a hint or a TLE from the notes the
candidate writes below the `---` rule in the solve file's docstring. kg_extract
strips that docstring to keep prompts small, and for a long time it stripped the
notes with it — silently, because nothing asserted they made it through. These
tests fail if that ever regresses."""

import glob
import os
from importlib.machinery import SourceFileLoader

UTILS = os.path.dirname(os.path.abspath(__file__))
kg_extract = SourceFileLoader("kg_extract", os.path.join(UTILS, "kg_extract")).load_module()

SOLVE = '''"""
1. Two Sum

Given an array of integers, return indices of the two numbers that add to
target.

---
Peeked at the editorial for the complement trick.
"""

from typing import List


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = {}  # running dict, built as we scan
        for i, n in enumerate(nums):
            if target - n in seen:
                return [seen[target - n], i]
            seen[n] = i


sol = Solution()
assert sol.twoSum([2, 7, 11, 15], 9) == [0, 1]
'''


def test_notes_survive_statement_strip():
    out = kg_extract.strip_statement(SOLVE)
    assert "Peeked at the editorial" in out


def test_statement_is_stripped():
    out = kg_extract.strip_statement(SOLVE)
    assert "Given an array of integers" not in out


def test_code_and_inline_comments_survive():
    out = kg_extract.strip_statement(SOLVE)
    assert "def twoSum" in out
    assert "running dict, built as we scan" in out  # comments are notes too


def test_no_docstring_is_left_alone():
    code = "class Solution:\n    pass\n"
    assert kg_extract.strip_statement(code) == code


def test_unparseable_file_still_yields_a_body():
    """Abandoned attempts must not crash the extractor."""
    broken = '"""\n1. Two Sum\n\n---\nGave up.\n"""\n\ndef f(:\n'
    out = kg_extract.strip_statement(broken)
    assert "def f(:" in out


def test_real_solves_with_notes_keep_them():
    """The regression that actually happened, against the real corpus."""
    checked = 0
    for path in sorted(glob.glob(os.path.join(UTILS, "..", "solved", "*.py")))[:400]:
        code = open(path).read()
        doc_end = code.find('"""', 3)
        if not code.startswith('"""') or doc_end == -1:
            continue
        doc = code[3:doc_end]
        if "\n---" not in doc:
            continue
        tail = doc.split("\n---", 1)[1].strip()
        if not tail:
            continue
        out = kg_extract.strip_statement(code)
        first_line = tail.splitlines()[0].strip()
        if len(first_line) > 20:  # skip rules/separators, match on real prose
            assert first_line in out, f"notes dropped for {os.path.basename(path)}"
            checked += 1
    assert checked > 20, f"expected many noted solves in the corpus, saw {checked}"
