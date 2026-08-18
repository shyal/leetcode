"""
DRILL: Bundle Refunds
TRAINS: recursive-descent

A warehouse settles its account as one long string of credits and debits,
e.g. "12-(3+4-(2))". A '+' means money in, a '-' means money out. Related
items are grouped in parentheses: subtracting a bundle means the whole
bundle's value goes out. Bundles nest.

Return the final balance. It may be negative. Only '+' and '-' exist;
there is no multiplication.

The grammar:

    expr := atom (('+' | '-') atom)*
    atom := number | '(' expr ')'

Example 1:

Input: S = "12-(3+4-(2))"
Output: 7
Explanation: the inner bundle is 2, so the outer bundle is 3+4-2 = 5,
and 12-5 = 7.

Example 2:

Input: S = "10-(2+3)+1"
Output: 6

Example 3:

Input: S = "((7))"
Output: 7

Constraints:

    1 <= len(S) <= 10^5
    S contains only digits, '+', '-', '(' and ')'. No spaces.
    Parentheses are balanced; every '(' is eventually closed.
    Every bundle and the whole string start with a number or a '('.

    REQUIRED: one function per grammar rule, sharing one cursor into S.
    No eval, no split, no regex, no int() on slices.
    The '(' branch of `atom` is a recursive call back to `expr`;
    after it returns, the cursor must be sitting on the ')' - consume it.
"""


class Solution:
    def settle(self, S: str) -> int:
        pass


sol = Solution()

assert sol.settle("12-(3+4-(2))") == 7
assert sol.settle("10-(2+3)+1") == 6
assert sol.settle("((7))") == 7
assert sol.settle("(1+2)") == 3
assert sol.settle("2-(3)") == -1
assert sol.settle("1-(2-(3-(4)))") == -2
assert sol.settle("100-(20+30)-(10-5)") == 45
assert sol.settle("42") == 42

print("All tests passed!")
