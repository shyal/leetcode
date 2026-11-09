"""
EPI 4.2 Swap bits

Given a 64-bit unsigned integer x and two bit positions i and j, return
x with the bit at position i and the bit at position j exchanged.
Position 0 is the least significant bit. Every other bit of x does not
change.

Example 1:

Input: x = 0b10110, i = 0, j = 4
Output: 7
Explanation: bit 4 of x is 1 and bit 0 is 0. The result is 0b00111.

Example 2:

Input: x = 0b101, i = 0, j = 2
Output: 5
Explanation: both bits are 1, so the result is x.

Example 3:

Input: x = 1, i = 0, j = 63
Output: 9223372036854775808
Explanation: the result is 2^63.

Constraints:

    0 <= x < 2^64
    0 <= i < 64
    0 <= j < 64

    REQUIRED: O(1) time. NO loop, NO bin(), NO format(), NO str().
"""


class Solution:
    def swap_bits(self, x: int, i: int, j: int) -> int:
        pass


sol = Solution()

print(sol.swap_bits(0b10110, 0, 4))  # 7

# assert sol.swap_bits(0b10110, 0, 4) == 7
# assert sol.swap_bits(0b10110, 4, 0) == 7
# assert sol.swap_bits(0b101, 0, 2) == 5
# assert sol.swap_bits(1, 0, 63) == 2 ** 63
# assert sol.swap_bits(2 ** 63, 63, 0) == 1
# assert sol.swap_bits(0, 5, 9) == 0
# assert sol.swap_bits(2 ** 64 - 1, 0, 63) == 2 ** 64 - 1
# assert sol.swap_bits(0b1000, 3, 3) == 0b1000
# assert sol.swap_bits(0b10, 1, 2) == 0b100
# assert sol.swap_bits(0b01001001, 1, 6) == 0b00001011
# assert sol.swap_bits(2 ** 64 - 2, 0, 1) == 2 ** 64 - 3
# assert sol.swap_bits(0xF0F0F0F0F0F0F0F0, 3, 4) == 0xF0F0F0F0F0F0F0E8
# assert sol.swap_bits(0x8000000000000000, 62, 63) == 0x4000000000000000
