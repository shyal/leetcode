# Given a positive integer x, return the value of its lowest set bit. A
# bit is set when it is 1. The lowest set bit is the set bit of least
# value.
#
# Example 1:
#
# Input: x = 0b11001
# Output: 0b1
#
# Example 2:
#
# Input: x = 0b110100
# Output: 0b100
# Explanation: The lowest set bit has value 4. The bits of values 1 and 2
# are not set.
#
# Example 3:
#
# Input: x = 0b1000
# Output: 0b1000
#
# Constraints:
#
#     1 <= x <= 10^9
#
#     REQUIRED: O(1), one expression on x. NO loop, NO search for the
#     position of the bit, NO bin() and no string.
#
# ---

# mu 0.17

class Solution
  def lowestSetBit(x: int) -> int
    x & ~(x - 1)

sol = Solution()

print(sol.lowestSetBit(25))  # 1

assert sol.lowestSetBit(25) == 1
assert sol.lowestSetBit(52) == 4
assert sol.lowestSetBit(8) == 8
assert sol.lowestSetBit(1) == 1
assert sol.lowestSetBit(3) == 1
assert sol.lowestSetBit(14) == 2
assert sol.lowestSetBit(80) == 16
assert sol.lowestSetBit(2 ** 29) == 2 ** 29
assert sol.lowestSetBit(10 ** 9) == 512
assert avoids(Solution, bin, str, format)
