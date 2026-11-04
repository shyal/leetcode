"""
Given an integer array nums, return an array dp of the same length. The
cell dp[i] is the length of the longest strictly increasing subsequence of
nums that ends at index i. For example with nums = [4, 1, 6, 2, 8, 5, 9],
the longest strictly increasing subsequence that ends at index 5 is
1, 2, 5, so dp[5] is 3.

Example 1:

Input: nums = [4, 1, 6, 2, 8, 5, 9]
Output: [1, 1, 2, 2, 3, 3, 4]
Explanation: the longest ending at the 9 is 1, 2, 5, 9, so dp[6] is 4.

Example 2:

Input: nums = [5, 4, 3, 2, 1]
Output: [1, 1, 1, 1, 1]

Example 3:

Input: nums = [2, 3, 1, 4]
Output: [1, 2, 1, 3]
Explanation: the longest ending at the 4 is 2, 3, 4, so dp[3] is 3.

Constraints:

    1 <= len(nums) <= 2500
    -10^4 <= nums[i] <= 10^4

    REQUIRED: O(n^2). NO sorting, NO binary search.
"""


class Solution:
    def longestEndingAt(self, nums: List[int]) -> List[int]:
        pass


sol = Solution()

print(sol.longestEndingAt([4, 1, 6, 2, 8, 5, 9]))  # [1, 1, 2, 2, 3, 3, 4]

# assert sol.longestEndingAt([4, 1, 6, 2, 8, 5, 9]) == [1, 1, 2, 2, 3, 3, 4]
# assert sol.longestEndingAt([5, 4, 3, 2, 1]) == [1, 1, 1, 1, 1]
# assert sol.longestEndingAt([2, 3, 1, 4]) == [1, 2, 1, 3]
# assert sol.longestEndingAt([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]
# assert sol.longestEndingAt([7]) == [1]
# assert sol.longestEndingAt([3, 3, 3]) == [1, 1, 1]
# assert sol.longestEndingAt([2, 2, 3, 3]) == [1, 1, 2, 2]
# assert sol.longestEndingAt([-1, -3, -2, 0]) == [1, 1, 2, 3]
# assert sol.longestEndingAt([9, 1, 8, 2, 7, 3]) == [1, 1, 2, 2, 3, 3]
# assert sol.longestEndingAt([1, 5, 6, 2, 3, 4]) == [1, 2, 3, 2, 3, 4]
# assert sol.longestEndingAt([10, 9, 2, 5, 3, 7, 101, 18]) == [1, 1, 1, 2, 2, 3, 4, 4]
# assert sol.longestEndingAt(list(range(2500)))[-1] == 2500
