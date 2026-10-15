"""
URL: https://leetcode.com/problems/decode-ways/description/?envType=problem-list-v2&envId=vn57k9wr

91. Decode Ways

You have intercepted a secret message encoded as a string of numbers. The message is decoded via the following mapping:

"1" -> 'A'
"2" -> 'B'
...
"25" -> 'Y'
"26" -> 'Z'

However, while decoding the message, you realize that there are many different ways you can decode the message because some codes are contained in other codes ("2" and "5" vs "25").

For example, "11106" can be decoded into:
- "AAJF" with the grouping (1, 1, 10, 6)
- "KJF" with the grouping (11, 10, 6)
- The grouping (1, 11, 06) is invalid because "06" is not a valid code (only "6" is valid).

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
Learning

LEETCODE: Accepted (49 ms, 20.4 MB)
"""


# mu 0.10
# class Solution
#   def numDecodings(s: str) -> int
#     memo decode(i)
#       if i == len(s)
#         return 1
#       if s[i] == "0"
#         return 0
#       ways = decode(i + 1)
#       long = s[i : i + 2]
#       if len(long) == 2 and int(long) <= 26
#         ways += decode(i + 2)
#       return ways
#     decode(0)

import sys
import threading


sys.setrecursionlimit(1 << 20)


def cache(fn):
    """Memoise fn on its arguments. Pure Python, so a deep memo recursion
    is not cut short by the C recursion limit of Python 3.12 and 3.13."""
    memo = {}

    def cached(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items()))) if kwargs else args
        if key not in memo:
            memo[key] = fn(*args, **kwargs)
        return memo[key]

    cached.__name__, cached.__doc__, cached.__wrapped__ = fn.__name__, fn.__doc__, fn
    return cached


def deep(fn):
    """Run fn on a thread with a 256 MB stack, so deep memo recursion fits."""
    out, err = [], []

    def target():
        try:
            out.append(fn())
        except BaseException as e:
            err.append(e)

    threading.stack_size(1 << 28)
    t = threading.Thread(target=target)
    t.start()
    t.join()
    if err:
        raise err[0]
    return out[0]


class Solution:
    def numDecodings(self, s: str) -> int:
        def run():
            @cache
            def decode(i):
                if i == len(s):
                    return 1
                if s[i] == "0":
                    return 0
                ways = decode(i + 1)
                long = s[i:i + 2]
                if len(long) == 2 and int(long) <= 26:
                    ways += decode(i + 2)
                return ways
            return decode(0)
        return deep(run)


sol = Solution()
print(sol.numDecodings('12'))
_l, _r = sol.numDecodings('12'), 2
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.numDecodings('226'), 3
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.numDecodings('06'), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.numDecodings('0'), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.numDecodings('10'), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.numDecodings('100'), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.numDecodings('110'), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.numDecodings('27'), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.numDecodings('1010'), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.numDecodings('1111111111'), 89
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.numDecodings('11111111111111111111111111111111111111111111111111'), 20365011074
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.numDecodings('2611055971756562'), 4
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.numDecodings('301'), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.numDecodings('230'), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.numDecodings('1001'), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
