"""
URL: https://leetcode.com/problems/remove-outermost-parentheses/description/?envType=problem-list-v2&envId=vn57k9wr

1021. Remove Outermost Parentheses

A valid parentheses string is either empty "", "(" + A + ")", or A + B, where A
and B are valid parentheses strings, and + represents string concatenation.

    For example, "", "()", "(())()", and "(()(()))" are all valid parentheses
    strings.

A valid parentheses string s is primitive if it is nonempty, and there does not
exist a way to split it into s = A + B, with A and B nonempty valid parentheses
strings.

Given a valid parentheses string s, consider its primitive decomposition:
s = P1 + P2 + ... + Pk, where Pi are primitive valid parentheses strings.

Return s after removing the outermost parentheses of every primitive string in
the primitive decomposition of s.


Example 1:

Input: s = "(()())(())"
Output: "()()()"
Explanation:
The input string is "(()())(())", with primitive decomposition "(()())" + "(())".
After removing outer parentheses of each part, this is "()()" + "()" = "()()()".

Example 2:

Input: s = "(()())(())(()(()))"
Output: "()()()()(())"
Explanation:
The input string is "(()())(())(()(()))", with primitive decomposition
"(()())" + "(())" + "(()(()))".
After removing outer parentheses of each part, this is "()()" + "()" + "()(())"
= "()()()()(())".

Example 3:

Input: s = "()()"
Output: ""
Explanation:
The input string is "()()", with primitive decomposition "()" + "()".
After removing outer parentheses of each part, this is "" + "" = "".


Constraints:

    1 <= s.length <= 10^5
    s[i] is either '(' or ')'.
    s is a valid parentheses string.
"""


class Solution:
    def removeOuterParentheses(self, s: str) -> str:
        count = 0
        res = ""
        for c in s:
            if c == "(":
                if count > 0:
                    res += c
                count += 1
            else:
                count -= 1
                if count > 0:
                    res += c
        return res


sol = Solution()
# print(sol.removeOuterParentheses("(())"))  # "()"

assert sol.removeOuterParentheses("(()())(())") == "()()()"
assert sol.removeOuterParentheses("(()())(())(()(()))") == "()()()()(())"
assert sol.removeOuterParentheses("()()") == ""

assert sol.removeOuterParentheses("") == ""
assert sol.removeOuterParentheses("()") == ""
assert sol.removeOuterParentheses("()()()") == ""
assert sol.removeOuterParentheses("()" * 7) == ""

assert sol.removeOuterParentheses("(())") == "()"
assert sol.removeOuterParentheses("((()))") == "(())"
assert sol.removeOuterParentheses("(((())))") == "((()))"
assert sol.removeOuterParentheses("(()(()))") == "()(())"
assert sol.removeOuterParentheses("((())())") == "(())()"
assert sol.removeOuterParentheses("((()())(()))") == "(()())(())"

assert sol.removeOuterParentheses("()(())") == "()"
assert sol.removeOuterParentheses("(())()") == "()"
assert sol.removeOuterParentheses("(())(())") == "()()"
assert sol.removeOuterParentheses("(())()(())") == "()()"
assert sol.removeOuterParentheses("()((()))") == "(())"
assert sol.removeOuterParentheses("((()))()") == "(())"
assert sol.removeOuterParentheses("(()())(())(())") == "()()()()"
assert sol.removeOuterParentheses("(()(()))()") == "()(())"
assert sol.removeOuterParentheses("()(()(()))") == "()(())"
assert sol.removeOuterParentheses("(())((()))(())") == "()(())()"

assert sol.removeOuterParentheses(sol.removeOuterParentheses("(()())(())")) == ""
assert sol.removeOuterParentheses(sol.removeOuterParentheses("((()))")) == "()"
assert sol.removeOuterParentheses(sol.removeOuterParentheses("((()()))")) == "()()"
assert (
    sol.removeOuterParentheses(sol.removeOuterParentheses("(()())(())(()(()))")) == "()"
)

assert len(sol.removeOuterParentheses("(()())(())")) == len("(()())(())") - 4
assert len(sol.removeOuterParentheses("()" * 100)) == 0

_deep = "(" * 500 + ")" * 500
assert sol.removeOuterParentheses(_deep) == "(" * 499 + ")" * 499

_flat = "()" * 50000
assert sol.removeOuterParentheses(_flat) == ""

_wide = "(())" * 25000
assert sol.removeOuterParentheses(_wide) == "()" * 25000

_deep_big = "(" * 50000 + ")" * 50000
assert sol.removeOuterParentheses(_deep_big) == "(" * 49999 + ")" * 49999
