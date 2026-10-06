"""
URL: https://leetcode.com/problems/minimum-sum-of-mountain-triplets-ii/description/?envType=problem-list-v2&envId=vn57k9wr

2909. Minimum Sum of Mountain Triplets II

You are given a 0-indexed array nums of integers.

A triplet of indices (i, j, k) is a mountain if:

- i < j < k
- nums[i] < nums[j] and nums[k] < nums[j]

Return the minimum possible sum of a mountain triplet of nums. If no such triplet exists, return -1.

Example 1:

Input: nums = [8,6,1,5,3]
Output: 9
Explanation: Triplet (2, 3, 4) is a mountain triplet of sum 9 since:
- 2 < 3 < 4
- nums[2] < nums[3] and nums[4] < nums[3]
And the sum of this triplet is nums[2] + nums[3] + nums[4] = 9. It can be shown that there are no mountain triplets with a sum of less than 9.

Example 2:

Input: nums = [5,4,8,7,10,2]
Output: 13
Explanation: Triplet (1, 3, 5) is a mountain triplet of sum 13 since:
- 1 < 3 < 5
- nums[1] < nums[3] and nums[5] < nums[3]
And the sum of this triplet is nums[1] + nums[3] + nums[5] = 13. It can be shown that there are no mountain triplets with a sum of less than 13.

Example 3:

Input: nums = [6,5,4,3,4,5]
Output: -1
Explanation: It can be shown that there are no mountain triplets in nums.

Constraints:

    3 <= nums.length <= 10^5
    1 <= nums[i] <= 10^8
---
Brute force solution.

TLE on lc

def minimumSum(nums: [int]) -> int
  res = inf
  for j in 1..len(nums) - 2
    for i in 0..j-1
      for k in j+1..len(nums)-1
        if nums[i] < nums[j] and nums[k] < nums[j]
          res = min(nums[i] + nums[j] + nums[k], res)
  res or -1 if inf

insight: we can pre-compute which is are small than js
and pre-compute which ks are smaller than js

this avoids the cubic time complexity

I don't know. I was only able to produce the brute force solution.

LEETCODE: Time Limit Exceeded (730/788 cases)
"""


# mu 0.7
# def minimumSum(nums: [int]) -> int
#   res = inf
#   for j in 1..len(nums) - 2
#     for i in 0..j-1
#       for k in j+1..len(nums)-1
#         if nums[i] < nums[j] and nums[k] < nums[j]
#           res = min(nums[i] + nums[j] + nums[k], res)
#   res or -1 if inf
#
# # def minimumSum(nums: [int]) -> int
#   # lt = table(len(nums), len(nums), fill=False)
#   # gt = table(len(nums), len(nums), fill=False)
#   # for j in 1..len(nums) - 2
#   #   for i in 0..j-1
#   #     if nums[i] < nums[j]
#   #       lt[i][j] = True
#   # tabulate(lt)
#   # for j in 1..len(nums) - 2
#   #   for k in j+1..len(nums) - 1
#   #     if nums[j] > nums[k]
#   #       gt[j][k] = True
#   # tabulate(gt)
#
#   # for j in 1..len(nums) - 2
#   #   i_candidates = []
#   #   for i in 0..j -1
#   #     if nums[i] < nums[j]
#   #       print(nums[i], nums[j])
#   #   for k in j+1..len(nums) - 1
#   #     if nums[j] > nums[k]
#   #       print('         ', nums[j], nums[k])

from math import inf


class Solution:
    def minimumSum(self, nums: list[int]) -> int:
        res = inf
        for j in range(1, len(nums) - 2 + 1):
            for i in range(0, j - 1 + 1):
                for k in range(j + 1, len(nums) - 1 + 1):
                    if nums[i] < nums[j] and nums[k] < nums[j]:
                        res = min(nums[i] + nums[j] + nums[k], res)
        return (-1 if res == inf else res)


sol = Solution()
print(sol.minimumSum([8, 6, 1, 5, 3]))
assert sol.minimumSum([8, 6, 1, 5, 3]) == 9
assert sol.minimumSum([5, 4, 8, 7, 10, 2]) == 13
assert sol.minimumSum([6, 5, 4, 3, 4, 5]) == -1
assert sol.minimumSum([1, 2, 3]) == -1
assert sol.minimumSum([3, 2, 1]) == -1
assert sol.minimumSum([1, 3, 2]) == 6
assert sol.minimumSum([2, 3, 2, 1, 2, 3, 1]) == 4
assert sol.minimumSum([10 ** 8, 1, 10 ** 8]) == -1
assert sol.minimumSum([1, 1, 1, 1, 1]) == -1
assert sol.minimumSum([1, 2, 1, 2, 1, 2]) == 4
assert sol.minimumSum([2, 2, 2, 3, 2, 2, 2]) == 7
assert sol.minimumSum([1, 100, 1, 100, 1, 100, 1]) == 102
assert sol.minimumSum([5, 1, 5, 1, 5, 1, 5]) == 7
assert sol.minimumSum([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) == -1
assert sol.minimumSum([10, 9, 8, 7, 6, 5, 4, 3, 2, 1]) == -1
