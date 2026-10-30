# Given two positive integers s and c, return the sum of the c consecutive
# integers that start at s: s + (s + 1) + ... + (s + c - 1).
#
# Example 1:
#
# Input: s = 4, c = 3
# Output: 15
# Explanation: 4 + 5 + 6 = 15.
#
# Example 2:
#
# Input: s = 1, c = 100
# Output: 5050
#
# Example 3:
#
# Input: s = 7, c = 1
# Output: 7
# Explanation: The sum of one integer is the integer itself.
#
# Constraints:
#
#     1 <= s <= 10^9
#     1 <= c <= 10^5
#
#     REQUIRED: O(1), one arithmetic expression. NO loop. NO sum. NO range.
#
# ---

# mu 0.14

class Solution
  def sumOfConsecutive(s: int, c: int) -> int
    prefix = s * (s - 1) // 2
    full = (s + c) * ((s + c) - 1) // 2
    full - prefix

sol = Solution()

print(sol.sumOfConsecutive(4, 3))  # 15

assert sol.sumOfConsecutive(4, 3) == 15
assert sol.sumOfConsecutive(1, 100) == 5050
assert sol.sumOfConsecutive(7, 1) == 7
assert sol.sumOfConsecutive(7, 2) == 15
assert sol.sumOfConsecutive(1, 5) == 15
assert sol.sumOfConsecutive(8, 2) == 17
assert sol.sumOfConsecutive(100, 3) == 303
assert sol.sumOfConsecutive(10 ** 9, 10 ** 5) == sum(10 ** 9..<10 ** 9 + 10 ** 5)
assert sol.sumOfConsecutive(1, 1) == 1
