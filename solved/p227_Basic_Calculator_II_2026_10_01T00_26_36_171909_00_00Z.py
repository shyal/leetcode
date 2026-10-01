"""
URL: https://leetcode.com/problems/basic-calculator-ii/description/?envType=problem-list-v2&envId=vn57k9wr

227. Basic Calculator II

Given a string s which represents an expression, evaluate this expression and return its value.

The integer division should truncate toward zero.

You may assume that the given expression is always valid. All intermediate results will be in the range of [-2^31, 2^31 - 1].

Note: You are not allowed to use any built-in function which evaluates strings as mathematical expressions, such as eval().

Example 1:

Input: s = "3+2*2"
Output: 7

Example 2:

Input: s = " 3/2 "
Output: 1

Example 3:

Input: s = " 3+5 / 2 "
Output: 5

Constraints:

    1 <= s.length <= 3 * 10^5
    s consists of integers and operators ('+', '-', '*', '/') separated by some number of spaces.
    s represents a valid expression.
    All the integers in the expression are non-negative integers in the range [0, 2^31 - 1].
    The answer is guaranteed to fit in a 32-bit integer.
"""


# mu 0.7
# def calculate(s: str) -> int
#   stack, op, num = [],'+', 0
#   for c in s + '+'
#     if c.isdigit()
#       num = num * 10 + int(c)
#     elif c == ' '
#       continue
#     else
#       if op == '+'
#         stack <- num
#       elif op == '-'
#         stack <- -num
#       elif op == '*'
#         prev = stack .
#         stack <- prev * num
#       elif op == '/'
#         prev = stack .
#         stack <- prev // num
#       num, op = 0, c
#   sum(stack)

class Solution:
    def calculate(self, s: str) -> int:
        stack, op, num = [], '+', 0
        for c in s + '+':
            if c.isdigit():
                num = num * 10 + int(c)
            elif c == ' ':
                continue
            else:
                if op == '+':
                    stack.append(num)
                elif op == '-':
                    stack.append(-num)
                elif op == '*':
                    prev = stack.pop()
                    stack.append(prev * num)
                elif op == '/':
                    prev = stack.pop()
                    stack.append(prev // num)
                num, op = 0, c
        return sum(stack)


sol = Solution()
print(sol.calculate('3+2*2'))
assert sol.calculate('3+2*2') == 7
assert sol.calculate(' 3/2 ') == 1
assert sol.calculate(' 3+5 / 2 ') == 5
assert sol.calculate('0') == 0
assert sol.calculate('1-1') == 0
assert sol.calculate('2*3*4') == 24
assert sol.calculate('1000000000+1000000000') == 2000000000
assert sol.calculate('2147483647-2147483647') == 0
assert sol.calculate('10/3') == 3
assert sol.calculate('10-20*3') == -50
assert sol.calculate('5+5-5+5-5+5-5+5') == 10
assert sol.calculate('1+2*3/4-5+6*7/8-9') == -7
assert sol.calculate('0*0+0/1-0') == 0
assert sol.calculate('1-2+3-4+5-6+7-8+9-10') == -5
assert sol.calculate('2147483647/1') == 2147483647
