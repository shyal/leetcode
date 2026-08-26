"""
DRILL: Ledger Tally
TRAINS: stack-nested-eval

At closing time a shopkeeper's register prints one long paper tape: every
sale and refund of the day glued into a single string, e.g. "120+45-30-8+7".
A '+' means the following amount came in, a '-' means it went out. The tape
always starts with a plain (positive) amount.

Return the final balance. It may be negative.

Example 1:

Input: S = "120+45-30-8+7"
Output: 134

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
    Amounts fit in a normal int; the answer may be negative.

    REQUIRED: one pass over the characters. No eval, no split, no regex,
    no int() on slices - build each amount digit by digit as you walk.
"""


class Solution:
    def tally(self, S: str) -> int:
        pass


sol = Solution()

print(sol.tally("120+45-30-8+7"))  # 134

# assert sol.tally("120+45-30-8+7") == 134
# assert sol.tally("3-9") == -6
# assert sol.tally("7") == 7
# assert sol.tally("10-100+1000") == 910
# assert sol.tally("1+2+3+4") == 10
# assert sol.tally("100-100") == 0
# assert sol.tally("5-3-3") == -1
# assert sol.tally("300+21") == 321
# assert sol.tally("999999+1") == 1000000
