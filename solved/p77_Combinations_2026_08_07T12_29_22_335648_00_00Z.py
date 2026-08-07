"""
URL: https://leetcode.com/problems/combinations/description/?envType=problem-list-v2&envId=vn57k9wr

77. Combinations

Given two integers n and k, return all possible combinations of k numbers
chosen from the range [1, n].

You may return the answer in any order.


Example 1:

Input: n = 4, k = 2
Output: [[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]
Explanation: There are 4 choose 2 = 6 total combinations.
Note that combinations are unordered, i.e., [1,2] and [2,1] are considered
to be the same combination.

Example 2:

Input: n = 1, k = 1
Output: [[1]]
Explanation: There is 1 choose 1 = 1 total combination.


Constraints:

    1 <= n <= 20
    1 <= k <= n
"""


class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        ret = []
        curr = []
        def dp(i):
            if len(curr) == k:
                ret.append(curr[:])
                return
            for j in range(i, n):
                curr.append(j + 1)
                dp(j + 1)
                curr.pop()
        dp(0)
        return ret


sol = Solution()

# print(sol.combine(4, 2))  # [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]

assert sorted(sol.combine(4, 2)) == [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]
assert sorted(sol.combine(1, 1)) == [[1]]
assert sorted(sol.combine(4, 3)) == [[1, 2, 3], [1, 2, 4], [1, 3, 4], [2, 3, 4]]
assert sorted(sol.combine(3, 2)) == [[1, 2], [1, 3], [2, 3]]
assert sorted(sol.combine(5, 1)) == [[1], [2], [3], [4], [5]]
assert sorted(sol.combine(5, 5)) == [[1, 2, 3, 4, 5]]
assert sorted(sol.combine(2, 2)) == [[1, 2]]
assert sol.combine(20, 20) == [list(range(1, 21))]
assert len(sol.combine(20, 1)) == 20
assert len(sol.combine(20, 2)) == 190
assert len(sol.combine(10, 3)) == 120
assert len(sol.combine(12, 6)) == 924

result = sol.combine(6, 3)
assert len(result) == 20
assert len({tuple(c) for c in result}) == 20
assert all(len(c) == 3 for c in result)
assert all(c == sorted(c) for c in result)
assert all(len(set(c)) == len(c) for c in result)
assert all(1 <= x <= 6 for c in result for x in c)