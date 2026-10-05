"""
DRILL: Clear Lowest Set Bit
TRAINS: bit-iterate

Given a positive integer x, return x with its lowest set bit cleared. A
bit is set when it is 1. The lowest set bit is the set bit of least
value. Every other bit of x stays as it is.

Example 1:

Input: x = 0b11001
Output: 0b11000

Example 2:

Input: x = 0b110110
Output: 0b110100
Explanation: The lowest set bit has value 2. The bit of value 1 is not set.

Example 3:

Input: x = 0b1000
Output: 0
Explanation: The lowest set bit is the only set bit.

Constraints:

    1 <= x <= 10^9

    REQUIRED: O(1), one expression on x. NO loop, NO search for the
    position of the bit, NO bin() and no string.
"""


# mu 0.7
# def clearLowestSetBit(x: int) -> int
#   x & (x - 1)

class Solution:
    def clearLowestSetBit(self, x: int) -> int:
        return x & (x - 1)


sol = Solution()
print(sol.clearLowestSetBit(25))
assert sol.clearLowestSetBit(25) == 24
assert sol.clearLowestSetBit(54) == 52
assert sol.clearLowestSetBit(8) == 0
assert sol.clearLowestSetBit(1) == 0
assert sol.clearLowestSetBit(3) == 2
assert sol.clearLowestSetBit(15) == 14
assert sol.clearLowestSetBit(80) == 64
assert sol.clearLowestSetBit(2 ** 29) == 0
assert sol.clearLowestSetBit(10 ** 9) == 10 ** 9 - 512
assert avoids(Solution, bin, str, format)
