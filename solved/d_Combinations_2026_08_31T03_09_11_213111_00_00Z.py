"""
DRILL: Combinations
TRAINS: backtracking-start-index

Given two integers n and k, return every combination of k distinct
integers chosen from 1 to n. List each combination in increasing order,
and list the combinations in lexicographic order.

Example 1:

Input: n = 4, k = 2
Output: [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]

Example 2:

Input: n = 3, k = 3
Output: [[1, 2, 3]]

Constraints:

    1 <= n <= 20
    1 <= k <= n

    REQUIRED: never build [2, 1], not even to discard it. NO swapping
    elements of a list, NO used or visited set, NO itertools, NO sorting
    or de-duplicating the answer at the end.

---

Looked up a past solution.

"""


class Solution:
    def combine(self, n: int, k: int) -> list[list[int]]:
        def dp(i):
            if len(sub) == k:
                res.append(sub[::])
                return
            for j in range(i, n):
                sub.append(j + 1)
                dp(j + 1)
                sub.pop()

        res, sub = [], []
        dp(0)
        return res


sol = Solution()

print(sol.combine(4, 2))  # [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]

assert sol.combine(4, 2) == [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]
assert sol.combine(1, 1) == [[1]]
assert sol.combine(3, 3) == [[1, 2, 3]]
assert sol.combine(3, 1) == [[1], [2], [3]]

res = sol.combine(9, 3)
assert len(res) == 84
assert len({tuple(c) for c in res}) == 84
assert all(len(c) == 3 and c == sorted(c) for c in res)

res = sol.combine(20, 2)
assert len(res) == 190
assert all(1 <= a < b <= 20 for a, b in res)
