"""
DRILL: Divisible Difference Pairs

Given an integer array nums and an integer m, return the number of index
pairs (i, j) with i < j such that nums[j] - nums[i] is divisible by m.
Values can be negative.

Example 1:

Input: nums = [1, 6, 3, 11, 8], m = 5
Output: 4
Explanation: 1, 6 and 11 make 3 pairs, and 3 and 8 make 1.

Example 2:

Input: nums = [-3, 7, 2], m = 5
Output: 3
Explanation: 7 - (-3) = 10, 2 - (-3) = 5 and 2 - 7 = -5 are all divisible
by 5.

Example 3:

Input: nums = [1, 2, 3], m = 4
Output: 0

Constraints:

    1 <= len(nums) <= 10^5
    -10^4 <= nums[i] <= 10^4
    2 <= m <= 10^4

    REQUIRED: O(n), one pass over nums. NO enumeration of index pairs.
---
Learning
"""


# mu 0.7
# def divisiblePairs(nums: [int], m: int) -> int
#   cnt = counter()
#   ret res = 0
#   for n in nums
#     res += cnt[n % m]
#     cnt[n % m] += 1

from collections import Counter


class Solution:
    def divisiblePairs(self, nums: list[int], m: int) -> int:
        cnt = Counter()
        res = 0
        for n in nums:
            res += cnt[n % m]
            cnt[n % m] += 1
        return res


sol = Solution()
print(sol.divisiblePairs([1, 6, 3, 11, 8], 5))
assert sol.divisiblePairs([1, 6, 3, 11, 8], 5) == 4
assert sol.divisiblePairs([-3, 7, 2], 5) == 3
assert sol.divisiblePairs([1, 2, 3], 4) == 0
assert sol.divisiblePairs([5], 2) == 0
assert sol.divisiblePairs([4, 4], 3) == 1
assert sol.divisiblePairs([0, 5, 10], 5) == 3
assert sol.divisiblePairs([-1, 1], 2) == 1
assert sol.divisiblePairs([-1, 1], 3) == 0
assert sol.divisiblePairs([2, 9, 9, 4], 7) == 3
assert sol.divisiblePairs([7] * 10 ** 5, 7) == 4999950000
assert sol.divisiblePairs(list(range(0, 10 ** 5)), 10 ** 4) == 450000
