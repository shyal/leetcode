"""
DRILL: Unequal Pairs

Given an integer array nums, return the number of index pairs (i, j) with
i < j and nums[i] != nums[j].

Example 1:

Input: nums = [5, 1, 5, 2, 1, 5]
Output: 11
Explanation: Of the 15 index pairs, 3 pair two 5s and 1 pairs two 1s.
The other 11 pair different values.

Example 2:

Input: nums = [6, 6, 6]
Output: 0

Example 3:

Input: nums = [1, 2, 3, 4]
Output: 6

Constraints:

    1 <= len(nums) <= 10^5
    1 <= nums[i] <= 1000

    REQUIRED: O(n), one pass over the group sizes. NO enumeration of index
    pairs. NO subtraction from the total pair count.
"""


class Solution:

    def unequalPairs(self, nums: List[int]) -> int:
        pass


sol = Solution()

print(sol.unequalPairs([5, 1, 5, 2, 1, 5]))  # 11

# assert sol.unequalPairs([5, 1, 5, 2, 1, 5]) == 11
# assert sol.unequalPairs([6, 6, 6]) == 0
# assert sol.unequalPairs([1, 2, 3, 4]) == 6
# assert sol.unequalPairs([7]) == 0
# assert sol.unequalPairs([1, 2]) == 1
# assert sol.unequalPairs([2, 2, 1]) == 2
# assert sol.unequalPairs([1, 2, 3] * 3) == 27
# assert sol.unequalPairs([1, 1, 2, 2, 3, 3]) == 12
# assert sol.unequalPairs(list(range(1, 1001))) == 499500
# assert sol.unequalPairs([9] * 99999 + [8]) == 99999
# assert sol.unequalPairs([1] * 50000 + [2] * 50000) == 2500000000
