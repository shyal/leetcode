# DRILL: Read The Signed Numbers
#
# Given a string s of nonnegative integers separated by single '+' or '-'
# characters, return the numbers in the order they appear, each with its
# sign. A number that follows a '-' is negated. The first number and any
# number that follows a '+' do not change.
#
# Example 1:
#
# Input: s = "3-2+2"
# Output: [3, -2, 2]
#
# Example 2:
#
# Input: s = "14-3-7"
# Output: [14, -3, -7]
# Explanation: 14 is one number and has no operator in front of it.
#
# Example 3:
#
# Input: s = "42"
# Output: [42]
#
# Constraints:
#
#     1 <= len(s) <= 10^5
#     s contains only digits, '+' and '-'. No spaces.
#     s starts and ends with a digit; every operator is followed by a digit.
#
#     REQUIRED: one pass over the characters, building each number digit by
#     digit as you walk. NO split, NO regex, NO int() on slices.
#
# ---

# mu 0.12

class Solution
  def getPositiveAndNegativeNumbers(s: str) -> [int]
    ret res, num, op = [], 0, '+'
    for c in s + '+'
      if c.isdigit()
        num = num * 10 + int(c)
      else
        if op == '+'
          res <- num
        else
          res <- -num
        num, op = 0, c


sol = Solution()

print(sol.getPositiveAndNegativeNumbers('3-2+2'))  # [3, -2, 2]

assert sol.getPositiveAndNegativeNumbers('3-2+2') == [3, -2, 2]
assert sol.getPositiveAndNegativeNumbers('14-3-7') == [14, -3, -7]
assert sol.getPositiveAndNegativeNumbers('42') == [42]
assert sol.getPositiveAndNegativeNumbers('100+10-1') == [100, 10, -1]
assert sol.getPositiveAndNegativeNumbers('0-0') == [0, 0]
assert sol.getPositiveAndNegativeNumbers('7-7-7') == [7, -7, -7]
assert sol.getPositiveAndNegativeNumbers('123456-9') == [123456, -9]
