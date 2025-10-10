"""
URL: https://leetcode.com/problems/minimum-operations-to-exceed-threshold-value-i/description/

3065. Minimum Operations to Exceed Threshold Value I

You are given a 0-indexed integer array nums, and an integer k.

In one operation, you can remove one occurrence of the smallest element of nums.

Return the minimum number of operations needed so that all elements of the array are greater than or equal to k.


Example 1:

Input: nums = [2,11,10,1,3], k = 10
Output: 3
Explanation: After one operation, nums becomes [2,11,10,3].
After two operations, nums becomes [11,10,3].
After three operations, nums becomes [11,10].
Now, all elements are greater than or equal to 10.

Example 2:

Input: nums = [1,1,2,4,9], k = 1
Output: 0
Explanation: All elements are greater than or equal to 1.

Example 3:

Input: nums = [1,1,2,4,9], k = 9
Output: 4
Explanation: After one operation, nums becomes [1,2,4,9].
After two operations, nums becomes [2,4,9].
After three operations, nums becomes [4,9].
After four operations, nums becomes [9].
Now, all elements are greater than or equal to 9.


Constraints:

    1 <= nums.length <= 50
    1 <= nums[i] <= 100
    1 <= k <= 100
    The input is generated such that k is less than or equal to the maximum element in nums.
"""


class Solution:
    def minOperations(self, nums: List[int], k: int) -> int:
        return len([x for x in nums if x < k])


sol = Solution()

assert sol.minOperations([2, 11, 10, 1, 3], 10) == 3
assert sol.minOperations([1, 1, 2, 4, 9], 1) == 0
assert sol.minOperations([1, 1, 2, 4, 9], 9) == 4
assert sol.minOperations([1], 1) == 0
assert sol.minOperations([100], 100) == 0
assert sol.minOperations([100], 1) == 0
assert sol.minOperations([1, 2, 3, 10], 10) == 3
assert sol.minOperations([5, 5, 5, 5], 5) == 0
assert sol.minOperations([4, 4, 4, 4, 5], 5) == 4
assert sol.minOperations([1, 2, 3, 4, 5], 3) == 2
assert sol.minOperations(list(range(1, 51)), 50) == 49
assert sol.minOperations([99] * 49 + [100], 100) == 49
assert sol.minOperations([1, 100, 1, 100], 100) == 2
assert sol.minOperations([50] * 50, 50) == 0
assert sol.minOperations([1, 1, 1, 1, 1], 1) == 0
