"""
DRILL: Read The Numbers
TRAINS: stack-nested-eval

Given a string s of nonnegative integers separated by single operator
characters, return the integers in the order they appear. Operators are
'+'. They separate the numbers and are otherwise ignored.

Example 1:

Input: s = "3+2+2"
Output: [3, 2, 2]

Example 2:

Input: s = "14+3+7"
Output: [14, 3, 7]
Explanation: 14 is one number, not a 1 and a 4.

Example 3:

Input: s = "42"
Output: [42]

Constraints:

    1 <= len(s) <= 10^5
    s contains only digits and the characters '+'. No spaces.
    s starts and ends with a digit; every operator is followed by a digit.

    REQUIRED: one pass over the characters, building each number digit by
    digit as you walk. NO split, NO regex, NO int() on slices.
"""


class Solution:
    def getNumbers(self, s: str) -> List[int]:
        num = 0
        stack = []
        for i, c in enumerate(s):
            if c.isdigit():
                num += num * 10 + int(c)
            if not c.isdigit() or i == len(s) - 1:
                stack.append(num)
                num = 0
        return stack


sol = Solution()

print(sol.getNumbers("3+2+2"))  # [3, 2, 2]
