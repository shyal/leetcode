# URL: https://leetcode.com/problems/sum-of-digit-differences-of-all-pairs/description/?envType=problem-list-v2&envId=vn57k9wr
#
# 3153. Sum of Digit Differences of All Pairs
#
# You are given an array nums consisting of positive integers where all integers have the same number of digits.
#
# The digit difference between two integers is the count of different digits that are in the same position in the two integers.
#
# Return the sum of the digit differences between all pairs of integers in nums.
#
# Example 1:
#
# Input: nums = [13,23,12]
# Output: 4
# Explanation:
# We have the following:
# - The digit difference between 13 and 23 is 1.
# - The digit difference between 13 and 12 is 1.
# - The digit difference between 23 and 12 is 2.
# So the total sum of digit differences between all pairs of integers is 1 + 1 + 2 = 4.
#
# Example 2:
#
# Input: nums = [10,10,10,10]
# Output: 0
# Explanation:
# All the integers in the array are the same. So the total sum of digit differences between all pairs of integers will be 0.
#
# Constraints:
#
#     2 <= nums.length <= 10^5
#     1 <= nums[i] < 10^9
#     All integers in nums have the same number of digits.
#
# ---
# learning

class Solution
  def sumDigitDifferences(nums: [int]) -> int
    n = len nums
    rows = [*map(to_digits, nums)]
    cols = [col for col in zip(*rows)]
    pairs = sum for col in zip(*rows): sum for c in counter(col).values(): c * (n - c)
    pairs // 2

sol = Solution()

print(sol.sumDigitDifferences([13, 23, 12]))  # 4

assert sol.sumDigitDifferences([13, 23, 12]) == 4
assert sol.sumDigitDifferences([10, 10, 10, 10]) == 0
assert Solution().sumDigitDifferences([1, 2]) == 1
assert Solution().sumDigitDifferences([111, 111, 111]) == 0
assert Solution().sumDigitDifferences([123, 456, 789]) == 9
assert Solution().sumDigitDifferences([999999999, 888888888]) == 9
assert Solution().sumDigitDifferences([10 ** 8, 10 ** 8 + 1]) == 1
assert Solution().sumDigitDifferences([12345, 12355, 12365]) == 3
assert Solution().sumDigitDifferences([111, 222, 333, 444, 555]) == 30
assert Solution().sumDigitDifferences([100000000, 200000000, 300000000]) == 3
assert Solution().sumDigitDifferences([123456789, 123456788, 123456787]) == 3
assert Solution().sumDigitDifferences([10, 20, 30, 40, 50, 60, 70, 80, 90]) == 36
assert Solution().sumDigitDifferences([123456789] * 100000) == 0
assert Solution().sumDigitDifferences([123456789, 987654321]) == 8
