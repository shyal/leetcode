"""
Given a positive integer x, return the value of its lowest set bit. A
bit is set when it is 1. The lowest set bit is the set bit of least
value.

Example 1:

Input: x = 0b11001
Output: 0b1

Example 2:

Input: x = 0b110100
Output: 0b100
Explanation: The lowest set bit has value 4. The bits of values 1 and 2
are not set.

Example 3:

Input: x = 0b1000
Output: 0b1000

Constraints:

    1 <= x <= 10^9

    REQUIRED: O(1), one expression on x. NO loop, NO search for the
    position of the bit, NO bin() and no string.
"""


class Solution:
    def lowestSetBit(self, x: int) -> int:
        pass


sol = Solution()

print(sol.lowestSetBit(0b11001))  # 1

# assert sol.lowestSetBit(0b11001) == 0b1
# assert sol.lowestSetBit(0b110100) == 0b100
# assert sol.lowestSetBit(0b1000) == 0b1000
# assert sol.lowestSetBit(1) == 1
# assert sol.lowestSetBit(0b11) == 0b1
# assert sol.lowestSetBit(0b1110) == 0b10
# assert sol.lowestSetBit(0b1010000) == 0b10000
# assert sol.lowestSetBit(2**29) == 2**29
# assert sol.lowestSetBit(10**9) == 512
# assert avoids(Solution, bin, str, format)
