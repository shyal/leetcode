"""
DRILL: Last Off Bulb

Given a row of bulbs lit, where lit[i] is True when bulb i is on, return
the index of the last bulb that is off. Every bulb before it is off and
every bulb after it is on. At least one bulb is off.

Example 1:

Input: lit = [False, False, False, True, True]
Output: 2

Example 2:

Input: lit = [False, False, False, False, False, False, False, True]
Output: 6

Example 3:

Input: lit = [False, True, True, True, True, True, True, True]
Output: 0

Example 4:

Input: lit = [False, False, False, False, False, False, False, False]
Output: 7

Example 5:

Input: lit = [False, False, False, False, True, True, True, True]
Output: 3

Constraints:

    1 <= len(lit) <= 10^5
    lit is False for a prefix and True for the rest.

    REQUIRED: must run in O(log n) time. NO scan from the right.
"""


class Solution:

    def lastOff(self, lit: List[bool]) -> int:
        return bisect_left(lit, True) - 1


sol = Solution()

print(sol.lastOff([False, False, False, True, True]))  # 2

assert sol.lastOff([False, False, False, True, True]) == 2
assert sol.lastOff([False, False, False, False, False, False, False, True]) == 6
assert sol.lastOff([False, True, True, True, True, True, True, True]) == 0
assert sol.lastOff([False, False, False, False, False, False, False, False]) == 7
assert sol.lastOff([False, False, False, False, True, True, True, True]) == 3
assert sol.lastOff([False]) == 0
assert sol.lastOff([False] + [True] * 99999) == 0
assert sol.lastOff([False] * 99999 + [True]) == 99998
assert sol.lastOff([False] * 100000) == 99999
