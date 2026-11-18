# Pairs With An Odd Number
#
# Given an integer array nums, return the number of index pairs (i, j) with
# i < j such that at least one of nums[i] and nums[j] is odd.
#
# Example 1:
#
# Input: nums = [2, 4, 3, 6, 5, 8, 10]
# Output: 11
# Explanation: The pairs include (2, 3), (3, 5) and (5, 8). The pair (4, 6) is not counted.
#
# Example 2:
#
# Input: nums = [2, 4]
# Output: 0
#
# Example 3:
#
# Input: nums = [1, 3, 5]
# Output: 3
#
# Constraints:
#
#     1 <= len(nums) <= 10^5
#     1 <= nums[i] <= 10^6
#
#     REQUIRED: O(len(nums)) time. NO nested loop.
#
# ---

# mu 0.18

class Solution
  def odd_pairs(nums: [int]) -> int
    evenc = count for nums: _ is even
    even_pairs = comb(evenc, 2)
    comb(len nums, 2) - even_pairs

sol = Solution()

print(sol.odd_pairs([2, 4, 3, 6, 5, 8, 10]))  # 11

assert sol.odd_pairs([2, 4, 3, 6, 5, 8, 10]) == 11
assert sol.odd_pairs([2, 4]) == 0
assert sol.odd_pairs([1, 3, 5]) == 3
assert sol.odd_pairs([3]) == 0
assert sol.odd_pairs([1, 2]) == 1
assert sol.odd_pairs([2, 2, 2, 2, 2]) == 0
assert sol.odd_pairs([1, 1, 1, 1]) == 6
assert sol.odd_pairs([7, 2, 2, 2, 2, 2]) == 5
assert sol.odd_pairs([2] * 99999 + [1]) == 99999
assert sol.odd_pairs([1] * 10 ** 5) == 4999950000
