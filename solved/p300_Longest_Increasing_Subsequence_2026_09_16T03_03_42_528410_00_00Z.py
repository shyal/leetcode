"""
URL: https://leetcode.com/problems/longest-increasing-subsequence/description/?envType=problem-list-v2&envId=vn57k9wr

300. Longest Increasing Subsequence

Given an integer array nums, return the length of the longest strictly increasing subsequence.

Example 1:

Input: nums = [10,9,2,5,3,7,101,18]
Output: 4
Explanation: The longest increasing subsequence is [2,3,7,101], therefore the length is 4.

Example 2:

Input: nums = [0,1,0,3,2,3]
Output: 4

Example 3:

Input: nums = [7,7,7,7,7,7,7]
Output: 1

Constraints:

    1 <= nums.length <= 2500
    -10^4 <= nums[i] <= 10^4

Follow up: Can you come up with an algorithm that runs in O(n log(n)) time complexity?

---

Learning

LEETCODE: Runtime Error (Line 1: ModuleNotFoundError: No module named 'rich')
"""


class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        dp = table(len(nums), fill=1)
        for i, x in enumerate(nums):
            for j in range(i):
                if nums[j] < x:
                    dp[i] = max(dp[i], dp[j] + 1)
        tabulate(dp, headers=nums)
        return max(dp) if dp else 0


sol = Solution()

print(sol.lengthOfLIS([10, 9, 2, 5, 3, 7, 101, 18]))  # 4

assert sol.lengthOfLIS([10, 9, 2, 5, 3, 7, 101, 18]) == 4
assert sol.lengthOfLIS([0, 1, 0, 3, 2, 3]) == 4
assert sol.lengthOfLIS([7, 7, 7, 7, 7, 7, 7]) == 1

assert sol.lengthOfLIS([]) == 0
assert sol.lengthOfLIS([1]) == 1
assert sol.lengthOfLIS([2, 2, 2, 2, 2]) == 1
assert sol.lengthOfLIS([-1, -2, -3, -4]) == 1
assert sol.lengthOfLIS([-1, 0, 1, 2, 3]) == 5
assert sol.lengthOfLIS([1, 3, 5, 4, 7]) == 4
assert sol.lengthOfLIS([10**4] * 2500) == 1
assert sol.lengthOfLIS(list(range(2500))) == 2500
assert sol.lengthOfLIS(list(range(2500, 0, -1))) == 1
assert sol.lengthOfLIS([1, 2, 2, 3, 4, 4, 5]) == 5
assert sol.lengthOfLIS([10000, -10000] * 1250) == 2
assert sol.lengthOfLIS([3, 1, 2]) == 2
