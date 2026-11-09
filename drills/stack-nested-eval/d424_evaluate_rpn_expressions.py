"""
EPI 8.2 Evaluate RPN expressions

Given an arithmetic expression in Reverse Polish notation, return its
value. The tokens are separated by ','. A token is an integer or an
operator: '+', '-', '*' or '/'. An operator applies to the two
values before it, the earlier value on the left. The operator '/' is
integer division that rounds toward zero.

Example 1:

Input: expression = "2,1,+,3,*"
Output: 9
Explanation: (2 + 1) * 3.

Example 2:

Input: expression = "-7,2,/"
Output: -3

Example 3:

Input: expression = "42"
Output: 42

Constraints:

    1 <= len(expression) <= 2 * 10^5
    expression is a valid RPN expression with no division by zero.
    Every intermediate value is in [-2^31, 2^31 - 1].

    REQUIRED: O(n) time. NO eval(), NO recursion.
"""


class Solution:
    def evaluate(self, expression: str) -> int:
        pass


sol = Solution()

print(sol.evaluate("2,1,+,3,*"))  # 9

# assert sol.evaluate("2,1,+,3,*") == 9
# assert sol.evaluate("-7,2,/") == -3
# assert sol.evaluate("42") == 42
# assert sol.evaluate("-5") == -5
# assert sol.evaluate("0") == 0
# assert sol.evaluate("1,2,-") == -1
# assert sol.evaluate("8,2,/") == 4
# assert sol.evaluate("7,-2,/") == -3
# assert sol.evaluate("-7,-2,/") == 3
# assert sol.evaluate("0,3,/") == 0
# assert sol.evaluate("2,3,4,*,+") == 14
# assert sol.evaluate("3,4,-,5,*") == -5
# assert sol.evaluate("5,1,2,+,4,*,+,3,-") == 14
# assert sol.evaluate("4,13,5,/,+") == 6
# assert sol.evaluate(",".join(["1"] * 50000 + ["+"] * 49999)) == 50000
# assert sol.evaluate("1," + ",".join(["1", "+"] * 49999)) == 50000
# assert sol.evaluate("1," + ",".join(["3", "*", "2", "-"] * 25000)) == 1
