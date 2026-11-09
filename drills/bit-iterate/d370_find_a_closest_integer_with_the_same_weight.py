"""
EPI 4.4 Find a closest integer with the same weight

Given a 64-bit unsigned integer x, return the 64-bit unsigned integer y,
with y != x, that has the same number of 1 bits as x and makes |y - x|
as small as possible. That y is unique.

Example 1:

Input: x = 6
Output: 5
Explanation: 6 is 0b110 and 5 is 0b101. Both have two 1 bits, and
|5 - 6| = 1.

Example 2:

Input: x = 7
Output: 11
Explanation: 7 is 0b111. No number below 7 has three 1 bits. The next
number above 7 with three 1 bits is 11, which is 0b1011.

Example 3:

Input: x = 8
Output: 4

Constraints:

    0 < x < 2^64 - 1

    REQUIRED: O(n) time, where n = 64 is the word size, and O(1) extra
    space. NO loop over candidate values of y, NO bin(), NO format(),
    NO str().
"""


class Solution:
    def closest_int_same_bit_count(self, x: int) -> int:
        pass


sol = Solution()

print(sol.closest_int_same_bit_count(6))  # 5

# assert sol.closest_int_same_bit_count(6) == 5
# assert sol.closest_int_same_bit_count(7) == 11
# assert sol.closest_int_same_bit_count(8) == 4
# assert sol.closest_int_same_bit_count(1) == 2
# assert sol.closest_int_same_bit_count(2) == 1
# assert sol.closest_int_same_bit_count(0b1010) == 0b1001
# assert sol.closest_int_same_bit_count(0b1011000) == 0b1010100
# assert sol.closest_int_same_bit_count(0b1111000000) == 0b1110100000
# assert sol.closest_int_same_bit_count(2 ** 63) == 2 ** 62
# assert sol.closest_int_same_bit_count(2 ** 64 - 2) == 2 ** 64 - 3
# assert sol.closest_int_same_bit_count(2 ** 63 - 1) == 0xBFFFFFFFFFFFFFFF
# assert sol.closest_int_same_bit_count(0x5555555555555555) == 0x5555555555555556
# assert sol.closest_int_same_bit_count(0xAAAAAAAAAAAAAAAA) == 0xAAAAAAAAAAAAAAA9
# assert sol.closest_int_same_bit_count(0xFFFFFFFF00000000) == 0xFFFFFFFE80000000
