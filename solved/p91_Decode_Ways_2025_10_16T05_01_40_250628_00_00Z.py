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

I was going in the right direction, but i guess i'm not good enough yet with DP:


class Solution:
    def numDecodings(self, s: str) -> int:
        S = [int(x) for x in s]
        n = len(S)
        invalid = "_"
        dp = [[invalid] * (n + 1), [invalid] * (n + 1)]
        dp[0][0] = 0
        dp[1][0] = 0

        def is_valid(a, b=None):
            if b is None:
                return a > 0
            else:
                if a == 0:
                    return False
                num = a + b
                return num <= 26

        for i in range(1, n + 1):
            curr = S[i - 1]
            if is_valid(curr):
                dp[0][i] = 1

        rich_print(tabulate([dp[0]], headers=["Letter"] + [asc[int(x)] for x in s]))

        for i in range(2, n + 1, 2):
            prev = S[i - 2]
            curr = S[i - 1]
            if prev != 0 and (prev * 10) + curr <= 26:
                dp[1][i] = int(is_valid((prev * 10) + curr))

        # print("")

        rich_print(tabulate([dp[1]], headers=["Letter"] + S))

Yeah it's a mess.

Looked up the solution: https://leetcode.com/problems/decode-ways/solutions/4454037/97-43-easy-solution-with-explanation/

Will need to revisit this problem soon.

"""


class Solution:
    def numDecodings(self, s: str) -> int:
        if not s or s[0] == "0":
            return 0

        n = len(s)
        dp = [0] * (n + 1)
        dp[0] = 1
        dp[1] = 1

        for i in range(2, n + 1):
            one_digit = int(s[i - 1])
            two_digits = int(s[i - 2 : i])

            if one_digit != 0:
                dp[i] += dp[i - 1]

            if 10 <= two_digits <= 26:
                dp[i] += dp[i - 2]

        return dp[n]


sol = Solution()
res = sol.numDecodings("12123")
# print(res)
