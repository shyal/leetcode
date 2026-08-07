"""
DRILL: Level Groups
TRAINS: tree-bfs-levels

An n-ary tree is encoded as nested lists: each node is [value, *children].
Return the node values grouped by depth, top to bottom, left to right
within each level.

Example 1:

Input: tree = [1, [2, [4]], [3, [5], [6]]]
Output: [[1], [2, 3], [4, 5, 6]]
Explanation:
    depth 0: 1
    depth 1: 2, 3
    depth 2: 4 (child of 2), 5 and 6 (children of 3)

Example 2:

Input: tree = [7]
Output: [[7]]

Example 3:

Input: tree = [1, [2, [3, [4, [5]]]]]
Output: [[1], [2], [3], [4], [5]]  (a vine: one node per level)

Constraints:

    1 <= total nodes <= 10^4

    REQUIRED: iterative, with a queue (collections.deque). NO recursion,
    no depth bookkeeping carried on the nodes. Process one whole level
    per outer-loop iteration: snapshot how many nodes the queue holds,
    drain exactly that many, append their children behind them.
    Depth is the count of layers you have drained - nothing else.
"""

from collections import deque
from typing import List


class Solution:

    def levelGroups(self, tree: list) -> List[List[int]]:
        raise NotImplementedError


if __name__ == "__main__":
    s = Solution()
    assert s.levelGroups([1, [2, [4]], [3, [5], [6]]]) == [[1], [2, 3], [4, 5, 6]]
    assert s.levelGroups([7]) == [[7]]
    assert s.levelGroups([1, [2, [3, [4, [5]]]]]) == [[1], [2], [3], [4], [5]]
    assert s.levelGroups([1, [2], [3], [4]]) == [[1], [2, 3, 4]]
    print("ok")
