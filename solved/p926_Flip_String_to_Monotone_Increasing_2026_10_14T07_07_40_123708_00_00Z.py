"""
URL: https://leetcode.com/problems/flip-string-to-monotone-increasing/description/?envType=problem-list-v2&envId=vn57k9wr

926. Flip String to Monotone Increasing

A binary string is monotone increasing if it consists of some number of 0's (possibly none), followed by some number of 1's (also possibly none).

You are given a binary string s. You can flip s[i] changing it from 0 to 1 or from 1 to 0.

Return the minimum number of flips to make s monotone increasing.

Example 1:

Input: s = "00110"
Output: 1
Explanation: We flip the last digit to get 00111.

Example 2:

Input: s = "010110"
Output: 2
Explanation: We flip to get 011111, or alternatively 000111.

Example 3:

Input: s = "00011000"
Output: 2
Explanation: We flip to get 00000000.

Constraints:

    1 <= s.length <= 10^5
    s[i] is either '0' or '1'.
---
struggled with this one, but the question is actually simple:
what costs less, ones, or another flip?

Learning

LEETCODE: Accepted (42 ms, 19.7 MB)
"""


# mu 0.10
# class Solution
#   def minFlipsMonoIncr(s: str) -> int
#     ones = flips = 0
#     for c in s
#       if c == '1'
#         ones += 1
#       else
#         flips = min(flips + 1, ones)
#     flips

class Solution:
    def minFlipsMonoIncr(self, s: str) -> int:
        ones = flips = 0
        for c in s:
            if c == '1':
                ones += 1
            else:
                flips = min(flips + 1, ones)
        return flips


sol = Solution()
print(sol.minFlipsMonoIncr('10011111110010111011'))
_l, _r = sol.minFlipsMonoIncr('0101100011'), 3
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minFlipsMonoIncr('00110'), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minFlipsMonoIncr('010110'), 2
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minFlipsMonoIncr('00011000'), 2
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minFlipsMonoIncr('0'), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minFlipsMonoIncr('1'), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minFlipsMonoIncr('11111'), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minFlipsMonoIncr('00000'), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minFlipsMonoIncr('1010101010'), 5
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minFlipsMonoIncr('1111100000'), 5
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minFlipsMonoIncr('0000011111'), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minFlipsMonoIncr('1' * 50000 + '0' * 50000), 50000
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minFlipsMonoIncr('0' * 50000 + '1' * 50000), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minFlipsMonoIncr('1' * 100000), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minFlipsMonoIncr('0' * 100000), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minFlipsMonoIncr('10' * 50000), 50000
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
