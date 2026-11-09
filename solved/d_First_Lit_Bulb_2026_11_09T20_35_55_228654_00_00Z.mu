# Given a row of bulbs lit, where lit[i] is True when bulb i is on, return
# the index of the first bulb that is on. Every bulb before it is off and
# every bulb after it is on. At least one bulb is on.
#
# Example 1:
#
# Input: lit = [False, False, False, True, True]
# Output: 3
#
# Example 2:
#
# Input: lit = [False, False, False, False, False, False, False, True]
# Output: 7
#
# Example 3:
#
# Input: lit = [False, True, True, True, True, True, True, True]
# Output: 1
#
# Example 4:
#
# Input: lit = [True, True, True, True, True, True, True, True]
# Output: 0
#
# Example 5:
#
# Input: lit = [False, False, False, False, True, True, True, True]
# Output: 4
#
# Constraints:
#
#     1 <= len(lit) <= 10^5
#     lit is False for a prefix and True for the rest.
#
#     REQUIRED: must run in O(log n) time. NO scan from the left.
#
# ---

# mu 0.16

class Solution
  def firstLit(lit: [bool]) -> int
    first_true(0, len(lit)-1, ok = x -> lit[x])

sol = Solution()

print(sol.firstLit([false, false, false, true, true]))  # 3

assert sol.firstLit([false, false, false, true, true]) == 3
assert sol.firstLit([false, false, false, false, false, false, false, true]) == 7
assert sol.firstLit([false, true, true, true, true, true, true, true]) == 1
assert sol.firstLit([true, true, true, true, true, true, true, true]) == 0
assert sol.firstLit([false, false, false, false, true, true, true, true]) == 4
assert sol.firstLit([true]) == 0
assert sol.firstLit([false] * 99999 + [true]) == 99999
assert sol.firstLit([true] * 100000) == 0
