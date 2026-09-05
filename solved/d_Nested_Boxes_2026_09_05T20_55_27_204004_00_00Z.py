"""
DRILL: Nested Boxes
TRAINS: stack-nested-eval

Given a string s of digits and brackets, return its weight. A matching
'(' and ')' enclose a box. The weight of a box is the sum of the digits
directly inside it, plus twice the weight of each box directly inside it.
The whole string is the outermost box.

Example 1:

Input: s = "3(4)"
Output: 11
Explanation: The box (4) weighs 4. The string holds a 3 and that box: 3 + 2 * 4 = 11.

Example 2:

Input: s = "(1(2))"
Output: 10
Explanation: (2) weighs 2. (1(2)) weighs 1 + 2 * 2 = 5. The string holds only that box: 2 * 5 = 10.

Example 3:

Input: s = "2(3(4)5)"
Output: 34
Explanation: (4) weighs 4. (3(4)5) weighs 3 + 8 + 5 = 16. The string: 2 + 2 * 16 = 34.

Constraints:

    1 <= len(s) <= 10^5
    s contains only the characters '0' to '9', '(' and ')'.
    The brackets are balanced.
    Every digit is one item on its own: "12" is a 1 and a 2.

    REQUIRED: one pass over the characters with a stack of running weights,
    one entry per open box. NO recursion, NO second pass.

---

Learning

"""


class Solution:
    def weight(self, s: str) -> int:
        stack = [0]
        for c in s:
            if c.isdigit():
                stack[-1] += int(c)
            elif c == "(":
                stack.append(0)
            elif c == ")":
                v = stack.pop()
                stack[-1] += 2 * v
        return stack[0]


sol = Solution()

print(sol.weight("2(3(4)5)"))  # 34

assert sol.weight("3(4)") == 11
assert sol.weight("(1(2))") == 10
assert sol.weight("2(3(4)5)") == 34
assert sol.weight("5") == 5
assert sol.weight("12") == 3
assert sol.weight("()") == 0
assert sol.weight("(1)(1)") == 4
assert sol.weight("((1))") == 4
assert sol.weight("9(0)9") == 18
assert sol.weight("(1(1(1(1))))") == 30
