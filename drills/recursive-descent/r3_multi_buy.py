"""
DRILL: Multi-Buy
TRAINS: recursive-descent

A market stall tots up a customer's order as one string, e.g. "2+3*4/6".
'+' and '-' separate the items bought and returned; '*' and '/' express
multi-buys and per-unit splits inside a single item, and bind tighter:
"2+3*4" is one item of 2 and one item of 3*4, never (2+3)*4. Division is
integer division, truncating (all running values stay non-negative, so
floor and truncate agree). There are no parentheses.

Return the total. It may be negative.

The grammar has three levels now - write it first, then one function per
rule. The only hint: a new rule sits between the sum level and the number
level, and it owns '*' and '/'.

Example 1:

Input: S = "2+3*4/6"
Output: 4
Explanation: 3*4/6 = 2, and 2+2 = 4.

Example 2:

Input: S = "10-2*3"
Output: 4

Example 3:

Input: S = "20/3"
Output: 6

Constraints:

    1 <= len(S) <= 10^5
    S contains only digits, '+', '-', '*' and '/'. No spaces.
    S starts with a digit; operators are always followed by a number.
    No division by zero; '*' and '/' chains evaluate left to right.

    REQUIRED: one function per grammar rule, sharing one cursor into S.
    No eval, no split, no regex, no int() on slices.
    The sum-level function never touches '*' or '/' - it asks the level
    below for a finished value and only ever sees '+' and '-'.
"""


class Solution:
    def total(self, S: str) -> int:
        pass


sol = Solution()

assert sol.total("2+3*4/6") == 4
assert sol.total("10-2*3") == 4
assert sol.total("20/3") == 6
assert sol.total("100/10/5") == 2
assert sol.total("3*4-2*5") == 2
assert sol.total("1+2*3+4") == 11
assert sol.total("2*2*2-16/2") == 0
assert sol.total("7") == 7
assert sol.total("1-10*10") == -99

print("All tests passed!")
