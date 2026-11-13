# URL: https://leetcode.com/problems/top-k-frequent-elements/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 347. Top K Frequent Elements
#
# Given an integer array nums and an integer k, return the k most frequent elements. You may return the answer in any order.
#
# Example 1:
#
# Input: nums = [1,1,1,2,2,3], k = 2
# Output: [1,2]
#
# Example 2:
#
# Input: nums = [1], k = 1
# Output: [1]
#
# Example 3:
#
# Input: nums = [1,2,1,2,1,2,3,1,3,2], k = 2
# Output: [1,2]
#
# Constraints:
#
#     1 <= nums.length <= 10^5
#     -10^4 <= nums[i] <= 10^4
#     k is in the range [1, the number of unique elements in the array].
#     It is guaranteed that the answer is unique.
#
# Follow up: Your algorithm's time complexity must be better than O(n log n), where n is the array's size.
#
# ---
# STAGE 1 of 3 - the approach. Write it in plain English under this line. Then run make solved.
#
# count with a counter, then take the k keys with the largest counts
# STAGE 1: pass
# STAGE 2 of 3 - the pseudocode. Write one comment line for each step in the solve below. Then run make solved.

# mu 0.17

class Solution
  def solve(x)
    # cnt = counter of nums
    # sort the keys by count, largest first
    # return the first k keys
    pass

sol = Solution()
