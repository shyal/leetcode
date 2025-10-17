"""
URL: https://leetcode.com/problems/subsets-ii/description/

90. Subsets II

Given an integer array nums that may contain duplicates, return all possible subsets (the power set).

The solution set must not contain duplicate subsets. Return the solution in any order.


Example 1:
Input: nums = [1,2,2]
Output: [[],[1],[1,2],[1,2,2],[2],[2,2]]
Example 2:
Input: nums = [0]
Output: [[],[0]]


Constraints:

        1 <= nums.length <= 10
        -10 <= nums[i] <= 10

---

My first thought is to add the subsets to a set, but
let's explore whether there's a more elegant way of
doing this.

So it seems that sorting the input, and pruning paths
using a `prev` variable is the right solution.

I find it a bit unintuitive that sorting works, because
i would have assumed that the subsets would have to be
interally in the same order.

Solved.
"""


class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        def dfs(i, depth=0):
            res.append(sub[:])
            future_choices = [*range(i, len(nums))]
            if future_choices:
                prev = None
                for j in future_choices:
                    if prev == nums[j]:
                        continue
                    sub.append(nums[j])
                    dfs(j + 1, depth + 1)
                    prev = sub.pop()

        nums.sort()
        res, sub = [], []
        dfs(0)
        return res


sol = Solution()

res = sol.subsetsWithDup([1, 1, 2, 2, 3, 3, 1])
assert res == [
    [],
    [1],
    [1, 1],
    [1, 1, 1],
    [1, 1, 1, 2],
    [1, 1, 1, 2, 2],
    [1, 1, 1, 2, 2, 3],
    [1, 1, 1, 2, 2, 3, 3],
    [1, 1, 1, 2, 3],
    [1, 1, 1, 2, 3, 3],
    [1, 1, 1, 3],
    [1, 1, 1, 3, 3],
    [1, 1, 2],
    [1, 1, 2, 2],
    [1, 1, 2, 2, 3],
    [1, 1, 2, 2, 3, 3],
    [1, 1, 2, 3],
    [1, 1, 2, 3, 3],
    [1, 1, 3],
    [1, 1, 3, 3],
    [1, 2],
    [1, 2, 2],
    [1, 2, 2, 3],
    [1, 2, 2, 3, 3],
    [1, 2, 3],
    [1, 2, 3, 3],
    [1, 3],
    [1, 3, 3],
    [2],
    [2, 2],
    [2, 2, 3],
    [2, 2, 3, 3],
    [2, 3],
    [2, 3, 3],
    [3],
    [3, 3],
]
