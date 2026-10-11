"""
URL: https://leetcode.com/problems/minimize-result-by-adding-parentheses-to-expression/description/?envType=problem-list-v2&envId=vn57k9wr

2232. Minimize Result by Adding Parentheses to Expression

You are given a 0-indexed string expression of the form "<num1>+<num2>" where <num1> and <num2> represent positive integers.

Add a pair of parentheses to expression such that after the addition of parentheses, expression is a valid mathematical expression and evaluates to the smallest possible value. The left parenthesis must be added to the left of '+' and the right parenthesis must be added to the right of '+'.

Return expression after adding a pair of parentheses such that expression evaluates to the smallest possible value. If there are multiple answers that yield the same result, return any of them.

The input has been generated such that the original value of expression, and the value of expression after adding any pair of parentheses that meets the requirements fits within a signed 32-bit integer.

Example 1:

Input: expression = "247+38"
Output: "2(47+38)"
Explanation: The expression evaluates to 2 * (47 + 38) = 2 * 85 = 170.
Note that "2(4)7+38" is invalid because the right parenthesis must be to the right of the '+'.
It can be shown that 170 is the smallest possible value.

Example 2:

Input: expression = "12+34"
Output: "1(2+3)4"
Explanation: The expression evaluates to 1 * (2 + 3) * 4 = 1 * 5 * 4 = 20.

Example 3:

Input: expression = "999+999"
Output: "(999+999)"
Explanation: The expression evaluates to 999 + 999 = 1998.

Constraints:

    3 <= expression.length <= 10
    expression consists of digits from '1' to '9' and '+'.
    expression starts and ends with digits.
    expression contains exactly one '+'.
    The original value of expression, and the value of expression after adding any pair of parentheses that meets the requirements fits within a signed 32-bit integer.
---
247+38 let's work with each side independently

247 should become (247, 2*(47, , 24*(7

LEETCODE: Accepted (11 ms, 19.3 MB)
"""


# mu 0.7
# def minimizeResult(expression: str) -> str
#   left, right = expression.split('+')
#   _min = inf
#   ret min_expr = ''
#   for i in 0..<len(left)
#     for j in 1..len(right)
#       e = left[:i] + ('*' if i != 0 else '') + '(' + left[i:] + '+' + right[:j] + ')' + ('*' if j != len(right) else '' ) + right[j:]
#       r = eval(e)
#       if r < _min
#         _min = r
#         min_expr = ''.join(e.split('*'))
#

from math import inf


class Solution:
    def minimizeResult(self, expression: str) -> str:
        left, right = expression.split('+')
        _min = inf
        min_expr = ''
        for i in range(0, len(left)):
            for j in range(1, len(right) + 1):
                e = left[:i] + ('*' if i != 0 else '') + '(' + left[i:] + '+' + right[:j] + ')' + ('*' if j != len(right) else '') + right[j:]
                r = eval(e)
                if r < _min:
                    _min = r
                    min_expr = ''.join(e.split('*'))
        return min_expr


sol = Solution()
print(sol.minimizeResult('247+38'))
_l, _r = sol.minimizeResult('247+38'), '2(47+38)'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minimizeResult('12+34'), '1(2+3)4'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minimizeResult('999+999'), '(999+999)'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minimizeResult('1+1'), '(1+1)'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minimizeResult('123+456'), '1(23+45)6'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minimizeResult('9+9'), '(9+9)'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minimizeResult('111+111'), '1(11+11)1'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minimizeResult('1234+5678'), '1(234+5678)'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minimizeResult('9876+5432'), '(9876+5432)'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minimizeResult('1+999999999'), '(1+99999999)9'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minimizeResult('999999999+1'), '9(99999999+1)'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minimizeResult('11111+22222'), '1(1111+2222)2'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minimizeResult('123456789+987654321'), '1(23456789+98765432)1'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minimizeResult('999999999+999999999'), '(999999999+999999999)'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
_l, _r = sol.minimizeResult('10+10'), '(10+1)0'
assert _l == _r, f"left : {_l!r}\nright: {_r!r}"
