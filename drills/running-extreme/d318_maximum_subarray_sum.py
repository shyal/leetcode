"""
Given an integer array nums, return the largest sum of a non-empty
subarray. Walk nums from the left with two values: the largest sum of a
subarray that ends at the current element, and the largest sum seen so
far. At each element x, the subarray that ends at x either starts at x
or extends the subarray that ended at the element before it: take the
larger of x and x plus the previous value. Then raise the largest sum
seen so far to it when it is larger. For example with
nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4], the sums that end at each
element are -2, 1, -2, 4, 3, 5, 6, 1, 5. The answer is 6, the subarray
[4, -1, 2, 1]. This is Kadane's algorithm.

Example 1:

Input: nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
Output: 6

Example 2:

Input: nums = [-3, -1, -2]
Output: -1
Explanation: every subarray has a negative sum; [-1] is the largest.

Example 3:

Input: nums = [5]
Output: 5

Constraints:

    1 <= len(nums) <= 10^5
    -10^4 <= nums[i] <= 10^4

    REQUIRED: O(n) time, O(1) extra space, a single pass. NO
    enumeration of subarrays. The empty subarray is not allowed: on
    [-3, -1, -2] the answer is -1, not 0.
"""


class Solution:
    def maxSubArray(self, nums: list[int]) -> int:
        pass


sol = Solution()

print(sol.maxSubArray([-2, 1, -3, 4, -1, 2, 1, -5, 4]))  # 6

# assert sol.maxSubArray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
# assert sol.maxSubArray([-3, -1, -2]) == -1
# assert sol.maxSubArray([5]) == 5
# assert sol.maxSubArray([5, 4, -1, 7, 8]) == 23
# assert sol.maxSubArray([-5, 4]) == 4
# assert sol.maxSubArray([4, -5]) == 4
# assert sol.maxSubArray([2, -1, 2, -1, 2]) == 4
# assert sol.maxSubArray([-1, -1, 3, -1, -1]) == 3
# assert sol.maxSubArray([1, 2, 3, -100, 4]) == 6
# assert sol.maxSubArray([0, 0, 0]) == 0
# assert sol.maxSubArray([-10 ** 4] * 10 ** 5) == -10 ** 4
# assert sol.maxSubArray([10 ** 4] * 10 ** 5) == 10 ** 9
# assert sol.maxSubArray([1, -1] * 50000) == 1
