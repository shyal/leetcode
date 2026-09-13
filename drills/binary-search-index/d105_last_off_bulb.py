"""
DRILL: Last Off Bulb

Given a row of bulbs lit, where lit[i] is True when bulb i is on, return
the index of the last bulb that is off. Every bulb before it is off and
every bulb after it is on. At least one bulb is off.

Example 1:

Input: lit = [False, False, False, True, True]
Output: 2

Example 2:

Input: lit = [False, False]
Output: 1

Example 3:

Input: lit = [False, True]
Output: 0

Constraints:

    1 <= len(lit) <= 10^5
    lit is False for a prefix and True for the rest.

    REQUIRED: must run in O(log n) time. NO scan from the right.
"""


class Solution:

    def lastOff(self, lit: List[bool]) -> int:
        pass


sol = Solution()

print(sol.lastOff([False, False, False, True, True]))  # 2

# assert sol.lastOff([False, False, False, True, True]) == 2
# assert sol.lastOff([False, False]) == 1
# assert sol.lastOff([False, True]) == 0
# assert sol.lastOff([False]) == 0
# assert sol.lastOff([False] + [True] * 99999) == 0
# assert sol.lastOff([False] * 99999 + [True]) == 99998
# assert sol.lastOff([False, False, True, True, True, True, True]) == 1
