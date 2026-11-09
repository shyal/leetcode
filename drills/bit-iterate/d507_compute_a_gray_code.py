"""
EPI 15.11 Compute a Gray code

Given num_bits, return a list of the 2^num_bits integers 0 to
2^num_bits - 1, each exactly once, in an order where every two
neighbours differ in exactly one bit. The last and the first entries
are neighbours too. Any such list is accepted.

Example 1:

Input: num_bits = 3
Output: [0, 1, 3, 2, 6, 7, 5, 4]
Explanation: in binary, 000 001 011 010 110 111 101 100. Each entry
differs from the next in one bit, and 100 differs from 000 in one bit.

Example 2:

Input: num_bits = 1
Output: [0, 1]

Example 3:

Input: num_bits = 0
Output: [0]
Explanation: a list of one entry has no two different neighbours.

Constraints:

    0 <= num_bits <= 16

    REQUIRED: O(2^num_bits) time. NO search that undoes a choice.
"""


class Solution:
    def gray_code(self, num_bits: int) -> list[int]:
        pass


sol = Solution()


def one_bit(x, y):
    d = x ^ y
    return d > 0 and d & (d - 1) == 0


def is_gray(codes, num_bits):
    n = 1 << num_bits
    if sorted(codes) != list(range(n)):
        return False
    start = 0 if n > 1 else 1
    return all(one_bit(codes[i - 1], codes[i]) for i in range(start, n))


print(sol.gray_code(3))  # [0, 1, 3, 2, 6, 7, 5, 4]

# assert sol.gray_code(0) == [0]
# assert sol.gray_code(1) in ([0, 1], [1, 0])
# assert is_gray(sol.gray_code(2), 2)
# assert is_gray(sol.gray_code(3), 3)
# assert is_gray(sol.gray_code(4), 4)
# assert len(sol.gray_code(4)) == 16
# assert is_gray(sol.gray_code(5), 5)
# assert is_gray(sol.gray_code(8), 8)
# assert is_gray(sol.gray_code(10), 10)
# assert is_gray(sol.gray_code(13), 13)
# assert is_gray(sol.gray_code(16), 16)
# assert len(sol.gray_code(16)) == 65536
