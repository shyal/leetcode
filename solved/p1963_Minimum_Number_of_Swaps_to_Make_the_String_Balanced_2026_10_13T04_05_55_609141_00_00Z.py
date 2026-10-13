"""
URL: https://leetcode.com/problems/minimum-number-of-swaps-to-make-the-string-balanced/description/?envType=problem-list-v2&envId=vn57k9wr

1963. Minimum Number of Swaps to Make the String Balanced

You are given a 0-indexed string s of even length n. The string consists of exactly n / 2 opening brackets '[' and n / 2 closing brackets ']'.

A string is called balanced if and only if:
- It is the empty string, or
- It can be written as AB, where both A and B are balanced strings, or
- It can be written as [C], where C is a balanced string.

You may swap the brackets at any two indices any number of times.

Return the minimum number of swaps to make s balanced.

Example 1:

Input: s = "][]["
Output: 1
Explanation: You can make the string balanced by swapping index 0 with index 3.
The resulting string is "[[]]".

Example 2:

Input: s = "]]][[["
Output: 2
Explanation: You can do the following to make the string balanced:
- Swap index 0 with index 4. s = "[]][][".
- Swap index 1 with index 5. s = "[[][]]".
The resulting string is "[[][]]".

Example 3:

Input: s = "[]"
Output: 0
Explanation: The string is already balanced.

Constraints:

    n == s.length
    2 <= n <= 10^6
    n is even.
    s[i] is either '[' or ']'.
    The number of opening brackets '[' equals n / 2, and the number of closing brackets ']' equals n / 2.
---
find the number of matched brackets
the solution should be the remaining number of brackets divided by 2
to count matched brackets, we can simply increment a count to +1 on [ and -1 on ]
e.g []
    10
    ]  ]  [  [ 
   -1 -2  -1 0
if we set the floor at 0?
    ]  ]  [  [ 
    0  0  1  2

LEETCODE: Accepted (155 ms, 24.9 MB)
"""


# mu 0.10
# class Solution
#   def minSwaps(s: str) -> int
#     count = 0
#     for c in s
#       if c == '['
#         count += 1
#       else
#         count = max(count - 1, 0)
#     return ceil(count / 2)

class Solution:
    def minSwaps(self, s: str) -> int:
        count = 0
        for c in s:
            if c == '[':
                count += 1
            else:
                count = max(count - 1, 0)
        return -(-(count) // (2))


sol = Solution()
print(sol.minSwaps('][]['))
_l, _r = sol.minSwaps('][]['), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minSwaps(']]][[['), 2
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minSwaps('[]'), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minSwaps('[]'), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minSwaps('][' * 500000), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minSwaps('[]' * 500000), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minSwaps(']]]]]]]]]]' + '[[[[[[[[[['), 5
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minSwaps('[' * 500000 + ']' * 500000), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minSwaps(']' * 500000 + '[' * 500000), 250000
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minSwaps('][' * 1), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minSwaps('[]' * 1), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minSwaps('][' * 2), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minSwaps('[]][' * 250000), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minSwaps(']' * 2 + '[' * 2), 1
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minSwaps('[]' * 1000000), 0
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
