"""
URL: https://leetcode.com/problems/longest-increasing-subsequence/description/

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
        -104 <= nums[i] <= 104


Follow up: Can you come up with an algorithm that runs in O(n log(n)) time complexity?

---

Someone dropped some hints in the discussion, so was able to solve it. However,
this is an O(n^2) solution, not O(n log(n)).
I could revisit this later to try a more optimal solution.

"""


class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        DP = [1] * len(nums)
        for i in range(1, len(nums)):
            max_increasing = 0
            for j in range(i):
                if nums[j] < nums[i]:
                    max_increasing = max(max_increasing, DP[j])
            DP[i] = max_increasing + 1
        return max(DP)


sol = Solution()
assert sol.lengthOfLIS(nums=[10, 9, 2, 5, 3, 7, 101, 18]) == 4
assert sol.lengthOfLIS(nums=[0, 1, 0, 3, 2, 3]) == 4
assert sol.lengthOfLIS(nums=[7, 7, 7, 7, 7, 7, 7]) == 1
