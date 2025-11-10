"""
URL: https://leetcode.com/problems/number-complement/description/?envType=problem-list-v2&envId=vn57k9wr

476. Number Complement

The complement of an integer is the integer you get when you flip all the 0's to 1's and all the 1's to 0's in its binary representation.

- For example, The integer 5 is "101" in binary and its complement is "010" which is the integer 2.

Given an integer num, return its complement.

Example 1:

Input: num = 5
Output: 2
Explanation: The binary representation of 5 is 101 (no leading zero bits), and its complement is 010. So you need to output 2.

Example 2:

Input: num = 1
Output: 0
Explanation: The binary representation of 1 is 1 (no leading zero bits), and its complement is 0. So you need to output 0.

Constraints:

    1 <= num < 2^31

Note: This question is the same as 1009: https://leetcode.com/problems/complement-of-base-10-integer/
"""


class Solution:
    def findComplement(self, num: int) -> int:
        return num ^ ((1 << (floor(log2(num)) + 1)) - 1)


sol = Solution()

# print(sol.findComplement(5))  # 2

assert sol.findComplement(5) == 2
assert sol.findComplement(1) == 0
assert sol.findComplement(2) == 1
assert sol.findComplement(3) == 0
assert sol.findComplement(4) == 3
assert sol.findComplement(6) == 1
assert sol.findComplement(7) == 0
assert sol.findComplement(8) == 7
assert sol.findComplement(2147483647) == 0
assert sol.findComplement(2147483646) == 1
