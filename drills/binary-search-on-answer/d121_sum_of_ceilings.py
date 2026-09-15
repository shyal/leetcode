"""
DRILL: Sum Of Ceilings

Given an array nums of positive integers and a positive integer k, return
the sum over all i of nums[i] / k rounded up to the nearest integer.

Example 1:

Input: nums = [5, 9, 2, 7], k = 4
Output: 8
Explanation: 2 + 3 + 1 + 2. Each of 5 and 7 needs two 4s, 9 needs three,
2 needs one.

Example 2:

Input: nums = [5, 9, 2, 7], k = 1
Output: 23

Example 3:

Input: nums = [5, 9, 2, 7], k = 100
Output: 4

Constraints:

    1 <= len(nums) <= 10^5
    1 <= nums[i] <= 10^9
    1 <= k <= 10^9

    REQUIRED: must run in O(n) time. NO float division and NO math.ceil;
    integer arithmetic only.
"""


class Solution:

    def sumOfCeilings(self, nums: List[int], k: int) -> int:
        pass


sol = Solution()

print(sol.sumOfCeilings([5, 9, 2, 7], 4))  # 8

# assert sol.sumOfCeilings([5, 9, 2, 7], 4) == 8
# assert sol.sumOfCeilings([5, 9, 2, 7], 1) == 23
# assert sol.sumOfCeilings([5, 9, 2, 7], 100) == 4
# assert sol.sumOfCeilings([8, 4, 12], 4) == 6
# assert sol.sumOfCeilings([8, 4, 12], 5) == 6
# assert sol.sumOfCeilings([8, 4, 12], 3) == 9
# assert sol.sumOfCeilings([1], 1) == 1
# assert sol.sumOfCeilings([1, 1, 1], 2) == 3
# assert sol.sumOfCeilings([10**9], 10**9) == 1
# assert sol.sumOfCeilings([10**9], 10**9 - 1) == 2
# assert sol.sumOfCeilings([10**9, 1, 10**9], 7) == 285714287
