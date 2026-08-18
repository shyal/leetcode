"""
DRILL: Tape Reader
TRAINS: recursive-descent

At closing time a shopkeeper's register prints one long paper tape: every
sale and refund of the day glued into a single string, e.g. "120+45-30".
A '+' means the following amount came in, a '-' means it went out. The
tape always starts with a plain (positive) amount.

Return the final balance. It may be negative.

The grammar:

    expr   := number (('+' | '-') number)*
    number := digit+

Example 1:

Input: S = "120+45-30"
Output: 135

Example 2:

Input: S = "3-9"
Output: -6

Example 3:

Input: S = "7"
Output: 7

Constraints:

    1 <= len(S) <= 10^5
    S contains only digits, '+' and '-'. No spaces.
    S starts with a digit; operators are always followed by a number.

    REQUIRED: one function per grammar rule, sharing one cursor into S.
    No eval, no split, no regex, no int() on slices - `number` builds its
    value digit by digit and leaves the cursor on the first non-digit.
    Every rule function consumes exactly the characters its rule matches.
"""


class Solution:
    def tally(self, S: str) -> int:
        pass


sol = Solution()

assert sol.tally("120+45-30") == 135
assert sol.tally("3-9") == -6
assert sol.tally("7") == 7
assert sol.tally("10-100+1000") == 910
assert sol.tally("5-3-3") == -1
assert sol.tally("999999+1") == 1000000

print("All tests passed!")
