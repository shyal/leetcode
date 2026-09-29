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
"""


# mu 0.6
# def equalPairs(nums: [int]) -> int
#   c = {:int}
#   sum for n in nums
#     res = c[n]
#     c[n] += 1
#     res

from collections import defaultdict


class Solution:
    def equalPairs(self, nums: list[int]) -> int:
        c = defaultdict(int)
        acc = 0
        for n in nums:
            res = c[n]
            c[n] += 1
            acc += res
        return acc


sol = Solution()
print(sol.equalPairs([1, 2, 3, 1, 1, 3]))
assert sol.equalPairs([1, 2, 3, 1, 1, 3]) == 4
assert sol.equalPairs([1, 2, 3]) == 0
assert sol.equalPairs([1, 1, 1, 1]) == 6
assert sol.equalPairs([5]) == 0
assert sol.equalPairs([4, 4]) == 1
assert sol.equalPairs([4, 5, 4]) == 1
assert sol.equalPairs([1, 2, 1, 2]) == 2
assert sol.equalPairs([7] * 100000) == 4999950000
assert folds(Solution, 'sum', block=True)
