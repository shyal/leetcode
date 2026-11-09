"""
EPI 4.1 Computing the parity of a word

Given a 64-bit unsigned integer x, return its parity: 1 when the number
of 1 bits in x is odd, and 0 when it is even.

Example 1:

Input: x = 0b1011
Output: 1
Explanation: x has three 1 bits.

Example 2:

Input: x = 0b10001000
Output: 0
Explanation: x has two 1 bits.

Example 3:

Input: x = 0
Output: 0

Constraints:

    0 <= x < 2^64

    REQUIRED: O(log n) time, where n = 64 is the word size, and O(1)
    extra space. NO bin(), NO format(), NO str(), NO int.bit_count().
"""


class Solution:
    def parity(self, x: int) -> int:
        pass


sol = Solution()

print(sol.parity(0b1011))  # 1

# assert sol.parity(0b1011) == 1
# assert sol.parity(0b10001000) == 0
# assert sol.parity(0) == 0
# assert sol.parity(1) == 1
# assert sol.parity(2 ** 63) == 1
# assert sol.parity(2 ** 63 + 1) == 0
# assert sol.parity(2 ** 64 - 1) == 0
# assert sol.parity(2 ** 64 - 2) == 1
# assert sol.parity(0xFFFFFFFF) == 0
# assert sol.parity(0xFFFFFFFF << 32) == 0
# assert sol.parity(0x5555555555555555) == 0
# assert sol.parity(0x8000000100000000) == 0
# assert sol.parity(0x0000000100000000) == 1
# assert int_ops(sol.parity, 2 ** 64 - 1) <= 6 * 6  # 6 = log2(64), the word size
# assert int_ops(sol.parity, 2 ** 63) <= 6 * 6
# assert all(sol.parity(v) == bin(v).count("1") % 2 for v in range(4096))
# assert all(sol.parity(v) == bin(v).count("1") % 2 for v in ((i * 0x9E3779B97F4A7C15) % 2 ** 64 for i in range(10 ** 4)))
