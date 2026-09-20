"""
URL: https://leetcode.com/problems/combination-sum-ii/description/?envType=problem-list-v2&envId=vn57k9wr

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

LEETCODE: Accepted (23 ms, 19.6 MB)
"""


class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        def helper(i, total):
            if total == target:
                res.append(path[:])
                return
            if total > target:
                return
            for j in range(i, len(candidates)):
                if j > i and candidates[j] == candidates[j - 1]:
                    continue
                path.append(candidates[j])
                helper(j + 1, total + candidates[j])
                path.pop()

        candidates.sort()
        path, res = [], []
        helper(0, 0)
        return res


sol = Solution()

# print_orig(
#     sol.combinationSum2([10, 1, 2, 7, 6, 1, 5], 8)
# )  # [[1,1,6],[1,2,5],[1,7],[2,6]]

assert sorted(sol.combinationSum2([10, 1, 2, 7, 6, 1, 5], 8)) == sorted(
    [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]
)
assert sorted(sol.combinationSum2([2, 5, 2, 1, 2], 5)) == sorted([[1, 2, 2], [5]])

assert sol.combinationSum2([], 0) == [[]]
assert sol.combinationSum2([], 10) == []
assert sol.combinationSum2([1], 1) == [[1]]
assert sol.combinationSum2([1], 2) == []
assert sol.combinationSum2([1, 1, 1, 1], 2) == [[1, 1]]
assert sol.combinationSum2([50] * 100, 50) == [[50]]
assert sol.combinationSum2([50] * 100, 100) == [[50, 50]]
assert sol.combinationSum2([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 15) == [
    [1, 2, 3, 4, 5],
    [1, 2, 3, 9],
    [1, 2, 4, 8],
    [1, 2, 5, 7],
    [1, 3, 4, 7],
    [1, 3, 5, 6],
    [1, 4, 10],
    [1, 5, 9],
    [1, 6, 8],
    [2, 3, 4, 6],
    [2, 3, 10],
    [2, 4, 9],
    [2, 5, 8],
    [2, 6, 7],
    [3, 4, 8],
    [3, 5, 7],
    [4, 5, 6],
    [5, 10],
    [6, 9],
    [7, 8],
]
assert sol.combinationSum2([1, 1, 2, 2, 3, 3, 4, 4, 5, 5], 10) == [
    [1, 1, 2, 2, 4],
    [1, 1, 2, 3, 3],
    [1, 1, 3, 5],
    [1, 1, 4, 4],
    [1, 2, 2, 5],
    [1, 2, 3, 4],
    [1, 4, 5],
    [2, 2, 3, 3],
    [2, 3, 5],
    [2, 4, 4],
    [3, 3, 4],
    [5, 5],
]
assert sol.combinationSum2([5, 5, 5, 5, 5, 5, 5, 5, 5, 5], 15) == [[5, 5, 5]]
assert sol.combinationSum2([1, 2, 3, -1, -2, -3], 0) == [[]]
assert sol.combinationSum2([2, 3, 6, 7], 7) == [[7]]
