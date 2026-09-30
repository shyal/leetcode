"""
DRILL: Subarray Sum Equals K

Given an array of integers nums and an integer k, return the total number of
subarrays whose sum equals to k.

A subarray is a contiguous non-empty sequence of elements within an array.

Example 1:

Input: nums = [1,1,1], k = 2
Output: 2

Example 2:

Input: nums = [1,2,3], k = 3
Output: 2

Constraints:

    1 <= nums.length <= 2 * 10^4
    -1000 <= nums[i] <= 1000
    -10^7 <= k <= 10^7
"""


# mu 0.7
# def subarraySum(nums: [int], k: int) -> int
#   D = {:int}
#   D[0] = 1
#   ret res, prefix = 0, 0
#   for i, n in nums
#     prefix += n
#     res += D[prefix - k]
#     D[prefix] += 1

from collections import defaultdict


class Solution:
    def subarraySum(self, nums: list[int], k: int) -> int:
        D = defaultdict(int)
        D[0] = 1
        res, prefix = 0, 0
        for i, n in enumerate(nums):
            prefix += n
            res += D[prefix - k]
            D[prefix] += 1
        return res


sol = Solution()
print(sol.subarraySum([1, 1, 1], 2))
assert sol.subarraySum([1, 1, 1], 2) == 2
assert sol.subarraySum([1, 2, 3], 3) == 2
assert sol.subarraySum([], 0) == 0
assert sol.subarraySum([0], 0) == 1
assert sol.subarraySum([1], 1) == 1
assert sol.subarraySum([-1, -1, 1], 0) == 1
assert sol.subarraySum([1000] * 20000, 1000) == 20000
assert sol.subarraySum([1, 2, 3, 4, 5], 15) == 1
assert sol.subarraySum([1, -1, 1, -1, 1], 0) == 6
assert sol.subarraySum([0] * 20000, 0) == 200010000
assert sol.subarraySum([1] * 20000, 2) == 19999
assert sol.subarraySum([-1000] * 20000, -1000) == 20000
assert sol.subarraySum([1, 2, 3, 4, 5], 100) == 0
assert sol.subarraySum([1, 2, -1, 2, -1, 2], 3) == 4
