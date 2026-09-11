"""
URL: https://leetcode.com/problems/combination-sum/description/?envType=problem-list-v2&envId=vn57k9wr

39. Combination Sum

Given an array of distinct integers candidates and a target integer target, return a list of all unique combinations of candidates where the chosen numbers sum to target. You may return the combinations in any order.

The same number may be chosen from candidates an unlimited number of times. Two combinations are unique if the frequency of at least one of the chosen numbers is different.

The test cases are generated such that the number of unique combinations that sum up to target is less than 150 combinations for the given input.

Example 1:

Input: candidates = [2,3,6,7], target = 7
Output: [[2,2,3],[7]]
Explanation:
2 and 3 are candidates, and 2 + 2 + 3 = 7. Note that 2 can be used multiple times.
7 is a candidate, and 7 = 7.
These are the only two combinations.

Example 2:

Input: candidates = [2,3,5], target = 8
Output: [[2,2,2,2],[2,3,3],[3,5]]

Example 3:

Input: candidates = [2], target = 1
Output: []

Constraints:

    1 <= candidates.length <= 30
    2 <= candidates[i] <= 40
    All elements of candidates are distinct.
    1 <= target <= 40
"""


class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        def helper(i, total):
            if total == target:
                res.append(path[:])

            if total > target:
                return

            for j in range(i, len(candidates)):
                path.append(candidates[j])
                helper(j, total + candidates[j])
                path.pop()

        res, path = [], []
        helper(0, 0)
        return res


sol = Solution()

print(sol.combinationSum([2, 3, 6, 7], 7))  # [[2,2,3],[7]]

assert sol.combinationSum([2, 3, 6, 7], 7) == [[2, 2, 3], [7]]
assert sol.combinationSum([2, 3, 5], 8) == [[2, 2, 2, 2], [2, 3, 3], [3, 5]]
assert sol.combinationSum([2], 1) == []

assert sol.combinationSum([1], 1) == [[1]]
assert sol.combinationSum([1], 2) == [[1, 1]]
assert sol.combinationSum([2, 3, 5], 0) == [[]]
assert sol.combinationSum([40], 40) == [[40]]
assert sol.combinationSum([2, 4, 6, 8, 10], 20) == [
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 4],
    [2, 2, 2, 2, 2, 2, 2, 6],
    [2, 2, 2, 2, 2, 2, 4, 4],
    [2, 2, 2, 2, 2, 2, 8],
    [2, 2, 2, 2, 2, 4, 6],
    [2, 2, 2, 2, 2, 10],
    [2, 2, 2, 2, 4, 4, 4],
    [2, 2, 2, 2, 4, 8],
    [2, 2, 2, 2, 6, 6],
    [2, 2, 2, 4, 4, 6],
    [2, 2, 2, 4, 10],
    [2, 2, 2, 6, 8],
    [2, 2, 4, 4, 4, 4],
    [2, 2, 4, 4, 8],
    [2, 2, 4, 6, 6],
    [2, 2, 6, 10],
    [2, 2, 8, 8],
    [2, 4, 4, 4, 6],
    [2, 4, 4, 10],
    [2, 4, 6, 8],
    [2, 6, 6, 6],
    [2, 8, 10],
    [4, 4, 4, 4, 4],
    [4, 4, 4, 8],
    [4, 4, 6, 6],
    [4, 6, 10],
    [4, 8, 8],
    [6, 6, 8],
    [10, 10],
]
assert sol.combinationSum([3, 5, 7], 1) == []
assert sol.combinationSum([2, 3, 5], 7) == [[2, 2, 3], [2, 5]]
assert sol.combinationSum([2, 3, 5], 1) == []
assert sol.combinationSum([2], 40) == [
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
]
