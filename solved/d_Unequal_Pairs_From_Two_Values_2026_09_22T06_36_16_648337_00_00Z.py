"""
DRILL: Unequal Pairs From Two Values

Given an integer array nums that contains exactly two distinct values,
return the number of index pairs (i, j) with i < j and nums[i] != nums[j].

Example 1:

Input: nums = [4, 4, 2, 4, 2]
Output: 6
Explanation: Each of the three 4s pairs with each of the two 2s.

Example 2:

Input: nums = [7, 7, 7, 7, 1]
Output: 4

Example 3:

Input: nums = [5, 3]
Output: 1

Constraints:

    2 <= len(nums) <= 10^5
    1 <= nums[i] <= 1000
    nums has exactly two distinct values

    REQUIRED: O(n). NO enumeration of index pairs.
"""


class Solution:

    def unequalPairs(self, nums: List[int]) -> int:
        a, b = Counter(nums).values()
        return a * b


sol = Solution()

print(sol.unequalPairs([4, 4, 2, 4, 2]))  # 6

assert sol.unequalPairs([4, 4, 2, 4, 2]) == 6
assert sol.unequalPairs([7, 7, 7, 7, 1]) == 4
assert sol.unequalPairs([5, 3]) == 1
assert sol.unequalPairs([1, 2, 1, 2, 1, 2]) == 9
assert sol.unequalPairs([2, 1, 1, 1, 1, 1]) == 5
assert sol.unequalPairs([9] * 99999 + [8]) == 99999
assert sol.unequalPairs([1] * 50000 + [2] * 50000) == 2500000000
