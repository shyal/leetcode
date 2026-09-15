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

---

Learning

"""

from enum import Flag, auto


class Color(Flag):
    red = auto()
    green = auto()
    blue = auto()


class Solution:
    def seen(self, names: list[str]) -> Flag:
        result = Color(0)
        for name in names:
            result |= Color[name]
        return result


sol = Solution()

print(sol.seen(["blue", "red", "blue"]))  # Color.blue|red

assert sol.seen(["blue", "red", "blue"]) == Color.red | Color.blue
assert sol.seen([]) == Color(0)
assert sol.seen(["green"]) == Color.green
assert sol.seen(["red", "green", "blue"]) == Color.red | Color.green | Color.blue
assert sol.seen(["green", "green", "green"]) == Color.green
assert sol.seen(["blue"] * 999 + ["red"]) == Color.red | Color.blue
assert isinstance(sol.seen(["blue"]), Color)
