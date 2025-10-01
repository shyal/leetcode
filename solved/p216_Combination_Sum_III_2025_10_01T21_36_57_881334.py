"""
URL: https://leetcode.com/problems/combination-sum-iii/description/?envType=study-plan-v2&envId=leetcode-75

216. Combination Sum III

Find all valid combinations of k numbers that sum up to n such that the following conditions are true:

        Only numbers 1 through 9 are used.
        Each number is used at most once.

Return a list of all possible valid combinations. The list must not contain the same combination twice, and the combinations may be returned in any order.


Example 1:

Input: k = 3, n = 7
Output: [[1,2,4]]
Explanation:
1 + 2 + 4 = 7
There are no other valid combinations.

Example 2:

Input: k = 3, n = 9
Output: [[1,2,6],[1,3,5],[2,3,4]]
Explanation:
1 + 2 + 6 = 9
1 + 3 + 5 = 9
2 + 3 + 4 = 9
There are no other valid combinations.

Example 3:

Input: k = 4, n = 1
Output: []
Explanation: There are no valid combinations.
Using 4 different numbers in the range [1,9], the smallest sum we can get is 1+2+3+4 = 10 and since 10 > 1, there are no valid combination.


Constraints:

        2 <= k <= 9
        1 <= n <= 60
"""

from typing import List


class Solution:

    def brute_force(self, k, n):
        from itertools import combinations

        combs = combinations(range(1, 10), k)
        return [list(x) for x in combs if sum(x) == n and len(x) == len(set(x))]

    def combinationSum3(self, k: int, n: int) -> List[List[int]]:
        nums = [i for i in range(1, 10)]

        def dfs(i, curr, prefix=0):
            if len(curr) == k and prefix == n:
                res.append(curr[:])
                return
            for j in range(i, len(nums)):
                curr.append(nums[j])
                prefix += nums[j]
                dfs(j + 1, curr, prefix)
                prefix -= curr.pop()

        res = []
        dfs(0, [])
        return res


s = Solution()

result = s.combinationSum3(3, 7)
expected = [[1, 2, 4]]
assert sorted(map(tuple, result)) == sorted(map(tuple, expected))

result = s.combinationSum3(3, 9)
expected = [[1, 2, 6], [1, 3, 5], [2, 3, 4]]
assert sorted(map(tuple, result)) == sorted(map(tuple, expected))

result = s.combinationSum3(2, 10)
expected = [[1, 9], [2, 8], [3, 7], [4, 6]]
assert sorted(map(tuple, result)) == sorted(map(tuple, expected))

result = s.combinationSum3(1, 5)
expected = [[5]]
assert sorted(map(tuple, result)) == sorted(map(tuple, expected))

result = s.combinationSum3(4, 10)
expected = [[1, 2, 3, 4]]
assert sorted(map(tuple, result)) == sorted(map(tuple, expected))

result = s.combinationSum3(3, 1)
expected = []
assert sorted(map(tuple, result)) == sorted(map(tuple, expected))

result = s.combinationSum3(3, 30)
expected = []
assert sorted(map(tuple, result)) == sorted(map(tuple, expected))

result = s.combinationSum3(9, 45)
expected = [[1, 2, 3, 4, 5, 6, 7, 8, 9]]
assert sorted(map(tuple, result)) == sorted(map(tuple, expected))

result = s.combinationSum3(0, 0)
expected = [[]]
assert sorted(map(tuple, result)) == sorted(map(tuple, expected))

result = s.combinationSum3(5, 15)
expected = s.brute_force(5, 15)
assert sorted(map(tuple, result)) == sorted(map(tuple, expected))

result = s.combinationSum3(4, 24)
expected = s.brute_force(4, 24)
assert sorted(map(tuple, result)) == sorted(map(tuple, expected))

result = s.combinationSum3(2, 1)
expected = []
assert sorted(map(tuple, result)) == sorted(map(tuple, expected))

result = s.combinationSum3(6, 21)
expected = s.brute_force(6, 21)
assert sorted(map(tuple, result)) == sorted(map(tuple, expected))

result = s.combinationSum3(-1, 10)
expected = []
assert sorted(map(tuple, result)) == sorted(map(tuple, expected))

result = s.combinationSum3(10, 45)
expected = []
assert sorted(map(tuple, result)) == sorted(map(tuple, expected))
