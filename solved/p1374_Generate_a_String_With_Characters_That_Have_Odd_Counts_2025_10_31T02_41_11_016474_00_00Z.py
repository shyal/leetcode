"""
URL: https://leetcode.com/problems/generate-a-string-with-characters-that-have-odd-counts/description/?envType=problem-list-v2&envId=vn57k9wr

1374. Generate a String With Characters That Have Odd Counts

Given an integer n, return a string with n characters such that each character in such string occurs an odd number of times.

The returned string must contain only lowercase English letters. If there are multiples valid strings, return any of them.


Example 1:

Input: n = 4
Output: "pppz"
Explanation: "pppz" is a valid string since the character 'p' occurs three times and the character 'z' occurs once. Note that there are many other valid strings such as "ohhh" and "love".

Example 2:

Input: n = 2
Output: "xy"
Explanation: "xy" is a valid string since the characters 'x' and 'y' occur once. Note that there are many other valid strings such as "ag" and "ur".

Example 3:

Input: n = 7
Output: "holasss"


Constraints:

    1 <= n <= 500
"""


class Solution:
    def generateTheString(self, n: int) -> str:
        if n % 2 != 0:
            return "p" * n
        else:
            return "p" * (n - 1) + "z"


sol = Solution()

# print(sol.generateTheString(4))  # "pppz"

from collections import Counter

result = sol.generateTheString(4)
assert len(result) == 4
assert all(v % 2 == 1 for v in Counter(result).values())

result = sol.generateTheString(2)
assert len(result) == 2
assert all(v % 2 == 1 for v in Counter(result).values())

result = sol.generateTheString(7)
assert len(result) == 7
assert all(v % 2 == 1 for v in Counter(result).values())

result = sol.generateTheString(1)
assert len(result) == 1
assert all(v % 2 == 1 for v in Counter(result).values())
assert result.isalpha()
assert result.islower()

result = sol.generateTheString(3)
assert len(result) == 3
assert all(v % 2 == 1 for v in Counter(result).values())
assert result.isalpha()
assert result.islower()

result = sol.generateTheString(500)
assert len(result) == 500
assert all(v % 2 == 1 for v in Counter(result).values())
assert result.isalpha()
assert result.islower()

result = sol.generateTheString(499)
assert len(result) == 499
assert all(v % 2 == 1 for v in Counter(result).values())
assert result.isalpha()
assert result.islower()
