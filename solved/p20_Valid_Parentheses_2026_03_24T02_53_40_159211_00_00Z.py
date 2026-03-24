"""
URL: https://leetcode.com/problems/valid-parentheses/description/?envType=problem-list-v2&envId=vn57k9wr

20. Valid Parentheses

Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

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


---

Ok so this definitely involves a stack, and a way to map closes to opens:

b = {
    ')': '(',
    ']': '[',
    '}': '{'
}

Input: s = "()"

When we encounter the open (, we pop it on the stack. 

stack = '('

Then when we encounter a close, if it matches the top of the stack, we pop the stack.

Input: s = "([)]"


"""
class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        b = {
            ')': '(',
            ']': '[',
            '}': '{'
        }
        for c in s:
            if c in b:
                "it's a close"
                if stack:
                    top = stack[-1]
                    if b[c] == top:
                        stack.pop()
                    else:
                        return False
                else:
                    return False
            else:
                "it's an open"
                stack.append(c)
        return len(stack) == 0


sol = Solution()

# print(sol.isValid("(]"))  # true

assert sol.isValid("()") == True
assert sol.isValid("()[]{}") == True
assert sol.isValid("(]") == False
assert sol.isValid("([])") == True
assert sol.isValid("([)]") == False
assert sol.isValid("(") == False
assert sol.isValid(")") == False
assert sol.isValid("{") == False
assert sol.isValid("}") == False
assert sol.isValid("[") == False
assert sol.isValid("]") == False
assert sol.isValid("((()))") == True
assert sol.isValid("{{{}}}") == True
assert sol.isValid("[[[]]]") == True
assert sol.isValid("()(") == False
assert sol.isValid("())") == False
assert sol.isValid("{[]}") == True
assert sol.isValid("[(])") == False
assert sol.isValid("([{}])") == True
assert sol.isValid("([}{])") == False
assert sol.isValid("[](){}") == True
assert sol.isValid("[({})]") == True
assert sol.isValid("[({}]") == False
assert sol.isValid("(((") == False
assert sol.isValid(")))") == False
assert sol.isValid("((") == False
assert sol.isValid("))") == False
assert sol.isValid("(){") == False
assert sol.isValid("(}") == False
assert sol.isValid("{)") == False