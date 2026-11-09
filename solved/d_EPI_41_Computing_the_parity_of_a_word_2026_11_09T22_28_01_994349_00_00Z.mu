# EPI 4.1 Computing the parity of a word
#
# Given a 64-bit unsigned integer x, return its parity: 1 when the number
# of 1 bits in x is odd, and 0 when it is even.
#
# Example 1:
#
# Input: x = 0b1011
# Output: 1
# Explanation: x has three 1 bits.
#
# Example 2:
#
# Input: x = 0b10001000
# Output: 0
# Explanation: x has two 1 bits.
#
# Example 3:
#
# Input: x = 0
# Output: 0
#
# Constraints:
#
#     0 <= x < 2^64
#
#     REQUIRED: O(log n) time, where n = 64 is the word size, and O(1)
#     extra space. NO bin(), NO format(), NO str(), NO int.bit_count().
#
# ---

# mu 0.17

class Solution
  def parity(x: int) -> int
    ret res = 0
    while x
      if x & 1
        res ^= 1
      x >>= 1

sol = Solution()

print(sol.parity(11))  # 1

assert sol.parity(11) == 1
assert sol.parity(136) == 0
assert sol.parity(0) == 0
assert sol.parity(1) == 1
assert sol.parity(2 ** 63) == 1
assert sol.parity(2 ** 63 + 1) == 0
assert sol.parity(2 ** 64 - 1) == 0
assert sol.parity(2 ** 64 - 2) == 1
assert sol.parity(4294967295) == 0
assert sol.parity(4294967295 << 32) == 0
assert sol.parity(6148914691236517205) == 0
assert sol.parity(9223372041149743104) == 0
assert sol.parity(4294967296) == 1
assert all((sol.parity(v) == bin(v).count('1') % 2 for v in 0..<4096))
assert all((sol.parity(v) == bin(v).count('1') % 2 for v in (i * 11400714819323198485 % 2 ** 64 for i in 0..<10 ** 4)))
