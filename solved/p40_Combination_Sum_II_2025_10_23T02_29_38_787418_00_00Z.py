"""
URL: https://leetcode.com/problems/combination-sum-ii/description/

40. Combination Sum II

Given a collection of candidate numbers (candidates) and a target number (target), find all unique combinations in candidates where the candidate numbers sum to target.

Each number in candidates may only be used once in the combination.

Note: The solution set must not contain duplicate combinations.


Example 1:

Input: candidates = [10,1,2,7,6,1,5], target = 8
Output:
[
[1,1,6],
[1,2,5],
[1,7],
[2,6]
]

Example 2:

Input: candidates = [2,5,2,1,2], target = 5
Output:
[
[1,2,2],
[5]
]


Constraints:

        1 <= candidates.length <= 100
        1 <= candidates[i] <= 50
        1 <= target <= 30
"""


class Solution:

    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        def dfs(i, prefix=0):
            if prefix == target:
                res.append([*sorted(subset[:])])
                return
            prev = None
            for j in range(i, len(candidates)):
                if candidates[j] == prev:
                    continue
                prev = candidates[j]
                if prefix + candidates[j] <= target:
                    subset.append(candidates[j])
                    dfs(j + 1, prefix + candidates[j])
                    subset.pop()

        candidates.sort()
        res = []
        subset = []
        dfs(0)
        return [x for x in sorted(res)]


sol = Solution()
res = sol.combinationSum2(candidates=[10, 1, 2, 7, 6, 1, 5], target=8)
assert res == [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]


res = sol.combinationSum2(candidates=[2, 5, 2, 1, 2], target=5)
assert res == [[1, 2, 2], [5]]

TLE = [
    14,
    6,
    25,
    9,
    30,
    20,
    33,
    34,
    28,
    30,
    16,
    12,
    31,
    9,
    9,
    12,
    34,
    16,
    25,
    32,
    8,
    7,
    30,
    12,
    33,
    20,
    21,
    29,
    24,
    17,
    27,
    34,
    11,
    17,
    30,
    6,
    32,
    21,
    27,
    17,
    16,
    8,
    24,
    12,
    12,
    28,
    11,
    33,
    10,
    32,
    22,
    13,
    34,
    18,
    12,
]
res = sol.combinationSum2(candidates=TLE, target=27)
TLE = [
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
]
res = sol.combinationSum2(candidates=TLE, target=30)
