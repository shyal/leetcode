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

---

I've been struggling with this problem. Previously i was focussing on the bottom up tabular
solution, which may have been a bit too advanced. So will try recursive backtracking this time.

Ok i fumbled this one again. I got as far as building the correct structure, with dfs
and backtracking, but on two digits.

Maybe it'll make more sense starting from the end of the string?

Not my solution. Keeping in learning mode. Will revisit later.
"""


class Solution:
    def numDecodings(self, s: str) -> int:
        @cache
        def dfs(i):
            if i == len(s):
                return 1
            if s[i] == "0":
                return 0
            ways = dfs(i + 1)
            if i + 1 < len(s) and "10" <= s[i : i + 2] <= "26":
                ways += dfs(i + 2)
            return ways

        return dfs(0)


sol = Solution()

# print(sol.numDecodings("12"))

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
