"""
DRILL: Held By Either

Given two Color values a and b and a list names of strings, each one of
"red", "green" or "blue", return the strings of names whose member is
held by a or by b, in the order they appear in names.

Example 1:

Input: a = Color.red, b = Color.blue, names = ["blue", "green", "red"]
Output: ["blue", "red"]
Explanation: blue is held by b and red is held by a. Neither holds green.

Example 2:

Input: a = Color(0), b = Color(0), names = ["red", "green"]
Output: []
Explanation: neither value holds a member.

Example 3:

Input: a = Color.green, b = Color.green, names = ["green", "red", "green"]
Output: ["green", "green"]

Constraints:

    0 <= len(names) <= 1000
    names[i] is "red", "green" or "blue".

    REQUIRED: O(n). One membership test per name, on one value built
    from a and b. NO test on a and then on b. NO conversion of a or b
    to an int, a set or a list.
"""

from enum import Flag, auto


class Color(Flag):
    red = auto()
    green = auto()
    blue = auto()


class Solution:
    @as_list
    def either(self, a: Color, b: Color, names: list[str]) -> list[str]:
        for n in names:
            if Color[n] in a | b:
                yield n


sol = Solution()

print(sol.either(Color.red, Color.blue, ["blue", "green", "red"]))  # ['blue', 'red']

assert sol.either(Color.red, Color.blue, ["blue", "green", "red"]) == ["blue", "red"]
assert sol.either(Color(0), Color(0), ["red", "green"]) == []
assert sol.either(Color.green, Color.green, ["green", "red", "green"]) == [
    "green",
    "green",
]
assert sol.either(Color.red | Color.green, Color.blue, ["blue", "red", "green"]) == [
    "blue",
    "red",
    "green",
]
assert sol.either(Color.red, Color(0), ["green", "green", "red", "green", "green"]) == [
    "red"
]
assert sol.either(Color(0), Color.blue, ["green", "red", "green", "blue"]) == ["blue"]
assert sol.either(Color.red, Color.green, []) == []
assert sol.either(Color.red, Color.blue, ["green"] * 999 + ["blue"]) == ["blue"]
