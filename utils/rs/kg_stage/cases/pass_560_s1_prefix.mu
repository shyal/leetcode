# URL: https://leetcode.com/problems/subarray-sum-equals-k/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 560. Subarray Sum Equals K
#
# Given an array of integers nums and an integer k, return the total number of subarrays whose sum equals to k.
#
# A subarray is a contiguous non-empty sequence of elements within an array.
#
# Example 1:
#
# Input: nums = [1,1,1], k = 2
# Output: 2
#
# Example 2:
#
# Input: nums = [1,2,3], k = 3
# Output: 2
#
# Constraints:
#
#     1 <= nums.length <= 2 * 10^4
#     -1000 <= nums[i] <= 1000
#     -10^7 <= k <= 10^7
#
# ---
# STAGE 1 of 3 - the approach. Write it in plain English under this line. Then run make solved.
#
# prefix sums with a hashmap of how many times each prefix sum was seen; for each prefix add count[prefix - k].

# mu 0.17

class Solution
  def solve(x)
    pass

sol = Solution()
