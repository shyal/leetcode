"""
URL: https://leetcode.com/problems/basic-calculator-ii/description/?envType=problem-list-v2&envId=vn57k9wr

227. Basic Calculator II

Given a string s which represents an expression, evaluate this expression and
return its value.

The integer division should truncate toward zero.

You may assume that the given expression is always valid. All intermediate
results will be in the range of [-2^31, 2^31 - 1].

Note: You are not allowed to use any built-in function which evaluates strings
as mathematical expressions, such as eval().


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

---

Went as far as i could. Need to consolidate recursive descent first.
Fail.
"""
class Parser:

    def __init__(self, S):
        self.S = S
        self.i = 0

    @property
    def curr(self):
        return self.S[self.i]

    def complete(self):
        return self.i >= len(self.S)

    def number(self):
        val = 0
        while not self.complete() and self.curr not in '+-*/':
            val = val * 10 + int(self.curr)
            self.i += 1
        return TreeNode(val)

    def atom(self):
        # forgot
        pass

    def iter(self):
        val = self.number()
        while not self.complete():
            op = self.curr
            self.i += 1
            val = TreeNode(left=val, val=op, right=self.number())
        return val

    


class Solution:
    def calculate(self, s: str) -> int:
        p = Parser(s)
        draw_tree(p.iter())


sol = Solution()

print(sol.calculate("3+2*2"))  # 7

# assert sol.calculate("3+2*2") == 7
# assert sol.calculate(" 3/2 ") == 1
# assert sol.calculate(" 3+5 / 2 ") == 5
# assert sol.calculate("42") == 42
# assert sol.calculate(" 42 ") == 42
# assert sol.calculate("0") == 0
# assert sol.calculate("0-0") == 0
# assert sol.calculate("1-1+1") == 1
# assert sol.calculate("2*3*4") == 24
# assert sol.calculate("2+3*4") == 14
# assert sol.calculate("2*3+4") == 10
# assert sol.calculate("14-3/2") == 13
# assert sol.calculate("1-2*3/4") == 0
# assert sol.calculate("0-3/2") == -1
# assert sol.calculate("7-6/4") == 6
# assert sol.calculate("22/7") == 3
# assert sol.calculate("100/10/5") == 2
# assert sol.calculate("0*5+3") == 3
# assert sol.calculate("3+2*2-4/2") == 5
# assert sol.calculate("1*2-3/4+5*6-7*8+9/10") == -24
# assert sol.calculate("2147483647") == 2147483647
# assert sol.calculate("0-2147483647") == -2147483647
# assert sol.calculate("1000000000/1") == 1000000000
# assert sol.calculate("  3  +  5  /  2  ") == 5
# assert sol.calculate("12*12") == 144
# assert sol.calculate("10-4/3") == 9
# assert sol.calculate("100-100/3*3") == 1

# FAILED: walked away after 12m 25s; no working solution.
# Judge the moves actually attempted as struggled, not clean.
