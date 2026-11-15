"""
Given two integer arrays nums and colors of the same length n, choose
indices of nums and return the maximum sum of nums over the chosen
indices. You must not choose two adjacent indices i and i + 1 when
colors[i] == colors[i + 1].

Example 1:

Input: nums = [3, 1, 2, 4], colors = [2, 3, 2, 2]
Output: 8
Explanation: indices 0, 1 and 3: 3 + 1 + 4. Indices 2 and 3 have the
same colour, thus only the larger of nums[2] and nums[3] is chosen.

Example 2:

Input: nums = [1, 9, 10, 9], colors = [1, 1, 1, 1]
Output: 18
Explanation: indices 1 and 3: 9 + 9.

Example 3:

Input: nums = [1, 1, 1, 1, 1, 1], colors = [1, 2, 1, 2, 1, 2]
Output: 6
Explanation: no two adjacent indices have the same colour, thus every
index is chosen.

Constraints:

    1 <= n <= 10^5
    1 <= nums[i], colors[i] <= 10^5

    REQUIRED: O(n) time.
"""


class Solution:
    def maxSum(self, nums: list[int], colors: list[int]) -> int:
        pass


sol = Solution()

print(sol.maxSum([3, 1, 2, 4], [2, 3, 2, 2]))  # 8

# assert sol.maxSum([3, 1, 2, 4], [2, 3, 2, 2]) == 8
# assert sol.maxSum([1, 9, 10, 9], [1, 1, 1, 1]) == 18
# assert sol.maxSum([1, 1, 1, 1, 1, 1], [1, 2, 1, 2, 1, 2]) == 6
# assert sol.maxSum([1, 4, 3, 5], [1, 1, 2, 2]) == 9
# assert sol.maxSum([10, 1, 3, 9], [1, 1, 1, 2]) == 22
# assert sol.maxSum([1], [1]) == 1
# assert sol.maxSum([5, 5, 5, 5], [1, 1, 1, 1]) == 10
# assert sol.maxSum([5, 5, 5, 5], [1, 2, 1, 2]) == 20
# assert sol.maxSum([1, 2, 3, 4, 5], [1, 1, 1, 1, 1]) == 9
# assert sol.maxSum([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]) == 15
# assert sol.maxSum([1, 2, 3, 4, 5], [1, 1, 2, 2, 3]) == 11
# assert sol.maxSum([10, 1, 10, 1, 10], [1, 2, 1, 2, 1]) == 32
# assert sol.maxSum([10, 10, 10, 10, 10], [1, 1, 2, 2, 1]) == 30
# assert sol.maxSum([1, 2, 3, 4, 5, 6], [1, 2, 2, 3, 3, 4]) == 15
# assert sol.maxSum([100000] * 100000, [1] * 100000) == 5000000000
# assert sol.maxSum([1] * 100000, list(range(1, 100001))) == 100000
