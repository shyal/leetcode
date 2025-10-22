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
---

An approach might be to generate all subsets, and checking if their
sum equals target.

To avoid duplicates subsets, we put them in a set.

I'll do that as a first pass, then optimize.

Great so seems to work, but we hit a TLE on long inputs, so a prefix
optimization is likely required, also better pruning, i.e
if the prefix is greater than target, no more need to explore.

Well sadly i'm still hitting a TLE when many repeats, and i'm running
out of time to solve this question. I'll mark it as 'learning'
and go through the logic carefully before re-attempting,
to better understand pruning for the repeats.

Reschedule.
"""


class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        def dfs(i, prefix):
            if prefix == target:
                res.add(tuple(subset[:]))
                return False
            if prefix > target:
                return -1
            prev = None
            for j in range(i, len(candidates)):
                subset.append(candidates[j])
                r = dfs(j + 1, prefix + candidates[j])
                subset.pop()
                if r == False:
                    if prev == candidates[j]:
                        break
                prev = candidates[j]
                if r == -1:
                    break
            return True

        candidates.sort()
        res = set([])
        subset = []
        dfs(0, 0)
        return [list(x) for x in res]


sol = Solution()

res = sol.combinationSum2(candidates=[10, 1, 2, 7, 6, 1, 5], target=8)
assert res == [[1, 7], [1, 1, 6], [1, 2, 5], [2, 6]]

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
# print(res)
# assert res == [[1, 2, 2], [5]]

# TLE = [
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
#     1,
# ]
# res = sol.combinationSum2(candidates=TLE, target=30)
# print(res)
