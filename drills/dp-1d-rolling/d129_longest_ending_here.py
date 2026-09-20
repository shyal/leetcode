"""
DRILL: Longest Ending Here
TRAINS: dp-1d-rolling

Given an integer array nums, return an array dp of the same length where
dp[i] is the length of the longest strictly increasing subsequence of
nums that ends at index i. The subsequence keeps the order of nums and
may skip values. Its last value is nums[i], so dp[i] is at least 1.

Example 1:

Input: nums = [4, 1, 6, 2, 8, 5, 9]
Output: [1, 1, 2, 2, 3, 3, 4]
Explanation: the longest ending at the 9 is 1, 2, 5, 9 or 4, 6, 8, 9.
The longest ending at the 5 is 1, 2, 5, so dp[5] is 3.

Example 2:

Input: nums = [5, 4, 3, 2, 1]
Output: [1, 1, 1, 1, 1]

Example 3:

Input: nums = [2, 3, 1, 4]
Output: [1, 2, 1, 3]
Explanation: three values before the 4 are smaller than it, but 2, 3, 1
is not increasing, so the longest ending at the 4 is 2, 3, 4.

Constraints:

    1 <= len(nums) <= 2500
    -10^4 <= nums[i] <= 10^4

    REQUIRED: O(n^2), every earlier index compared against i. NO sorting,
    NO binary search. Counting the smaller values before i is the fail:
    Example 3 returns 4 at the last index instead of 3.
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
# assert sol.longestEndingAt(list(range(2500)))[-1] == 2500
