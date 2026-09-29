"""
DRILL: Longest Ending Here
TRAINS: dp-1d-rolling

Given an integer array nums. Make a table dp with one cell per index of
nums, every cell 1. Visit every pair of indices j < i. When nums[j] is
smaller than nums[i], set dp[i] to the larger of dp[i] and dp[j] + 1.
For example with nums = [4, 1, 6, 2, 8, 5, 9], the 5 at index 5 sees
4, 1 and 2 as smaller. Their cells hold 1, 1 and 2, so dp[5] becomes
2 + 1 = 3. Return dp. The cell dp[i] is the length of the longest
strictly increasing subsequence of nums that ends at nums[i].

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
Explanation: three values before the 4 are smaller than it, but their
cells hold 1, 2 and 1, so dp[3] is 2 + 1 = 3, not 4.

Constraints:

    1 <= len(nums) <= 2500
    -10^4 <= nums[i] <= 10^4

    REQUIRED: O(n^2). NO sorting, NO binary search. Each cell MUST be
    built from the earlier cells it can follow; counting the smaller
    values before i returns 4 at the end of Example 3.
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
