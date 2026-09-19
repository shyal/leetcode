"""
DRILL: First Lit Bulb

Given a row of bulbs lit, where lit[i] is True when bulb i is on, return
the index of the first bulb that is on. Every bulb before it is off and
every bulb after it is on. At least one bulb is on.

Example 1:

Input: lit = [False, False, False, True, True]
Output: 3

Example 2:

Input: lit = [False, False, False, False, False, False, False, True]
Output: 7

Example 3:

Input: lit = [False, True, True, True, True, True, True, True]
Output: 1

Example 4:

Input: lit = [True, True, True, True, True, True, True, True]
Output: 0

Example 5:

Input: lit = [False, False, False, False, True, True, True, True]
Output: 4

Constraints:

    1 <= len(lit) <= 10^5
    lit is False for a prefix and True for the rest.

    REQUIRED: must run in O(log n) time. NO scan from the left.
"""


class Solution:

    def firstLit(self, lit: List[bool]) -> int:
        return first_true(0, len(lit) - 1, lambda x: lit[x])


sol = Solution()

print(sol.firstLit([False, False, False, True, True]))  # 3

assert sol.firstLit([False, False, False, True, True]) == 3
assert sol.firstLit([False, False, False, False, False, False, False, True]) == 7
assert sol.firstLit([False, True, True, True, True, True, True, True]) == 1
assert sol.firstLit([True, True, True, True, True, True, True, True]) == 0
assert sol.firstLit([False, False, False, False, True, True, True, True]) == 4
assert sol.firstLit([True]) == 0
assert sol.firstLit([False] * 99999 + [True]) == 99999
assert sol.firstLit([True] * 100000) == 0
