"""
EPI 4.3 Reverse bits

Given a 64-bit unsigned integer x, return the 64-bit integer whose bit
at position i is the bit of x at position 63 - i, for each i from 0 to
63. Position 0 is the least significant bit. Many calls are made on one
Solution object.

Example 1:

Input: x = 1
Output: 9223372036854775808
Explanation: bit 0 moves to bit 63, so the result is 2^63.

Example 2:

Input: x = 0b1011
Output: 14987979559889010688
Explanation: bits 0, 1 and 3 move to bits 63, 62 and 60. The result is
0xD000000000000000.

Example 3:

Input: x = 2^64 - 1
Output: 18446744073709551615

Constraints:

    0 <= x < 2^64
    1 <= number of calls <= 10^5

    REQUIRED: O(n / L) time for each call, where n = 64 and L = 16,
    after a constructor of O(2^L) time and space. NO bin(), NO
    format(), NO str(), NO int(s, 2).
"""


class Solution:
    def reverse_bits(self, x: int) -> int:
        pass


sol = Solution()

print(sol.reverse_bits(1))  # 9223372036854775808

# assert sol.reverse_bits(1) == 2 ** 63
# assert sol.reverse_bits(2 ** 63) == 1
# assert sol.reverse_bits(0b1011) == 0xD000000000000000
# assert sol.reverse_bits(2 ** 64 - 1) == 2 ** 64 - 1
# assert sol.reverse_bits(0) == 0
# assert sol.reverse_bits(3) == 0xC000000000000000
# assert sol.reverse_bits(0xF0) == 0x0F00000000000000
# assert sol.reverse_bits(0xFFFF) == 0xFFFF000000000000
# assert sol.reverse_bits(0x0123456789ABCDEF) == 0xF7B3D591E6A2C480
# assert sol.reverse_bits(0x5555555555555555) == 0xAAAAAAAAAAAAAAAA
# assert sol.reverse_bits(0x8000000000000001) == 0x8000000000000001
# assert sol.reverse_bits(0x00000000FFFFFFFF) == 0xFFFFFFFF00000000
# assert all(sol.reverse_bits(v) == int(format(v, "064b")[::-1], 2) for v in ((i * 0x9E3779B97F4A7C15) % 2 ** 64 for i in range(10 ** 5)))
