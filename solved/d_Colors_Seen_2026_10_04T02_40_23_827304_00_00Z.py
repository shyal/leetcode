"""
DRILL: Colors Seen
SNIPPET: lcflag

Given a list names of strings, each one of "red", "green" or "blue",
return one Color value holding every name that appears in names. Color
is a Flag whose members are red, green and blue, with values from
auto().

Example 1:

Input: names = ["blue", "red", "blue"]
Output: Color.red | Color.blue

Example 2:

Input: names = []
Output: Color(0)
Explanation: no name appears, so the value holds no member.

Example 3:

Input: names = ["green"]
Output: Color.green

Constraints:

    0 <= len(names) <= 1000
    names[i] is "red", "green" or "blue".

    REQUIRED: O(n). The return value must be a Color, NOT a set, a list
    or an int. NO arithmetic on member values.
"""

from enum import Flag, auto


# mu 0.7
# from enum import Flag, auto
#
# Color = Flag('Color', 'red green blue')
#
# def seen(names: [str]) -> Flag
#   ret res = Color(0)
#   for n in names
#     res |= Color[n]

from enum import Flag, auto


Color = Flag('Color', 'red green blue')


class Solution:
    def seen(self, names: list[str]) -> Flag:
        res = Color(0)
        for n in names:
            res |= Color[n]
        return res


sol = Solution()
print(sol.seen(['blue', 'red', 'blue']))
assert sol.seen(['blue', 'red', 'blue']) == Color.red | Color.blue
assert sol.seen([]) == Color(0)
assert sol.seen(['green']) == Color.green
assert sol.seen(['red', 'green', 'blue']) == Color.red | Color.green | Color.blue
assert sol.seen(['green', 'green', 'green']) == Color.green
assert sol.seen(['blue'] * 999 + ['red']) == Color.red | Color.blue
assert isinstance(sol.seen(['blue']), Color)
