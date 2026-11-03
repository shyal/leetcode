"""
Given an integer array nums, return the largest alternating sum of a
non-empty subarray. The alternating sum of a subarray is its first
element minus its second plus its third, and so on: the elements at
even positions in the subarray are added, the elements at odd positions
are subtracted. Walk nums from the left with two values: the largest
alternating sum of a subarray that ends at the current element with that
element added, and the largest with that element subtracted. At each
element x, the added value is the larger of x on its own and x plus the
previous subtracted value. The subtracted value is the previous added
value minus x. Compute both from the previous pair before either
changes. The answer is the largest value seen in either. For example
with nums = [-54, 77, 97], the added values are -54, 77, 97 and the
subtracted values are none, -131, -20. The answer is 97, the subarray
[97].

Example 1:

Input: nums = [-54, 77, 97]
Output: 97
Explanation: the subarray [97]; the whole array gives -54 - 77 + 97 = -34.

Example 2:

Input: nums = [10, -100]
Output: 110
Explanation: the whole array, 10 - (-100); the answer ends on a
subtracted element.

Example 3:

Input: nums = [3, 8, 1, 9]
Output: 16
Explanation: the subarray [8, 1, 9], 8 - 1 + 9.

Constraints:

    1 <= len(nums) <= 10^5
    -10^5 <= nums[i] <= 10^5

    REQUIRED: O(n) time, O(1) extra space, a single pass. Both values
    must come from the previous pair: updating the added value first and
    reading it for the subtracted value puts x on both sides. NO
    enumeration of subarrays. The empty subarray is not allowed.
"""


class Solution:
    def maxAlternatingSum(self, nums: list[int]) -> int:
        pass


sol = Solution()

print(sol.maxAlternatingSum([-54, 77, 97]))  # 97

# assert sol.maxAlternatingSum([-54, 77, 97]) == 97
# assert sol.maxAlternatingSum([10, -100]) == 110
# assert sol.maxAlternatingSum([3, 8, 1, 9]) == 16
# assert sol.maxAlternatingSum([5, -5, 1]) == 11
# assert sol.maxAlternatingSum([4, 7]) == 7
# assert sol.maxAlternatingSum([-72]) == -72
# assert sol.maxAlternatingSum([-5, -5]) == 0
# assert sol.maxAlternatingSum([1, -1, 1, -1, 1]) == 5
# assert sol.maxAlternatingSum([9, 1, 1, 1, 1, 1, 1, 1]) == 9
# assert sol.maxAlternatingSum([1, 1, 1, 1, 1, 1, 1, 9]) == 9
# assert sol.maxAlternatingSum([1, 1, 1, 9, 1, 1, 1, 1]) == 9
# assert sol.maxAlternatingSum([2, -3, 2, -3, 2, -3, 2, -3]) == 20
# assert sol.maxAlternatingSum([1, -1] * 50000) == 100000
# assert sol.maxAlternatingSum([10 ** 5] * 10 ** 5) == 10 ** 5
# assert sol.maxAlternatingSum([-10 ** 5] * 10 ** 5) == 0
