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
[10, 9, 2, 5, 3, 7, 101, 18]

To find greatest LCS, we need to 'hop back', and write the LCS so far.

def lengthOfLIS(nums: [int]) -> int
  dp = table(len(nums))
  for i in range(len(nums))
    count = 0
    if nums[i] == 101
      for j in range(i)
        if nums[j] < nums[i]
          print(nums[j])
          count += 1
    dp[i] = count
  print(dp)

Learning - building drill - gating
WHERE: blank on the recurrence, the cell reading an earlier cell: dp[i] = max(dp[i], dp[j] + 1) when nums[j] < nums[i]
"""


# mu 0.6
# def lengthOfLIS(nums)
#     if not nums
#         return 0
#     dp = table(len(nums))
#     for (j, i) in pairs(len(nums))
#         if nums[j] < nums[i]
#             dp[i] = max(dp[i], dp[j] + 1)
#             print(dp)
#     return max(dp) + 1

def table(*dims, fill=0):
    if len(dims) == 1:
        return [fill] * dims[0]
    if len(dims) == 2:
        return [[fill] * dims[1] for _ in range(dims[0])]
    return [table(*dims[1:], fill=fill) for _ in range(dims[0])]


def pairs(n, type=tuple):
    for i in range(n):
        for j in range(i + 1, n):
            yield type((i, j))


class Solution:
    def lengthOfLIS(self, nums):
        if not nums:
            return 0
        dp = table(len(nums))
        for (j, i) in pairs(len(nums)):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
                print(dp)
        return max(dp) + 1


sol = Solution()
print(sol.lengthOfLIS([10, 9, 2, 5, 3, 7, 101, 18]))


# FAILED: walked away after 24m 29s; no working solution.
# Judge the moves actually attempted as struggled, not clean.
