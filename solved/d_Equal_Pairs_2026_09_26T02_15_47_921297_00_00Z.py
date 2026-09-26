"""
DRILL: Equal Pairs

Given an integer array nums, return the number of index pairs (i, j) with
i < j and nums[i] == nums[j].

Example 1:

Input: nums = [1, 2, 3, 1, 1, 3]
Output: 4
Explanation: The three 1s make 3 pairs and the two 3s make 1.

Example 2:

Input: nums = [1, 2, 3]
Output: 0

Constraints:

    1 <= len(nums) <= 10^5
    1 <= nums[i] <= 1000

    REQUIRED: O(n), one pass over nums. NO accumulator variable. NO
    enumeration of index pairs. NO arithmetic on group sizes.
---
Learning
"""


# mu 0.4
# def equalPairs(nums: [int]) -> int
#   cnt = counter()
#   sum for x in nums
#     got = cnt[x]
#     cnt[x] += 1
#     got

from collections import Counter


class Solution:
    def equalPairs(self, nums: list[int]) -> int:
        cnt = Counter()
        acc = 0
        for x in nums:
            got = cnt[x]
            cnt[x] += 1
            acc += got
        return acc


sol = Solution()
print(sol.equalPairs([1, 2, 3, 1, 1, 3]))
