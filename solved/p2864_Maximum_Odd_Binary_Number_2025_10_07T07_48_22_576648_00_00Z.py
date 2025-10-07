"""
URL: https://leetcode.com/problems/maximum-odd-binary-number/description/

2864. Maximum Odd Binary Number

You are given a binary string s that contains at least one '1'.

You have to rearrange the bits in such a way that the resulting binary number is the maximum odd binary number that can be obtained.

Return this maximum odd binary number. The result should also have the same length as s.


Example 1:

Input: s = "010"
Output: "001"
Explanation: "001" is "1" in decimal, and it is odd. Other rearrangements like "010" and "100" are even.

Example 2:

Input: s = "0101"
Output: "1001"
Explanation: "1001" is "9" in decimal, and it is odd. It is the maximum odd value possible.


Constraints:

    1 <= s.length <= 100
    s consists only of '0' and '1'.
    s contains at least one '1'.

---

Interesting problem. I'm thinking of just computing the maximum value possible for the given bits,
then interating backwards until i get an odd number.
"""


class Solution:
    def maximumOddBinaryNumber(self, s: str) -> str:
        ones = s.count("1")
        zeros = len(s) - ones
        return "1" * (ones - 1) + ("0" * zeros) + ("1")


sol = Solution()

assert sol.maximumOddBinaryNumber("010") == "001"
assert sol.maximumOddBinaryNumber("0101") == "1001"
assert sol.maximumOddBinaryNumber("1") == "1"
assert sol.maximumOddBinaryNumber("10") == "01"
assert sol.maximumOddBinaryNumber("11") == "11"
assert sol.maximumOddBinaryNumber("111") == "111"
assert sol.maximumOddBinaryNumber("100") == "001"
assert sol.maximumOddBinaryNumber("101") == "101"
assert sol.maximumOddBinaryNumber("0011") == "1001"
assert sol.maximumOddBinaryNumber("0001") == "0001"
assert sol.maximumOddBinaryNumber("1110") == "1101"
assert sol.maximumOddBinaryNumber("101010") == "110001"
assert sol.maximumOddBinaryNumber("1" + "0" * 99) == "0" * 99 + "1"
assert sol.maximumOddBinaryNumber("0" + "1" * 99) == "1" * 98 + "0" + "1"
