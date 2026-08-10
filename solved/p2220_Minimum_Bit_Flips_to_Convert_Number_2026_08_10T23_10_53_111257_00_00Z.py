"""
URL: https://leetcode.com/problems/minimum-bit-flips-to-convert-number/description/?envType=problem-list-v2&envId=vn57k9wr

2220. Minimum Bit Flips to Convert Number

A bit flip of a number x is choosing a bit in the binary representation of x
and flipping it from either 0 to 1 or 1 to 0.

    For example, for x = 7, the binary representation is 111 and we may choose
    any bit (including any leading zeros not shown) and flip it. We can flip the
    first bit from the right to get 110, flip the second bit from the right to
    get 101, flip the fifth bit from the right (a leading zero) to get 10111, etc.

Given two integers start and goal, return the minimum number of bit flips to
convert start to goal.


Example 1:

Input: start = 10, goal = 7
Output: 3
Explanation: The binary representation of 10 and 7 are 1010 and 0111 respectively.
We can convert 10 to 7 in 3 steps:
- Flip the first bit from the right: 1010 -> 1011.
- Flip the third bit from the right: 1011 -> 1111.
- Flip the fourth bit from the right: 1111 -> 0111.
It can be shown we cannot convert 10 to 7 in less than 3 steps. Hence, we return 3.

Example 2:

Input: start = 3, goal = 4
Output: 3
Explanation: The binary representation of 3 and 4 are 011 and 100 respectively.
We can convert 3 to 4 in 3 steps:
- Flip the first bit from the right: 011 -> 010.
- Flip the second bit from the right: 010 -> 000.
- Flip the third bit from the right: 000 -> 100.
It can be shown we cannot convert 3 to 4 in less than 3 steps. Hence, we return 3.


Constraints:

    0 <= start, goal <= 10^9


Note: This question is the same as 461: Hamming Distance.
"""


class Solution:
    def minBitFlips(self, start: int, goal: int) -> int:
        xor = start ^ goal
        count = 0
        while xor:
            if xor & 1:
                count += 1
            xor >>= 1
        return count


sol = Solution()

assert sol.minBitFlips(10, 7) == 3
assert sol.minBitFlips(3, 4) == 3

assert sol.minBitFlips(0, 0) == 0
assert sol.minBitFlips(7, 7) == 0
assert sol.minBitFlips(10**9, 10**9) == 0

assert sol.minBitFlips(0, 1) == 1
assert sol.minBitFlips(1, 0) == 1
assert sol.minBitFlips(0, 512) == 1
assert sol.minBitFlips(512, 0) == 1
assert sol.minBitFlips(1, 2) == 2

assert sol.minBitFlips(0, 255) == 8
assert sol.minBitFlips(255, 0) == 8
assert sol.minBitFlips(1023, 0) == 10
assert sol.minBitFlips(0, 1023) == 10

assert sol.minBitFlips(42, 21) == 6
assert sol.minBitFlips(21, 42) == 6
assert sol.minBitFlips(15, 16) == 5
assert sol.minBitFlips(16, 15) == 5
assert sol.minBitFlips(255, 256) == 9

assert sol.minBitFlips(0, 10**9) == 13
assert sol.minBitFlips(10**9, 0) == 13
assert sol.minBitFlips(0, 999999999) == 21
assert sol.minBitFlips(10**9, 999999999) == 10
assert sol.minBitFlips(10**9, 7) == 16
assert sol.minBitFlips(10**9, 536870912) == 12

assert sol.minBitFlips(1073741823, 0) == 30
assert sol.minBitFlips(536870912, 536870911) == 30

for a in (0, 1, 2, 3, 7, 8, 42, 255, 4096, 65535, 123456789, 536870911, 10**9):
    for b in (0, 1, 5, 6, 31, 512, 1024, 99999, 987654321, 10**9):
        expected = bin(a ^ b).count("1")
        assert sol.minBitFlips(a, b) == expected
        assert sol.minBitFlips(b, a) == expected

for k in range(31):
    assert sol.minBitFlips(0, 1 << k) == 1
    assert sol.minBitFlips(1 << k, 1 << k) == 0
    assert sol.minBitFlips((1 << k) - 1, 0) == k