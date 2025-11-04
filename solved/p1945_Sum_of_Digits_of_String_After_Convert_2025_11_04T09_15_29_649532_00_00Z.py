"""
URL: https://leetcode.com/problems/sum-of-digits-of-string-after-convert/description/?envType=problem-list-v2&envId=vn57k9wr

1945. Sum of Digits of String After Convert

You are given a string s consisting of lowercase English letters, and an integer k. Your task is to convert the string into an integer by a special process, and then transform it by summing its digits repeatedly k times. More specifically, perform the following steps:

1. Convert s into an integer by replacing each letter with its position in the alphabet (i.e. replace 'a' with 1, 'b' with 2, ..., 'z' with 26).

2. Transform the integer by replacing it with the sum of its digits.

3. Repeat the transform operation (step 2) k times in total.

For example, if s = "zbax" and k = 2, then the resulting integer would be 8 by the following operations:

1. Convert: "zbax" ➝ "(26)(2)(1)(24)" ➝ "262124" ➝ 262124

2. Transform #1: 262124 ➝ 2 + 6 + 2 + 1 + 2 + 4 ➝ 17

3. Transform #2: 17 ➝ 1 + 7 ➝ 8

Return the resulting integer after performing the operations described above.

Example 1:

Input: s = "iiii", k = 1

Output: 36

Explanation:

The operations are as follows:
- Convert: "iiii" ➝ "(9)(9)(9)(9)" ➝ "9999" ➝ 9999
- Transform #1: 9999 ➝ 9 + 9 + 9 + 9 ➝ 36
Thus the resulting integer is 36.

Example 2:

Input: s = "leetcode", k = 2

Output: 6

Explanation:

The operations are as follows:
- Convert: "leetcode" ➝ "(12)(5)(5)(20)(3)(15)(4)(5)" ➝ "12552031545" ➝ 12552031545
- Transform #1: 12552031545 ➝ 1 + 2 + 5 + 5 + 2 + 0 + 3 + 1 + 5 + 4 + 5 ➝ 33
- Transform #2: 33 ➝ 3 + 3 ➝ 6
Thus the resulting integer is 6.

Example 3:

Input: s = "zbax", k = 2

Output: 8

Constraints:

1 <= s.length <= 100
1 <= k <= 10
s consists of lowercase English letters.
"""


class Solution:

    def getDigits(self, num):
        digits = []
        while num:
            digits.append(num % 10)
            num //= 10
        return digits

    def sumDigits(self, s):
        return sum(self.getDigits(s))

    def getLucky(self, s: str, k: int) -> int:
        digit = ""
        for c in s:
            digit += str(ord(c) - ord("a") + 1)
        digit = int(digit)
        for _ in range(k):
            digit = self.sumDigits(digit)
        return digit


sol = Solution()

# print(sol.getLucky("iiii", 1))  # 36

assert sol.getLucky("iiii", 1) == 36
assert sol.getLucky("leetcode", 2) == 6
assert sol.getLucky("zbax", 2) == 8
assert sol.getLucky("a", 1) == 1
assert sol.getLucky("a", 2) == 1
assert sol.getLucky("z", 1) == 8
assert sol.getLucky("z", 2) == 8
assert sol.getLucky("s", 1) == 10
assert sol.getLucky("s", 2) == 1
assert sol.getLucky("ss", 1) == 20
assert sol.getLucky("ss", 2) == 2
assert sol.getLucky("s" * 10, 1) == 100
assert sol.getLucky("s" * 10, 2) == 1
assert sol.getLucky("s" * 9 + "i", 1) == 99
assert sol.getLucky("s" * 9 + "i", 2) == 18
assert sol.getLucky("s" * 9 + "i", 3) == 9
assert sol.getLucky("s" * 9 + "i", 10) == 9
assert sol.getLucky("s" * 100, 1) == 1000
assert sol.getLucky("s" * 100, 2) == 1
assert sol.getLucky("s" * 100, 10) == 1
