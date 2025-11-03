"""
URL: https://leetcode.com/problems/decode-ways/description/

91. Decode Ways

You have intercepted a secret message encoded as a string of numbers. The message is decoded via the following mapping:

"1" -> 'A'
"2" -> 'B'
...
"25" -> 'Y'
"26" -> 'Z'

However, while decoding the message, you realize that there are many different ways you can decode the message because some codes are contained in other codes ("2" and "5" vs "25").

For example, "11106" can be decoded into:

        "AAJF" with the grouping (1, 1, 10, 6)
        "KJF" with the grouping (11, 10, 6)
        The grouping (1, 11, 06) is invalid because "06" is not a valid code (only "6" is valid).

Note: there may be strings that are impossible to decode.

Given a string s containing only digits, return the number of ways to decode it. If the entire string cannot be decoded in any valid way, return 0.

The test cases are generated so that the answer fits in a 32-bit integer.


Example 1:

Input: s = "12"

Output: 2

Explanation:

"12" could be decoded as "AB" (1 2) or "L" (12).

Example 2:

Input: s = "226"

Output: 3

Explanation:

"226" could be decoded as "BZ" (2 26), "VF" (22 6), or "BBF" (2 2 6).

Example 3:

Input: s = "06"

Output: 0

Explanation:

"06" cannot be mapped to "F" because of the leading zero ("6" is different from "06"). In this case, the string is not a valid encoding, so return 0.


Constraints:

        1 <= s.length <= 100
        s contains only digits and may contain leading zero(s).
"""


class Solution:

    def numDecodings(self, s: str) -> int:
        @cache
        def dfs(i):
            if i <= 0:
                return 1
            ways = 0
            if i > 0 and "1" <= s[i] <= "9":
                ways += dfs(i - 1)
            if "10" <= s[i - 1 : i + 1] <= "26":
                ways += dfs(i - 2)
            return ways

        if s[0] == "0":
            return 0
        return dfs(len(s) - 1)


sol = Solution()
assert sol.numDecodings("12") == 2
assert sol.numDecodings("226") == 3
assert sol.numDecodings("06") == 0
assert sol.numDecodings("0") == 0
assert sol.numDecodings("1") == 1
assert sol.numDecodings("10") == 1
assert sol.numDecodings("11") == 2
assert sol.numDecodings("01") == 0
assert sol.numDecodings("100") == 0
assert sol.numDecodings("101") == 1
assert sol.numDecodings("110") == 1
assert sol.numDecodings("111") == 3
assert sol.numDecodings("27") == 1
assert sol.numDecodings("26") == 2
assert sol.numDecodings("206") == 1
assert sol.numDecodings("1206") == 1
assert sol.numDecodings("1001") == 0
assert sol.numDecodings("301") == 0
assert sol.numDecodings("7") == 1
assert sol.numDecodings("99") == 1
assert sol.numDecodings("19") == 2
assert sol.numDecodings("09") == 0
assert sol.numDecodings("109") == 1
assert sol.numDecodings("1226") == 5
assert sol.numDecodings("251") == 2
assert sol.numDecodings("30") == 0
assert sol.numDecodings("111111111111111111111111111111111111111111111") == 1836311903
