"""
URL: https://leetcode.com/problems/find-ultimate-boss/description/

2850. Find Ultimate Boss

You are given an integer n representing the number of employees in a company, labeled from 0 to n-1. You are also given an array boss of length n, where boss[i] is the direct boss of employee i. If boss[i] == -1, then employee i has no boss and is a top-level boss themselves.

The hierarchy forms a forest (multiple trees, no cycles). Your task is to return an array ans of length n, where ans[i] is the ultimate boss (the root of the tree, i.e., the top-level boss) for employee i.

Implement this using a find function with path compression for efficiency, though the parent array may be modified in the process.

Example 1:

Input: n = 5, boss = [-1, 0, 1, 2, 2]
Output: [0, 0, 0, 0, 0]
Explanation:
- Employee 0 is top-level (-1 means root).
- 1 reports to 0 → ultimate 0
- 2 reports to 1 → ultimate 0
- 3 reports to 2 → ultimate 0
- 4 reports to 2 → ultimate 0

Example 2:

Input: n = 3, boss = [-1, -1, -1]
Output: [0, 1, 2]
Explanation: All are top-level bosses.

Example 3:

Input: n = 4, boss = [1, 2, 3, -1]
Output: [3, 3, 3, 3]
Explanation: Chain 0 → 1 → 2 → 3 (root).

Constraints:

    1 <= n <= 2000
    boss.length == n
    -1 <= boss[i] < n
    boss[i] != i (no self-boss except implied by -1)
    The hierarchy forms a valid forest (no cycles, each non-root has exactly one boss)

"""


class Solution:
    def findUltimateBoss(self, n: int, boss: List[int]) -> List[int]:
        parent = [(i if boss[i] == -1 else boss[i]) for i in range(n)]

        def find(x: int) -> int:
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        ans = [0] * n
        for i in range(n):
            ans[i] = find(i)
        return ans


sol = Solution()

sol.findUltimateBoss(5, [-1, 0, 1, 2, 2])


assert sol.findUltimateBoss(5, [-1, 0, 1, 2, 2]) == [0, 0, 0, 0, 0]
assert sol.findUltimateBoss(3, [-1, -1, -1]) == [0, 1, 2]
assert sol.findUltimateBoss(4, [1, 2, 3, -1]) == [3, 3, 3, 3]
assert sol.findUltimateBoss(1, [-1]) == [0]
assert sol.findUltimateBoss(2, [-1, 0]) == [0, 0]
assert sol.findUltimateBoss(2, [1, -1]) == [1, 1]
assert sol.findUltimateBoss(6, [-1, 0, 0, 1, 1, -1]) == [0, 0, 0, 0, 0, 5]
