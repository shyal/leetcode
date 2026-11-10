# URL: https://leetcode.com/problems/minimum-operations-to-make-binary-palindrome/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 3766. Minimum Operations to Make Binary Palindrome
#
# You are given an integer array nums.
#
# For each element nums[i], you may perform the following operations any number of times (including zero):
# - Increase nums[i] by 1, or
# - Decrease nums[i] by 1.
#
# A number is called a binary palindrome if its binary representation without leading zeros reads the same forward and backward.
#
# Your task is to return an integer array ans, where ans[i] represents the minimum number of operations required to convert nums[i] into a binary palindrome.
#
# Example 1:
#
# Input: nums = [1,2,4]
# Output: [0,1,1]
# Explanation:
# One optimal set of operations:
#
# nums[i] | Binary(nums[i]) | Nearest Palindrome | Binary(Palindrome) | Operations Required | ans[i]
# --------|-----------------|--------------------|--------------------|---------------------|-------
# 1       | 1               | 1                  | 1                  | Already palindrome   | 0
# 2       | 10              | 3                  | 11                 | Increase by 1       | 1
# 4       | 100             | 3                  | 11                 | Decrease by 1       | 1
#
# Thus, ans = [0, 1, 1].
#
# Example 2:
#
# Input: nums = [6,7,12]
# Output: [1,0,3]
# Explanation:
# One optimal set of operations:
#
# nums[i] | Binary(nums[i]) | Nearest Palindrome | Binary(Palindrome) | Operations Required | ans[i]
# --------|-----------------|--------------------|--------------------|---------------------|-------
# 6       | 110             | 5                  | 101                | Decrease by 1       | 1
# 7       | 111             | 7                  | 111                | Already palindrome   | 0
# 12      | 1100            | 15                 | 1111               | Increase by 3       | 3
#
# Thus, ans = [1, 0, 3].
#
# Constraints:
#
#     1 <= nums.length <= 5000
#     1 <= nums[i] <= 5000
#
# ---
# LEETCODE: Accepted (6808 ms, 19.8 MB)

# mu 0.17

class Solution
  def isPalindrome(d)
    d == d[::-1]
  
  def findNearestPalindrome(n)
    n_orig = n
    i = 0
    while true
      if self.isPalindrome(to_digits(n, base=2))
        break
      i += 1
      n += 1
    n = n_orig
    j = 0
    while true
      if self.isPalindrome(to_digits(n, base=2))
        break
      j += 1
      n -= 1
    min(i, j)

  def minOperations(nums: [int]) -> [int]
    ret res = []
    for n in nums
      res <- self.findNearestPalindrome(n)


sol = Solution()

print(sol.minOperations([1, 2, 4]))  # [0,1,1]

assert sol.minOperations([1, 2, 4]) == [0, 1, 1]
assert sol.minOperations([6, 7, 12]) == [1, 0, 3]
