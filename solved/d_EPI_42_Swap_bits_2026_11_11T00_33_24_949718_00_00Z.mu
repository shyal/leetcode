# EPI 4.2 Swap bits
#
# Given a 64-bit unsigned integer x and two bit positions i and j, return
# x with the bit at position i and the bit at position j exchanged.
# Position 0 is the least significant bit. Every other bit of x does not
# change.
#
# Example 1:
#
# Input: x = 0b10110, i = 0, j = 4
# Output: 7
# Explanation: bit 4 of x is 1 and bit 0 is 0. The result is 0b00111.
#
# Example 2:
#
# Input: x = 0b101, i = 0, j = 2
# Output: 5
# Explanation: both bits are 1, so the result is x.
#
# Example 3:
#
# Input: x = 1, i = 0, j = 63
# Output: 9223372036854775808
# Explanation: the result is 2^63.
#
# Constraints:
#
#     0 <= x < 2^64
#     0 <= i < 64
#     0 <= j < 64
#
#     REQUIRED: O(1) time. NO loop, NO bin(), NO format(), NO str().
#
# ---

# mu 0.17

class Solution
  def swap_bits(x: int, i: int, j: int) -> int
    if (x >> i & 1) != (x >> j & 1)
      mask = (1 << i) | (1 << j)
      x ^= mask
    x

sol = Solution()

print(sol.swap_bits(22, 0, 4))  # 7

assert sol.swap_bits(22, 0, 4) == 7
assert sol.swap_bits(22, 4, 0) == 7
assert sol.swap_bits(5, 0, 2) == 5
assert sol.swap_bits(1, 0, 63) == 2 ** 63
assert sol.swap_bits(2 ** 63, 63, 0) == 1
assert sol.swap_bits(0, 5, 9) == 0
assert sol.swap_bits(2 ** 64 - 1, 0, 63) == 2 ** 64 - 1
assert sol.swap_bits(8, 3, 3) == 8
assert sol.swap_bits(2, 1, 2) == 4
assert sol.swap_bits(73, 1, 6) == 11
assert sol.swap_bits(2 ** 64 - 2, 0, 1) == 2 ** 64 - 3
assert sol.swap_bits(17361641481138401520, 3, 4) == 17361641481138401512
assert sol.swap_bits(9223372036854775808, 62, 63) == 4611686018427387904
