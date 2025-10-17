"""
URL: https://leetcode.com/problems/combinations/description/

77. Combinations

Given two integers n and k, return all possible combinations of k numbers chosen from the range [1, n].

You may return the answer in any order.


Example 1:

Input: n = 4, k = 2
Output: [[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]
Explanation: There are 4 choose 2 = 6 total combinations.
Note that combinations are unordered, i.e., [1,2] and [2,1] are considered to be the same combination.

Example 2:

Input: n = 1, k = 1
Output: [[1]]
Explanation: There is 1 choose 1 = 1 total combination.


Constraints:

        1 <= n <= 20
        1 <= k <= n

---

This solution is correct but suboptimial because it lacks prunine.
Revisit.

"""


class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        def dfs(i):
            if len(sub) == k:
                res.append(sub[:])
            future_choices = range(i, n)
            for j in future_choices:
                sub.append(j + 1)
                dfs(j + 1)
                sub.pop()

        res, sub = [], []
        dfs(0)
        return res


sol = Solution()
res = sol.combine(n=4, k=2)
# print(res)

assert res == [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]
