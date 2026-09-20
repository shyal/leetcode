"""
DRILL: Held By Both

Given two Color values a and b and a list names of strings, each one of
"red", "green" or "blue", return the strings of names whose member is
held by a and by b, in the order they appear in names.

Example 1:

Input: a = Color.red | Color.blue, b = Color.blue | Color.green, names = ["blue", "red", "green"]
Output: ["blue"]
Explanation: blue is the one member held by both values.

Example 2:

Input: a = Color.red | Color.green, b = Color.blue, names = ["red", "green"]
Output: []
Explanation: no member is held by both values.

Example 3:

Input: a = Color.green, b = Color.green | Color.red, names = ["green", "red", "green"]
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
    def both(self, a: Color, b: Color, names: list[str]) -> list[str]:
        for n in names:
            if Color[n] in a & b:
                yield n


sol = Solution()

print(
    sol.both(Color.red | Color.blue, Color.blue | Color.green, ["blue", "red", "green"])
)  # ['blue']

assert sol.both(
    Color.red | Color.blue, Color.blue | Color.green, ["blue", "red", "green"]
) == ["blue"]
assert sol.both(Color.red | Color.green, Color.blue, ["red", "green"]) == []
assert sol.both(Color.green, Color.green | Color.red, ["green", "red", "green"]) == [
    "green",
    "green",
]
assert sol.both(
    Color.red | Color.green | Color.blue,
    Color.red | Color.green | Color.blue,
    ["blue", "red", "green"],
) == ["blue", "red", "green"]
assert sol.both(
    Color.red | Color.blue,
    Color.red | Color.blue,
    ["green", "green", "blue", "green", "green"],
) == ["blue"]
assert sol.both(
    Color.blue, Color.blue | Color.green, ["green", "red", "green", "blue"]
) == ["blue"]
assert (
    sol.both(Color(0), Color.red | Color.green | Color.blue, ["red", "green", "blue"])
    == []
)
assert sol.both(Color.red, Color.red, []) == []
assert sol.both(
    Color.red | Color.green, Color.green | Color.blue, ["red"] * 999 + ["green"]
) == ["green"]
