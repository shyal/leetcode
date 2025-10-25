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

Alright i spent a bit of time trying to solve this, but realize
i'm still fuzzy on the correct approach, so am better off going
back to learning mode on this one.

My incorrect solution:


class Solution:

    def numDecodings(self, s: str) -> int:
        DP = [1] + [0] * len(s)
        for i in range(2, len(s) + 2):
            one_digit = int(s[i - 1 : i])
            two_digits = int(s[i - 2 : i])

            if one_digit < 10:
                DP[i] = DP[i - 1] + 1

            if 10 <= two_digits <= 26:
                DP[i] = DP[i - 1] + 1

        return DP[-1]

In the correct solution we start by checking if the string starts with 0.
If it does, then there is no valid encoding.

For 12, we then declare a DP table of:

DP = [1, 1, 0]

This seems kind of aribrary.

We then start iterating with `for i in range(2, n + 1)` which
also feels arbitrary..

one_digit = int(s[i - 1 : i])
two_digits = int(s[i - 2 : i])

This sort of makes sense, but not really, because `one_digit`
turns out to be `2` and `two_digits` turns out to be `12`.

So we never explored the possibility of `one_digit` being `1` which
is confusing.

if one_digit != 0:
    dp[i] += dp[i - 1]

Why are we checking for one_digit not being zero? I guess this makes
sense as we can have for example 10, in which case we'd have the letters
A and J, and the 0 would be skipped.

In the correct solution we also do:

if 10 <= two_digits <= 26:
    dp[i] += dp[i - 2]

Which kind of makes sense but dp[i] += dp[i - 2] also feels arbitrary.

Time to ask an LLM about my confusions:

Excellent — this is one of those classic dynamic programming (DP) problems that feels weirdly arbitrary at first, but once you understand what each dp[i] actually means, it all clicks into place. Let's go step by step and make every line intuitive.

⸻

🧩 The Core Idea

We want dp[i] to represent:

The number of ways to decode the first i characters of the string s.

That means:
        •	dp[0] → number of ways to decode the empty prefix (””), which is 1 (there's exactly one way: do nothing).
        •	dp[1] → number of ways to decode the first 1 character, e.g., "1" → A.

This is our base case.

⸻

🧠 Why dp = [1, 1, 0, …]

Let's say s = "12".
Then n = 2, and we make a dp array of size n + 1 = 3.

Index:   0  1  2
Meaning: "" "1" "12"

We initialize:

dp[0] = 1  # one way to decode an empty string
dp[1] = 1  # one way to decode the first char, as long as it's not "0"

That's why it “feels arbitrary” — but it's actually defining the meaning of dp[i] as “up to i characters.”

⸻

🔍 The Loop: for i in range(2, n + 1)

We start from i = 2 because the first two base cases are known:
        •	dp[0] for the empty string,
        •	dp[1] for the first character.

From here on, for each position i, we look back one step and two steps to see if we can decode either one or two digits ending at position i.

⸻

🔢 These two lines are the heart of it

one_digit = int(s[i - 1 : i])
two_digits = int(s[i - 2 : i])

Example: "12"

i	Substring	one_digit	two_digits
2	"12"	"2"	"12"

✅ We don't see "1" at this step because "1" was already handled when i = 1.
Each iteration's job is only to look at the “ending” of the substring up to position i.

⸻

🧮 Why the conditions

if one_digit != 0:
    dp[i] += dp[i - 1]

If the current single digit isn't "0", then you can decode it as one character.
So the number of ways to decode up to i includes all ways to decode up to i - 1, extended by this one new letter.

Example:
        •	"12": you can decode "1" (A), then "2" (B), so dp[2] gets dp[1].

⸻


if 10 <= two_digits <= 26:
    dp[i] += dp[i - 2]

If the last two digits form a valid letter (10 → J, …, 26 → Z),
then we can decode them together.
In that case, the number of new decodings we gain is equal to all the ways to decode up to i - 2.

Example:
        •	"12": "12" → L, so dp[2] += dp[0] (1).

⸻

🧩 Intuition in Action

Let's simulate s = "12":

i	s[:i]	one_digit	two_digits	dp[i]	Explanation
0	“”	—	—	1	base
1	“1”	“1”	—	1	“A”
2	“12”	“2”	“12”	dp[1] + dp[0] = 1 + 1 = 2	“AB”, “L”

✅ Output = dp[2] = 2

⸻

🔄 Another Example: s = "226"

i	s[:i]	one_digit	two_digits	dp[i]	Reason
0	“”	—	—	1	base
1	“2”	2	—	1	“B”
2	“22”	2	22	2	“BB”, “V”
3	“226”	6	26	dp[2] + dp[1] = 2 + 1 = 3	“BZ”, “VF”, “BBF”

✅ Output = 3

⸻

🚫 Why Check for "0"

A '0' cannot stand alone — there's no mapping for "0".
So if one_digit == 0, skip it.

However, "10" and "20" are valid (J and T),
which is why the second condition checks for 10 <= two_digits <= 26.

⸻

🧩 Summary of Logic

Concept	Meaning
dp[i]	number of ways to decode the first i characters
dp[0] = 1	empty string base case
dp[1] = 1 if s[0] != '0' else 0	can decode the first char
one_digit	last single digit at position i-1
two_digits	last two digits ending at position i-1
Update rules	add dp[i - 1] if one_digit valid; add dp[i - 2] if two_digits valid


⸻

🧠 TL;DR Mental Model

You're standing at the end of the string.
At each step i, you can:
        •	Take 1 step back if the single digit is valid.
        •	Take 2 steps back if the last two digits form a valid code.

So the recurrence is:

dp[i] = (one_digit_valid ? dp[i-1] : 0) + (two_digits_valid ? dp[i-2] : 0)

That's the entire decoding problem distilled into one clean line.

⸻

OK i'll keep this problem in the learning queue for now.

Next attempt, i'll try this backtracking approach as it seems
more intuitive:

class Solution:
    def numDecodings(self, s: str) -> int:
        @cache
        def dfs(i):
            if i == len(s):           # reached end successfully
                return 1
            if s[i] == '0':           # invalid path
                return 0

            res = dfs(i + 1)          # take one digit

            if i + 1 < len(s) and 10 <= int(s[i:i+2]) <= 26:
                res += dfs(i + 2)     # take two digits

            return res

        return dfs(0)

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
            one_digit = int(s[i - 1 : i])
            two_digits = int(s[i - 2 : i])

            if one_digit != 0:
                dp[i] += dp[i - 1]

            if 10 <= two_digits <= 26:
                dp[i] += dp[i - 2]

        return dp[n]


sol = Solution()
assert sol.numDecodings("12") == 2
assert sol.numDecodings("226") == 3
assert sol.numDecodings("06") == 0
