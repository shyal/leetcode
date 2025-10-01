"""
URL: https://leetcode.com/problems/excel-sheet-column-title/description/

168. Excel Sheet Column Title

Given an integer columnNumber, return its corresponding column title as it appears in an Excel sheet.

For example:

A -> 1
B -> 2
C -> 3
...
Z -> 26
AA -> 27
AB -> 28
...


Example 1:

Input: columnNumber = 1
Output: "A"

Example 2:

Input: columnNumber = 28
Output: "AB"

Example 3:

Input: columnNumber = 701
Output: "ZY"


Constraints:

    1 <= columnNumber <= 231 - 1
"""

from string import ascii_uppercase


class Solution:
    def convertToTitle(self, columnNumber: int) -> str:
        res = ""
        while columnNumber:
            columnNumber -= 1
            mod = columnNumber % 26
            res = ascii_uppercase[mod] + res
            columnNumber //= 26
        return res


sol = Solution()
assert sol.convertToTitle(1) == "A"
assert sol.convertToTitle(28) == "AB"
assert sol.convertToTitle(701) == "ZY"
assert sol.convertToTitle(26) == "Z"
assert sol.convertToTitle(27) == "AA"
assert sol.convertToTitle(52) == "AZ"
assert sol.convertToTitle(53) == "BA"
assert sol.convertToTitle(676) == "YZ"
assert sol.convertToTitle(677) == "ZA"
assert sol.convertToTitle(702) == "ZZ"
assert sol.convertToTitle(703) == "AAA"
assert sol.convertToTitle(321272406) == "ZZZZZZ"
assert sol.convertToTitle(321272407) == "AAAAAAA"
assert sol.convertToTitle(2147483647) == "FXSHRXW"
