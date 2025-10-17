"""
URL: https://leetcode.com/problems/subsets/description/

78. Subsets

Given an integer array nums of unique elements, return all possible subsets (the power set).

The solution set must not contain duplicate subsets. Return the solution in any order.


Example 1:

Input: nums = [1,2,3]
Output: [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]

Example 2:

Input: nums = [0]
Output: [[],[0]]


Constraints:

        1 <= nums.length <= 10
        -10 <= nums[i] <= 10
        All the numbers of nums are unique.
"""


class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        def dfs(i):
            res.append(sub[:])
            for j in range(i, len(nums)):
                sub.append(nums[j])
                dfs(j + 1)
                sub.pop()

        sub, res = [], []
        dfs(0)
        return res


sol = Solution()
res = sol.subsets(nums=[1, 2, 3])
assert res == [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]
