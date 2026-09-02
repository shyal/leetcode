"""
DRILL: Build Parents
TRAINS: union-find

Given n, the number of employees, labeled 0 to n - 1, return the list
parent, where parent[i] is the manager of employee i. Nobody has been
assigned a manager yet, so every employee is their own manager.

Example 1:

Input: n = 4
Output: [0, 1, 2, 3]

Example 2:

Input: n = 1
Output: [0]

Constraints:

    1 <= n <= 1000

    REQUIRED: must run in O(n) time and return a list the caller can
    assign into. NO dict; NO range object.
"""


class Solution:

    def buildParent(self, n: int) -> List[int]:
        pass


sol = Solution()

print(sol.buildParent(4))  # [0, 1, 2, 3]

# assert sol.buildParent(4) == [0, 1, 2, 3]
# assert sol.buildParent(1) == [0]
# parent = sol.buildParent(3)
# parent[1] = 0
# assert parent == [0, 0, 2]
