"""
URL: https://leetcode.com/problems/maximum-value-of-an-ordered-triplet-ii/description/?envType=problem-list-v2&envId=vn57k9wr

2874. Maximum Value of an Ordered Triplet II

You are given a 0-indexed integer array nums.

Return the maximum value over all triplets of indices (i, j, k) such that i < j < k. If all such triplets have a negative value, return 0.

The value of a triplet of indices (i, j, k) is equal to (nums[i] - nums[j]) * nums[k].

Example 1:

Input: nums = [12,6,1,2,7]
Output: 77
Explanation: The value of the triplet (0, 2, 4) is (nums[0] - nums[2]) * nums[4] = 77.
It can be shown that there are no ordered triplets of indices with a value greater than 77.

Example 2:

Input: nums = [1,10,3,4,19]
Output: 133
Explanation: The value of the triplet (1, 2, 4) is (nums[1] - nums[2]) * nums[4] = 133.
It can be shown that there are no ordered triplets of indices with a value greater than 133.

Example 3:

Input: nums = [1,2,3]
Output: 0
Explanation: The only ordered triplet of indices (0, 1, 2) has a negative value of (nums[0] - nums[1]) * nums[2] = -3. Hence, the answer would be 0.

Constraints:

    3 <= nums.length <= 10^5
    1 <= nums[i] <= 10^6
---
Brute force solution:

def maximumTripletValue(nums: [int]) -> int
  ret res = 0
  for k in range(2, len(nums))
    for j in range(1, k)
      for i in range(0, j)
        res = max(res, (nums[i] - nums[j]) * nums[k])

we want to maximize nums[i] - nums[j] which means looking for the max nums[i] and the min nums[j]

for example, we could sweep k, and pick the min and max before it
this would be an O(n) algorithm. So store all the mins so far, and all the maxes so far

                               i      j
print(sol.maximumTripletValue([12, 6, 1, 2, 7]))  # 77

only works, conincidentally, but doens't work with:

                                   i   j      k
assert sol.maximumTripletValue([1, 10, 3, 4, 19]) == 133

since the mins really has to be the minds ahead of the picked i
so maybe we could store the mins between i and k
"""


# mu 0.7
# def maximumTripletValue(nums: [int]) -> int
#   mins = [*scan(min, nums)]
#   maxes = [*scan(max, nums)]
#   print(mins)
#   print(maxes)
#   ret res = 0
#   for k in range(2, len(nums))
#     res = max(res, (maxes[k-2] - mins[k-1]) * nums[k])

from itertools import accumulate


class Solution:
    def maximumTripletValue(self, nums: list[int]) -> int:
        mins = [*accumulate(nums, min)]
        maxes = [*accumulate(nums, max)]
        print(mins)
        print(maxes)
        res = 0
        for k in range(2, len(nums)):
            res = max(res, (maxes[k - 2] - mins[k - 1]) * nums[k])
        return res


sol = Solution()
_l, _r = sol.maximumTripletValue([1, 10, 3, 4, 19]), 133
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"


# FAILED: walked away after 21m 38s; no working solution.
# Judge the move the defect is in as struggled, not clean. A move the code never reached gets no verdict.
