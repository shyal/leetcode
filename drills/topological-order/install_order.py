"""
DRILL: Install Order
TRAINS: topological-order

Given n packages numbered 0 to n - 1 and deps, where deps[i] = [a, b]
means package a must be installed before package b, return an order that
installs every package. If several orders work, return any of them. If no
order installs every package, return an empty list.

Example 1:

Input: n = 4, deps = [[2, 0], [0, 3], [3, 1], [2, 3]]
Output: [2, 0, 3, 1]
Explanation: nothing has to come before 2, so it goes first. Then 0 is
free, then 3, then 1.

Example 2:

Input: n = 3, deps = [[0, 1], [1, 2], [2, 1]]
Output: []
Explanation: 1 and 2 each wait for the other, so neither is ever
installed.

Constraints:

    1 <= n <= 2000
    0 <= len(deps) <= 5000
    deps[i] = [a, b] with 0 <= a, b < n and a != b
    no pair appears twice

    REQUIRED: must run in O(n + len(deps)) time. NO rescanning every
    package each time one is installed; NO recursion.
"""


class Solution:

    def installOrder(self, n: int, deps: List[List[int]]) -> List[int]:
        pass


sol = Solution()

print(sol.installOrder(4, [[2, 0], [0, 3], [3, 1], [2, 3]]))  # [2, 0, 3, 1]

# assert sol.installOrder(4, [[2, 0], [0, 3], [3, 1], [2, 3]]) == [2, 0, 3, 1]
# assert sol.installOrder(3, [[0, 1], [1, 2], [2, 1]]) == []
# assert sol.installOrder(1, []) == [0]
# assert sol.installOrder(3, [[1, 0], [0, 2], [1, 2]]) == [1, 0, 2]
# assert sol.installOrder(2, [[0, 1], [1, 0]]) == []
