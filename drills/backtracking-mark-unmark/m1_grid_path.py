"""
DRILL: Grid Path
TRAINS: backtracking-mark-unmark

Given a grid of lowercase letters and a string word, return True if word
can be spelled by a path through the grid. A path starts at any cell and
steps only to a cell directly above, below, left or right of the one
before it. One path never uses the same cell twice.

Example 1:

Input: grid = [["a", "b"], ["d", "c"]], word = "abcd"
Output: True
Explanation: the path runs (0,0) -> (0,1) -> (1,1) -> (1,0).

Example 2:

Input: grid = [["a", "b"], ["d", "c"]], word = "abd"
Output: False
Explanation: "b" and "d" are diagonal neighbours, and a path steps only
up, down, left or right.

Example 3:

Input: grid = [["a", "a"]], word = "aaa"
Output: False
Explanation: only two cells hold "a", and one path cannot use a cell
twice.

Constraints:

    1 <= len(grid), len(grid[0]) <= 6
    1 <= len(word) <= 15
    grid and word hold lowercase English letters.

    REQUIRED: mark a cell taken by writing over it in the grid itself,
    then restore its letter after the recursive call returns. NO separate
    visited set or visited grid. The restore is the whole drill: a cell
    that is off-limits for the path currently being walked must be free
    again for a path that starts somewhere else, and a cell left marked
    turns later True answers into False. Return as soon as one path
    spells the word.
"""


class Solution:
    def exist(self, grid: list[list[str]], word: str) -> bool:
        pass


sol = Solution()

print(sol.exist([["a", "b"], ["d", "c"]], "abcd"))  # True

# assert sol.exist([["a", "b"], ["d", "c"]], "abcd") is True
# assert sol.exist([["a", "b"], ["d", "c"]], "abd") is False
# assert sol.exist([["a", "a"]], "aaa") is False
# assert sol.exist([["a"]], "a") is True
# assert sol.exist([["a"]], "b") is False

# g = [["a", "b", "c", "e"], ["s", "f", "c", "s"], ["a", "d", "e", "e"]]
# assert sol.exist(g, "abcced") is True
# assert sol.exist(g, "see") is True
# assert sol.exist(g, "abcb") is False
# assert sol.exist(g, "sfdaaa") is False

# the same grid answered twice: a cell left marked breaks the second call
# assert sol.exist(g, "abcced") is True
