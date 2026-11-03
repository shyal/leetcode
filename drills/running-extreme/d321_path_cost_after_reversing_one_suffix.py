"""
Given an integer array nums, return the smallest total cost of the path
0, nums[0], nums[1], ..., nums[-1] after you reverse one suffix of nums.
Each pair of consecutive values a, b on the path costs abs(a - b).
Before you cost the path you reverse a suffix nums[k:] for any index k;
the last element alone counts, and reversing it changes nothing.

A reversed suffix has the same consecutive pairs in reverse order, so
every pair inside it costs the same as before. Only the pair into the
suffix changes: the value before nums[k] is now paired with the last
element of nums instead of nums[k]. So iterate over nums once with the
total cost and the largest saving of any pair: the cost of the pair
(previous value, nums[k]) minus the cost of the pair (previous value,
last element). The saving is at least 0. The answer is the total minus
the largest saving.

For example with nums = [2, 6, 5] the path is 0, 2, 6, 5 and its pairs
cost 2, 4, 1 for a total of 7. The pair (2, 6) costs 4 and the pair (2,
5) costs 3, a saving of 1. The answer is 6, the path 0, 2, 5, 6.

Example 1:

Input: nums = [2, 6, 5]
Output: 6

Example 2:

Input: nums = [9, 1, 2]
Output: 11
Explanation: reverse the whole array; the path is 0, 2, 1, 9.

Example 3:

Input: nums = [1, 2, 3]
Output: 3
Explanation: no reversal lowers the cost.

Constraints:

    1 <= len(nums) <= 10^5
    0 <= nums[i] <= 10^9

    REQUIRED: O(n) time, a single pass. NO rebuilding the reversed
    array for each k: n reversals each iterated in full is quadratic and
    is the failure mode this drill exists to kill.
"""


class Solution:
    def minCost(self, nums: list[int]) -> int:
        pass


sol = Solution()

print(sol.minCost([2, 6, 5]))  # 6

# assert sol.minCost([2, 6, 5]) == 6
# assert sol.minCost([9, 1, 2]) == 11
# assert sol.minCost([1, 2, 3]) == 3
# assert sol.minCost([5, 8, 5]) == 8
# assert sol.minCost([7]) == 7
# assert sol.minCost([0]) == 0
# assert sol.minCost([3, 3, 3]) == 3
# assert sol.minCost([1, 9, 2]) == 9
# assert sol.minCost([4, 1, 1, 1, 1, 1, 1, 9]) == 15
# assert sol.minCost([1, 1, 1, 1, 9, 1, 1, 1]) == 9
# assert sol.minCost([1, 1, 1, 9, 1, 1, 1, 1]) == 9
# assert sol.minCost([10 ** 9, 0]) == 10 ** 9
# assert sol.minCost(list(range(1, 10 ** 5 + 1))) == 10 ** 5
# assert sol.minCost([10 ** 9, 0] * 50000) == 10 ** 9 * 99999
