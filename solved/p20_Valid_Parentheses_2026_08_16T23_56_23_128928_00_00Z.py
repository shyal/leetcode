"""
URL: https://leetcode.com/problems/valid-parentheses/description/?envType=problem-list-v2&envId=vn57k9wr

20. Valid Parentheses

Given a string s containing just the characters '(', ')', '{', '}', '[' and ']',
determine if the input string is valid.

An input string is valid if:

    1. Open brackets must be closed by the same type of brackets.
    2. Open brackets must be closed in the correct order.
    3. Every close bracket has a corresponding open bracket of the same type.


Example 1:

Input: s = "()"
Output: true

Example 2:

Input: s = "()[]{}"
Output: true

Example 3:

Input: s = "(]"
Output: false

Example 4:

Input: s = "([])"
Output: true

Example 5:

Input: s = "([)]"
Output: false


Constraints:

    1 <= s.length <= 10^4
    s consists of parentheses only '()[]{}'.
"""


class Solution:
    def isValid(self, s: str) -> bool:
        p = {
            ')': '(',
            ']': '[',
            '}': '{',
        }
        stack = []
        for c in s:
            if c in p and stack:
                if stack[-1] == p[c]:
                    stack.pop()
                else:
                    return False
            else:
                stack.append(c)
        return len(stack) == 0


sol = Solution()

# print(sol.isValid("()"))  # True

assert sol.isValid("()") == True
assert sol.isValid("()[]{}") == True
assert sol.isValid("(]") == False
assert sol.isValid("([])") == True
assert sol.isValid("([)]") == False
assert sol.isValid("(") == False
assert sol.isValid(")") == False
assert sol.isValid("[") == False
assert sol.isValid("]") == False
assert sol.isValid("{") == False
assert sol.isValid("}") == False
assert sol.isValid("((") == False
assert sol.isValid("))") == False
assert sol.isValid(")(") == False
assert sol.isValid("}{") == False
assert sol.isValid("(()") == False
assert sol.isValid("())") == False
assert sol.isValid("]()") == False
assert sol.isValid("()[") == False
assert sol.isValid("{[]}") == True
assert sol.isValid("{[()]}") == True
assert sol.isValid("([{}])") == True
assert sol.isValid("([{})]") == False
assert sol.isValid("()()()") == True
assert sol.isValid("(((())))") == True
assert sol.isValid("[({})](]") == False
assert sol.isValid("(" * 5000 + ")" * 5000) == True
assert sol.isValid("()" * 5000) == True
assert sol.isValid("(" * 5000 + "]" * 5000) == False
assert sol.isValid("(" * 10000) == False