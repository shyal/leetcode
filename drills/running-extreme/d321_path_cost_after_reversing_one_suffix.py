"""
Given an integer array nums, visit its elements in order, starting at
value 0. Each move from value a to value b costs abs(a - b). Before the
walk you may reverse a suffix of nums, nums[k:] for any index k. Return
the smallest total cost. A reversed suffix is walked backwards over the
same pairs, so every move inside it costs the same as before, and only
the move into the suffix changes: from the value before nums[k], the
move into nums[k] becomes a move into the last element of nums. So walk
nums once with the total cost and the largest saving of any move: the
cost of the move into nums[k] minus the cost of a move from the same
value into the last element. Reversing the last element alone changes
nothing, so the saving is at least 0. The answer is the total minus the
largest saving. For example with nums = [2, 6, 5] the moves cost 2, 4,
1 for a total of 7. The move 2 to 6 costs 4 and the move 2 to 5 costs
3, a saving of 1. The answer is 6, the walk 0, 2, 5, 6.

Example 1:

Input: nums = [2, 6, 5]
Output: 6

Example 2:

Input: nums = [9, 1, 2]
Output: 11
Explanation: reverse the whole array and walk 0, 2, 1, 9.

Example 3:

Input: nums = [1, 2, 3]
Output: 3
Explanation: no reversal lowers the cost.

Constraints:

    1 <= len(nums) <= 10^5
    0 <= nums[i] <= 10^9

    REQUIRED: O(n) time, a single pass. NO rebuilding the reversed
    array for each k: n reversals each walked in full is quadratic and
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
