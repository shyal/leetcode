"""
URL: https://leetcode.com/problems/permutations/description/

46. Permutations

Given an array nums of distinct integers, return all the possible permutations. You can return the answer in any order.


Example 1:
Input: nums = [1,2,3]
Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]
Example 2:
Input: nums = [0,1]
Output: [[0,1],[1,0]]
Example 3:
Input: nums = [1]
Output: [[1]]


Constraints:

        1 <= nums.length <= 6
        -10 <= nums[i] <= 10
        All the integers of nums are unique.
---

Interesting problem!

Can't really think of a solution, so will just
experiment with subset generation as a base, and
try swapping elements instead of skipping them.

Hmm i give up. This is as close as i got.

"""


class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        def swap(i, j, nums):
            nums[i], nums[j] = nums[j], nums[i]
            r = nums[:]
            nums[i], nums[j] = nums[j], nums[i]
            return r

        res = []
        for k in range(len(nums)):
            for i, j in combinations(range(len(nums[k:])), 2):
                res.append(nums[:k] + swap(i, j, nums[k:]))
        return res


sol = Solution()
res = sol.permute(nums=[1, 2, 3])
# print(res)
