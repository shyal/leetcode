"""
DRILL: Read The Numbers
TRAINS: stack-nested-eval

Given a string s of nonnegative integers separated by single '+'
characters, return the integers in the order they appear. The '+'
separates the numbers and is otherwise ignored.

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
    s contains only digits and '+'. No spaces.
    s starts and ends with a digit; every '+' is followed by a digit.

    REQUIRED: one pass over the characters, building each number digit by
    digit as you walk. NO split, NO regex, NO int() on slices.
"""


class Solution:
    def getNumbers(self, s: str) -> List[int]:
        pass


sol = Solution()

print(sol.getNumbers("3+2+2"))  # [3, 2, 2]

# assert sol.getNumbers("3+2+2") == [3, 2, 2]
# assert sol.getNumbers("14+3+7") == [14, 3, 7]
# assert sol.getNumbers("42") == [42]
# assert sol.getNumbers("100+10+1") == [100, 10, 1]
# assert sol.getNumbers("0+0") == [0, 0]
# assert sol.getNumbers("7+7+7") == [7, 7, 7]
# assert sol.getNumbers("123456+9") == [123456, 9]
